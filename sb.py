import requests
from manifest import *

#response = requests.get(UI_HOST+'/flow/insert',params={'cid':1,'param':'5,8,6,9,3,5','result':'23.23','lable':'大脚优化','fstate':1})
res = requests.get(UI_HOST + '/flow/updateResult',
                                        params={'fid': 1, 'result':45 })
#print(res)
print(res.json())
