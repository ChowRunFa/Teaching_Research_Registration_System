import hashlib
import time 
import simplejson as json#pip install simplejson 或者 pip install python-simplejson
import base64
import hmac

def md5(m):
	return hashlib.md5(m.encode()).hexdigest()

def getNowDataTime():
	return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

def getTimeStamp():
	return time.time()

def getOrderNum():
	orderNum = str(getTimeStamp()).replace('.','')
	return orderNum

# #生成token 入参：用户id
# def generate_token(key, expire=3600):
#     ts_str = str(time.time() + expire)
#     ts_byte = ts_str.encode("utf-8")
#     sha1_tshexstr  = hmac.new(key.encode("utf-8"),ts_byte,'sha1').hexdigest()
#     token = ts_str+':'+sha1_tshexstr
#     b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
#     return b64_token.decode("utf-8")
#
# #验证token 入参：用户id 和 token
# def certify_token(key, token):
#     token_str = base64.urlsafe_b64decode(token).decode('utf-8')
#     token_list = token_str.split(':')
#     if len(token_list) != 2:
#         return False
#     ts_str = token_list[0]
#     if float(ts_str) < time.time():
#         # token expired
#         return False
#     known_sha1_tsstr = token_list[1]
#     sha1 = hmac.new(key.encode("utf-8"),ts_str.encode('utf-8'),'sha1')
#     calc_sha1_tsstr = sha1.hexdigest()
#     if calc_sha1_tsstr != known_sha1_tsstr:
#         # token certification failed
#         return False
#     # token certification success
#     return True

