import random
import base64
import hashlib
import re
import requests
import os 

wrong_msg = ["我可运行不了这种呀","不支持这么写啦", "看不懂这种呀", "哎呀，没有运行成功~"]
hack_msg=["听说你想fuxk我？","求求师傅别打啦！","师傅tql！！","别卷了,我爬还不行嘛","球球师傅给条活路吧！"]

def get_music(msg):
	msg=msg[6:-1]
	try:
		handle = requests.get(url="http://musicapi.leanapp.cn/search?keywords="+msg)
		id = str(handle.json()['result']['songs'][0]['id'])
	except:
 		return "呜呜呜~该音乐未找到..."
	msg='[CQ:music,type=163,id={}]'.format(id)
	return msg

def  get_image(msg):
	data = []
	if "F" in msg and "新" in msg :
		with open("/sand/data.bytes","r") as rs:
			tmp = rs.readlines()
			for i in range(len(tmp)):
				data.append(tmp[i].strip())
	elif "新" in msg:
		with open("/sand/data_newer.bytes","r") as rs:
			tmp = rs.readlines()
			for i in range(len(tmp)):
				data.append(tmp[i].strip())
	else:
		data = ['79162701','85926694-1','85926694-2','85926694-3','85926694-4','85926694-5','85925189','85925985-1','85925985-2','85944683','85925180','85931099','85925168','85925949','85944698','85944657','85926839','85925147','85948504']
	
	msg = '[CQ:image,file=http://pixiv.cat/{}.jpg]'.format(random.choice(data))
	return msg

def keyword_flider(keyword, msg):
	for i in keyword:
		if i not in msg:
			return False
	return True


def py_flider(msg):
	handle = open("/tmp/data.logs","a")
	handle.write(str(msg)+"\n")
	handle.close()
	if re.findall(r"request|class|read|open|exit|import|eval|dict|exec|popen|main|dir|sys|globals|\+|_|builtins|\'|\.|\\x|\[|\]|{|}|\||os|system|%",msg):
		return False
	return True
	

def do_python(msg):
	msg = msg[6:-1]
	try:
		if py_flider(msg):
			msg = msg.replace('"','\\"')
			a='{}'.format(msg)
			s='''python -c "print(eval('{}'))"'''.format(a)
			#print(msg)
			print(s)
			temp=os.popen(s).read()[0:-1]
			#temp = temp.replace('\\"','"')

			#temp = eval(msg)
		else:
			return random.choice(hack_msg)
		if temp != None and temp !='':
			return str(temp)
		else:
			return random.choice(wrong_msg)
	except:
		return "runtime error occurred!\n"+random.choice(wrong_msg)


def rcode(msg):
	if msg[:6] == "print(" and msg[-1] == ")":
		return [True, do_python(msg)]
	elif msg[:6] == "music(" and msg[-1] == ")":
		return [True, get_music(msg)]
	elif (msg[:4] == "md5(" or msg[:4] == "MD5(") and msg[-1] == ")":
		return [True, hashlib.md5(msg[4:-1].encode()).hexdigest()]
	elif (msg[:7] == "sha256(" or msg[:7] == "SHA256(") and msg[-1] == ")":
		return [True, hashlib.sha256(msg[7:-1].encode()).hexdigest()]
	elif (msg[:7] == "sha512(" or msg[:7] == "SHA512(") and msg[-1] == ")":
		return [True, hashlib.sha512(msg[7:-1].encode()).hexdigest()]
	elif msg[:10] == "b64encode(" and msg[-1] == ")":
		return [True, base64.b64encode(msg[10:-1].encode()).decode()]
	elif msg[:10] == "b64decode(" and msg[-1] == ")":
		return [True, base64.b64decode(msg[10:-1]).decode()]
	elif "涩图" in msg:
		return [True, get_image(msg)]
	else:
		return [None]
