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
import os

from django.utils import timezone
import datetime

from django.core.mail import send_mail
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.db.models import Q




#########
#lp shit!
def IndexView(request):
    if request.method == "POST":
        pass


    else:
        
        context = {}
        return render(request, "main/index.html", context)


def PrivacyView(request):
    if request.method == "POST":
        pass


    else:
        
        context = {}
        return render(request, "main/privacy.html", context)



def ContactView(request):
    if request.method == "POST":
        pass


    else:
        
        context = {}
        return render(request, "main/contact.html", context)


def FaqView(request):
    if request.method == "POST":
        pass


    else:
        
        context = {}
        return render(request, "main/faq.html", context)




def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def RayRename(old_path):

    ext = old_path[-3:]
    new_path = str(old_path[:-4])
    new_path = new_path + id_generator() +"." + ext
    
    return new_path



def RemoveVideoFunc():

    try:
        from datetime import datetime

        all_problems = Problem.objects.all()

        for item in all_problems:

            switch_date = datetime(int(str(item.switch_date)[:4]), int(str(item.switch_date)[5:7]), int(str(item.switch_date)[8:10]))
            today_date = datetime.now()

            if today_date > switch_date or today_date == switch_date:

                problem = Problem.objects.get(id=item.id)

                
                try:
                    if os.path.exists(problem.video.path):
                        os.remove(problem.video.path)

                        #problem.video.path = "pp_files/videos/default_files/default.mp4"
                        #problem.save()

                except:
                    pass

                problem.status = False
                problem.save()



                all_solutions = Solution.objects.filter(problem__pk=item.id)

                for item2 in all_solutions:

                    try:
                        if os.path.exists(item2.video.path):
                            os.remove(item2.video.path)

                    except:
                        pass

                    item2.status = False
                    item2.save()


            else:
                output = str(today_date) +" " +str(switch_date)

    except:
        pass




#RemoveVideoFunc()

def ray_randomiser(length=12):
    landd = string.ascii_letters + string.digits
    return ''.join((random.choice(landd) for i in range(length)))




def RaySendMail(subject, message, to_email, code=None):

    try:
        context = {"subject": subject, "message": message, "code": code}
        html_message = render_to_string('main/message.html', context)
        message = strip_tags(message)
    
        send_mail(
            subject,
            message,
            'hello@helloonions.com',
            [to_email,],
            html_message=html_message,
            fail_silently=False,
        )

    except:
        pass




def NewProblemAlert(category):

    app_users = AppUser.objects.filter(interest=category)

    for item in app_users:
        RaySendMail("New Problem Alert!", "You have a new problem needs your solution!", item.user.username)



def EndTimeAlert(solution_id):

    solution = Solution.objects.get(id=solution_id)
    RaySendMail("Congratulations!", "Your solution(%s) with %s claps turned out to be the best!" % (solution.title, solution.claps.count()), solution.app_user.user.username)


@api_view(['POST'])
def SignUpView(request):
    if request.method == 'POST':

        request.session.create()
        auth_code = request.session.session_key

        first_name =request.data["first_name"]
        last_name =request.data["last_name"]
        email =request.data["email"]
        password = request.data["password"]

        try:

            user = User(username=email)
            user.set_password(password)
            user.save()

            app_user = AppUser.objects.create(user=user, auth_code=auth_code, first_name=first_name, last_name=last_name, email=email)

            request_code = ray_randomiser()
            app_user.request_code = request_code
            app_user.save()

            RaySendMail("Authentication", "Welcome to Onions, Please use the authentication code above to complete your sign up!", app_user.user.username, code=request_code)


            data = {"status": "sign up successful", "status_lean": True}

            serializer = StatusLeanSerializer(data=data)

            if serializer.is_valid():
                #serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



        except:

            data = {"status": "Error, email address already used.", "status_lean": False}

            serializer = StatusLeanSerializer(data=data)

            if serializer.is_valid():
                #serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
def SignInView(request):
    if request.method == 'POST':

        #RemoveVideoFunc()

        email = request.data["email"]
        password = request.data["password"]

        user = authenticate(username=email, password=password)
        
        try:
            if user.is_active:
                login(request, user)

            app_user = AppUser.objects.get(user__pk=request.user.id)
            data = {
                "status": True,
                "message": "Sign In Successful",
                "auth_code": app_user.auth_code,
                "first_name": app_user.first_name,
                "last_name": app_user.last_name,
                "payment_status": app_user.payment_status,
            }

            serializer = SignInStatusSerializer(data=data)

            if serializer.is_valid():
                #serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



        except:
            data = {
                "status": False,
                "message": "Error, incorrect username or password.",
                "auth_code": "None",
                "first_name": "None",
                "last_name": "None",
            }

            serializer = SignInStatusSerializer(data=data)

            if serializer.is_valid():
                #serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def ACGetAppUserView(request, auth_code):
    app_user = AppUser.objects.get(auth_code=auth_code)
    if request.method == 'GET':

        #RemoveVideoFunc()

        data = {
                "status": app_user.status,
                "profile_photo": app_user.profile_photo.url,
                "first_name": app_user.first_name,
                "last_name": app_user.last_name,
                "email": app_user.user.username,
                "payment_status": app_user.payment_status,
            }

        serializer = AppUserSerializer(data=data)

        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET'])
