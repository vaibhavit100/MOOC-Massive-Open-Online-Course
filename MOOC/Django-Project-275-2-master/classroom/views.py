# Create your views here.
from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login
# from classroom.models import posts
from django.http import HttpResponse
from django.template import RequestContext
import requests
import json
import sys
import simplejson
from classroom.models import MOOC_User
from django.contrib.auth import logout

#from requests import session
import httpconnection
#SQLite-Django auth
from django.contrib.auth import logout
#SQLite models 
#from classroom.models import userTable
#from requests import session
import httpconnection
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db import IntegrityError

def index(request):
    return render(request, 'index.html')

def signIn(request):
    #c={}
    #c.update(csrf((request)))
    return render(request, 'login.html')


def addMOOC(request):
    list=MOOC_User.objects.all()
    return render_to_response("home.html",{"message":list})



# login to home page - This is called when user is in the DB and login is successful
def home(request):
  list=MOOC_User.objects.all()

  try:
      username = password = ''
      if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        print username
        print password
        user = authenticate(username=username, password=password)
        print "User value is",user

        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['username'] = username
                request.session['user'] = user

                return render_to_response('home.html',{"user" : username ,"list": list})
                # Redirect to a success page.
            else:
                return render_to_response('login.html',{"message": "User is Inactive"})

                # Return a 'disabled account' error message

        else:
            return render_to_response('login.html',{"message": "Invalid Credential"})
      else:
          return render_to_response('home.html',{"user" : request.session['username']})
  except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})


#
# Sign Up function
def signUp(request):

   return render(request, 'signUp.html')



# signup_home page fucntion is called when there is new user entry
def signUpHome(request):
    try:
        if request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            user = User.objects.create_user(username, '', password)
            user.last_name = lastname
            user.first_name= firstname
            payload = { "email": username,"own": [] ,"enrolled": [] ,"quizzes": [] }
            data=json.dumps(payload)
            r=httpconnection.signUpHome_Connect(data)
            print "Status code is",r.status_code
            if r.status_code==200 or r.status_code==201 :
                user.save()
                return render_to_response("login.html",{"message":"You have successfully registered"})

            else:
                return render_to_response("login.html", {"message": "Username already exist"})
        else:
                return render_to_response("login.html")

    except IntegrityError,e:
        return render_to_response("error.html", {"message": "Username Already exist"})



#Profile of User
def getUser(request):
    try:
        username=request.session['username']
        fname = User.objects.get(username__exact=username).first_name
        lname = User.objects.get(username__exact=username).last_name
        print "user first name is", fname
        return render_to_response("profile.html",{"username":username,"fname":fname,"lname":lname})

    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})





# UpdateUser
def updateUser(request):
    try:

        username=request.session['username']
        fname = User.objects.get(username__exact=username).first_name
        lname = User.objects.get(username__exact=username).last_name
        password = User.objects.get(username__exact=username).password
        print "user first name is", fname
        return render_to_response("update.html",{"username":username,"fname":fname,"lname":lname, "pwd":password})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})



def updateUser_Success(request):
    try:
        if request.POST:
                fname = request.POST.get('fname')
                lname = request.POST.get('lname')
                pwd = request.POST.get('password')
                print "inside post firstname is",fname
                uname=request.session['username']
                u = User.objects.get(username=uname)
                u.first_name=fname
                u.last_name=lname
                u.save()
                print"User Object is",u
                print "user first name is", fname
                return render_to_response("profile.html",{"username":uname,"fname":fname,"lname":lname,"password":pwd})
        else:
                return render_to_response("profile.html")
    except IntegrityError, e:
            return render_to_response("error.html", {"message": e.message})




def deleteUser(request):
    try:
        username=request.session['username']
        print "Inside delete user is",username
        user= User.objects.get(username__exact=username)
        print "Uname is",user
        r=httpconnection.deleteUser_Connect(username)
        print "Status code is",r.status_code
        if r.status_code==200 or r.status_code==201 :
            user.delete()
            return render_to_response("login.html",{"message_delete":"Your Profile have successfully deleted"})

        else:
            return render_to_response("login.html", {"message_delete": "Please try again"})
    except IntegrityError, e:
        return render_to_response("error.html", {"message": e.message})



# sign out function
def signOut(request):
    try:
        logout(request)
        return render(request, 'login.html')
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})
   

##-----------COURSE----------##

