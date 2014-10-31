#!/usr/bin/env python
# coding: utf-8

"""
douban_seek

https://github.com/xiazcx/douban_seek

Copyright (C)  2014 nagev

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
import hashlib
import difflib
import random
import socket
import zlib
import time
import math
import json
import sys
import re
import os

ERROR_RETURN = False
SUCCESS_RETURN = True
MAX_TRY_TIME = 3
url_group_buffer = ""
douban_cookie = cookielib.CookieJar()
douban_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(douban_cookie))

douban_params = {
    "form_email":"707922063@qq.com",
    "form_password":"*********",
    "source":"index_nav"
}


def login_douban():
	print "First, please Login to douban"
	url_login = 'http://www.douban.com/accounts/login'
	response_login = douban_opener.open(url_login,urllib.urlencode(douban_params))
	if (response_login.geturl() == "http://www.douban.com/"):
		print "Login Success!"
	else:
		print response_login.read() 
	

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
	global douban_cookie
	member_content = re.findall(r'<a href="(.*)" class="nbg">',url_group_buffer)
	for member in member_content:
		member_id = re.search( r'http://www.douban.com/group/people/(.*)/',member)
		member_page = 'http://www.douban.com/group/people/' + member_id.group(1) + '/'
		#member_buffer = urllib.urlopen(member_page).read()
		member_buffer = douban_opener.open(member_page,urllib.urlencode(douban_params)).read()
		
		common_like_num = re.search(r'我和.*共同的喜好(\d)', member_buffer)
		print common_like_num 
	


def main():
	print "Start to seek your friends!"
	login_douban()
	if (open_group() == ERROR_RETURN):
		print "Open group failed, exit program"
	else:
		print "Start to from the group..."
		seek_group()

main()

