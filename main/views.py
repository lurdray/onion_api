from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User


import random
import string

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags




def ray_randomiser(length=12):
    landd = string.ascii_letters + string.digits
    return ''.join((random.choice(landd) for i in range(length)))




def RaySendMail(request, subject, message, to_email, code=None):

    context = {"subject": subject, "message": message, "code": code}
    html_message = render_to_string('main/message.html', context)
    message = strip_tags(message)

    send_mail(
        subject,
        message,
        'onionng@onionng.com',
        [to_email,],
        html_message=html_message,
        fail_silently=False,
    )




@api_view(['POST'])
def SignUpView(request):

    if request.method == 'POST':

        request.session.create()
        auth_code = request.session.session_key

        first_name =request.data["first_name"]
        last_name =request.data["last_name"]
        email =request.data["email"]
        password = request.data["password"]

        user = User(username=email)
        user.set_password(password)
        user.save()

        app_user = AppUser.objects.create(user=user, auth_code=auth_code, first_name=first_name, last_name=last_name, email=email)

        request_code = ray_randomiser()
        app_user.request_code = request_code
        app_user.save()

        RaySendMail(request, "Authentication", "Welcome to Onionng.com, Please use the authentication code below to complete your sign up!", app_user.user.username, code=request_code)


        data = {"status": "sign up successful"}

        serializer = StatusSerializer(data=data)

        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def SignInView(request):
    if request.method == 'POST':

        email = request.data["email"]
        password = request.data["password"]

        user = authenticate(username=email, password=password)

        if user:
            if user.is_active:
                login(request, user)

            data = {"status": "sign in successful"}

            serializer = StatusSerializer(data=data)

            if serializer.is_valid():
                #serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        else:
            return Response(status.HTTP_400_BAD_REQUEST)
            #return HttpResponse(str("errors!"))






@api_view(['GET'])
def GetAppUserView(request, app_user_id):
    app_user = AppUser.objects.filter(id=app_user_id)
    if request.method == 'GET':

        serializer = AppUserSerializer(app_user, many=True)
        if serializer:
            return Response(serializer.data)

        else:
            return HttpResponse(str("errors!"))








@api_view(['POST'])
def AddProblemView(request):

    if request.method == 'POST':

        auth_code =request.data["auth_code"]
        title =request.data["title"]
        video = request.FILES["video"]
        detail = request.data["detail"]

        category =request.data["category"]
        tag1 =request.data["tag1"]
        tag2 =request.data["tag2"]
        tag3 =request.data["tag3"]
        tag4 =request.data["tag4"]
        tag5 =request.data["tag5"]

        app_user = AppUser.objects.get(auth_code=auth_code)

        problem = Problem.objects.create(app_user=app_user, title=title, detail=detail,
            category=category, tag1=tag1, tag2=tag2, tag3=tag3, tag4=tag4, tag5=tag5)
        
        problem.video = video
        problem.save()

        data = {"status": "Problem added successfully"}

        serializer = StatusSerializer(data=data)

        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def EditProblemView(request):
    if request.method == 'POST':

        auth_code =request.data["auth_code"]

        category =request.data["category"]
        tag1 =request.data["tag1"]
        tag2 =request.data["tag2"]
        tag3 =request.data["tag3"]
        tag4 =request.data["tag4"]
        tag5 =request.data["tag5"]

        problem_id = request.data["problem_id"]

        app_user = AppUser.objects.get(auth_code=auth_code)

        problem = Problem.objects.get(id=problem_id)
        problem.category = category
        problem.tag1 = tag1
        problem.tag2 = tag2
        problem.tag3 = tag3
        problem.tag4 = tag4
        problem.tag5 = tag5

        problem.save()

        data = {"status": "Problem edited successfully"}

        serializer = StatusSerializer(data=data)

        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






