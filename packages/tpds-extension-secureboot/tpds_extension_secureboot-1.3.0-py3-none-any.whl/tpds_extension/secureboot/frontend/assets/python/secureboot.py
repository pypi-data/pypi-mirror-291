import os
import shutil
import warnings
import time
from tpds.flash_program import FlashProgram
from tpds.tp_utils.tp_print import print
from hsm_protocol import HSM
import os
from intelhex import IntelHex
from tpds.flash_program import FlashProgram
from tpds.tp_utils.tp_print import print
import tpds.tp_utils.tp_input_dialog as tp_userinput
from tpds.tp_utils.tp_keys import TPAsymmetricKey
from tpds.helper import log
from tpds.tp_utils.tp_settings import TPSettings
from tpds.tp_utils import run_subprocess_cmd
import hid
import xml.etree.ElementTree as ET


warnings.filterwarnings('ignore')


class SecureBootUsecase:
    def __init__(self, boards, publickeylen=0, VID=0x04D8, PID=0x003F, secboot_publickey_slot=5):
        self.boards = boards
        self.secboot_pulickey_slot = secboot_publickey_slot
        self.VID = VID
        self.PID = PID
        self.hsm_usb = hid.device()
        self.publickeylen = publickeylen

 # Step 1
    def generate_resources(self, b=None):
        self.__connect_to_SE(b)
        self.__gnerate_resources()
        self.__secboot_pulickey_slotno(b)
        print("\r\nSending Commands to HSM for Provisioning...")
        self.delete_slot(b)
        self.write_slot(b)
        self.write_nvm(b)
        self.read_slot(b)
        self.changetestsbc(b)  # test mode for sequential secure boot
        self.write_nvm(b)

        print("Completed.")

 # Step 2
    def app_hex(self, b=None):
        print('Select Application image file...', canvas=b)
        hsm_flash = tp_userinput.TPInputFileUpload(
            file_filter=['*.hex'],
            nav_dir=os.getcwd(),
            dialog_title='Upload hsm flash boot hex')
        hsm_flash.invoke_dialog()
        print(
            f'Selected file is: {hsm_flash.file_selection}',
            canvas=b)
        assert hsm_flash.file_selection is not None, \
            'Select valid application image file'
        self.app_image = hsm_flash.file_selection
        print(self.app_image)


# Step 3


    def flash_xml_modify(self, b=None):
        self.path = os.path.join(os.getcwd(), 'FWmetadatatool')
        # update SourceFlash xml
        ET.register_namespace(
            "hsmsf", "http://www.example.org/hsmSecureFlash")
        ET.register_namespace(
            "xsi", "http://www.w3.org/2001/XMLSchema-instance")
        ET.register_namespace(
            "schemaLocation", "http://www.example.org/hsmSecureFlash hsmSecureFlash.xsd ")

        self.sourceflash = os.path.join(self.path, 'SecureFlashPage0.xml')
        tree = ET.parse(self.sourceflash)
        root = tree.getroot()
        child = list(root)
        xml_variableslot = list(child[HSM.VariableSlots][HSM.Variableslot])
        # update slot_Index
        xml_slot_index = xml_variableslot[HSM.variableslot_header][HSM.index]
        xml_slot_index.text = str(self.secboot_pulickey_slot)
        # update private key size
        xml_ecc = list(
            xml_variableslot[HSM.data][HSM.asymmmetrical_key][HSM.ecc][HSM.weierstrassPrime])
        # update privatekey
        xml_prvkey = list(xml_ecc[HSM.privatekey])
        xml_key = xml_prvkey[HSM.key]
        xml_key.text = self.privatekey
        tree.write(self.sourceflash, encoding='UTF-8', xml_declaration=True)

        # update RiversideFwMd.xml
        if (self.device == 'EV16W43A'):
            self.Metadatafile = 'RiversideFwMd.xml'
            ET.register_namespace(
                "tns", "http://www.example.org/FirmwareMetadata")
            ET.register_namespace(
                "xsi", "http://www.w3.org/2001/XMLSchema-instance")
            ET.register_namespace(
                "schemaLocation", "http://www.example.org/hsmSecureFlash hsmSecureFlash.xsd ")
            self.fwmd = os.path.join(self.path,  self.Metadatafile)
            tree = ET.parse(self.fwmd)
            root = tree.getroot()
            child = list(root)
            # update hsm hex path
            hsm_hex_path = os.path.join(os.getcwd(), 'HSM_pic32czca90.hex')
            xml_hsm_hex_path = child[HSM.image_hsm][HSM.imageFileInputPath]
            xml_hsm_hex_path.text = hsm_hex_path
            # update application hex path
            app_hex_path = self.app_image
            xml_app_hex_path = child[HSM.image_app][HSM.imageFileInputPath]
            xml_app_hex_path.text = app_hex_path
            # update algorithm for secure boot
            tree.write(self.fwmd, encoding='UTF-8', xml_declaration=True)

        # update UnicornFwMd.xml
        if (self.device == 'EA14V17A'):
            self.Metadatafile = 'UnicornFwMd.xml'
            ET.register_namespace(
                "tns", "http://www.example.org/FirmwareMetadata")
            ET.register_namespace(
                "xsi", "http://www.w3.org/2001/XMLSchema-instance")
            ET.register_namespace(
                "schemaLocation", "http://www.example.org/hsmSecureFlash hsmSecureFlash.xsd ")
            self.fwmd = os.path.join(self.path, 'UnicornFwMd.xml')
            tree = ET.parse(self.fwmd)
            root = tree.getroot()
            child = list(root)

            # update hsm hex path
            hsm_hex_path = os.path.join(os.getcwd(), 'HSM_pic32cksg01.hex')
            xml_hsm_hex_path = child[HSM.image_hsm][HSM.imageFileInputPath]
            xml_hsm_hex_path.text = hsm_hex_path
            # update application hex path
            app_hex_path = self.app_image
            xml_app_hex_path = child[HSM.image_app][HSM.imageFileInputPath]
            xml_app_hex_path.text = app_hex_path
            # update algorithm for secure boot
            tree.write(self.fwmd, encoding='UTF-8', xml_declaration=True)

