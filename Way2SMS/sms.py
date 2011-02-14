#Class to send sms using Way2SMS.com

import urllib,urllib2,httplib2

class Way2SMS:
	
	def __init__(self,your_mobile_number,your_way2sms_password):
		self.__mobile_number = your_mobile_number
		self.__way2sms_password = your_way2sms_password
		self.__http = httplib2.Http()

	def sendSMS(self,receipient_number,message):
		cookie = self.__login()
		if(cookie == False):
			return 'Login Failed !.Please verify that your mobile number and way2sms password are correct.'
		action=self.__getActionValue(cookie)
		url = 'http://site3.way2sms.com/FirstServletsms'
		header_data={'Content-type': 'application/x-www-form-urlencoded',
	'User-Agent':'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
	'Cookie':cookie
	}
		body={'Action':action,'HiddenAction':'instantsms','MobNo':receipient_number,'catnamedis':'Birthday','chkall':'on',
			 'gpwd':'*******','guid':'username','textArea':message,'ypwd':'*******','yuid':'username'}		
		
		try:
			response,content = self.__http.request(url,'POST',headers=header_data,body=urllib.urlencode(body)) 
		except:
			return 'Oops,unable to send message !'

		if content.find("successfully") <> -1:
	       	    return 'Message sent successfully ! :)'
		else:
		    return 'Oops,message was not sent !'

	def __login(self):
		url='http://site3.way2sms.com/auth.cl'
		header_data={'Content-type': 'application/x-www-form-urlencoded',
	'User-Agent':'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10'
	}
		body={'username':self.__mobile_number,'password':self.__way2sms_password,'Submit':'Sign in'}
		try:
			response,content = self.__http.request(url,'POST',headers=header_data,body=urllib.urlencode(body))
			if(response['location'].find("Main") == -1):
				return False
			else:
				return response['set-cookie']
				 
		except:
			return False
				

	def __getActionValue(self,cookie):
		url = 'http://site3.way2sms.com/jsp/InstantSMS.jsp'
		header_data={'Content-type': 'application/x-www-form-urlencoded',
	'User-Agent':'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
	'Cookie':cookie
	}
		try:
			request = urllib2.Request(url,headers=header_data)
			content = urllib2.urlopen(request).read()
			pos = content.find("<input type=\"hidden\" name=\"Action")
			pos = pos+54 #Position of the first character of the action string
			action="" 
			while content[pos:pos+1] != "\"": #action string length is different for different way2sms accounts
				action+=content[pos:pos+1]
				pos+=1
			return action
		except:
			return False
		