@api_view(['POST'])
def EditAppUserView(request):
    print(request.session.session_key)

    if request.method == 'POST':

        auth_code =request.data["auth_code"]

        first_name =request.data["first_name"]
        last_name =request.data["last_name"]

        password =request.data["password"]


        app_user = AppUser.objects.get(auth_code=auth_code)

        user = User.objects.get(username=app_user.email)
        user.set_password(password)
        user.save()

        app_user.first_name = first_name
        app_user.last_name = last_name

        app_user.save()

        data = {"status": "User edited successfully"}

        serializer = StatusSerializer(data=data)

        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        



@api_view(['POST'])
def AddSolutionView(request):

    if request.method == 'POST':

        auth_code =request.data["auth_code"]
        title =request.data["title"]
        video = request.FILES["video"]
        detail = request.data["detail"]
        problem_id = request.data["problem_id"]

        app_user = AppUser.objects.get(auth_code=auth_code)

        problem = Problem.objects.get(id=problem_id)
        solution = Solution.objects.create(app_user=app_user, problem=problem, title=title, detail=detail)
        solution.video = video
        solution.save()

        data = {"status": "Solution added successfully"}

        serializer = StatusSerializer(data=data)

        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def GetUserProblemsView(request, app_user_id):
    app_user = AppUser.objects.get(id=app_user_id)
    if request.method == 'GET':
        problems = Problem.objects.filter(app_user=app_user)

        serializer = ProblemSerializer(problems, many=True)
        if serializer:
            return Response(serializer.data)

        else:
            return HttpResponse(str("errors!"))



@api_view(['GET'])
def GetUserSolutionsView(request, app_user_id):
    app_user = AppUser.objects.get(id=app_user_id)
    if request.method == 'GET':
        solutions = Solution.objects.filter(app_user=app_user)

        serializer = SolutionSerializer(solutions, many=True)
        if serializer:
            return Response(serializer.data)

        else:
            return HttpResponse(str("errors!"))




@api_view(['GET'])
def GetProblemSolutionsView(request, problem_id):
    problem = Problem.objects.get(id=problem_id)
    if request.method == 'GET':
        solutions = Solution.objects.filter(problem=problem)

        serializer = SolutionSerializer(solutions, many=True)
        if serializer:
            return Response(serializer.data)

        else:
            return HttpResponse(str("errors!"))




@api_view(['GET'])
def GetAllProblemsView(request):
    if request.method == 'GET':
        problems = Problem.objects.all()

        serializer = ProblemSerializer(problems, many=True)
        if serializer:
            return Response(serializer.data)

        else:
            return HttpResponse(str("errors!"))



@api_view(['GET'])
def GetAllSolutionsView(request):
    if request.method == 'GET':
        solutions = Solution.objects.all()

        serializer = SolutionSerializer(solutions, many=True)
        if serializer:
            return Response(serializer.data)

        else:
            return HttpResponse(str("errors!"))




@api_view(['POST'])
def AddProblemClapView(request):

    if request.method == 'POST':

        auth_code =request.data["auth_code"]
        problem_id = request.data["problem_id"]

        app_user = AppUser.objects.get(auth_code=auth_code)

        problem = Problem.objects.get(id=problem_id)
        clap = Clap.objects.create(app_user=app_user)

        pc = ProblemClapConnector(problem=problem, clap=clap)
        pc.save()

        data = {"status": "Clap added successfully"}

        serializer = StatusSerializer(data=data)

        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def AddProblemBuzzView(request):

    if request.method == 'POST':

        auth_code =request.data["auth_code"]
        problem_id = request.data["problem_id"]

        app_user = AppUser.objects.get(auth_code=auth_code)

        problem = Problem.objects.get(id=problem_id)
        buzzer = Buzzer.objects.create(app_user=app_user)

        pb = ProblemBuzzerConnector(problem=problem, buzzer=buzzer)
        pb.save()

        data = {"status": "Buzz added successfully"}

        serializer = StatusSerializer(data=data)

        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