def IDGetAppUserView(request, app_user_id):
    app_user = AppUser.objects.get(id=app_user_id)
    if request.method == 'GET':

        #RemoveVideoFunc()

        data = {
                "status": app_user.status,
                "profile_photo": app_user.profile_photo.url,
                "first_name": app_user.first_name,
                "last_name": app_user.last_name,
                "email": app_user.user.username,
                "payment_status": app_user.payment_status,
            }

        serializer = AppUserSerializer(data=data)

        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








@api_view(['POST'])
def AddProblemView(request):

    if request.method == 'POST':
        auth_code =request.data["auth_code"]
        title =request.data["title"]
        video = request.FILES["video"]
        detail = request.data["detail"]

        category =request.data["category"]
        duration =request.data["duration"]

        if duration == "24hrs":
            days = 1

        elif duration == "48hrs":
            days = 2

        else:
            days = 3

        try:
            tag1 =request.data["tag1"]
        except:
            tag1 = None
            
        try:
            tag2 =request.data["tag2"]
        except:
            tag2 = None
            
        try:
            tag3 =request.data["tag3"]
        except:
            tag3 = None
            
        try:
            tag4 =request.data["tag4"]
        except:
            tag4 = None
            
        try:
            tag5 =request.data["tag5"]
        except:
            tag5 = None

        app_user = AppUser.objects.get(auth_code=auth_code)

        category = Category.objects.create(name=category, creator=str(app_user.user.username))
        category.save()
        
        problem = Problem.objects.create(app_user=app_user, auth_code=app_user.auth_code, app_user_name1=app_user.first_name, app_user_name2=app_user.last_name, profile_photo=app_user.profile_photo, title=title, detail=detail, category=category.name)
        
        if tag1:
            problem.tag1 = tag1
        if tag2:
            problem.tag2 = tag2
        if tag3:
            problem.tag3 = tag3
        if tag4:
            problem.tag4 = tag4
        if tag5:
            problem.tag5 = tag5

        today = timezone.now().date()
        nextD = today + datetime.timedelta(days=days)

        problem.switch_date = nextD

        problem.video = video
        problem.save()
        
        #os.rename(problem.video.path, RayRename(problem.video.path))

        NewProblemAlert(problem.category)

        data = {
            "status": "Problem added successfully",
            "status_lean": True,
            "problem_id": problem.id,
        }

        serializer = AddProblemStatusSerializer(data=data)

        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def EditProblemView(request):
    if request.method == 'POST':

        auth_code =request.data["auth_code"]

        category =request.data["category"]
        
        try:
            tag1 =request.data["tag1"]
        except:
            tag1 = None
            
        try:
            tag2 =request.data["tag2"]
        except:
            tag2 = None
            
        try:
            tag3 =request.data["tag3"]
        except:
            tag3 = None
            
        try:
            tag4 =request.data["tag4"]
        except:
            tag4 = None
            
        try:
            tag5 =request.data["tag5"]
        except:
            tag5 = None
            
            
        problem_id = request.data["problem_id"]

        app_user = AppUser.objects.get(auth_code=auth_code)

        problem = Problem.objects.get(id=problem_id)
        problem.category = category
        
        if tag1:
            problem.tag1 = tag1
        if tag2:
            problem.tag2 = tag2
        if tag3:
            problem.tag3 = tag3
        if tag4:
            problem.tag4 = tag4
        if tag5:
            problem.tag5 = tag5

        problem.save()

        data = {
            "status": "Problem edited successfully",
            "problem_id": problem.id,
        }

        serializer = AddProblemStatusSerializer(data=data)

        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