#Add Course
def addCourse(request):
    try:
        response = httpconnection.listCategory_Connect()
        print "response status for category= ", response.status_code
        convertToJson = response.json()
        print "Return Category Json is",convertToJson
        email=request.session['username']
        fname=User.objects.get(username__exact=email).first_name
        return render_to_response("addCourse.html", {"email": email,"fname":fname,"categoryName":convertToJson})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})
#courseHome function is called when a new course is added
def courseHome(request):
    try:
    
        if request.POST:
            category = request.POST.get('category')
            title = request.POST.get('title')
            section = request.POST.get('section')
            department = request.POST.get('department')
            term = request.POST.get('term')
            year = request.POST.get('year')
            name = request.POST.get('name')
            email = request.POST.get('email')
            days = request.POST.getlist('days')
            hours = request.POST.getlist('hours')
            description = request.POST.get('description')
            attachment = request.POST.get('attachment')
            #email=request.user.username;
            print "days are ", days
            print "Email of user adding course is ", email
            payload = {
            "category": category,
            "title": title,
            "section": section,
            "dept": department,
            "term": term,
            "year": year,
            "instructor": [
            {
                "name": name,
                "email": email
            }
            ],
            "days": days,
            "hours": hours,
            "Description": description,
            "attachment": attachment,
            "version": "1"
            }

            data=json.dumps(payload)

            response = httpconnection.addCourse_Connect(data)
            print "response status code = ", response.status_code
            convertToJson = response.json()
            #print convertToJson
        return render_to_response("courseHome.html",{"message":"Course "+title+" successfully added"})
    except:
            print "inside exception"
            return render_to_response("courseHome.html",context_instance=RequestContext(request))




#List Course
def listCourse(request):
    try:
        response = httpconnection.listCourse_Connect()
        print "response status = ", response.status_code
        convertToJson = response.json()
        print "Return Course Json is",convertToJson
        return render_to_response("listCourse.html",{"list":convertToJson})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})
#Get Course
def getCourse(request):
    try:
        courseId=request.GET.get('courseSelection')
        print "course id with team name is: ", courseId
        #fullCourseId=courseId.split(":")
        #print "courseId :", fullCourseId[1]
        #cId=fullCourseId[1]
        #print "Course id : ", cId
        response = httpconnection.getCourse_Connect(courseId)
        print "response status = ", response.status_code
        convertToJson = response.json()
        print "Return Course Json is",convertToJson
        return render_to_response("getCourse.html",{"list":convertToJson})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})
#List Course to delete
def listCourseDelete(request):
    try:
        response = httpconnection.getOwnedCourse_Connect(request.session['username'])
        print "response status = ", response.status_code
        convertToJson = response.json()
        print "Return Course Json is",convertToJson
        return render_to_response("listCourseDelete.html",{"list":convertToJson})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})

#Delete course
def deleteCourse(request):
    try:
        courseId=request.GET.get('courseSelection')
        print "course id with team name is: ", courseId
        #fullCourseId=courseId.split(":")
        #print "courseId :", fullCourseId[1]
        #cId=fullCourseId[1]
        #print "Course id : ", cId
        response = httpconnection.deleteCourse_Connect(courseId)
        print response.status_code
        if response.status_code==200 or response.status_code==201 :
                    print "response status code = ", response.status_code
                    convertToJson = response.json()
                    print convertToJson
                    return render_to_response("courseHome.html",{"message":"Course Successfully Deleted"})
        elif response.status_code==400 :
                    print "Inside elif",response.status_code
                    return render_to_response("courseHome.html",{"message":" Id is invalid"})
        elif response.status_code==404 :
                    print "Inside elif",response.status_code
        return render_to_response("courseHome.html",{"message":"User not found"})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})

#Enroll Course
def enrollCourse(request):
    try:
        response = httpconnection.listCourse_Connect()
        print "response status = ", response.status_code
        convertToJson = response.json()
        #print "Return Course Json is",convertToJson
        return render_to_response("enrollCourse.html",{"list":convertToJson})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})



def enrollCourseHome(request):
    try:
        courseId=request.GET.get('courseSelection')
        #fullCourseId=courseId.split(":")
        #print "courseId :", fullCourseId[1]
        #cId=fullCourseId[1]
        username=request.session['username']
        payload = { "email": username, "courseId":courseId }
        data=json.dumps(payload)
        response = httpconnection.enrollCourse_Connect(data)
        print "response status = ", response.status_code
        #convertToJson = response.json()
        #print "Return Course Json is",convertToJson
        if response.status_code==200 or response.status_code==201 :
            return render_to_response("courseHome.html",{"message":"You have successfully enrolled in the course"})


        elif response.status_code == 500:
            print "I am in 500"
            return render_to_response("courseHome.html",{"message":"You are already enrolled in the course"})
        else:
            return render_to_response("courseHome.html",{"message":"Problem in enrolling"})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})





