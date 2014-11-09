#!/usr/bin/env python
# coding: utf-8

"""
douban_seek: contact branch

https://github.com/xiazcx/douban_seek

Copyright (C)  2014 xiazcx

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""


from __future__ import print_function

__version__ = "0.20.16"
__author__ = "nagev"
__license__ = "GPLv3"

import __main__
import cookielib
import urllib
import urllib2
import logging
import getpass 
import time
import sys
import re
import os

douban_params = {
    "form_email":"xx@xx.com",
    "form_password":"******",
    "source":"index_nav"
}

class user_info(object):
	USER_ID = 0
	DOUBAN_ID = ""
	COMMON_RESULT = 0
	COMMON_STRING = ""


ERROR_RETURN = False
SUCCESS_RETURN = True
MEMBERS_PAGE_CNT = 20
contact_page_number = 0

list_contact_user = []
douban_cookie = cookielib.CookieJar()
douban_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(douban_cookie))


def login_douban():
	url_login = 'http://www.douban.com/accounts/login'
	email_login= raw_input("Please input your login email:")

	if re.match("\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*", email_login) == None:
		print ("Email not valid")
		return ERROR_RETURN
	else:
		douban_params["form_email"] = email_login
		psw_login = getpass.getpass("Please input your login password:")  
		douban_params["form_password"] = psw_login
		response_login = douban_opener.open(url_login,urllib.urlencode(douban_params))

		if(response_login.geturl() == "http://www.douban.com/"):
				return SUCCESS_RETURN
		else:
			html_login = response_login.read()
			imgurl_login = re.search('<img id="captcha_image" src="(.+?)" alt="captcha" class="captcha_image"/>', html_login)

			if imgurl_login:
				url_captcha = imgurl_login.group(1)
				res_captcha = urllib.urlretrieve(url_captcha, 'captcha.jpg')
				img_captcha = re.search('<input type="hidden" name="captcha-id" value="(.+?)"/>' ,html_login)

				if img_captcha:
					vcode_login =raw_input("Check image <captcha.jpg> at local directory and input:")
					douban_params["captcha-solution"] = vcode_login
					douban_params["captcha-id"] = img_captcha.group(1)
					douban_params["user_login"] = "登录"
					response_login = douban_opener.open(url_login,urllib.urlencode(douban_params))

					if (response_login.geturl() == "http://www.douban.com/"):
						return SUCCESS_RETURN
					else:
						return ERROR_RETURN
				else:
					return ERROR_RETURN
			else:
				return ERROR_RETURN

	

def open_contact():
	global contact_page_number
	contact_contacts_url = "http://www.douban.com/contacts/list"
	url_contact_buffer = douban_opener.open(contact_contacts_url).read()
	contact_page_str = re.search(r'<span class="thispage" data-total-page="(\d)*"', url_contact_buffer)
	if contact_page_str:
		contact_page_number = int(contact_page_str.group(1))
	else:
		contact_page_number = 1
	return SUCCESS_RETURN
			

def seek_contact():
	global contact_page_number
	page_cnt = 0
	id_cnt = 0
	
	print ("Start to counting...")
	while(page_cnt < contact_page_number):
		temp_contact_url = "http://www.douban.com/contacts/list?tag=0&start=" + str(page_cnt * MEMBERS_PAGE_CNT)		
		temp_contact_buffer = douban_opener.open(temp_contact_url).read()
		contact_content = re.findall(r'<a href="http://www.douban.com/people/(.*)/" title=".*">.*</a>',temp_contact_buffer)

		if contact_content:
			for contact in contact_content:
				contact_page_url = "http://www.douban.com/people/" + str(contact) + "/"
				contact_buffer = douban_opener.open(contact_page_url).read()
				time.sleep(1)
				common_like = re.search(r'我和.*共同的喜好\((\d*)\)', contact_buffer)
			
				if common_like:
					#print (common_like.group(0))
					temp_str = (common_like.group(0)).decode('utf-8').encode('gb18030')
					print (temp_str)
					found_contact = user_info()
					found_contact.USER_ID = id_cnt
					found_contact.COMMON_RESULT = int(common_like.group(1))	
					found_contact.DOUBAN_ID = contact_page_url 
					found_contact.COMMON_STRING = common_like.group(0) 
					list_contact_user.append(found_contact)	
					id_cnt += 1

		page_cnt += 1

	if id_cnt != 0:
		return SUCCESS_RETURN
	else:
		return ERROR_RETURN
	

def sortsave_result():
	global list_contact_user	
	list_contact_user.sort(key = lambda user_info:user_info.COMMON_RESULT,reverse = True)
	contact_list = open("contact_list.txt","w")
	for user in list_contact_user:
		contact_list.write( user.COMMON_STRING + "\n" )
	contact_list.close()
	return SUCCESS_RETURN 
	

def main():
	print ("Start to count your common-like number with your friends!")
	if( login_douban() == ERROR_RETURN):
		print ("Login Failed! exit program")
		return ERROR_RETURN
	else:
		print ("Login Success!")
		if (open_contact() == ERROR_RETURN):
			print ("Open friend list failed, exit program")
			return ERROR_RETURN
		else:
			if(seek_contact() == ERROR_RETURN):
				print ("Cannot find common-like with you friends, exit program")
				return ERROR_RETURN
			else:
				if( sortsave_result() == SUCCESS_RETURN):
					print ("Count complete, please check <contact_list.txt<> at local directory")
					return SUCCESS_RETURN
				else:
					print ("Save result failed, exit program")
					return ERROR_RETURN

if __name__ == "__main__":
	main()

