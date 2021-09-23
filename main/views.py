from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User



@api_view(['POST'])
def SignUpView(request):

    if request.method == 'POST':

        full_name =request.data["full_name"]
        email =request.data["email"]
        username = request.data["username"]
        password = request.data["password"]

        user = User(username=username)
        user.set_password(password)
        user.save()

        app_user = AppUser.objects.create(user=user, full_name=full_name, email=email)
        app_user.save()

        data = {"status": "sign up successful"}

        serializer = StatusSerializer(data=data)

        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def SignInView(request):
    if request.method == 'POST':

        username = request.data["username"]
        password = request.data["password"]

        user = authenticate(username=username, password=password)

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
            return HttpResponse(str("errors!"))






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
    app_user = AppUser.objects.get(user__pk=request.user.id)

    if request.method == 'POST':
        #is_private = request.POST['is_private']

        title =request.data["title"]
        #video = request.FILES["video"]
        detail = request.data["detail"]

        #enctype=multipart/form-data
        #return HttpResponse(video)

        problem = Problem.objects.create(app_user=app_user, title=title, detail=detail)
        problem.save()

        data = {"status": "Problem added successfully"}

        serializer = StatusSerializer(data=data)

        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def AddSolutionView(request):
    app_user = AppUser.objects.get(user__pk=request.user.id)
    

    if request.method == 'POST':

        title =request.data["title"]
        #video = request.FILES["video"]
        detail = request.data["detail"]

        problem = Problem.objects.get(id=request.data["problem_id"])
        solution = Solution.objects.create(app_user=app_user, problem=problem, title=title, detail=detail)
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







