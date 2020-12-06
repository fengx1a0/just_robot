"""
/*** 本模块实现了自定义音乐查询获取并返回音乐CQ码kuq接口进行反向传输  ****/
/*** 音乐可以来自任何平台，并且支持查询操作****/
/*** write by @fengx1a0
"""
class FindMusic():
	def __init__(self,key):
		self.__key = key
		import requests
		self.__request = requests.get
		handle = self.__request(url="http://musicapi.leanapp.cn/search?keywords="+self.__key)
		_json = handle.json()
		self.__id = str(_json['result']['songs'][0]['id'])
		self.__songname = _json['result']['songs'][0]['name']
		self.__albumid = str(_json['result']['songs'][0]['album']['id'])
		
		tmp = _json['result']['songs'][0]['artists']
		self.__auth = ''
		for i in tmp:
			self.__auth+=i["name"]
			self.__auth+="/"
		self.__auth = self.__auth[:-1]
		handle.close()

	def get_url(self):
		return "https://music.163.com/#/song?id="+self.__id
	def get_image(self):
		handle = self.__request(url="http://musicapi.leanapp.cn/album?id="+self.__albumid)
		_json = handle.json()
		imageurl = _json['songs'][0]['al']['picUrl']
		handle.close()
		return imageurl
	def getaudio(self):
		return "https://music.163.com/song/media/outer/url?id="+self.__id+".mp3"
	def gettitle(self):
		return self.__songname
	def getcontent(self):
		return self.__auth

def get_music(msg): # 音乐名+fuzz搜索

	music=msg[6:-1]
	musicInfo = FindMusic(msg)
	try:
		musicInfo = FindMusic(msg)
	except:
		return "呜呜呜~该音乐未找到..."
	msg = "[CQ:music,type=custom,url={},audio={},title={},content={},image={}]".format(musicInfo.get_url() ,musicInfo.getaudio(),musicInfo.gettitle(),musicInfo.getcontent(),musicInfo.get_image())
	print(msg)
	return msg