@api_view(['POST'])
def EditAppUserView(request):
    #print(request.session.session_key)

    if request.method == 'POST':

        try:
            auth_code =request.data["auth_code"]

            try:
                profile_photo = request.FILES["profile_photo"]

            except:
                profile_photo = None

            first_name =request.data["first_name"]
            last_name =request.data["last_name"]
            interest =request.data["interest"]

            try:
                password =request.data["password"]

            except:
                password = None


            app_user = AppUser.objects.get(auth_code=auth_code)
            
            if password != None:

                user = User.objects.get(username=app_user.email)
                user.set_password(password)
                user.save()

            app_user.first_name = first_name
            app_user.last_name = last_name
            app_user.interest = interest
            
            if profile_photo != None:
                app_user.profile_photo = profile_photo

            app_user.save()

            comments = Comment.objects.filter(app_user__id=app_user.id)
            for item in comments:
                item.first_name = app_user.first_name
                item.last_name = app_user.last_name
                item.profile_photo = app_user.profile_photo
                item.save()


            solutions = Solution.objects.filter(app_user__id=app_user.id)
            for item in solutions:
                item.app_user_name1 = app_user.first_name
                item.app_user_name2 = app_user.last_name
                item.profile_photo = app_user.profile_photo
                item.save()


            problems = Problem.objects.filter(app_user__id=app_user.id)
            for item in problems:
                item.app_user_name1 = app_user.first_name
                item.app_user_name2 = app_user.last_name
                item.profile_photo = app_user.profile_photo
                item.save()

            data = {"status": "User profile edited successfully", "status_lean": True}

            serializer = EditUserStatusSerializer(data=data)

            if serializer.is_valid():
                #serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except:
            data = {"status": "Sorry, profile did not edit successfully", "status_lean": False}

            serializer = EditUserStatusSerializer(data=data)

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
        solution = Solution.objects.create(app_user=app_user, auth_code=app_user.auth_code, app_user_name1=app_user.first_name, app_user_name2=app_user.last_name, profile_photo=app_user.profile_photo, problem=problem, title=title, detail=detail)
        solution.video = video
        solution.save()
        
        #os.rename(solution.video.path, RayRename(solution.video.path))

        data = {
            "status": "Solution added successfully",
            "status_lean": True,
            "solution_id": solution.id,
        }

        serializer = AddSolutionStatusSerializer(data=data)

        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def AddSCommentView(request):
    
    if request.method == 'POST':
        
        auth_code =request.data["auth_code"]
        comment =request.data["comment"]
        solution_id =request.data["solution_id"]
        
        app_user = AppUser.objects.get(auth_code=auth_code)
        solution = Solution.objects.get(id=solution_id)
        
        comment = Comment.objects.create(app_user=app_user, profile_photo=app_user.profile_photo, first_name=app_user.first_name, last_name=app_user.last_name, comment=comment)
        comment.save()
        sc = SolutionCommentConnector(solution=solution, comment=comment)
        sc.save()
        
        solution.comment_count += 1
        solution.save()
        
        data = {
            "status": "Comment added successfully", "status_lean": True
        }
        
        serializer = StatusLeanSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['POST'])
def AddPCommentView(request):
    
    if request.method == 'POST':
        
        auth_code =request.data["auth_code"]
        comment =request.data["comment"]
        problem_id =request.data["problem_id"]
        
        app_user = AppUser.objects.get(auth_code=auth_code)
        problem = Problem.objects.get(id=problem_id)
        
        comment = Comment.objects.create(app_user=app_user, profile_photo=app_user.profile_photo, first_name=app_user.first_name, last_name=app_user.last_name, comment=comment)
        comment.save()
        pc = ProblemCommentConnector(problem=problem, comment=comment)
        pc.save()
        
        problem.comment_count += 1
        problem.save()
        
        data = {
            "status": "Comment added successfully", "status_lean": True
        }
        
        serializer = StatusLeanSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



@api_view(['GET'])
def GetUserProblemsView(request, auth_code):
    app_user = AppUser.objects.get(auth_code=auth_code)
    if request.method == 'GET':
        problems = Problem.objects.filter(app_user=app_user)

        serializer = ProblemSerializer(problems, many=True)
        if serializer:
            return Response(serializer.data)

        else:
            return HttpResponse(str("errors!"))



@api_view(['GET'])
def GetUserSolutionsView(request, auth_code):
    app_user = AppUser.objects.get(auth_code=auth_code)
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
        solutions = Solution.objects.filter(problem=problem).order_by('-pub_date')

        serializer = SolutionSerializer(solutions, many=True)
        if serializer:
            return Response(serializer.data)

        else:
            return HttpResponse(str("errors!"))




@api_view(['GET'])
def GetAllProblemsView(request):
    if request.method == 'GET':

        #RemoveVideoFunc()

        problems = Problem.objects.filter(status=True).order_by('-pub_date')

        serializer = ProblemSerializer(problems, many=True)
        if serializer:
            return Response(serializer.data)

        else:
            return HttpResponse(str("errors!"))
            
            

@api_view(['GET'])
def GetAppUserNotificationView(request, auth_code):
    if request.method == 'GET':

        #RemoveVideoFunc()

        notifications = Notification.objects.filter(app_user__auth_code=auth_code).order_by('-pub_date')

        serializer = NotificationSerializer(notifications, many=True)
        if serializer:
            return Response(serializer.data)

        else:
            return HttpResponse(str("errors!"))
            
            

