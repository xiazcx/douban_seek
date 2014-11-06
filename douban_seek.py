#!/usr/bin/env python
# coding: utf-8

"""
douban_seek

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



__version__ = "0.20.16"
__author__ = "nagev"
__license__ = "GPLv3"

import cookielib
import urllib
import urllib2
import logging
import getpass 
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
MAX_TRY_TIME = 3

url_group_buffer = ""
list_found_user = []
douban_cookie = cookielib.CookieJar()
douban_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(douban_cookie))


def login_douban():
	url_login = 'http://www.douban.com/accounts/login'
	email_login= raw_input("Please input your login email:")

	if re.match("\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*", email_login) == None:
		print "Email not valid"
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
					vcode_login =raw_input("Check image <captcha.jpg> at local directory and input captcha:")
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

	

def open_group():
	global url_group_buffer
	try_cnt = 0

	while(try_cnt < MAX_TRY_TIME):
		group_id = raw_input("Please specify the group name or id your want to seek:")
		group_members_url ="http://www.douban.com/group/" + group_id +"/members"
		url_group_buffer = urllib.urlopen(group_members_url).read()
		title_content = re.search(r'<title>([\s\S]*)</title>', url_group_buffer)
		if title_content:
			if(title_content.group(1) == "页面不存在"):			
				print "Group name or id not valid"
				try_cnt +=1
				continue
			else:
				print "Enter the group - " + group_id
				break
		else:
			print "Group name or id not valid"
			try_cnt +=1
			continue
		
		if(try_cnt == MAX_TRY_TIME):
			return ERROR_RETURN
		else:
			return SUCCESS_RETURN 



def seek_group():
	global url_group_buffer
	global list_found_user	
	id_cnt = 0
	member_content = re.findall(r'<a href="(.*)" class="nbg">',url_group_buffer)

	for member in member_content:
		member_id = re.search( r'http://www.douban.com/group/people/(.*)/',member)
		member_page = 'http://www.douban.com/people/' + member_id.group(1) + '/'
		member_buffer = douban_opener.open(member_page).read()
		
		common_like = re.search(r'我和.*共同的喜好\((\d*)\)', member_buffer)
		if common_like:
			print common_like.group(0)
			found_member = user_info()
			found_member.USER_ID = id_cnt
			found_member.COMMON_RESULT = int(common_like.group(1))	
			found_member.DOUBAN_ID = member_page 
			found_member.COMMON_STRING = common_like.group(0) 
			list_found_user.append(found_member)	
			id_cnt += 1

	if id_cnt != 0:
		return SUCCESS_RETURN
	else:
		return ERROR_RETURN
	

def sortsave_result():
	global list_found_user	
	list_found_user.sort(key = lambda user_info:user_info.COMMON_RESULT,reverse = True)
	friend_list = open("friend_list.txt","w")
	for user in list_found_user:
		friend_list.write( user.COMMON_STRING +(" --> ") + user.DOUBAN_ID + "\n" )
	friend_list.close()
	return SUCCESS_RETURN 
	

def main():
	print "Start to seek your friends!"
	if( login_douban() == ERROR_RETURN):
		print "Login Failed! exit program"
		return ERROR_RETURN
	else:
		print "Login Success!"
		if (open_group() == ERROR_RETURN):
			print "Open group failed, exit program"
			return ERROR_RETURN
		else:
			print "Start seek from the group..."
			if(seek_group() == ERROR_RETURN):
				print "Cannot find friends in this group, exit program"
				return ERROR_RETURN
			else:
				if( sortsave_result() == SUCCESS_RETURN):
					print "Seek complete, please check <friend_list.txt<> at local directory"
					return SUCCESS_RETURN
				else:
					print "Save result failed, exit program"
					return ERROR_RETURN

main()