# step 4
    def FWMDtool_combined_hex(self, b=None):
        print("Creating Metadata...")
        self.tool = os.path.join(
            os.getcwd(), 'FWmetadatatool')
        self.tool_path = [str(self.tool)]
        self.FWMD_tool = os.path.join(self.tool, 'hsmsfmdgen.exe')
        FWMD_tool_path = [str(self.FWMD_tool)]
        FWMD_cmd = (
            FWMD_tool_path
            + [
                "-s",
                os.path.join(self.tool, "SecureFlashPage0.xml"),
                "-m",
                os.path.join(self.tool, self.Metadatafile),
                "-x",
                os.path.join(self.tool, "hsmSecureFlash.xsd"),
                "-y",
                os.path.join(self.tool, "FirmwareMetadata.xsd"),
                "-d",
                os.path.join(self.tool, "outputfwmd.hex"),
                "-o",
                os.path.join(self.tool, "outputs.hex"),
            ]

        )
        subprocessout = run_subprocess_cmd(cmd=FWMD_cmd)
        if not subprocessout:
            print("Error creating Metadata. Reset and start from Step 1")
        print(subprocessout)
        print("OK")
# Step 5

    def prog_FWMD(self, b=None):
        self.kit_parser = FlashProgram(self.device)
        print('Combining Firmware metadata and application image...', canvas=b)
        self.__create_combined_firmware(
            'FWmetadatatool\outputfwmd.hex', self.app_image)
        FWMD_img_path = os.path.join(
            os.getcwd(), 'combined_image.hex')  # 'FWmetadatatool', 'outputfwmd.hex')
        self.kit_parser.load_hex_image_with_ipe(FWMD_img_path)