#Drop Course
def dropCourse(request):
    try:
        response = httpconnection.listCourse_Connect()
        print "response status = ", response.status_code
        convertToJson = response.json()
        #print "Return Course Json is",convertToJson
        return render_to_response("dropCourse.html",{"list":convertToJson})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})



#Drop Course Home
def dropCourseHome(request):
    try:
        courseId=request.GET.get('courseSelection')
        #fullCourseId=courseId.split(":")
        #print "courseId :", fullCourseId[1]
        #cId=fullCourseId[1]
        username=request.session['username']
        payload = { "email": username, "courseId":courseId }
        data=json.dumps(payload)
        response = httpconnection.dropCourse_Connect(data)
        print "response status = ", response.status_code
        #convertToJson = response.json()
        #print "Return Course Json is",convertToJson
        if response.status_code==200 or response.status_code==201 :
            return render_to_response("courseHome.html",{"message":"You have successfully dropped the course"})

        elif response.status_code == 500:
            print "I am in 500"
            return render_to_response("courseHome.html",{"message":"You are not enrolled in the course"})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})

# Update Course
def updateCourse(request):
    try:

        response = httpconnection.getOwnedCourse_Connect(request.session['username'])
        print "response status = ", response.status_code
        convertToJson = response.json()
        #print "Return Course Json is",convertToJson
        return render_to_response("updateCourse.html",{"list":convertToJson})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})





# Update CourseHome
def updateCourseHome(request):
    try:
        response = httpconnection.listCategory_Connect()
        print "response status for category= ", response.status_code
        convertToJson1 = response.json()
        print "Return Category Json is",convertToJson1
        courseId=request.GET.get('courseSelection')
        print "course id with team name is: ", courseId
        #fullCourseId=courseId.split(":")
        #print "courseId :", fullCourseId[1]
        #cId=fullCourseId[1]
        #
        #print "Course id : ", cId
        request.session['courseId'] = courseId
        response = httpconnection.getCourse_Connect(courseId)
        print "response status = ", response.status_code
        convertToJson = response.json()
        #print "Return Course Json is",convertToJson
        return render_to_response("updateCourseHome.html",{"list":convertToJson,"categoryName":convertToJson1})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})



# Update CourseSuccess
def updateCourseSuccess(request):
    print "inside updateCourseSuccess in views.py"
    #courseId=request.GET.get('courseSelection')
    try:

        fname = User.objects.get(username__exact=request.session['username']).first_name



        courseId=request.session['courseId']
        print "course id with team name is: ", courseId
        payload = {
                "category": request.GET.get('category'),
                "title": request.GET.get('title'),
                "section": request.GET.get('section'),
                "dept": request.GET.get('department'),
                "term": request.GET.get('term'),
                "year": request.GET.get('year'),
                "instructor": [
                    {
                        "name": fname,
                        "email": request.session['username']
                    }
                ],
                "days": request.GET.get('days'),
                "hours": request.GET.get('hours'),
                "Description": request.GET.get('description'),
                "attachment": request.GET.get('attachment'),
                "version": request.GET.get('version')
                }

        data=json.dumps(payload)
        print " data to be updated", data



        response = httpconnection.updateCourse_Connect(courseId,data)
        print "response status = ", response.status_code
        convertToJson = response.json()
        if response.status_code==200 or response.status_code==201 :
                return render_to_response("courseHome.html",{"message":"You have successfully update the course"})

        elif response.status_code == 500:
                print "I am in 500"
                return render_to_response("courseHome.html",{"message":"Problem with updating the course"})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})




##-------------Category-------####
#Add Category
def addCategory(request):
    try:
        return render(request, 'addCategory.html')
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})


#categoryHome function is called when a new category is added
def categoryHome(request):
    try:
        if request.POST:
            name = request.POST.get('name')
            description = request.POST.get('description')
            payload = {
            "name": name,
            "description": description,
            }

            data=json.dumps(payload)

            response = httpconnection.addCategory_Connect(data)
            if response.status_code==200 or response.status_code==201 :
                print "response status code = ", response.status_code
                convertToJson = response.json()
                print convertToJson
                return render_to_response("categoryHome.html",convertToJson,context_instance=RequestContext(request))

            elif response.status_code==409 :
                print "Inside elif",response.status_code
                return render_to_response("categoryHome.html",{"message":"Category Name is Duplicated"})

            else:
                return render_to_response("error.html",{"message":"Category Name is Duplicated"})
    except:
            print "Inside add category exception"
    return render_to_response("categoryHome.html",{"user" : request.session['username']})