@api_view(['GET'])
def GetProblemDetailView(request, auth_code, problem_id):
    if request.method == 'GET':

        #RemoveVideoFunc()

        app_user = AppUser.objects.get(auth_code=auth_code)
        problem = Problem.objects.filter(id=problem_id)

        problem_k = Problem.objects.get(id=problem_id)
        view_status = False
        for item in problem_k.views.all():
            if item.app_user.id == app_user.id:
                view_status = True
                
        if view_status == False:
            view = View.objects.create(app_user=app_user)
            pv = ProblemViewConnector(problem=problem_k, view=view)
            pv.save()

            problem_k.view_count += 1
            problem_k.save()

        views = problem_k.views.all()
        viewed_users = []
        for item in views:
            viewed_users.append(item.app_user.auth_code)


        claps = problem_k.claps.all()
        clapped_users = []
        for item in claps:
            clapped_users.append(item.app_user.auth_code)


        buzzers = problem_k.buzzers.all()
        buzzed_users = []
        for item in buzzers:
            buzzed_users.append(item.app_user.auth_code)





        serializer = ProblemSerializer(problem, many=True)
        serializer_data = serializer.data + [{"viewed_users:": viewed_users}, {"buzzed_users:": buzzed_users}, {"clapped_users:": clapped_users}]
        if serializer:
            return Response(serializer.data)

        else:
            return HttpResponse(str("errors!"))
            
@api_view(['GET'])
def GetPCommentView(request, problem_id):
    if request.method == 'GET':
        problem = Problem.objects.get(id=problem_id)
        comments = problem.comments.all()

        serializer = CommentSerializer(comments, many=True)
        if serializer:
            return Response(serializer.data)

        else:
            return HttpResponse(str("errors!"))
    
    
@api_view(['GET'])
def GetSCommentView(request, solution_id):
    if request.method == 'GET':
        solution = Solution.objects.get(id=solution_id)
        comments = solution.comments.all()

        serializer = CommentSerializer(comments, many=True)
        if serializer:
            return Response(serializer.data)

        else:
            return HttpResponse(str("errors!"))


@api_view(['GET'])
def GetAllSolutionsView(request):
    if request.method == 'GET':

        #RemoveVideoFunc()

        solutions = Solution.objects.all().order_by('-pub_date')

        serializer = SolutionSerializer(solutions, many=True)
        if serializer:
            return Response(serializer.data)

        else:
            return HttpResponse(str("errors!"))



@api_view(['GET'])
def GetSolutionDetailView(request, auth_code, solution_id):
    if request.method == 'GET':

        #RemoveVideoFunc()

        app_user = AppUser.objects.get(auth_code=auth_code)
        solution = Solution.objects.filter(id=solution_id)

        solution_k = Solution.objects.get(id=solution_id)

        view_status = False
        for item in solution_k.views.all():
            if item.app_user.id == app_user.id:
                view_status = True
                
        if view_status == False:
            view = View.objects.create(app_user=app_user)
            sv = SolutionViewConnector(solution=solution_k, view=view)
            sv.save()

            solution_k.view_count += 1
            solution_k.save()

        views = solution_k.views.all()
        viewed_users = []
        for item in views:
            viewed_users.append(item.app_user.auth_code)


        claps = solution_k.claps.all()
        clapped_users = []
        for item in claps:
            clapped_users.append(item.app_user.auth_code)


        buzzers = solution_k.buzzers.all()
        buzzed_users = []
        for item in buzzers:
            buzzed_users.append(item.app_user.auth_code)


        serializer = SolutionSerializer(solution, many=True)
        serializer_data = serializer.data + [{"viewed_users:": viewed_users}, {"buzzed_users:": buzzed_users}, {"clapped_users:": clapped_users}]

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

        hand_status = False
        for clap in problem.claps.all():
            if clap.app_user.id == app_user.id:
                hand_status = True
                
        buzz_status = False
        for buzz in problem.buzzers.all():
            if buzz.app_user.id == app_user.id:
                buzz_status = True
                buzz.delete()
                problem.save()
                
        if hand_status == True:
            data = {"status": "Sorry, you clapped already", "status_lean": False}

            serializer = StatusCBSerializer(data=data)

            if serializer.is_valid():
                #serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            

        else:
            
            clap = Clap.objects.create(app_user=app_user)

            pc = ProblemClapConnector(problem=problem, clap=clap)
            pc.save()
            
            problem.clap_count = problem.claps.count()
            problem.buzzer_count = problem.buzzers.count()
            problem.save()

            data = {"status": "Clap added successfully", "status_lean": True}

            serializer = StatusCBSerializer(data=data)

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

        hand_status = False
        for buzz in problem.buzzers.all():
            if buzz.app_user.id == app_user.id:
                hand_status = True
                
        clap_status = False
        for clap in problem.claps.all():
            if clap.app_user.id == app_user.id:
                clap_status = True
                clap.delete()
                problem.save()
                
        if hand_status == True:
            data = {"status": "Sorry, you buzzed already.", "status_lean": False}

            serializer = StatusCBSerializer(data=data)

            if serializer.is_valid():
                #serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

        else:


            buzzer = Buzzer.objects.create(app_user=app_user)

            pb = ProblemBuzzerConnector(problem=problem, buzzer=buzzer)
            pb.save()
            
            problem.buzzer_count = problem.buzzers.count()
            problem.clap_count = problem.claps.count()
            problem.save()

            data = {"status": "Buzz added successfully", "status_lean": True}

            serializer = StatusCBSerializer(data=data)

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

        hand_status = False
        for clap in solution.claps.all():
            if clap.app_user.id == app_user.id:
                hand_status = True
                
        
        buzz_status = False
        for buzz in solution.buzzers.all():
            if buzz.app_user.id == app_user.id:
                buzz_status = True
                buzz.delete()
                solution.save()
                
                
        if hand_status == True:
            data = {"status": "Sorry, you clapped already.", "status_lean": False}

            serializer = StatusCBSerializer(data=data)

            if serializer.is_valid():
                #serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



        else:

            clap = Clap.objects.create(app_user=app_user)

            sc = SolutionClapConnector(solution=solution, clap=clap)
            sc.save()
            
            solution.clap_count = solution.claps.count()
            solution.buzzer_count = solution.buzzers.count()
            solution.save()

            data = {"status": "Clap added successfully", "status_lean": True}

            serializer = StatusCBSerializer(data=data)

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

        hand_status = False
        for buzz in solution.buzzers.all():
            if buzz.app_user.id == app_user.id:
                hand_status = True
                
        clap_status = False
        for clap in solution.claps.all():
            if clap.app_user.id == app_user.id:
                clap_status = True
                clap.delete()
                solution.save()
                
                
        if hand_status == True:
            data = {"status": "Sorry, you buzzed already.", "status_lean": False}

            serializer = StatusCBSerializer(data=data)

            if serializer.is_valid():
                #serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



        else:

            buzzer = Buzzer.objects.create(app_user=app_user)

            sb = SolutionBuzzerConnector(solution=solution, buzzer=buzzer)
            sb.save()
            
            solution.buzzer_count = solution.buzzers.count()
            solution.clap_count = solution.claps.count()
            solution.save()
            
            data = {"status": "Buzz added successfully", "status_lean": True}

            serializer = StatusCBSerializer(data=data)

            if serializer.is_valid():
                #serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def RateProblemView(request):
    if request.method == 'POST':

        auth_code =request.data["auth_code"]
        rating = request.data["rating"]
        problem_id = request.data["problem_id"]

        app_user = AppUser.objects.get(auth_code=auth_code)

        problem = Problem.objects.get(id=problem_id)
        problem.rating = int(rating)
        problem.save()

        data = {"status": "Rating added successfully", "status_lean": True}

        serializer = StatusLeanSerializer(data=data)

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

        data = {"status": "Rating added successfully", "status_lean": True}

        serializer = StatusLeanSerializer(data=data)

        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
