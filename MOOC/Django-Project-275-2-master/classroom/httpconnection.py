# The class provides connection to MOOC and Django over HTTP
# 
import sys
import requests
import json
from requests import session


user = "user"
quizzes = "quizzes"
quiz="quiz"
course = "course"
category = "category"
discussion = "discussion"
announcement = "announcement"
url = "http://localhost:8080/"

print "HTTP CONNECTION OF DJANGO & BOTTLE"
##--------User----##
# home - sign In Call
def home_Connect(data):
   print "homeConnect"
   return requests.post(url+user+"/auth",data)
   
# signUpHome - sign UP Call
def signUpHome_Connect(data):
   print "signUpHomeConnect"
   return requests.post(url+user, data)

# getUser - get User Call
def getUser_Connect(data):
   print "getUserConnect"
   return requests.post(url+user+"/abc@gmail.com", data)

# updateUser - update User Call
def updateUser_Connect(data):
   print "updateUserConnect"
   return requests.post(url+user+"/abc@gmail.com", data)

# deleteUser - delete User Call
def deleteUser_Connect(data):
   print "deleteUserConnect"
   return requests.delete(url+user+"/"+ data)



##-------COURSE--------####
# enrollCourse - enroll Course Call
def enrollCourse_Connect(data):
   print "enrollCourseConnect"
   return requests.put(url+course+"/enroll", data)

# dropCourse - drop Course Call
def dropCourse_Connect(data):
   print "dropCourseConnect"
   return requests.put(url+course+"/drop", data)

# addCourse - add Course Call
def addCourse_Connect(data):
   print "addCourseConnect"
   return requests.post(url+course, data)

# getCourse - get Course Call
def getCourse_Connect(data):
   print "getCourseConnect"
   return requests.get(url+course+"/"+data)



# Get own courses of the user
def getOwnedCourse_Connect(email):
    print "Get User owned courses"
    return requests.get(url + course + "/own/" + email)


# listCourse - list Course Call
def listCourse_Connect():
   print "listCourseConnect"
   return requests.get(url+course+"/list")

# updateCourse - update Course Call
def updateCourse_Connect(id,data):
   print "updateCourseConnect"
   return requests.put(url+course+"/update/"+id,data)
# deleteCourse - delete Course Call
def deleteCourse_Connect(data):
   print "deleteCourseConnect"
   return requests.delete(url+course+"/delete/"+data)

# addCategory - add Category Call
def addCategory_Connect(data):
   print "addCategoryConnect"
   return requests.post(url+category, data)

# getCategory - get Category Call
def getCategory_Connect(data):
   print "getCategoryConnect"
   return requests.get(url+category+"/"+data)

# listCategory - list Category Call
def listCategory_Connect():
   print "listCategoryConnect"
   return requests.get(url+category+"/list")

#__________________________ QUIZZES___________________________________#

# addQuiz - add Quiz Call
def addQuiz_Connect(jsonData):
   print "addQuizConnect"
   return requests.post(url+quizzes, jsonData)

# getQuiz - get Quiz Call
def getQuiz_Connect(quizId):
   print "getQuizConnect"
   return requests.get(url+quiz+"/"+quizId)

# listQuiz - list Quiz Call
def listQuiz_Connect():
   print "listQuizConnect"
   return requests.get(url+quiz+"/list")

# updateQuiz - update Quiz Call
def updateQuiz_Connect(quizId, jsonData):
   print "updateQuizConnect"
   return requests.put(url+quiz+"/update"+"/"+quizId, jsonData)

# deleteQuiz - delete Quiz Call
def deleteQuiz_Connect(quizId):
   print "deleteQuizConnect"
   return requests.delete(url+quiz+"/"+quizId)

#_____________________________ANNOUNCEMENT______________________________#

# addAnnouncement - add Announcement Call
def addAnnouncement_Connect(jsonData):
   print "addAnnouncementConnect"
   return requests.post(url+"announcements", jsonData)

# listAnnouncement - list Announcement Call
def listAnnouncement_Connect():
   print "listAnnouncementConnect"
   return requests.get(url+announcement+"/list")

# getAnnouncement - get Announcement Call
def getAnnouncement_Connect(annId):
   print "getAnnouncementConnect"
   return requests.get(url+announcement+"/"+annId)

# updateAnnouncement - update Announcement Call
def updateAnnouncement_Connect(annId, jsonData):
   print "updateAnnouncementConnect"
   return requests.put(url+announcement+"/update"+"/"+annId, jsonData)

# deleteAnnouncement - delete Announcement Call
def deleteAnnouncement_Connect(annId):
   print "deleteAnnouncementConnect"
   return requests.delete(url+announcement+"/delete/"+annId)



#####--------------------Discussion--------------########################
# addDiscussion - add Discussion Call
def addDiscussion_Connect(data):
   print "addDiscussionConnect"
   return requests.post(url+"discussions", data)



# getDiscussion - get Discussion Call
def getDiscussion_Connect(courseId):
   print "getDiscussionConnect"
   return requests.get(url+discussion+"/"+courseId)



# deleteDiscussion - delete Discussion Call
def deleteDiscussion_Connect(discussionId):
   print "deleteDiscussionConnect"
   return requests.delete(url+discussion+"/"+discussionId)

# addMessage - add Message Call
def addMessage_Connect(data):
   print "addMessageConnect"
   return requests.post(url+discussion+"/message", data)

# listMessage - list Message Call
def listMessage_Connect(data):
   print "listMessageConnect"
   return requests.post(url+discussion+"/message"+"/", data)

# updateMessage - update Message Call
def updateMessage_Connect(data):
   print "updateMessageConnect"
   return requests.post(url+discussion+"/message"+"/", data)

# deleteMessage - delete Message Call
def deleteMessage_Connect(data):
   print "deleteMessageConnect"
   return requests.post(url+discussion+"/", data)
