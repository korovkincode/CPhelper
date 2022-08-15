from django.shortcuts import render
from django.shortcuts import redirect
import requests
from bs4 import BeautifulSoup as BS
from dateutil import parser
from .models import Users
from datetime import datetime

#HEADERS = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
HEADERS = {}
proxies = {'https': '116.202.13.106:8080'}#'135.148.2.22:444', '204.199.174.68:999'}

def get_html(url, params = None):
	html = requests.get(url, headers = HEADERS, params = params, verify = False, proxies = proxies)
	if html.status_code == 200:
		return html.text
	else:
		print('Error code: {}'.format(html.status_code))
		return 'Error'

def atcoderdash():
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

def codechefdash():
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

def cfdash():
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
	return news

def atcodercont():
	html = get_html('https://atcoder.jp/contests/')
	soup = BS(html, 'html.parser')
	cont = []
	for contest in soup.find('div', id = 'contest-table-upcoming').find_all('tr')[1:]:
		title = contest.find_all('td')[1].find('a').text
		href = 'https://atcoder.jp' + contest.find_all('td')[1].find('a').get('href')
		date = contest.find('td').text.split()[0]
		datehref = contest.find('td').find('a').get('href')
		dur = contest.find_all('td')[-2].text
		cont.append({'title': title, 'href': href, 'date': date, 'datehref': datehref, 'writer': 'AtCoder', 'dur': dur})
	return cont

def codechefcont():
	html = get_html('https://www.codechef.com')
	soup = BS(html, 'html.parser')
	cont = []
	for contest in soup.find_all('div', class_ = 'm-other-event-card'):
		title = contest.find('h3', class_ = 'm-card-3__head').text
		href = contest.get('onclick')
		href = href[href.index("'") + 1:]
		href = href[:href.index('?')]
		date = contest.find('div', class_ = 'l-card-3__date-1-text').text + ' 2022'
		cont.append({'title': title, 'href': href, 'date': date, 'datehref': '', 'writer': 'CodeChef'})
	return cont

def cfcont():
	html = get_html('https://codeforces.com/contests?complete=true')
	soup = BS(html, 'html.parser')
	cont = []
	for contest in soup.find('div', class_ = 'datatable').find_all('tr')[1:]:
		title = contest.find('td').text
		href = 'https://codeforces.com/contest/' + contest.get('data-contestid')
		date = contest.find_all('td')[2].text.split()[0]
		datehref = contest.find_all('td')[2].find('a').get('href')
		dur = contest.find_all('td')[3].text
		writer = ''
		for aEl in contest.find_all('td')[1].find_all('a'):
			aEl['href'] = 'https://codeforces.com' + aEl['href']
			aEl['target'] = '_blank'
		for el in list(contest.find_all('td')[1].contents):
			writer += str(el)
		cont.append({'title': title, 'href': href, 'date': date, 'datehref': datehref, 'writer': writer, 'dur': dur})
	return cont

def index(request):
	return render(request, "main/index.html")

def dashboard(request):
	if request.session.get('username', 0) == 0:
		return redirect('/login')
	news = []
	curUser = Users.objects.get(username = request.session.get('username', 0))
	if curUser.codeforces == '1':
		news += cfdash()
	if curUser.atcoder == '1':
		news += atcoderdash()
	if curUser.codechef == '1':
		news += codechefdash()
	news.sort(key = lambda el: el['date'], reverse = True)
	return render(request, "main/dashboard.html", {'news': news, 'username': request.session.get('username', 0)})

def contests(request):
	if request.session.get('username', 0) == 0:
		return redirect('/login')
	contests = []
	curUser = Users.objects.get(username = request.session.get('username', 0))
	if curUser.atcoder == '1':
		contests += atcodercont()
	if curUser.codechef == '1':
		contests += codechefcont()
	if curUser.codeforces == '1':
		contests += cfcont()
	contests.sort(key = lambda el: parser.parse(el['date']))
	row = 1
	for x in range(len(contests)):
		contests[x]['row'] = row
		row += 1
	return render(request, "main/contests.html", {'contests': contests, 'username': request.session.get('username', 0)})

def signup(request):
	if request.session.get('username', 0):
		return redirect('/dashboard')
	if request.method == 'POST':
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		if username == '':
			return render(request, "main/regpage.html", {'errorname': 'Fill in the username.'})
		if password == '':
			return render(request, "main/regpage.html", {'errorpass': 'Fill in the password.'})
		if len(password) < 4:
			return render(request, "main/regpage.html", {'errorpass': 'Password length must be at least 4.'})
		try:
			Users.objects.get(username = username)
			return render(request, "main/regpage.html", {'errorname': 'This username is already in use. Try another'})
		except:
			pass
		datesignup = str(datetime.now()).split()[0]
		print(datesignup)
		Users.objects.create(username = username, password = password, codeforces = '1', atcoder = '1', codechef = '1', datesignup = datesignup)
		request.session['username'] = username
		request.session['password'] = password
		return redirect('/settings')
	return render(request, "main/regpage.html")

def login(request):
	if request.session.get('username', 0):
		return redirect('/dashboard')
	if request.method == 'POST':
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		if username == '':
			return render(request, "main/logpage.html", {'errorname': 'Fill in the username.'})
		if password == '':
			return render(request, "main/logpage.html", {'errorpass': 'Fill in the password.'})
		try:
			Users.objects.get(username = username)
		except:
			return render(request, "main/logpage.html", {'errorname': 'There is no account with this username. Try another'})
		try:
			Users.objects.get(username = username, password = password)
		except:
			return render(request, "main/logpage.html", {'errorpass': 'Password is incorrect. Try another'})
		request.session['username'] = username
		request.session['password'] = password
		return redirect('/dashboard')
	return render(request, "main/logpage.html")

def logout(request):
	if request.session.get('username', 0) == 0:
		return redirect('/login')
	request.session.flush()
	return redirect('/login')

def settings(request):
	if request.session.get('username', 0) == 0:
		return redirect('/login')
	if request.method == 'POST':
		username = request.session.get('username', 0)
		codeforces = request.POST.get('codeforces', '')
		codechef = request.POST.get('codechef', '')
		atcoder = request.POST.get('atcoder', '')
		if codeforces == 'on':
			codeforces = '1'
		else:
			codeforces = '0'
		if codechef == 'on':
			codechef = '1'
		else:
			codechef = '0'
		if atcoder == 'on':
			atcoder = '1'
		else:
			atcoder = '0'
		curUser = Users.objects.get(username = username)
		curUser.codeforces = codeforces
		curUser.codechef = codechef
		curUser.atcoder = atcoder
		curUser.save()

	curUser = Users.objects.get(username = request.session.get('username', 0))
	context = {'username': curUser.username, 'password': curUser.password, 'datesignup': curUser.datesignup, 'codeforces': curUser.codeforces,
	'atcoder': curUser.atcoder, 'codechef': curUser.codechef}
	return render(request, "main/setpage.html", context)