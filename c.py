from sys import argv
from re import match
from argparse import ArgumentParser
from requests import get
from bs4 import BeautifulSoup

validURL = lambda url: match(r'(https?:\/\/).*', url) is not None
fmtURL = lambda url: url if validURL(url) else 'http://' + url # Replace

agents = {
	'd': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
	'm': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
}

def handleLinks(url, t):
	soup = BeautifulSoup(t, 'html.parser')
	for tag, attr in [('link', 'href'), ('script', 'src')]:
		for t in soup.select(tag):
			if not t.attrs.get(attr):
				continue
			if not validURL(t.attrs[attr]):
				t.attrs[attr] = url + '/' + t.attrs[attr]
	return soup

def clone(url, output, mobile = False):
	print('+ Copiando em modo %s...'%('mobile' if mobile else 'desktop'))
	try:
		t = get(url, headers = {
				'User-Agent': agents['d' if not mobile else 'm']
			}).text
	except Exception as e:
		exit(e)
	fopen = lambda *a, **k: open(*a, **k) # Random
	with fopen(output, 'wb') as f:
		f.write(str(handleLinks(url, t)).encode())
	print('+ Página clonada com sucesso.')

parser = ArgumentParser()
parser.add_argument('url', help = 'Aponta a URL de destino.')
parser.add_argument('-o', '--output', help = 'Aponta o arquivo onde os dados serão gravados.')
parser.add_argument('-m', '--mobile', action = 'store_true', help = 'Se usado, usa um User-Agent mobile.')

v = parser.parse_args()

url = v.url
out = v.output or url.split('/')[-1]
isM = v.mobile

if __name__ == '__main__':
	exit(clone(fmtURL(url), out, isM))