def RequestNewPwView(request):

    if request.method == 'POST':

        email =request.data["email"]

        app_user = AppUser.objects.get(user__username=email)

        request_code = ray_randomiser()
        app_user.request_code = request_code
        app_user.save()

        RaySendMail("Password Reset", "Someone(you hopefully) have requested for a password change!", app_user.user.username, code=request_code)

        data = {"status": "New Password request was successful", "status_lean": True}

        serializer = StatusLeanSerializer(data=data)

        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def SetNewPwView(request):

    if request.method == 'POST':

        request_code =request.data["request_code"]
        password1 =request.data["password1"]
        password2 =request.data["password2"]

        if password2 == password1:

            app_user = AppUser.objects.get(request_code=request_code)

            if app_user.request_code == request_code:

                user = User.objects.get(username=app_user.email)
                user.set_password(password1)
                user.save()

                data = {"status": "New Password set successfully", "status_lean": True}

                serializer = StatusLeanSerializer(data=data)

                if serializer.is_valid():
                    #serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                data = {"status": "New Password Not set successfully", "status_lean": False}

                serializer = StatusLeanSerializer(data=data)

                if serializer.is_valid():
                    #serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)


        else:
            data = {"status": "New Password Not set successfully", "status_lean": False}

            serializer = StatusLeanSerializer(data=data)

            if serializer.is_valid():
                #serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)




@api_view(['POST'])
def ActivateUserView(request):

    if request.method == 'POST':

        request_code =request.data["request_code"]
        email =request.data["email"]

        app_user = AppUser.objects.get(user__username=email)

        if app_user.request_code == request_code:

            app_user.ec_status = True
            app_user.save()

            data = {"status": "Email confirmed successfully", "status_lean": True}

            serializer = StatusLeanSerializer(data=data)

            if serializer.is_valid():
                #serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            data = {"status": "Email Not confirmed successfully", "status_lean": False}

            serializer = StatusLeanSerializer(data=data)

            if serializer.is_valid():
                #serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)




@api_view(['POST'])
def SetPaymentView(request):

    if request.method == 'POST':

        auth_code =request.data["auth_code"]

        app_user = AppUser.objects.get(auth_code=auth_code)

        app_user.payment_status = True
        app_user.save()

        data = {"status": "Payment status set successfully", "status_lean": True}

        serializer = StatusLeanSerializer(data=data)

        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def GetAllTagView(request):

    if request.method == 'GET':

        problems = Problem.objects.all()

        tags = set()

        for item in problems:
            tags.add(item.tag1)
            tags.add(item.tag2)
            tags.add(item.tag3)
            tags.add(item.tag4)
            tags.add(item.tag5)

        data = {"status": True, "tags": tags}

        return Response(data)



