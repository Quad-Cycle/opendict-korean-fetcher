import xml.etree.ElementTree as ET
import re
import glob

class ODKReader:
    hypernym_set = []

    def __init__(self):
        self.hypernym_set = []

    @staticmethod
    def strip_special_chars(str):
        return re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", str)

    def get_data_by_file_reader(self, src):
        path = 'resources/*.xml'
        # fileList = glob.glob(path)
        tree = ET.parse(src)
        root = tree.getroot()
        for child in root.findall('item'):
            word = self.strip_special_chars(child.find('wordInfo').find('word').text)
            senseInfo = child.find('senseInfo')
            hypernyms = []

            # get field data
            fieldInfo = senseInfo.find('cat_info')
            if fieldInfo:
                field = self.strip_special_chars(fieldInfo.find('cat').text)
                hypernyms.append(field)

            # get hypernym word
            relations = senseInfo.findall('relation_info')
            for r in relations:
                if r.find('type').text == '상위어':
                    hypernym = self.strip_special_chars(r.find('word').text)[:-3]
                    hypernyms.append(hypernym)
            if hypernyms:
                self.hypernym_set.append((word, hypernyms))
        return self.hypernym_set
