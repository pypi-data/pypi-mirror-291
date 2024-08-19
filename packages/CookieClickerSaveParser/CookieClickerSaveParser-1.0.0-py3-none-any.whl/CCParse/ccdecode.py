import base64
import binascii
import re
from . import Enums
from .models import ccmobile , ccpc
import base64
import ast
from typing import Union

class CCDecode:
    def __init__(self):
        ...

    def decode(self, data: str, type: Enums.SaveType) -> Union[ccmobile.CCSaveMobile, ccpc.CCSavePC]:
        if type is Enums.SaveType.AUTODETECT:
            type = self.detectsavetype(data=data)
        try:

            if type is Enums.SaveType.PC:
                missing_padding = len(data) % 4
                if missing_padding != 0:
                    data += '=' * (4 - missing_padding)

                data = data[:-9]
                data = data.encode('ascii', 'ignore').decode('ascii')
                data = data.strip()
                data = data.replace("%3D%21END%21", "")
                decoded_save = base64.b64decode(data)
                decoded_save = decoded_save.decode("utf-8")
                sections = decoded_save.split('|')
                parsed_data = []

                for section in sections:
                    if ';' in section:
                        parts = [subpart.split(',') if ',' in subpart else subpart for subpart in section.split(';')]
                    else:
                        parts = section
                    
                    parsed_data.append(parts)
                return ccpc.CCSavePC(data=parsed_data)

            elif type is Enums.SaveType.MOBILE:
                decoded_save = base64.b64decode(data)
                decoded_save = decoded_save.decode("utf-8")
                decoded_save = ast.literal_eval(decoded_save)
                return ccmobile.CCSaveMobile(decoded_save)

        except (ValueError, binascii.Error) as e:
            print(f"An error occurred while decoding: {e}")


    def detectsavetype(self,data:str):
        if data.endswith("%3D%21END%21"):
            return Enums.SaveType.PC
        else:
            return Enums.SaveType.MOBILE

        