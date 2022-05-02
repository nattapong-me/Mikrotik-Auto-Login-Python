from urllib.request import urlopen
import requests
import urllib.parse
import re
import hashlib

######### SETTING HERE #############
url = 'http://192.168.182.1'
username = 'username'
password = 'password'
####################################

def get_page():
	page = urlopen(url+'/login').read()
	page = page[page.find('\''.encode()):page.find('\');'.encode())]
	page = page.split('+'.encode())
	if len(page) < 2:
		urlopen(url+'/logout')
		return get_page()
	page = page[0]+page[2]
	page = page.decode()
	return page

def get_salted_password():
	r = re.compile("\\\\\d*")
	salts = r.findall(get_page())	
	salted = ""
	for salt in salts:
		salted+=chr(int(salt[1:], 8))
	salted = salted[0:1]+password+salted[1:]
	return salted

def main():
	hashed_password= hashlib.md5(get_salted_password().encode('latin1')).hexdigest()
	values = {'username' : username, 'password': hashed_password}
	data = urllib.parse.urlencode(values)
	response = requests.post(url+'/login', data)

if __name__ == '__main__':
    main()