import random,redis,threading
import master

def add_spd(r, spd_set, key):
	dur = key+'dur'
	url = key+'url'
	r.sadd(spd_set,key)
	r.set(dur,0)
	r.set(url,'')
	return len(r.smembers(spd_set))


def del_spd(r, spd_set, key):
	dur = key+'dur'
	url = key+'url'
	r.srem(spd_set,key)
	r.delete(dur)
	r.delete(url)
	return len(r.smembers(spd_set))


def list_spds(r, spd_set):
	print(r.smembers(spd_set))
	print("total spiders(%d): %s" % (r.scard(spd_set), r.smembers(spd_set)))


def add_urls(r, urllist):
	# get new_urls from my sql

	# put new_urls into url_list
	for url in new_urls:
		r.lpush(urllist, url)

	l = r.llen(urllist)
	print("add_urls() to %d" % l)
	

def chk_urllist(r, urllist='urllist', threshold=32):
	print("chk_urllist ...")
	if r.llen(urllist)<threshold:
		add_urls(r, urllist)
	else:
		print("%s urls in list" % r.llen(urllist))
	t=threading.Timer(3, chk_urllist, (r,urllist,threshold,))
	t.start()


def new_spiders(r,max=4):
	print("new spider was born ", random.randint(1,10))
	ip = '10.0.0.'+str(random.randint(2,255))
	while add_spd(r, spd_set='spd_set', key=ip)<max:
		# add code for starting spider.py
		ip = '10.0.0.'+str(random.randint(2,255))


def chk_spiders(r, spd_set, interval=10, overtime=20):
	print("chk_spiders ---")
	spds = r.smembers(spd_set)
	n_spd = r.scard(spd_set)
	if n_spd<30:
		for i in range(30-n_spd):
			new_spiders(r)

	for spd in spds:
		s = spd.decode()
		dur = s+'dur'
		if int(r.get(dur).decode())>overtime:
			print('s failed.')
			del_spd(r, spd_set, s)
			new_spiders(r)
	t=threading.Timer(interval,chk_spiders,(r, spd_set,interval,overtime,))
	t.start()


def main():
	master_ip = '10.0.0.120'
	spd_set = 'spd_set'
	urllist = 'urllist'
	pool=redis.ConnectionPool(host=master_ip,port=6379)  
	r = redis.StrictRedis(connection_pool=pool) 

	if r.exists(spd_set):
		r.delete(spd_set)
	# chk_spiders(r, spd_set=spd_set, interval=10)
	chk_urllist(r, urllist=urllist, threshold=60)
 
	server = master.server_Process(r)
	server.start()
	

if __name__ == '__main__':
	main()
