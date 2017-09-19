import redis 
import socket
import multiprocessing
import time


class SpiderProcess(multiprocessing.Process):
	def __init__(self,rds,s2m):
		multiprocessing.Process.__init__(self)
		hostname = socket.gethostname()
		ip = socket.gethostbyname(hostname)		
		self.s2m = s2m
		self.m2s = ip
		self.name = ip
		self.rds = rds
		self.pub = rds.pubsub()

	# 在此函数中添加爬虫代码
	def __do_crawling(self, url='http://www.123.com/09889.jsp'):
		print("I am crawling %s" % url)
		time.sleep(2)
		
	# 在此函数中添加除爬虫外的其他功能
	def __do_sth(self, arg='nothing'):
		print("I am doing %s." % arg)
		time.sleep(1)

	def run(self):
		msg = str(0)+","+self.name
		rds.publish(self.s2m, msg)
		self.pub.subscribe(self.m2s)  
		for item in self.pub.listen():      
			if item['type'] == 'message':    
				data =item['data']   
				data = data.decode()
				msgs = data.split(",") 
				if msgs[0]=='0':
					# print("argument for do crawling is ", msgs[1])
					self.__do_crawling(url=msgs[1])
					msg = str(1)+","+self.name
					rds.publish(self.s2m,msg)
				elif msgs[0]=='1':
					self.__do_sth(arg=msgs[1])



if __name__ == "__main__":
	master_ip = 
	pool=redis.ConnectionPool(host=master_ip, port=6379)  
	rds = redis.StrictRedis(connection_pool=pool)  
	spd = SpiderProcess(rds,'s2m')
	spd.start()
