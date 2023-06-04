import xml.etree.ElementTree as ET
import re
from lxml import etree

class ODKReader:
    hypernym_set = []

    def __init__(self):
        self.hypernym_set = []

    @staticmethod
    def strip_special_chars(str):
        return re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", str)

    def get_data_by_file_reader(self, src):
        self.hypernym_set = []
        print("Reading data from [{}] file...".format(src))

        parser = etree.XMLParser(recover=True, encoding='utf-8')
        tree = ET.parse(src, parser=parser)
        root = tree.getroot()
        for child in root.findall('item'):
            word = self.strip_special_chars(child.find('wordInfo').find('word').text)
            if word == '' or not word: continue
            senseInfo = child.find('senseInfo')
            hypernyms = []

            # get field data
            fieldInfo = senseInfo.find('cat_info')
            if fieldInfo is not None:
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
        print("Completed reading word with hypernym!\n")
        return self.hypernym_set
