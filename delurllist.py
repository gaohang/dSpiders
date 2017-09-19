import redis


master_ip = '10.0.0.120'
spd_set = 'spd_set'
urllist = 'urllist'
pool=redis.ConnectionPool(host=server_ip, port=6379)  
r = redis.StrictRedis(connection_pool=pool) 

r.ltrim(urllist,0,0)
r.rpop(urllist)
print(r.llen(urllist))

