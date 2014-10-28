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


def open_group():
	cnt = 0
	while(cnt < 3):
		group_id = raw_input("Please specify the group name or id your want to seek:")
		group_members_url ="http://www.douban.com/group/" + group_id +"/members"
		url_buffer = urllib.urlopen(group_members_url).read()
		title_content = re.search(r'<title>([\s\S]*)</title>', url_buffer)
		if title_content:
			if(title_content.group(1) == "页面不存在"):
				print "Group name or id not valid"
				cnt +=1
				continue
			else:
				print "Enter the group - " + group_id
				break
		else:
			print "Group name or id not valid"
			cnt +=1
			continue
		
		if(cnt == 3):
			return 1
		else:
			return 0



def main():
	print "Start to seek your friends!"
	open_group()

main()

