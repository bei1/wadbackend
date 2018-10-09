import urllib.parse, urllib.request

paprams = urllib.parse.urlencode({'@username': '','@password': '','@action':'show'})

print(paprams)



webdata = urllib.request.urlopen('http://sw.bos.baidu.com/sw-search-sp/software/fe6cf004948ba/wrar_5.40.0.0_scp.exe').read()
output = open("../tests/wrar.exe", "wb")
output.write(webdata)
output.close()

print(len(webdata))
