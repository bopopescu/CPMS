from django.core import serializers
import mysql.connector
import csv

import string
import random

import smtplib

from email.mime.base import MIMEBase
from email import encoders

from email.mime.multipart import MIMEMultipart
from django.contrib.auth.models import User
from email.mime.text import MIMEText
from django.shortcuts import render,HttpResponseRedirect
from rest_framework.views import APIView
from .models import *
from django.http import HttpResponse
from .serializer import *
from django.contrib import messages
from django.contrib import auth
from django.http import JsonResponse





def loadSignup(request):
    return render(request, "System/signup.html")


def loadLogin(request):
    return render(request, "System/Index.html")


def loadCriteria(request):
    return render(request, "System/Criteria.html")


def loadstudenthome(request):
    return render(request,"System/StudentHome.html")

class reg(APIView):
    def post(self,request):
        email = request.POST['email']
        fnm = request.POST['fnm']
        lnm = request.POST['lnm']
        password = request.POST['password']

        User.objects.create_user(username=email,email=email,password=password,first_name=fnm,last_name=lnm)
        return HttpResponse('Created!')

class login(APIView):

    def post(self,request):
        email = request.POST['email']
        password = request.POST['password']
        request.session['email'] = email
        try:
            user = auth.authenticate(username=email,password=password)
            if user is not None:
                auth.login(request,user)
                if request.user.is_superuser:
                    return HttpResponseRedirect("/system/criteria/")
                else:
                    try:
                        personal.objects.get(email_id=email)
                        return HttpResponseRedirect("/system/home/")
                    except:
                        return HttpResponseRedirect("/system/personal/")

            else:
                messages.error(request, 'Username and Password did not matched !')

        except auth.ObjectDoesNotExist:
            print("Invalid user")

        return HttpResponseRedirect("/system/")


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/system/")



def loadpersonal(request):
    return render(request,"System/Personal.html")


def loadprofileoptions(request):
    return render(request,"System/ProfileOptions.html")


def loadplacement(request):
    return render(request,"System/PlacementDetails.html")

def retrievepersonal(request):
    email = request.user.email

    obj = personal.objects.get(email_id=email)
    context = personalSer(obj)
    return JsonResponse(context.data, safe=False)

def loadretrPersonal(request):
    return render(request,"System/RetrievePersonal.html")



class personals(APIView):
    def post(self,request):
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        contact = request.POST['contact']
        dob = request.POST['dob']
        fnm = request.POST['fnm']
        mnm = request.POST['mnm']
        lnm = request.POST['lnm']
        gender = request.POST['gender']

        email = request.session.get('email')


        personal.objects.create(email_id=email,gender=gender,dob=dob,address=address,city=city,state=state,contact=contact,first_name=fnm,middle_name=mnm,last_name=lnm)
        return HttpResponseRedirect("/system/profile/")


class criteria(APIView):


    def post(self,request):
        selecttype = request.POST.getlist('check')
        filename = request.POST['hide']
        Year = request.POST['Year']
        count = len(selecttype)

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="cpms"
        )

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="' + filename + '.csv"'

        writer = csv.writer(response)
        writer.writerow(['First name', 'Last name', 'Ssc', 'Hsc', 'Ug', 'pg', 'Year', 'Shift', 'Email address'])
        mycursor = mydb.cursor()

        query = "select r.first_name , r.last_name, p.ssc, p.hsc, p.ug, p.pg, p.year, p.shift, p.email_id from auth_user r inner join profile p on r.email= p.email_id where "
        query2 = "select p.email_id from auth_user r inner join profile p on r.email= p.email_id where "
        if count == 1:

            first = selecttype[0]
            val = checkit(first)
            cond1 = request.POST.get(val)


            query += "p." + first + " > " + cond1 + " AND p.year = '" + Year +"'"
            query2 += "p." + first + " > " + cond1 + " AND p.year = '" + Year +"'"


            mycursor = mydb.cursor()

            mycursor.execute(query)
            myresult = mycursor.fetchall()

            for i in myresult:
                writer.writerow(i)
            request.session['query'] = query2
            return response



        if count == 2:
            first = selecttype[0]
            second = selecttype[1]

            val1 = checkit(first)
            val2 = checkit(second)

            cond1 = request.POST.get(val1)
            cond2 = request.POST.get(val2)

            query += "p."+ first + " > " + cond1 + " AND " + "p." + second + " > " + cond2 + " AND p.year = '" + Year +"'"
            query2 += "p."+ first + " > " + cond1 + " AND " + "p." + second + " > " + cond2 + " AND p.year = '" + Year +"'"


            mycursor.execute(query)
            myresult = mycursor.fetchall()

            for i in myresult:
                writer.writerow(i)

            request.session['query'] = query2
            return response



        if count == 3:
            first = selecttype[0]
            second = selecttype[1]
            third = selecttype[2]

            val1 = checkit(first)
            val2 = checkit(second)
            val3 = checkit(third)

            cond1 = request.POST.get(val1)
            cond2 = request.POST.get(val2)
            cond3 = request.POST.get(val3)

            query += "p." + first + " > " + cond1 + " AND " + "p." + second + " > " + cond2 + " AND " + "p." + third + " > " + cond3 + " AND p.year = '" + Year +"'"
            query2 += "p." + first + " > " + cond1 + " AND " + "p." + second + " > " + cond2 + " AND " + "p." + third + " > " + cond3 + " AND p.year = '" + Year +"'"


            mycursor.execute(query)
            myresult = mycursor.fetchall()

            for i in myresult:
                writer.writerow(i)

            request.session['query'] = query2
            return response



        if count == 4:
            first = selecttype[0]
            second = selecttype[1]
            third = selecttype[2]
            fourth = selecttype[3]

            val1 = checkit(first)
            val2 = checkit(second)
            val3 = checkit(third)
            val4 = checkit(fourth)

            cond1 = request.POST.get(val1)
            cond2 = request.POST.get(val2)
            cond3 = request.POST.get(val3)
            cond4 = request.POST.get(val4)

            query += "p." + first + " > " + cond1 + " AND " + "p." + second + " > " + cond2 + " AND " + "p." + third + " > " + cond3 + " AND " + "p." + fourth + " > " + cond4 + " AND p.year = '" + Year +"'"
            query2 += "p." + first + " > " + cond1 + " AND " + "p." + second + " > " + cond2 + " AND " + "p." + third + " > " + cond3 + " AND " + "p." + fourth + " > " + cond4 + " AND p.year = '" + Year +"'"
            mycursor.execute(query)
            myresult = mycursor.fetchall()

            for i in myresult:
                writer.writerow(i)

            request.session['query'] = query2
            return response


