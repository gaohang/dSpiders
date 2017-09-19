import redis, multiprocessing, random, time, sched
import checker


class server_Process(multiprocessing.Process):
	def __init__(self,rds,spd_set):
		multiprocessing.Process.__init__(self)
		self.r = rds
		self.pub = rds.pubsub()
		self.urllist = 'urllist'
		self.spd_set = 'spd_set'

	def __register_spider(self, spd_id, url):
		self.r.sadd(self.spd_set,spd_id)
		self.r.set(spd_id+'dur',0)
		self.r.set(spd_id+'url',url)

	def __dispath_task(self, spd_id, url):
		self.r.set(spd_id+'dur', 0)
		self.r.set(spd_id+'url', url)
		
	def __get_url(self):
		(ls, ret) = self.r.brpop(self.urllist,0)
		return ret.decode()

	def __init_urllist_mock(self):
		# get new_urls from my sql

		# put new_urls into url_list
		for url in new_urls:
			self.r.lpush(self.urllist, url)

	
	


	def run(self):
		self.__init_urllist_mock()
		self.pub.subscribe("s2m")  
		for item in self.pub.listen():      
			print(type(item),item)
			if item['type'] == 'message':    
				data =item['data']   
				data = data.decode()
				msgs = data.split(",") 
				if msgs[0]=='0':
					ip = msgs[1]
					url = self.__get_url()
					msg = str(0)+','+url
					self.r.publish(ip, msg)
					self.__register_spider(spd_id=ip, url)
				elif msgs[0]=='1':
					ip = msgs[1]
					url = self.__get_url()
					msg = str(0)+','+url
					self.r.publish(ip, msg)
					self.__dispath_task(spd_id=ip, url)
					


def main():
	master_ip = 
	spd_set = 'spd_set'
	urllist='urllist'
	pool=redis.ConnectionPool(host=master_ip, port=6379)  
	r = redis.StrictRedis(connection_pool=pool) 
	server = server_Process(r, spd_set)
	server.start()

	if r.exists(spd_set):
		r.delete(spd_set)
	checker.chk_spiders(r, spd_set=spd_set, interval=16)
	checker.chk_urllist(r, urllist=urllist, threshold=64)
 
	

	

if __name__ == '__main__':
	main()