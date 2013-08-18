from django.conf.urls import patterns, include, url
import classroom.views
from classroom.views import deleteDiscussion,getDiscussionDelete,listCourseDiscussionDelete,getDiscussion,listCourseDiscussion,discussionHome,addDiscussion,listAnnouncementDelete,deleteAnnouncement,getAnnouncement,listAnnouncement,announcementHome,addAnnouncement,dropCourseHome,dropCourse,enrollCourseHome,enrollCourse,updateCourseSuccess,updateCourseHome,updateCourse,index,signIn, signOut, signUp, home, signUpHome, addCourse,courseHome, listCourse,getCourse, deleteCourse,listCourseDelete, getUser, updateUser,updateUser_Success, deleteUser, addCategory, categoryHome, listCategory,getCategory#, enrollCourse, dropCourse, updateCourse, addQuiz, getQuiz, listQuiz, updateQuiz, deleteQuiz, addAnnouncement, listAnnouncement, getAnnouncement, updateAnnouncement, deleteAnnouncement, addDiscussion, listDiscussion, getDiscussion, updateDiscussion, deleteDiscussion, addMessage, listMessage, updateMessage, deleteMessage

from django.conf.urls.defaults import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import django.contrib.admin
admin.autodiscover()

urlpatterns = patterns('',
      # user url's
      url(r'^$', index),
      url(r'^signIn/$', signIn),
      url(r'^signUp/$', signUp),       # signup is create user as mentioned in Format
      url(r'^home/$', home),
      url(r'^signUp_home/$', signUpHome),

      url(r'^get_user/$',getUser),
      url(r'^update_user/$',updateUser),
      url(r'^update_user_success/$',updateUser_Success),
      url(r'^delete_user/$',deleteUser),

      url(r'^logout/$', signOut),

      # course url's
      url(r'^update_course/$',updateCourse),
      url(r'^update_course_home/$',updateCourseHome),
      url(r'^update_course_success/$',updateCourseSuccess),
      url(r'^enroll_course/$',enrollCourse),
      url(r'^enroll_course_home/$',enrollCourseHome),
      url(r'^drop_course/$',dropCourse),
      url(r'^drop_course_home/$',dropCourseHome),
      #url(r'^enroll_course/$',enrollCourse),
      #url(r'^drop_course/$',dropCourse),
      url(r'^add_course/$',addCourse),
      url(r'^course_home/$',courseHome),
      url(r'^get_course/$',getCourse),
      url(r'^list_course/$',listCourse),
      #url(r'^update_course/$',updateCourse),
       url(r'^list_course_delete/$',listCourseDelete),
      url(r'^delete_course/$',deleteCourse),
      # Category url's
      url(r'^add_category/$',addCategory),
      url(r'^category_home/$',categoryHome),

      url(r'^get_category/$',getCategory),
      url(r'^list_category/$',listCategory),
      # Category url's
      #url(r'^add_category/$',addCategory),
      #url(r'^get_category/$',getCategory),
      #url(r'^list_category/$',listCategory),

      # Quiz url's
      #url(r'^add_quiz/$',addQuiz),
      #url(r'^get_quiz/$',getQuiz),
      #url(r'^list_quiz/$',listQuiz),
      #url(r'^update_quiz/$',updateQuiz),
      #url(r'^delete_quiz/$',deleteQuiz),

      # Announcement url's
      url(r'^add_announcement/$',addAnnouncement),
      url(r'^announcement_home/$',announcementHome),
      url(r'^list_announcement/$',listAnnouncement),
      url(r'^get_announcement/$',getAnnouncement),
      #url(r'^update_announcement/$',updateAnnouncement),
      url(r'^list_announcement_delete/$',listAnnouncementDelete),
      url(r'^delete_announcement/$',deleteAnnouncement),

      # Discussion url's
      url(r'^add_discussion/$',addDiscussion),
      url(r'^discussion_home/$',discussionHome),
      #url(r'^list_discussion/$',listDiscussion),
      url(r'^list_course_discussion/$',listCourseDiscussion),
      url(r'^get_discussion/$',getDiscussion),
       url(r'^list_course_discussion_delete/$',listCourseDiscussionDelete),
       url(r'^get_discussion_delete/$',getDiscussionDelete),
      #url(r'^update_discussion/$',updateDiscussion),
      url(r'^delete_discussion/$',deleteDiscussion),

      # Message url's
      #url(r'^add_message/$',addMessage),
      #url(r'^list_message/$',listMessage),
      #url(r'^update_message/$',updateMessage),
      #url(r'^delete_message/$',deleteMessage),
    # Examples:
    # url(r'^$', 'moo.views.home', name='home'),
    # url(r'^moo/', include('moo.foo.urls')),
      


    # Uncomment the admin/doc line below to enable admin documentation:
      url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
      url(r'^admin/', include(admin.site.urls)),
)