#List all Categories
def listCategory(request):
    try:
        response = httpconnection.listCategory_Connect()
        print "response status = ", response.status_code
        convertToJson = response.json()
        print "Return Category Json is",convertToJson
        return render_to_response("listCategory.html",{"list":convertToJson})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})

#get Category
def getCategory(request):
    try:
        categoryId=request.GET.get('categorySelection')
        print "category id with team name is: ", categoryId
        #fullCategoryId=categoryId.split(":")
        #print "categoryId :", fullCategoryId[1]
        #cId=fullCategoryId[1]
        #print "Category id : ", cId
        response = httpconnection.getCategory_Connect(categoryId)
        print "response status = ", response.status_code
        convertToJson = response.json()
        print "Return Category Json is",convertToJson
        return render_to_response("getCategory.html",{"list":convertToJson})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})

##--------Announcements------#####
##Add Announcment

def addAnnouncement(request):
    try:
        response = httpconnection.getOwnedCourse_Connect(request.session['username'])
        print "response status = ", response.status_code
        convertToJson = response.json()
        print "Return Course Json is",convertToJson
        return render_to_response("addAnnouncement.html",{"course":convertToJson})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})

#announcementHome function is called when a new announcement is added
def announcementHome(request):
    try:
        if request.POST:
            courseId = request.POST.get('courseId')
            title = request.POST.get('title')
            description = request.POST.get('description')
            payload = {
            "courseId": courseId,
            "title": title,
            "description": description
            }

            data=json.dumps(payload)

            response = httpconnection.addAnnouncement_Connect(data)

            print "response status code = ", response.status_code
            convertToJson = response.json()
            print convertToJson
            return render_to_response("announcementHome.html",{"message" : "Announcement Added"})
        else:
            return render_to_response("announcementHome.html",{"message" : "Select one of the options"})



    except:
            print "Inside add Announcement exception"
    return render_to_response("announcementHome.html",{"user" : " "})


##List Announcement
def listAnnouncement(request):
    try:
        response = httpconnection.listAnnouncement_Connect()
        print "response status = ", response.status_code
        convertToJson = response.json()
        print "Return Announcement Json is",convertToJson

        return render_to_response("listAnnouncement.html",{"list":convertToJson})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})

#Get Announcement
def getAnnouncement(request):
    try:
        courseId=request.GET.get('courseSelection')
        print "announcement id with team name is: ", courseId
        #fullCategoryId=categoryId.split(":")
        #print "categoryId :", fullCategoryId[1]
        #cId=fullCategoryId[1]
        #print "Category id : ", cId
        response = httpconnection.getAnnouncement_Connect(courseId)
        print "response status = ", response.status_code
        convertToJson = response.json()
        print "Return Announcement Json is",convertToJson
        return render_to_response("getAnnouncement.html",{"list":convertToJson})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})

#list announcement to delete

def listAnnouncementDelete(request):
    try:
        response = httpconnection.listAnnouncement_Connect()
        print "response status = ", response.status_code
        convertToJson = response.json()
        print "Return Announcement Json is",convertToJson

        return render_to_response("listAnnouncementDelete.html",{"list":convertToJson})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})

#Delete Announcement
def deleteAnnouncement(request):
    try:
        courseId=request.GET.get('courseSelection')
        print "course id with team name is: ", courseId
        #fullCourseId=courseId.split(":")
        #print "courseId :", fullCourseId[1]
        #cId=fullCourseId[1]
        #print "Course id : ", cId
        response = httpconnection.deleteAnnouncement_Connect(courseId)
        print response.status_code
        if response.status_code==200 or response.status_code==201 :
                    print "response status code = ", response.status_code
                    convertToJson = response.json()
                    print convertToJson
                    return render_to_response("announcementHome.html",{"message":"Announcement Successfully Deleted"})
        elif response.status_code==400 :
                    print "Inside elif",response.status_code
                    return render_to_response("announcementHome.html",{"message":" Id is invalid"})
        elif response.status_code==404 :
                    print "Inside elif",response.status_code
        return render_to_response("announcementHome.html",{"message":"Announcement not found"})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})

###-------------------------------Discussion----------###########
##Add Discussion
def addDiscussion(request):
    try:
        response = httpconnection.listCourse_Connect()
        print "response status = ", response.status_code
        convertToJson = response.json()
        print "Return Course Json is",convertToJson
        return render_to_response("addDiscussion.html",{"course":convertToJson,"user":request.session['username']})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})


