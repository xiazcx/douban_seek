Douban_Seek
===========

Douban_Seek is a Python Script used to seek the douban users who have 
common-like items with you form the douban groups.


current features:
---------------
  - Multi pages supported

  

How to Use
---------------

1. Download this Python code in any way

2. Run in console:
	python douban_seek.py

3. Enter your douban id(e-mail) and password.
If you are lucky enough, you will login directly;
But normally, you need to check the captcha image 
located at the same directory as douban_seek.py file, 
then input in console.
If you input the correct id, password and captcha code,
you will login successfully. Otherwise, please try again from 
step2;

4. Specify the douban group id you want to seek, like this group (Ubuntu):
"http://www.douban.com/group/ubuntu/", please input "ubuntu" 
(the string behind "...group/")

5. Input the page number of members you want to seek, each page 
contains 35 users; Please check the total pages first, make sure 
the number you input is less than the total number.

6. Just wait for a while, which depends on the page number you input.

7. After seek complete, the result is also saved at the same directory 
as douban_seek.py file, and it is sorted by descending order by the 
common-like number.


Requirements
------------
[Python](http://python.org/download/releases/) >= 2.6, 2.7 prefered


License
------------
Use of this source code is governed by a BSD-style
license that can be found in the License file.
