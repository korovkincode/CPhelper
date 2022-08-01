from django.shortcuts import render
import requests
from bs4 import BeautifulSoup as BS
from dateutil import parser

#HEADERS = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
HEADERS = {}
proxies = {'https': '135.148.2.22:444'}#'135.148.2.22:444', '204.199.174.68:999'}

def get_html(url, params = None):
	html = requests.get(url, headers = HEADERS, params = params, verify = False, proxies = proxies)
	if html.status_code == 200:
		return html.text
	else:
		print('Error code: {}'.format(html.status_code))
		return 'Error'

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
		dateshow = newsBlock.find('time', class_ = 'timeago').get('datetime')
		date = parser.parse(dateshow)
		news.append({'title': title, 'href': href, 'desc': desc, 'date': date, 'dateshow': dateshow})
	return news

def codechef():
	html = get_html('https://www.codechef.com/')
	soup = BS(html, 'html.parser')
	news = []
	for newsBlock in soup.find_all('div', class_ = 'l-announcement'):
		title = ' '.join(newsBlock.find('p', class_ = 'm-announcement__head').text.split())
		href = newsBlock.find('a', class_ = 'm-announcement__link').get('href')
		desc = newsBlock.find('p', class_ = 'm-announcement__desc').text
		dateshow = ' '.join(newsBlock.find('p', class_ = 'm-announcement__time').text.replace('IST', '').split())
		date = parser.parse(dateshow)
		news.append({'title': title, 'href': href, 'desc': desc, 'date': date, 'dateshow': dateshow})
	return news

def cf():
	html = get_html('https://codeforces.com')
	soup = BS(html, 'html.parser')
	news = []
	for newsBlock in soup.find_all('div', class_ = 'topic'):
		title = newsBlock.find('div', class_ = 'title').text
		href = 'https://codeforces.com' + newsBlock.find('a').get('href')
		date = parser.parse(newsBlock.find('span', class_ = 'format-humantime').get('title'))
		dateshow = newsBlock.find('div', class_ = 'info').text
		desc = ''
		descBlock = newsBlock.find('div', class_ = 'ttypography')
		for aBlock in descBlock.find_all('a'):
			if not aBlock['href'].startswith('http'):
				aBlock['href'] = 'https://codeforces.com' + aBlock['href']
			aBlock['target'] = '_blank'
		for imgBlock in descBlock.find_all('img'):
			imgBlock.decompose()
		for el in list(descBlock.contents):
			desc += str(el).replace('$$$', '')
		news.append({'title': title, 'href': href, 'desc': desc, 'date': date, 'dateshow': dateshow})
		if len(news) == 15:
			break
	return news

def index(request):
	return render(request, "main/index.html")

def dashboard(request):
	news = cf()
	news += atcoder()
	news += codechef()
	news.sort(key = lambda el: el['date'], reverse = True)
	return render(request, "main/dashboard.html", {'news': news})

def contests(request):
	contests = []
	return render(request, "main/contests.html", {'contests': contests})