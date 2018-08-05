import json

info_dict = {'user':'maoyu','password':'chuimao'}
print(info_dict)

teststr = json.dumps(info_dict)
print(teststr)

p = json.loads(teststr)

print(p)
print(p['user'])
print(p['password'])
