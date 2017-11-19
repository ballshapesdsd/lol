# coding:gbk
from PIL import Image, ImageFilter
from aip import AipOcr
import numpy as np
import cv2


class OCR():
    def __init__(self):
        self.APP_ID = '10253196'
        self.API_KEY = 'rHGiInWCSToEjuy5yK6PsnGI'
        self.SECRET_KEY = 'dknE6TYRHBzRHDg2FMIgHr4u9zb8HyEz'

        self.aipOcr = AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def ocr(self, file_name):
        result = self.aipOcr.basicGeneral(self.get_file_content(file_name))
        return result


