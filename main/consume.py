#/sign-in/

#{
#"username": "test1",
#"password": "0000"
#}


import requests
import random
import string

import os



url = "https://helloonions.com/sign-up/"
data = {
    "first_name": "ray guy",
    "last_name": "ray man",
    "email": "test1@helloonions.com",
    "password": "test1@2021*"
}

#r = requests.post(url, data=data)
#print(r.json())


url = "https://helloonions.com/sign-in/"
data = {
    "email": "raymondrayodiaga@gmail.com",
    "password": "0000"
}

r = requests.post(url, data=data)
print(r.json())


url = "https://helloonions.com/add-problem/"
files = {'video': open('/home/raymond/Downloads/yf.mp4','rb')}
data = {
	'auth_code': "fvt7646tas7ouvg2ur0ghh183hzs7wsm",
    'title' : "test from ray",
    'category' : "category ray",
    'duration' : "24hrs",
    'tag1' : "tag1",
    'detail'  : "this is a test from ray"
}

r = requests.post(url, files=files, data=data)
print(r.json())


url = "https://helloonions.com/add-solution/"
files = {'video': open('/home/raymond/Downloads/yf.mp4','rb')}
data = {
	'auth_code': "jtjm814njt16xwlbpidzbzu5qp0fl09j",
    'title' : "new solution 1",
    'problem_id': "109",
    'detail'  : "solution for issue 1"
}

#r = requests.post(url, files=files, data=data)
#print(r.status_code)




url = "http://localhost:8000/problem/add-clap/"
data = {
	'auth_code': "5zrzf0qwmp100yltv1bga6jvrymmj4yq",
    'problem_id': "1",
}

#r = requests.post(url, data=data)
#print(r.status_code)



url = "http://localhost:8000/problem/add-buzz/"
data = {
	"auth_code": "qd4r618hkxcns4erggpkcar1zoqn3s2d",
    "problem_id": "1",
}

#r = requests.post(url, data=data)
#print(r.status_code)





url = "https://helloonions.com/solution/add-clap/"
data = {
	'auth_code': "fvt7646tas7ouvg2ur0ghh183hzs7wsm",
    'solution_id': "22",
}

#r = requests.post(url, data=data)
#print(r.status_code)



url = "http://localhost:8000/solution/add-buzz/"
data = {
	'auth_code': "hxnn7vr4k87z2jqe8kl0px77ke7hw4qt",
    'solution_id': "1",
}

#r = requests.post(url, data=data)
#print(r.status_code)




url = "http://localhost:8000/solution/add-rating/"
data = {
	'auth_code': "hxnn7vr4k87z2jqe8kl0px77ke7hw4qt",
	'rating': "5",
    'solution_id': "1",
}

#r = requests.post(url, data=data)
#print(r.status_code)





url = "http://localhost:8000/edit-problem/"
data = {
	'auth_code': "hxnn7vr4k87z2jqe8kl0px77ke7hw4qt",

    'category' : "new category ray",
    'tag1' : "new tag1",
    'tag2' : "newest tag2",
    'tag3' : "newer tag3",
    'tag4' : "tag4",
    'tag5' : "tag5",

    "problem_id": "1"
}

#r = requests.post(url, data=data)
#print(r.status_code)




url = "https://onionsng.plglearn.com/edit-appuser/"
files = {'profile_photo': open('/home/raymond/Downloads/yf.mp4','rb')}
data = {
	'auth_code': "7xkypreqrw830cocvz919hzv2p0mv94v",

    'first_name' : "new fuck",
    'last_name' : "fuck ",
    'password': None

}

#r = requests.post(url, files=files, data=data)
#print(r.json())





url = "http://localhost:8000/appuser/request/new-password/"
data = {
	'auth_code': "fjei2f3lkghxpbmbbm57j9n4tupl8k9x",
    'email' : "odiagaraymondray@gmail.com"

}

#r = requests.post(url, data=data)
#print(r.status_code)




url = "http://localhost:8000/appuser/set/new-password/"
data = {
	'auth_code': "fjei2f3lkghxpbmbbm57j9n4tupl8k9x",

    'request_code' : "fjei2f3lkgh",
    'password1' : "7777",
    'password2': "7777"

}

#r = requests.post(url, data=data)
#print(r.status_code)




url = "http://localhost:8000/appuser/activate/"
data = {
	'auth_code': "fjei2f3lkghxpbmbbm57j9n4tupl8k9x",

    'request_code' : "fjei2f3lkg",
    'email' : "odiagaraymondray@gmail.com"

}

#r = requests.post(url, data=data)
#print(r.status_code)