def checkit(str) :
    if str == "ssc":
        return 'tenth'

    if str == "hsc":
        return 'twelth'

    if str == "ug":
        return 'underg'

    if str == "pg":
        return 'postg'


class profiles(APIView):

    def get(self,request):
        email = request.session.get('email')
        try:
            pro = profile.objects.get(email=email)
            return render(request, "System/Criteria.html")
        except:

            return render(request, "System/Profile.html",{"context":email})


    def post(self,request):


        ser = profileSer(data=request.data)
        if ser.is_valid():
            ser.save()
            return HttpResponseRedirect("/system/home/")
        else:
            return HttpResponse("Error")


class forgotPassword(APIView):


    def get(self,request):
        return render(request,"System/Forgot.html")

    def post(self, request):

        email = request.POST['email']

        try:
            u = User.objects.get(email=email)
            msg = MIMEMultipart()
            pwd = randompassword()
            message = "Your new password is : " + pwd
            u.set_password(pwd)
            u.save()
            password = "fcpark22"
            msg['From'] = "ankushgochke@gmail.com"
            msg['To'] = email
            msg['Subject'] = "MCOE MCA Placement system password change !"
            msg.attach(MIMEText(message, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com: 587')
            server.starttls()
            server.login(msg['From'], password)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            server.quit()
            return HttpResponse('')

        except:
            pass


def randompassword():
    chars=string.ascii_uppercase + string.ascii_lowercase + string.digits
    size= 8
    return ''.join(random.choice(chars) for x in range(size, 16))


class customEmail(APIView):
    def get(self,request):
        return render(request,"System/Custom_email.html")

    def post(self,request):

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="cpms"
        )

        mycursor = mydb.cursor()
        query = request.session['query']
        mycursor.execute(query)
        myresult = mycursor.fetchall()


        a = request.FILES.getlist('file')
        fromaddr = "ankushgochke@gmail.com"
        frompass = "fcpark22"
        msg = MIMEMultipart()

        msg['From'] = "ankushgochke@gmail.com"
        recp = ''

        for i in myresult:
            recp += "".join(i)+", "

        msg['To'] = recp
        msg['Subject'] = request.POST['subject']

        body =request.POST['email']

        msg.attach(MIMEText(body, 'plain'))

        for i in a:
            part = MIMEBase('application', 'octet-stream')

            part.set_payload(i.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % i)

            msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, frompass)
        text = msg.as_string()
        server.sendmail(fromaddr, recp.split(','), text)
        server.quit()


def genProfile(request):
    email = request.user.email

    obj = profile.objects.get(email_id=email)
    context = profileSer(obj)
    return JsonResponse(context.data,safe=False)


class generateProfile(APIView):
    def get(self,request):

        return render(request,"System/reqprofile.html")


class updateProfile(APIView):
    def post(self,request):
        email = request.user.email
        year = request.POST['year']
        shift = request.POST['shift']
        ssc = request.POST['ssc']
        hsc = request.POST['hsc']
        ug = request.POST['ug']
        pg1 = request.POST['pg1']
        pg2 = request.POST['pg2']
        pg3 = request.POST['pg3']
        pg4 = request.POST['pg4']
        pg5 = request.POST['pg5']
        profile.objects.all().filter(email_id=email).update(year=year,shift=shift,ssc=ssc,hsc=hsc,ug=ug,pg1=pg1,pg2=pg2,pg3=pg3,pg4=pg4,pg5=pg5)
        return HttpResponseRedirect("/system/home/")


class updatePersonal(APIView):
    def post(self,request):
        email = request.user.email
        fnm = request.POST['fnm']
        mnm = request.POST['mnm']
        lnm = request.POST['lnm']
        dob = request.POST['dob']
        gender = request.POST['gender']
        contact = request.POST['contact']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        personal.objects.all().filter(email_id=email).update(first_name=fnm,middle_name=mnm,last_name=lnm,dob=dob,gender=gender,contact=contact,address=address,city=city,state=state)
        return HttpResponseRedirect("/system/home/")



class account(APIView):
    def post(self, request):
        email = request.POST['email']
        try:
            u=User()
            msg = MIMEMultipart()
            pwd = randompassword()
            message ="Your password is : " + pwd
            u.set_password(pwd)
            u.email=email
            u.username=email
            u.save()
            password = "fcpark22"
            msg['From'] = "ankushgochke@gmail.com"
            msg['To'] = email
            msg['Subject'] = "Password for MCA placement System"
            msg.attach(MIMEText(message, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com: 587')
            server.starttls()
            server.login(msg['From'], password)

            server.sendmail(msg['From'], msg['To'],msg.as_string())
            server.quit()
            return HttpResponse('')
        except:
            return HttpResponse('Already Exists')