HOST = 'http://spamapp.us-east-1.elasticbeanstalk.com/' # Ejemplo:  'http://migrupo.us-west-1.elasticbeanstalk.com/'

PASSWORD_SMALL = '123456789rafael'
PASSWORD_BIG = '123456789roger'
##------------------------------
import requests
import json 


USERNAME_SMALL = 'rafael'
USERNAME_BIG = 'roger' # El username que nos crearon con cupta grande


# pruebo sin headers
res = requests.get(HOST+'quota_info')
assert(res.status_code==401)

res = requests.get(HOST+'history/1')
assert(res.status_code==401)

res = requests.post(HOST+'process_email')
assert(res.status_code==401)



#### USERNAME_SMALL
data_login = {'username': USERNAME_SMALL, 'password':PASSWORD_SMALL}
response = requests.post(HOST+'api-token-auth/',data_login)
token = json.loads(response.content.decode('utf-8'))['token']
headers = { 'Authorization': f'JWT {token}' }

# usuario con 10 quotas
res = requests.get(HOST+'quota_info',headers=headers)
assert(res.status_code==200)
res_dic = json.loads(res.content.decode('utf-8'))
assert('procesados' in res_dic)
assert(res_dic['procesados'] == 0 )
assert(res_dic['disponible'] == 10 )


# usuario con 10 quotas
for i in range(1,11):
    res = requests.post(HOST+'process_email',data = {'text':'Hola como estas?'},
        headers=headers)
    assert(res.status_code==200)
    res_dic = json.loads(res.content.decode('utf-8'))
    assert('status' in res_dic)
    assert('result' in res_dic)
    assert(res_dic['status'] == 'ok' )
    assert(res_dic['result'] in ['HAM','SPAM'] )

    print(i,res.content)

    res = requests.get(HOST+'quota_info',headers=headers)
    assert(res.status_code==200)
    res_dic = json.loads(res.content.decode('utf-8'))
    assert('procesados' in res_dic)
    assert(res_dic['procesados'] == i )
    assert(res_dic['disponible'] == 10-i )

res = requests.post(HOST+'process_email',data = {'text':'Hola como estas?'},
        headers=headers)
res_dic = json.loads(res.content.decode('utf-8'))
assert(res_dic['status'] == "fail")
assert(res_dic['message'] == "No quota left")



####### USERNAME_BIG
data_login = {'username': USERNAME_BIG, 'password':PASSWORD_BIG}
response = requests.post(HOST+'api-token-auth/',data_login)
token = json.loads(response.content.decode('utf-8'))['token']
headers = { 'Authorization': f'JWT {token}' }

# usuario con 10 quotas
res = requests.get(HOST+'quota_info',headers=headers)
assert(res.status_code==200)
res_dic = json.loads(res.content.decode('utf-8'))
assert('procesados' in res_dic)
assert(res_dic['procesados'] == 0 )
assert(res_dic['disponible'] == 1000 )


# usuario con 100 quotas
for i in range(1,100):
    res = requests.post(HOST+'process_email',data = {'text':'Hola como estas?'},
        headers=headers)
    assert(res.status_code==200)
    res_dic = json.loads(res.content.decode('utf-8'))
    assert('status' in res_dic)
    assert('result' in res_dic)
    assert(res_dic['status'] == 'ok' )
    assert(res_dic['result'] in ['HAM','SPAM'] )

    print(i,res.content)

    res = requests.get(HOST+'quota_info',headers=headers)
    assert(res.status_code==200)
    res_dic = json.loads(res.content.decode('utf-8'))
    assert('procesados' in res_dic)
    assert(res_dic['procesados'] == i )
    assert(res_dic['disponible'] == 1000-i )

print('OK')
