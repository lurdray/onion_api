#/sign-in/

#{
#"username": "test1",
#"password": "0000"
#}


import requests



url = "http://localhost:8000/sign-up/"
data = {
	"first_name": "test sam",
	"last_name": "muel",
	"email": "sam4@gmail.com",
	"password": "0000"
}

#r = requests.post(url, data=data)
#print(r.json())


url = "http://localhost:8000/sign-in/"
data = {
	"email": "sam4@gmail.com",
	"password": "0000"
}

r = requests.post(url, data=data)
print(r.json())


url = "http://localhost:8000/add-problem/"
files = {'video': open('/home/raymond/Downloads/yf.mp4','rb')}
data = {
	'auth_code': "5zrzf0qwmp100yltv1bga6jvrymmj4yq",
    'title' : "sample video upload",
    'category' : "category y",
    'duration' : "24hrs",
    'tag1' : "tag1",
    'tag2' : "tag2",
    'tag3' : "tag3",
    'tag4' : "tag4",
    'tag5' : "tag5",
    'detail'  : "sample problem video"
}

#r = requests.post(url, files=files, data=data)
#print(r.json())


url = "http://localhost:8000/add-solution/"
files = {'video': open('/home/raymond/Downloads/yf.mp4','rb')}
data = {
	'auth_code': "dmjy9xdsbyxucgdbt55s4g2clcna3ys6",
    'title' : "new solution video",
    'problem_id': "1",
    'detail'  : "this is just some solution video!"
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





url = "http://localhost:8000/solution/add-clap/"
data = {
	'auth_code': "qhjg6yadk3973hb2l8plv0sja9zgyvzk",
    'solution_id': "1",
}

r = requests.post(url, data=data)
print(r.status_code)



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


