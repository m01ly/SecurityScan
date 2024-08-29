#!flask/bin/python
#pip freeze > requirements.txt
#pip show pipreqs version
import socket
#pip install geoip2

import geoip2.database
import pandas as pd
result=[]
def readfile():
    # df = pd.read_csv("ip24h.csv",nrows =5)
    df = pd.read_csv("dnslist20231227.csv")
    for index, row in df.iterrows():
        # row是一个pandas的Series对象，表示csv文件的一行数据
        print(str(index)+"--"+row["hostname"])
        args_request(row["hostname"],row["count_"])
def args_request(domain,count):
    # 接收处理GET数据请求
    ips = []
    try:
        addrs = socket.getaddrinfo(domain, None)
        for item in addrs:
            if item[4][0] not in ips:
                ips.append(item[4][0])
        print(ips[0])
        reader = geoip2.database.Reader('./GeoLite2-Country.mmdb')  # mmdb文件路径
        c = reader.country(ips[0])
        print(c.country.name)  # 国家名
        print(c.country.geoname_id)  # 国家代码
        result.append([domain, ips,c.country.name,count])
        #return jsonify(result="success", ip=ips[0], country=c.country.name, fqdn=domain)
    except Exception as e:
         print(str(e))
        #return jsonify(result="success", ip="", country="",fqdn=domain)
if __name__ == '__main__':
    readfile()
    city = pd.DataFrame(result, columns=['domain', 'ips','country','count'])
    city=city.explode("ips")
    city.to_csv('dnstocountry20240808.csv')


