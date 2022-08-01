import requests
from bs4 import BeautifulSoup as BS

def atcoder():
	html = get_html('https://atcoder.jp')
	soup = BS(html, 'html.parser')
	news = []
	for newsBlock in soup.find_all('div', class_ = 'panel-default'):
		title = newsBlock.find('h3').text
		href = 'https://atcoder.jp' + newsBlock.find('a').get('href')
		descBlock = newsBlock.find('div', class_ = 'blog-post')
		desc = f'We will hold {title}.'
		flag = False
		for el in str(descBlock.text).split('\n'):
			if el.split() == []:
				continue
			if el[0] == '-' and not flag:
				flag = True
				desc += '<ul>'
			if el[0] != '-' and flag:
				flag = False
				desc += '</ul>'
			if 'Contest URL:' in el:
				continue
			if 'Start Time:' in el:
				continue
			if 'Writer:' in el:
				continue
			if 'Tester:' in el:
				continue
			if 'We will hold' in el:
				continue
			if flag:
				desc += '<li>'
				desc += el[1:]
				desc += '</li>'
			else:
				desc += el
		date = newsBlock.find('time', class_ = 'timeago').get('datetime')
		news.append({'title': title, 'href': href, 'desc': desc, 'date': date})
	return news