@api_view(['GET'])
def GetAllCategoriesView(request):

    if request.method == 'GET':

        #RemoveVideoFunc()

        items = Category.objects.all()

        categories = set()

        for item in items:
            categories.add(item.name)

        data = {"status": True, "categories": categories}

        return Response(data)


@api_view(['POST'])
def ReportProblemView(request):

    if request.method == 'POST':

        auth_code =request.data["auth_code"]
        problem_id =request.data["problem_id"]
        reason =request.data["reason"]

        app_user = AppUser.objects.get(auth_code=auth_code)
        problem = Problem.objects.get(id=problem_id)

        report = Report(app_user=app_user, reason=reason)
        report.save()

        pr = ProblemReportConnector(problem=problem, report=report)
        pr.save()

        problem.report_count += 1
        problem.save()

        data = {"status": "Video Reported Successfully.", "status_lean": True}

        serializer = StatusLeanSerializer(data=data)

        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def ReportSolutionView(request):

    if request.method == 'POST':

        auth_code =request.data["auth_code"]
        solution_id =request.data["solution_id"]
        reason =request.data["reason"]

        app_user = AppUser.objects.get(auth_code=auth_code)
        solution = Solution.objects.get(id=solution_id)

        report = Report(app_user=app_user, reason=reason)
        report.save()

        sr = SolutionReportConnector(solution=solution, report=report)
        sr.save()

        solution.report_count += 1
        solution.save()

        data = {"status": "Video Reported Successfully.", "status_lean": True}

        serializer = StatusLeanSerializer(data=data)

        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def FindAllProblemsTView(request):

    if request.method == 'POST':
        tag = request.data["tag"]

        problems = Problem.objects.filter(Q(tag1=tag) | Q(tag2=tag) | Q(tag3=tag) | Q(tag4=tag) | Q(tag5=tag)).order_by('-pub_date')

        serializer = ProblemSerializer(problems, many=True)
        if serializer:
            return Response(serializer.data)

        else:
            return HttpResponse(str("errors!"))


@api_view(['POST'])
def FindAllProblemsCView(request):
    if request.method == 'POST':
        category = request.data["category"]

        problems = Problem.objects.filter(category=category, status=True).order_by('-pub_date')

        serializer = ProblemSerializer(problems, many=True)
        if serializer:
            return Response(serializer.data)



@api_view(['POST'])
def FindAllProblemsTiView(request):
    if request.method == 'POST':
        title = request.data["title"]

        problems = Problem.objects.filter(title=title, status=True).order_by('-pub_date')

        serializer = ProblemSerializer(problems, many=True)
        if serializer:
            return Response(serializer.data)



@api_view(['GET'])
def GetTimelineView(request):

    if request.method == 'GET':

        #RemoveVideoFunc()

        problems = Problem.objects.filter(status=True)
        solutions = Solution.objects.all()
        timeline = []

        for i in problems:

            i_list = {}
            i_list1 = []
            top_solution = Solution.objects.filter(problem__id=i.id).order_by('-clap_count').first()

            if top_solution:
                top_solutions = Solution.objects.filter(problem__id=i.id, clap_count=top_solution.clap_count)

                i_list = {

                "problem_title": i.title,
                "problem_detail": i.detail,
                "problem_video": i.video.url,
                
                "problem_category": i.category,
                "problem_tags": i.tag1 +"" +i.tag2 +"" +i.tag3 +"" +i.tag4 +"" +i.tag5,
                "problem_views": i.view_count,

                "problem_uploader_name1": i.app_user_name1,
                "problem_uploader_name2": i.app_user_name2,
                "problem_uploader_photo": i.profile_photo.url,

                "solutions_count": top_solutions.count(),
                
                "switch_date": i.switch_date,

                }


                for item in top_solutions:

                    #i_list['solution%s' % (item.id)] = {
                    i_list['solution'] = {

                        "solution_title": item.title,
                        "solution_video": item.video.url,
                        "solution_views": item.view_count,
                        "solution_claps": item.clap_count,
                        "solution_buzzers": item.buzzer_count,

                        "solution_uploader_name1": item.app_user_name1,
                        "solution_uploader_name2": item.app_user_name2,
                        "solution_uploader_photo": item.profile_photo.url,

                        }

                    if i.status == True:
                        pass
                        #EndTimeAlert(item.id)

                timeline.append(i_list)
            
            
        data = {"timeline": timeline}

        return Response(data)