#####################################################################################################################################################

    def __connect_to_SE(self, b=None):
        print('Connect to Secure Element: ', canvas=b)
        if self.boards is None:
            print('Prototyping board MUST be selected!', canvas=b)
            return
        # print(self.boards.get_selected_board())
        assert self.boards.get_selected_board(), \
            'Select board to run an Usecase'
        if (self.boards.get_selected_board().get("name")) == "PIC32CZCA90 CUltra":
            self.device = 'EV16W43A'
            print(self.boards.get_selected_board().get("name"))

        if (self.boards.get_selected_board().get("name")) == "PIC32CKSG01 CUltra":
            self.device = 'EA14V17A'
            print(self.boards.get_selected_board().get("name"))

        self.kit_parser = FlashProgram(self.device)

        print(self.kit_parser.check_board_status())
        assert self.kit_parser.is_board_connected(), \
            'Check the Kit parser board connections'
        self.factory_hex = self.boards.get_kit_hex()
        if not self.kit_parser.is_factory_programmed():
            assert self.factory_hex, \
                'Factory hex is unavailable to program'
            self.program_kit_protocol()
            text_box_desc = (
                '''<font color=#0000ff><b>Reset the Board and press OK </b></font><br>
         <br>To discover HSM and to provisiong the keys<br>''')
            user_input = tp_userinput.TPMessageBox(
                info=text_box_desc,
                title='HSM',
                option_list='OK')
            user_input.invoke_dialog()

        assert self._discover_hsm() == HSM.hsm_found, \
            '\r\n   HSM not present:'\
            '\r\n   1. Reset the board'\
            '\r\n           OR'\
            '\r\n   2 . Power cycle the device'
        print("HSM Device found")

    def __gnerate_resources(self, b=None):
        self.publickeylen = 0
        print('\r\nGenerating crypto assets for Usecase...', canvas=b)
        self.secbootkey = TPAsymmetricKey(self.__get_private_key_file(b))
        privkey_file = 'private_key.pem'
        self.secbootkey.get_private_pem(privkey_file)
        self.privatekey = self.secbootkey.get_private_key_bytes().hex().upper()
        # print(f"Private Key Bytes:", self.privatekey, canvas=b)
        self.publickey = self.secbootkey.get_public_key_bytes().hex().upper()
        self.publickeylen = int(len(self.publickey)/2)
        print(f"Public Key Bytes:", self.publickey, canvas=b)
        # 64 byte key

    def __secboot_pulickey_slotno(self, b=None):
        print(f'Selected HSM slot is: 5', canvas=b)
        self.secboot_pulickey_slot = 5
        HSM.hsm_slotinfo[0] = self.publickeylen + \
            HSM.HEADER_BYTES
        HSM.hsm_slotinfo[1] = self.secboot_pulickey_slot << 8
        HSM.hsm_slotinfo[4] = self.publickeylen

    def __get_private_key_file(self, b=None):
        print("Select secure boot private key option", canvas=b)
        item_list = ["Generate Private key", "Upload Private key"]
        dropdown_desc = """<font color=#0000ff><b>Select Secure Boot private key option</b>
        </font><br>
        <br>Generate Private key - Generates new Secure Boot private key<br>
        Upload Private key - Use existing private key file. Requires
        private key file .pem<br>"""
        user_input = tp_userinput.TPInputDropdown(
            item_list=item_list,
            desc=dropdown_desc,
            dialog_title="Private key selection",
        )
        user_input.invoke_dialog()
        print(f"Selected option is: {user_input.user_option}", canvas=b)
        assert user_input.user_option is not None, "Select valid private key Option"

        if user_input.user_option == "Upload Private key":
            print("Select private key file...", canvas=b)
            privkey = tp_userinput.TPInputFileUpload(
                file_filter=["*.pem"],
                nav_dir=os.getcwd(),
                dialog_title="Upload Private key",
            )
            privkey.invoke_dialog()
            print(
                f"Selected private key file is: {privkey.file_selection}", canvas=b)
            assert privkey.file_selection is not None, "Select valid private key file"
            return privkey.file_selection
        else:
            return None

    def program_kit_protocol(self, b=None):
        print('Programming factory hex...', canvas=b)
        tp_settings = TPSettings()
        mplab_paths = tp_settings.get_mplab_paths()
        self.mplab_path = mplab_paths.get("ide_path")
        path = os.path.join(
            os.getcwd(), self.boards.get_selected_board().get("kit_hex"))
        print(f'Programming {path} file')
        self.kit_parser.load_hex_image_with_ipe(path)

    def delete_slot(self, b=None):
        self._delete_slot(self.secboot_pulickey_slot)

    def _delete_slot(self, slotnum, b=None):
        OUTDATA = b"\rhsm:talk(group[03]cmd[04]slot[%02x])\n" % slotnum
        self.__write_hsm_hid(OUTDATA)

    def write_slot(self, b=None):
        assert self.publickeylen > 0, \
            "Generate Public Key Before Loading key to Slot"
        assert self._hsm_load_public_key(
            self.secboot_pulickey_slot,
            self.publickey,
            self.publickeylen) == "KIT_STATUS_SUCCESS", \
            "HSM Key Load Failed"
        print("     HSM Write Complete", canvas=b)

    def _hsm_load_public_key(self, slot, key, keylen, b=None):
        hsm_wr_cmd = self.__combine_cmd_dataforwrite(slot, key, keylen)
        cmdLength = len(hsm_wr_cmd)
        numFullHidBufs = int(cmdLength/(HSM.HIDBUFSIZEBYTES+1))
        for i in range(numFullHidBufs):
            cmd_datastr = hsm_wr_cmd[i*(HSM.HIDBUFSIZEBYTES-1)                                     :((i+1)*(HSM.HIDBUFSIZEBYTES-1))]
            cmd_datastr = b"\r" + cmd_datastr
            self.__write_hsm_hid(cmd_datastr)
        remBufferBytes = cmdLength % (HSM.HIDBUFSIZEBYTES+1)
        if (remBufferBytes > 0):
            cmd_datastr = b"\r" + \
                hsm_wr_cmd[numFullHidBufs*(HSM.HIDBUFSIZEBYTES-1):]
            self.__write_hsm_hid(cmd_datastr)
            status = self.__hsm_read_resp()
        return (status)

    def __combine_cmd_dataforwrite(self, slot, key, keylen, b=None):

        dataLenWords = int((keylen/4) + (HSM.HEADER_BYTES)/4)
        OUTSTR = "hsm:talk(group[03]cmd[00]slot[%02x]length[%02x]" % (
            slot, (dataLenWords+1))
        print(" Sending Write Command...")
        OUTDATA = bytes(OUTSTR, 'utf-8')
        OUTKEY = bytes(key, 'utf-8')
        OUTDATA += b'data['
        for w in HSM.hsm_slotinfo:
            wle = int.from_bytes(w.to_bytes(4, byteorder='little'),
                                 byteorder='big',  signed=False)
            OUTDATA += bytes("%08x" % wle, 'utf-8')
        OUTDATA += OUTKEY
        OUTDATA += b"])\n"
        return (OUTDATA)

    def write_nvm(self, b=None):
        assert self._misc_write_nvm(self.secboot_pulickey_slot) == "KIT_STATUS_SUCCESS", \
            "       HSM NVM Write Failed"

    def _misc_write_nvm(self, b=None):
        OUTDATA = b"\rhsm:talk(group[F0]cmd[06])\n"
        self.__write_hsm_hid(OUTDATA)
        status = self.__hsm_read_resp()
        return (status)

    def changetestsbc(self, b=None):
        assert self._misc_write_sbc(self.secboot_pulickey_slot) == "KIT_STATUS_SUCCESS", \
            "       HSM SBC Failed"

    def _misc_write_sbc(self, b=None):
        print(" Sending SBC command")
        OUTDATA = b"\rhsm:talk(group[F0]cmd[0A])\n"
        self.__write_hsm_hid(OUTDATA)
        status = self.__hsm_read_resp()
        return (status)

    def read_slot(self, b=None):
        assert self._hsm_read(self.secboot_pulickey_slot, self.publickeylen, info=None) == "KIT_STATUS_SUCCESS", \
            "HSM Read Failed, No Key in Slot"
        assert (self.key_length != b'00000000'), \
            'Provisionig is not successful, Restart from step 1'
        print("     Read Completed")

    def _hsm_read(self, slot, keylen, info, b=None):
        maxLength = int((keylen/8) + (HSM.HEADER_BYTES)/4)
        maxNumBuffs = HSM.MAXRSPLENGTH/HSM.HIDBUFSIZEBYTES
        print(" Sending Read Command...")
        if info == True:
            hsm_readcmd = self.__hsm_read_slotinf_cmd(slot, maxLength)
        else:
            hsm_readcmd = self.__hsm_read_slot_cmd(slot, maxLength)

        hsm_readcmdbtyes = bytes(hsm_readcmd, 'utf-8')
        self.__write_hsm_hid(hsm_readcmdbtyes)
        eoc = False
        rsp = b""
        rspLen = 0
        numBuffs = 0
        while (True):
            d = self.__read_hsm_hid(64)
            numBuffs += 1
            if d:
                ds = bytes(d)
                # print("\n %s" % (bytearray(d).hex('/', 1)))
                delIdx = ds.find(0x0a)
                if (delIdx > -1):
                    rspLen += delIdx
                    rsp += ds[:delIdx+1]
                    eoc = True
                    break
                else:
                    rsp += ds
                    rspLen += HSM.HIDBUFSIZEBYTES
            else:
                eoc = True
                break
            if (numBuffs > maxNumBuffs):
                break

        # print("RSP:  %s" % (rsp))
        self.kc = int(rsp[:2], 16)
        rc = int(rsp[3:11], 16)
        dStart = rsp.find(0x28)+1  # '('
        dEnd = rsp.find(0x29)  # ')'
        if (dEnd > 0):
            dLength = dEnd-dStart
            # print("Data length:  %d" % (dLength))
            dData = rsp[dStart:(dEnd)]
            dWords = int(dLength/(HSM.CHARSPERWORD))
            dRem = dLength % (HSM.CHARSPERWORD)
            # print(" Read Slot Info:")
            for i in range(dWords):
                ws = dStart + i*HSM.CHARSPERWORD
                # read_key = (rsp[ws:we])
                if (i <= 5):
                    we = ws + HSM.CHARSPERWORD
                    # print("  W%02d: %s " %
                    # (i, (rsp[ws:we])), HSM.slot_info_words[i])
                    if (i == 5):
                        self.key_length = (rsp[ws:we])

                else:
                    print(" Key in Slot %d:" % self.secboot_pulickey_slot)
                    print("   %s" % (rsp[ws:dEnd]))
                    self.slotkeybytes = (rsp[ws:dEnd])
                    break

            if (dRem > 0):
                print("  W%02d: %s" % (i, (rsp[we-dRem:we])))
            return (HSM.kcDictR[self.kc])

        else:
            print("VSM_SLOT_INFO Response Error!!!")

    def __hsm_read_slot_cmd(self, slotnum, dataLength, b=None):
        OUTSTR = "\rhsm:talk(group[03]cmd[01]slot[%02x]length[%02x])\n" % (
            slotnum, dataLength)
        # print(OUTSTR)
        return (OUTSTR)

    def __hsm_read_slotinf_cmd(self, slotnum, b=None):
        OUTSTR = "\rhsm:talk(group[03]cmd[05]slot[%02x])\n" % slotnum
        # print(OUTSTR)
        return (OUTSTR)

    def _discover_hsm(self, b=None):
        hsmdiscovercmd = b"\rboard:device(00)\n"
        self.__write_hsm_hid(hsmdiscovercmd)
        hsm_response = self.__read_hsm_hid(64)
        hsm_discover = bytes(hsm_response)
        hsm_response_str = hsm_discover.decode()
        return (hsm_response_str.find('HSM'))

    def __hsm_read_resp(self, b=None):
        d = ""
        d = self.__read_hsm_hid(64)
        if d:
            ds = bytes(d)
        kc = int(ds[:2], 16)
        return (HSM.kcDictR[kc])

    def __open_hid(self, b=None):
        self.hsm_usb = hid.device()
        self.hsm_usb.open(self.VID, self.PID)

    def __write_hsm_hid(self, msg, b=None):
        self.__open_hid()
        assert self.hsm_usb.write(msg), 'Not able to wirte the HSM'
        time.sleep(0.05)

    def __read_hsm_hid(self, byt, b=None):
        response = self.hsm_usb.read(byt)
        return response

    def __create_combined_firmware(self, img1, img2, b=None):
        self.combined_hex = 'combined_image.hex'
        self.combined = IntelHex()
        boot_hex = 'boot.hex'
        hsm_hex = os.getcwd()
        print("\r\n")
        hsm_hex = os.path.join(os.getcwd(), img1)
        print(hsm_hex)
        shutil.copy(hsm_hex, boot_hex)
        self.combined.merge(IntelHex(boot_hex), overlap='replace')
        os.remove(boot_hex)
        app_hex = 'applicaion.hex'
        kit_hex = os.path.join(os.getcwd(), img2)
        print("\r\n")
        print(kit_hex)
        shutil.copy(kit_hex, app_hex)
        self.combined.merge(IntelHex(app_hex), overlap='replace')
        os.remove(app_hex)
        self.combined.tofile(self.combined_hex, format='hex')
        print('Completed', canvas=b)
        print(f'Combined image file is: {self.combined_hex}', canvas=b)
