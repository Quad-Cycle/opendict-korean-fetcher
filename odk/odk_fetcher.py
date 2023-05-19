import requests
import urllib3
import re
import apikey
from bs4 import BeautifulSoup

API_KEY = apikey.apikey

class ODKFetcher:
	relation_info_types = []

	search_url = 'https://opendict.korean.go.kr/api/search?key={key}&advanced=y&method=exact'.format(key=API_KEY)
	view_url = 'https://opendict.korean.go.kr/api/view?key={key}&method=word_info'.format(key=API_KEY)

	def __init__(self):
		urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

	def request_data_by_url(self, url):
		try:
			r = requests.get(url, verify=False, timeout=20)
		except Exception as e:
			err_msg = f'Network ERR: {e}'
			print(err_msg)
		else:
			soup = BeautifulSoup(r.text, 'html.parser')
			return soup

	def get_sense_no_list(self, word):
		data = self.request_data_by_url(self.search_url + '&q=' + word)
		sense_no_list = []
		for sense_no in data.find_all('sense_no'):
			sense_no_list.append(sense_no.get_text())
		return sense_no_list

	@staticmethod
	def get_field_data(soup):
		field_data = soup.find('cat')
		if field_data:
			return field_data.get_text()

	@staticmethod
	def strip_special_chars(str):
		return re.sub(r"[^\uAC00-\uD7A30-9a-zA-Z\s]", "", str)

	def get_hypernym_sets(self, soup, relation_type):
		hypernym = []
		relations = soup.findAll('relation_info')
		for rel in relations:
			child_type = rel.findChildren('type', recursive=False)
			if child_type[0].get_text() == relation_type:
				child_word = rel.findChildren('word', recursive=False)[0].get_text()[:-3]
				if child_word:
					hypernym.append(self.strip_special_chars(child_word))
		return hypernym

	def get_data_by_sense_no(self, word, relation_type='상위어'):
		"""
		:param relation_type: 필요한 관계 타입 지정 ('상위어', '높임말', '준말', '반대말', '비슷한말', '낮춤말', '참고 어휘', '하위어')
		"""
		sense_no_list = self.get_sense_no_list(word)
		hypernym_list = []
		for sense_no in sense_no_list:
			query_url = self.view_url + '&q=' + word + sense_no
			soup = self.request_data_by_url(query_url)
			if not soup:
				continue

			# get field data
			field_name = self.get_field_data(soup)
			if field_name:
				hypernym_list.append(field_name)

			# get hypernym words
			hypernym = self.get_hypernym_sets(soup, relation_type)
			hypernym_list.extend(hypernym)

		return hypernym_list