@api_view(['GET'])
def AnalyticsVRView(request):

    if request.method == 'GET':

        highest_rated_solutions = []
        lowest_rated_solutions = []

        top_solution = Solution.objects.all().order_by('-rating').first()

        if top_solution:
            all_top_solutions = Solution.objects.filter(view_count=top_solution.rating)

            for item in all_top_solutions:
                item_list = {
                    "title": item.title,
                    "video": item.video.url,
                    "views": item.view_count,
                    "claps": item.clap_count,
                    "buzzers": item.buzzer_count,

                    "first_name": item.app_user_name1,
                    "last_name": item.app_user_name2,
                    "profile_photo": item.profile_photo.url,

                }


                highest_rated_solutions.append(item_list)


        top_solution = Solution.objects.all().order_by('-rating').last()
        if top_solution:    
            all_top_solutions = Solution.objects.filter(view_count=top_solution.rating)

            for item in all_top_solutions:
                item_list = {
                    "title": item.title,
                    "video": item.video.url,
                    "views": item.view_count,
                    "claps": item.clap_count,
                    "buzzers": item.buzzer_count,

                    "first_name": item.app_user_name1,
                    "last_name": item.app_user_name2,
                    "profile_photo": item.profile_photo.url,

                }


                lowest_rated_solutions.append(item_list)
        

        result = {

            "highest_rated_soltuions": highest_rated_solutions, 
            "lowest_rated_solutions": lowest_rated_solutions,

            }


        data = {"result": result}

        return Response(data)


@api_view(['GET'])
def AnalyticsVView(request):
    if request.method == 'GET':

        highest_viewed_problems = []
        lowest_viewed_problems = []
        highest_viewed_solutions = []
        lowest_viewed_solutions = []

        top_problem = Problem.objects.all().order_by('-view_count').first()

        if top_problem:
            all_top_problems = Problem.objects.filter(view_count=top_problem.view_count)

            for item in all_top_problems:
                item_list = {

                    "problem_title": item.title,
                    "problem_detail": item.detail,
                    "problem_video": item.video.url,
                    "problem_category": item.category,
                    "problem_tags": item.tag1 +"" +item.tag2 +"" +item.tag3 +"" +item.tag4 +"" +item.tag5,
                    "problem_views": item.view_count,

                    "problem_uploader_name1": item.app_user_name1,
                    "problem_uploader_name2": item.app_user_name2,
                    "problem_uploader_photo": item.profile_photo.url,

                }

                highest_viewed_problems.append(item_list)


        bottom_problem = Problem.objects.all().order_by('view_count').first()
        if bottom_problem:
            all_bottom_problems = Problem.objects.filter(view_count=bottom_problem.view_count)

            for item in all_bottom_problems:
                item_list = {

                    "problem_title": item.title,
                    "problem_detail": item.detail,
                    "problem_video": item.video.url,
                    "problem_category": item.category,
                    "problem_tags": item.tag1 +"" +item.tag2 +"" +item.tag3 +"" +item.tag4 +"" +item.tag5,
                    "problem_views": item.view_count,

                    "problem_uploader_name1": item.app_user_name1,
                    "problem_uploader_name2": item.app_user_name2,
                    "problem_uploader_photo": item.profile_photo.url,

                }

                lowest_viewed_problems.append(item_list)



        top_solution = Solution.objects.all().order_by('-view_count').first()
        if top_solution:
            all_top_solutions = Solution.objects.filter(view_count=top_solution.view_count)

            for item in all_top_solutions:
                item_list = {
                    "title": item.title,
                    "video": item.video.url,
                    "views": item.view_count,
                    "claps": item.clap_count,
                    "buzzers": item.buzzer_count,

                    "first_name": item.app_user_name1,
                    "last_name": item.app_user_name2,
                    "profile_photo": item.profile_photo.url,

                }

                highest_viewed_solutions.append(item_list)


        bottom_solution = Solution.objects.all().order_by('view_count').first()
        if bottom_solution:
            all_bottom_solution = Solution.objects.filter(view_count=bottom_solution.view_count)

            for item in all_bottom_solution:
                item_list = {
                    "title": item.title,
                    "video": item.video.url,
                    "views": item.view_count,
                    "claps": item.clap_count,
                    "buzzers": item.buzzer_count,

                    "first_name": item.app_user_name1,
                    "last_name": item.app_user_name2,
                    "profile_photo": item.profile_photo.url,

                }


                lowest_viewed_solutions.append(item_list)




        

        result = {

            "highest_viewed_problems": highest_viewed_problems, 
            "lowest_viewed_problems": lowest_viewed_problems,

            "highest_viewed_solutions": highest_viewed_solutions, 
            "lowest_viewed_solutions": lowest_viewed_solutions,

            }


        data = {"result": result}

        return Response(data)


@api_view(['GET'])
def AnalyticsTVView(request):
    total_problems = Problem.objects.all().count()
    total_solutions = Solution.objects.all().count()

    result = {

            "total_problems": total_problems, 
            "total_solutions": total_solutions,

        }


    data = {"result": result}

    return Response(data)



