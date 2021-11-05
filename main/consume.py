#/sign-in/

#{
#"username": "test1",
#"password": "0000"
#}


import requests



url = "http://onionsng.com/sign-up/"
data = {
	"first_name": "test user20",
	"last_name": "ray",
	"email": "testemail20@gmail.com",
	"password": "0000"
}

r = requests.post(url, data=data)
r_json = r.json()
r_data = r_json["status"]

print(r_json)



url = "http://localhost:8000/sign-in/"
data = {
	"email": "odiagaraymondray@gmail.com",
	"password": "7777"
}

#r = requests.post(url, data=data)
#print(r.status_code)



url = "http://localhost:8000/add-problem/"
files = {'video': open('/home/raymond/Downloads/yf.mp4','rb')}
data = {
	'auth_code': "hxnn7vr4k87z2jqe8kl0px77ke7hw4qt",
    'title' : "sample video upload",
    'category' : "category y",
    'tag1' : "tag1",
    'tag2' : "tag2",
    'tag3' : "tag3",
    'tag4' : "tag4",
    'tag5' : "tag5",
    'detail'  : "sample problem video"
}

#r = requests.post(url, files=files, data=data)
#print(r.status_code)


url = "http://localhost:8000/add-solution/"
files = {'video': open('/home/raymond/Downloads/yf.mp4','rb')}
data = {
	'auth_code': "hxnn7vr4k87z2jqe8kl0px77ke7hw4qt",
    'title' : "new solution video",
    'problem_id': "1",
    'detail'  : "this is just some solution video!"
}

#r = requests.post(url, files=files, data=data)
#print(r.status_code)




url = "http://localhost:8000/problem/add-clap/"
data = {
	'auth_code': "hxnn7vr4k87z2jqe8kl0px77ke7hw4qt",
    'problem_id': "1",
}

#r = requests.post(url, data=data)
#print(r.status_code)



url = "http://localhost:8000/problem/add-buzz/"
data = {
	'auth_code': "hxnn7vr4k87z2jqe8kl0px77ke7hw4qt",
    'problem_id': "1",
}

#r = requests.post(url, data=data)
#print(r.status_code)





url = "http://localhost:8000/solution/add-clap/"
data = {
	'auth_code': "hxnn7vr4k87z2jqe8kl0px77ke7hw4qt",
    'solution_id': "1",
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




url = "http://localhost:8000/edit-appuser/"
data = {
	'auth_code': "fjei2f3lkghxpbmbbm57j9n4tupl8k9x",

    'first_name' : "new raymondo",
    'last_name' : "new odion-aga",
    'password': "7777"

}

#r = requests.post(url, data=data)
#print(r.status_code)





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


