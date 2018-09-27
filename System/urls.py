from django.contrib import admin
from django.urls import path,include
from .views import *

app_name = "system"
urlpatterns = [
    path('',loadLogin,name="Index"),
    path('criteria/',loadCriteria,name="criteria"),
    path('login/',login.as_view(),name="Login"),
    path('find_students/',criteria.as_view(),name="FindStudents"),
    path('register_student/', loadSignup, name="Signup"),
    path('register/', reg.as_view(), name="registers"),
    path('profile/', profiles.as_view(), name="profile"),
    path('ForgotPassword/', forgotPassword.as_view(), name="forgotpassword"),
    path('custom_email/', customEmail.as_view(), name="customemail"),
    path('logout/', logout, name="logout"),
    path('gprofile/', generateProfile.as_view(), name="generateProfile"),
    path('jsonprofile/', genProfile, name="jsonprofile"),
    path('personal/', loadpersonal, name="personal"),
    path('personalsave/', personals.as_view(), name="savepersonal"),
    path('account/', account.as_view(), name="account"),



]