@api_view(['GET'])
def AnalyticsUVRView(request, auth_code):
    if request.method == 'GET':

        highest_rated_solutions = []
        lowest_rated_solutions = []

        top_solution = Solution.objects.filter(auth_code=auth_code).order_by('-rating').first()
        
        if top_solution:
            all_top_solutions = Solution.objects.filter(auth_code=auth_code, view_count=top_solution.rating)

            for item in all_top_solutions:
                item_list = {
                    "title": item.title,
                    "video": item.video.url,
                    "views": item.view_count,
                    "claps": item.clap_count,
                    "buzzers": item.buzzer_count,

                    "first_name": item.app_user_name1,
                    "last_name": item.app_user_name2,
                    "profile_photo": item.profile_photo.url,

                }


                highest_rated_solutions.append(item_list)


        top_solution = Solution.objects.filter(auth_code=auth_code).order_by('-rating').last()
        if top_solution:
            all_top_solutions = Solution.objects.filter(auth_code=auth_code, view_count=top_solution.rating)

            for item in all_top_solutions:
                item_list = {
                    "title": item.title,
                    "video": item.video.url,
                    "views": item.view_count,
                    "claps": item.clap_count,
                    "buzzers": item.buzzer_count,

                    "first_name": item.app_user_name1,
                    "last_name": item.app_user_name2,
                    "profile_photo": item.profile_photo.url,

                }


                lowest_rated_solutions.append(item_list)
        

        result = {

            "highest_rated_soltuions": highest_rated_solutions, 
            "lowest_rated_solutions": lowest_rated_solutions,

            }


        data = {"result": result}

        return Response(data)


@api_view(['GET'])
def AnalyticsUVView(request, auth_code):
    if request.method == 'GET':

        highest_viewed_problems = []
        lowest_viewed_problems = []
        highest_viewed_solutions = []
        lowest_viewed_solutions = []

        top_problem = Problem.objects.filter(auth_code=auth_code).order_by('-view_count').first()
        
        if top_problem:
            all_top_problems = Problem.objects.filter(auth_code=auth_code, view_count=top_problem.view_count)

            for item in all_top_problems:
                item_list = {

                    "problem_title": item.title,
                    "problem_detail": item.detail,
                    "problem_video": item.video.url,
                    "problem_category": item.category,
                    "problem_tags": item.tag1 +"" +item.tag2 +"" +item.tag3 +"" +item.tag4 +"" +item.tag5,
                    "problem_views": item.view_count,

                    "problem_uploader_name1": item.app_user_name1,
                    "problem_uploader_name2": item.app_user_name2,
                    "problem_uploader_photo": item.profile_photo.url,

                }

                highest_viewed_problems.append(item_list)


        bottom_problem = Problem.objects.filter(auth_code=auth_code).order_by('view_count').first()
            
        if bottom_problem:    
            all_bottom_problems = Problem.objects.filter(auth_code=auth_code, view_count=bottom_problem.view_count)

            for item in all_bottom_problems:
                item_list = {

                    "problem_title": item.title,
                    "problem_detail": item.detail,
                    "problem_video": item.video.url,
                    "problem_category": item.category,
                    "problem_tags": item.tag1 +"" +item.tag2 +"" +item.tag3 +"" +item.tag4 +"" +item.tag5,
                    "problem_views": item.view_count,

                    "problem_uploader_name1": item.app_user_name1,
                    "problem_uploader_name2": item.app_user_name2,
                    "problem_uploader_photo": item.profile_photo.url,

                }

                lowest_viewed_problems.append(item_list)



        top_solution = Solution.objects.filter(auth_code=auth_code).order_by('-view_count').first()
        if top_solution:
            all_top_solutions = Solution.objects.filter(auth_code=auth_code, view_count=top_solution.view_count)

            for item in all_top_solutions:
                item_list = {
                    "title": item.title,
                    "video": item.video.url,
                    "views": item.view_count,
                    "claps": item.clap_count,
                    "buzzers": item.buzzer_count,

                    "first_name": item.app_user_name1,
                    "last_name": item.app_user_name2,
                    "profile_photo": item.profile_photo.url,

                }

                highest_viewed_solutions.append(item_list)


        bottom_solution = Solution.objects.filter(auth_code=auth_code).order_by('view_count').first()
        if bottom_solution:
            all_bottom_solution = Solution.objects.filter(auth_code=auth_code, view_count=bottom_solution.view_count)

            for item in all_bottom_solution:
                item_list = {
                    "title": item.title,
                    "video": item.video.url,
                    "views": item.view_count,
                    "claps": item.clap_count,
                    "buzzers": item.buzzer_count,

                    "first_name": item.app_user_name1,
                    "last_name": item.app_user_name2,
                    "profile_photo": item.profile_photo.url,

                }

                lowest_viewed_solutions.append(item_list)




            

        result = {

            "highest_viewed_problems": highest_viewed_problems, 
            "lowest_viewed_problems": lowest_viewed_problems,

            "highest_viewed_solutions": highest_viewed_solutions, 
            "lowest_viewed_solutions": lowest_viewed_solutions,

            }


        data = {"result": result}

        return Response(data)


@api_view(['GET'])
def AnalyticsUTVView(request, auth_code):
    total_problems = Problem.objects.filter(auth_code=auth_code).count()
    total_solutions = Solution.objects.filter(auth_code=auth_code).count()

    result = {

            "total_problems": total_problems, 
            "total_solutions": total_solutions,
            
        }


    data = {"result": result}

    return Response(data)







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