#discussionHome function is called when a new discussion is added
def discussionHome(request):
    try:
        print "1"
        if request.POST:
            courseId = request.POST.get('courseId')
            title = request.POST.get('title')
            created_by = request.POST.get('created_by')
            payload = {
            "courseId": courseId,
            "title": title,
            "created_by": created_by
            }
            print "2"

            data=json.dumps(payload)

            print "3"

            response = httpconnection.addDiscussion_Connect(data)

            print "response status code = ", response.status_code
            convertToJson = response.json()
            print "4"
            print convertToJson
            return render_to_response("discussionHome.html",{"message" : "Discussion Posted"})
        else:
            return render_to_response("discussionHome.html",{"message" : "Select one of the options"})



    except:
            print "Inside add Discussion exception"
    return render_to_response("discussionHome.html",{"user" : " "})

#Get Announcement
def getAnnouncement(request):
    try:
        courseId=request.GET.get('courseSelection')
        print "announcement id with team name is: ", courseId
        #fullCategoryId=categoryId.split(":")
        #print "categoryId :", fullCategoryId[1]
        #cId=fullCategoryId[1]
        #print "Category id : ", cId
        response = httpconnection.getAnnouncement_Connect(courseId)
        print "response status = ", response.status_code
        convertToJson = response.json()
        print "Return Announcement Json is",convertToJson
        return render_to_response("getAnnouncement.html",{"list":convertToJson})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})

#List Course to get Discussion
def listCourseDiscussion(request):
    try:
        print"inside list course discussion"
        response = httpconnection.listCourse_Connect()
        print "response status = ", response.status_code
        convertToJson = response.json()
        print "Return Course Json is",convertToJson
        return render_to_response("listCourseDiscussion.html",{"list":convertToJson})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})

#Get discussion based on courseId
def getDiscussion(request):
    try:
        courseId=request.GET.get('courseSelection')
        print "Course id with team name is: ", courseId
        #fullCategoryId=categoryId.split(":")
        #print "categoryId :", fullCategoryId[1]
        #cId=fullCategoryId[1]
        #print "Category id : ", cId
        response = httpconnection.getDiscussion_Connect(courseId)
        print "response status = ", response.status_code
        convertToJson = response.json()
        print "Return Discussion Json is",convertToJson
        return render_to_response("getDiscussion.html",{"list":convertToJson})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})

## List Discussion to delete

def listCourseDiscussionDelete(request):
    try:
        print"inside list course discussion"
        response = httpconnection.listCourse_Connect()
        print "response status = ", response.status_code
        convertToJson = response.json()
        print "Return Course Json is",convertToJson
        return render_to_response("listCourseDiscussionDelete.html",{"list":convertToJson})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})

#Get discussion based on courseId to delete
def getDiscussionDelete(request):
    try:
        courseId=request.GET.get('courseSelection')
        print "Course id with team name is: ", courseId
        #fullCategoryId=categoryId.split(":")
        #print "categoryId :", fullCategoryId[1]
        #cId=fullCategoryId[1]
        #print "Category id : ", cId
        response = httpconnection.getDiscussion_Connect(courseId)
        print "response status = ", response.status_code
        convertToJson = response.json()
        print "Return Discussion Json is",convertToJson
        return render_to_response("getDiscussionDelete.html",{"list":convertToJson})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})


#Delete discussion
def deleteDiscussion(request):
    try:
        discussionId=request.GET.get('discussionSelection')
        print "discussion id with team name is: ", discussionId
        #fullCourseId=courseId.split(":")
        #print "courseId :", fullCourseId[1]
        #cId=fullCourseId[1]
        #print "Course id : ", cId
        response = httpconnection.deleteDiscussion_Connect(discussionId)
        print response.status_code
        if response.status_code==200 or response.status_code==201 :
                    print "response status code = ", response.status_code
                    convertToJson = response.json()
                    print convertToJson
                    return render_to_response("discussionHome.html",{"message":"Discussion Successfully Deleted"})
        elif response.status_code==400 :
                    print "Inside elif",response.status_code
                    return render_to_response("discussionHome.html",{"message":" Id is invalid"})
        elif response.status_code==404 :
                    print "Inside elif",response.status_code
        return render_to_response("discussionHome.html",{"message":"Discussion not found"})
    except:
        return render_to_response('error.html',{"message": sys.exc_info()[0]})