def AddSolutionClapView(request):

    if request.method == 'POST':

        auth_code =request.data["auth_code"]
        solution_id = request.data["solution_id"]

        app_user = AppUser.objects.get(auth_code=auth_code)

        solution = Solution.objects.get(id=solution_id)
        clap = Clap.objects.create(app_user=app_user)

        sc = SolutionClapConnector(solution=solution, clap=clap)
        sc.save()

        data = {"status": "Clap added successfully"}

        serializer = StatusSerializer(data=data)

        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def AddSolutionBuzzView(request):

    if request.method == 'POST':

        auth_code =request.data["auth_code"]
        solution_id = request.data["solution_id"]

        app_user = AppUser.objects.get(auth_code=auth_code)

        solution = Solution.objects.get(id=solution_id)
        buzzer = Buzzer.objects.create(app_user=app_user)

        sb = SolutionBuzzerConnector(solution=solution, buzzer=buzzer)
        sb.save()

        data = {"status": "Buzz added successfully"}

        serializer = StatusSerializer(data=data)

        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
def RateSolutionView(request):

    if request.method == 'POST':

        auth_code =request.data["auth_code"]
        rating = request.data["rating"]
        solution_id = request.data["solution_id"]

        app_user = AppUser.objects.get(auth_code=auth_code)

        solution = Solution.objects.get(id=solution_id)
        solution.rating = int(rating)
        solution.save()

        data = {"status": "Rating added successfully"}

        serializer = StatusSerializer(data=data)

        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
def RequestNewPwView(request):

    if request.method == 'POST':

        auth_code =request.data["auth_code"]
        email =request.data["email"]

        app_user = AppUser.objects.get(auth_code=auth_code)

        request_code = ray_randomiser()
        app_user.request_code = request_code
        app_user.save()

        RaySendMail(request, "Password Reset", "Someone(you hopefully) have requested for a password change!", app_user.user.username, code=request_code)

        data = {"status": "New Password request was successful"}

        serializer = StatusSerializer(data=data)

        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def SetNewPwView(request):

    if request.method == 'POST':

        auth_code =request.data["auth_code"]
        request_code =request.data["request_code"]
        password1 =request.data["password1"]
        password2 =request.data["password2"]

        if password2 == password1:

            app_user = AppUser.objects.get(auth_code=auth_code)

            if app_user.request_code == request_code:

                user = User.objects.get(username=app_user.email)
                user.set_password(password1)
                user.save()

                data = {"status": "New Password set successfully"}

                serializer = StatusSerializer(data=data)

                if serializer.is_valid():
                    #serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)


        else:
            return Response(status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def ActivateUserView(request):

    if request.method == 'POST':

        auth_code =request.data["auth_code"]
        request_code =request.data["request_code"]
        email =request.data["email"]

        app_user = AppUser.objects.get(auth_code=auth_code)

        if app_user.request_code == request_code:

            app_user.ec_status = True
            app_user.save()

            data = {"status": "Email confirmed successfully"}

            serializer = StatusSerializer(data=data)

            if serializer.is_valid():
                #serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

























##########################################
@api_view(['GET'])
def GetBnbBalanceView(request, wallet_address):

    if request.method == 'GET':
        balance = GetBalance(wallet_address, "ether")

        data = {
        "balance": str(balance),
        }

        #return HttpResponse(str(data))

        serializer = BalanceSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data)

        else:
            return HttpResponse(str("errors!"))





@api_view(['POST'])
def SendBnbCoin(request,):

    if request.method == 'POST':
        sender = request.data["sender"]
        receiver = request.data["receiver"]
        amount = request.data["amount"]
        sender_key = request.data["sender_key"]

        txn_hash = Send(sender, receiver, amount, "ether", sender_key)

        data = {
        "txn_hash": str(txn_hash),

        }

        return HttpResponse(str(data))

        serializer = TxnSerializer(data=data)

        if serializer.is_valid():
            return Response(serializer.data)

        else:
            return HttpResponse(str("errors!"))







