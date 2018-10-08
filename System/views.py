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

def loadadminhome(request):
    return render(request,"System/AdminHome.html")


def loadupdateinternship(request):
    return render(request,"System/UpdateInternship.html")

def loadupdateplacement(request):
    return render(request,"System/UpdatePlacement.html")

def loadpisheet(request):
    return render(request,"System/PISheetOptions.html")

def loadplacementoptions(request):
    email = request.user.email
    try:
        internship.objects.get(email_id=email)
        try:
            placement.objects.get(email_id=email)
            return render(request,"System/PlacementOptionsAfterBoth.html")

        except:
            return render(request,"System/PlacementOptionsAfterInter.html")
    except:
        return render(request,"System/PlacementOptions.html")

def loadinternshipoptions(request):
    email = request.user.email
    try:
        internship.objects.get(email_id=email)
        return render(request,"System/StudentHome.html")
    except:
        return render(request,"System/InternshipDetails.html")

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
                    return HttpResponseRedirect("/system/adminhome/")
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

def loadmail(request):
    return render(request,"System/MailHome.html")



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
        writer.writerow(['First name', 'Middle name', 'Last name', 'Ssc', 'Hsc', 'Ug', 'MCA Sem 1','MCA Sem 2','MCA Sem 3','MCA Sem 4','MCA Sem 5', 'Year', 'Shift', 'Email address'])
        mycursor = mydb.cursor()


        query = "select r.first_name ,r.middle_name, r.last_name, p.ssc, p.hsc, p.ug, p.mca_sem1,p.mca_sem2,p.mca_sem3,p.mca_sem4,p.mca_sem5, p.year, p.shift, p.email_id from personal r inner join profile p on r.email_id= p.email_id where "

        if count == 0:
            query += 'p.year ="' + Year + '"'
            request.session['query'] = query

            mycursor = mydb.cursor()

            mycursor.execute(query)
            myresult = mycursor.fetchall()

            for i in myresult:
                writer.writerow(i)

            return response


        if count == 1:

            first = selecttype[0]
            val = checkit(first)
            cond1 = request.POST.get(val)


            query += "p." + first + " > " + cond1 + " AND p.year = '" + Year +"'"



            mycursor = mydb.cursor()

            mycursor.execute(query)
            myresult = mycursor.fetchall()

            for i in myresult:
                writer.writerow(i)

            return response



        if count == 2:
            first = selecttype[0]
            second = selecttype[1]

            val1 = checkit(first)
            val2 = checkit(second)

            cond1 = request.POST.get(val1)
            cond2 = request.POST.get(val2)

            query += "p."+ first + " > " + cond1 + " AND " + "p." + second + " > " + cond2 + " AND p.year = '" + Year +"'"



            mycursor.execute(query)
            myresult = mycursor.fetchall()

            for i in myresult:
                writer.writerow(i)


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



            mycursor.execute(query)
            myresult = mycursor.fetchall()

            for i in myresult:
                writer.writerow(i)


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

            mycursor.execute(query)
            myresult = mycursor.fetchall()

            for i in myresult:
                writer.writerow(i)


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

        email = request.user.email
        year = request.POST['year']
        shift = request.POST['shift']
        ssc = request.POST['ssc']
        hsc = request.POST['hsc']
        ug = request.POST['ug']
        mca_sem1 = request.POST['mca_sem1']
        mca_sem2 = request.POST['mca_sem2']
        mca_sem3 = request.POST['mca_sem3']
        mca_sem4 = request.POST['mca_sem4']
        mca_sem5 = request.POST['mca_sem5']
        ug_stream = request.POST['ug_stream']
        obj = profile()
        obj.email_id = email
        obj.ug_stream = ug_stream
        obj.year = year
        obj.shift = shift
        obj.ssc = ssc
        obj.hsc = hsc
        obj.ug = ug
        obj.mca_sem1 = mca_sem1
        obj.mca_sem2 = mca_sem2
        obj.mca_sem3 = mca_sem3
        obj.mca_sem4 = mca_sem4
        obj.mca_sem5 = mca_sem5
        obj.save()
        return HttpResponseRedirect("/system/home/")


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
            flag = 1
            return render(request,"System/Index.html",{"Message":msg,"flag":flag})


def randompassword():
    chars=string.ascii_uppercase + string.digits
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
        return render(request,"System/AdminHome.html")

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
        mca_sem1 = request.POST['mca_sem1']
        mca_sem2 = request.POST['mca_sem2']
        mca_sem3 = request.POST['mca_sem3']
        mca_sem4 = request.POST['mca_sem4']
        mca_sem5 = request.POST['mca_sem5']
        profile.objects.all().filter(email_id=email).update(year=year,shift=shift,ssc=ssc,hsc=hsc,ug=ug,mca_sem1=mca_sem1,mca_sem2=mca_sem2,mca_sem3=mca_sem3,mca_sem4=mca_sem4,mca_sem5=mca_sem5)
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
            return render(request,"System/Index.html")
        except:
            return HttpResponse("")

class mainmail(APIView):
    def post(self,request):
        selecttype = request.POST.getlist('check')
        Year = request.POST['Year']
        count = len(selecttype)


        #query = "select r.first_name ,r.middle_name, r.last_name, p.ssc, p.hsc, p.ug, p.pg1,p.pg2,p.pg3,p.pg4,p.pg5, p.year, p.shift, p.email_id from personal r inner join profile p on r.email_id= p.email_id where "
        query2 = "select p.email_id from auth_user r inner join profile p on r.email= p.email_id where "

        if count == 0:

            query2 += 'p.year ="' + Year + '"'
            request.session['query'] = query2
            return render(request,"System/Custom_email.html")

        if count == 1:

            first = selecttype[0]
            val = checkit(first)
            cond1 = request.POST.get(val)

           # query += "p." + first + " > " + cond1 + " AND p.year = '" + Year + "'"
            query2 += "p." + first + " > " + cond1 + " AND p.year = '" + Year + "'"


            request.session['query'] = query2
            return render(request, "System/Custom_email.html")

        if count == 2:
            first = selecttype[0]
            second = selecttype[1]

            val1 = checkit(first)
            val2 = checkit(second)

            cond1 = request.POST.get(val1)
            cond2 = request.POST.get(val2)

            #query += "p." + first + " > " + cond1 + " AND " + "p." + second + " > " + cond2 + " AND p.year = '" + Year + "'"
            query2 += "p." + first + " > " + cond1 + " AND " + "p." + second + " > " + cond2 + " AND p.year = '" + Year + "'"


            request.session['query'] = query2
            return render(request, "System/Custom_email.html")

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

            #query += "p." + first + " > " + cond1 + " AND " + "p." + second + " > " + cond2 + " AND " + "p." + third + " > " + cond3 + " AND p.year = '" + Year + "'"
            query2 += "p." + first + " > " + cond1 + " AND " + "p." + second + " > " + cond2 + " AND " + "p." + third + " > " + cond3 + " AND p.year = '" + Year + "'"


            request.session['query'] = query2
            return render(request, "System/Custom_email.html")

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

            #query += "p." + first + " > " + cond1 + " AND " + "p." + second + " > " + cond2 + " AND " + "p." + third + " > " + cond3 + " AND " + "p." + fourth + " > " + cond4 + " AND p.year = '" + Year + "'"
            query2 += "p." + first + " > " + cond1 + " AND " + "p." + second + " > " + cond2 + " AND " + "p." + third + " > " + cond3 + " AND " + "p." + fourth + " > " + cond4 + " AND p.year = '" + Year + "'"


            request.session['query'] = query2
            return render(request, "System/Custom_email.html")

class saveInternship(APIView):
    def post(self,request):

        email = request.user.email
        doji = request.POST['doji']
        hremail = request.POST['hremail']
        hrname = request.POST['hrname']
        hrcontact = request.POST['hrcontact']
        intern = request.POST['internship']
        ipackage = request.POST['ipackage']
        projectname = request.POST['projectname']
        seminar = request.POST['seminar']
        status = request.POST['status']
        try:
            internship.objects.create(email_id=email,hremail=hremail,doji=doji,hrname=hrname,hrcontact=hrcontact,internship=intern,ipackage=ipackage,projectname=projectname,seminar=seminar,status=status)
            return render(request,"System/StudentHome.html")
        except:
            return HttpResponse("Error")


class savePlacement(APIView):
    def post(self,request):
        email = request.user.email
        place = request.POST['placement']
        ppackage = request.POST['ppackage']
        dojp = request.POST['dojp']
        hrname = request.POST['hrname']
        hrcontact = request.POST['hrcontact']
        hremail = request.POST['hremail']
        status = request.POST['status']

        placement.objects.create(email_id=email,placement=place,ppackage=ppackage,
                                 dojp=dojp,hrname=hrname,hrcontact=hrcontact,hremail=hremail,status=status)

        return render(request,"System/StudentHome.html")


def jsoninternship(request):
    email = request.user.email
    obj = internship.objects.get(email_id=email)
    context = internshipSer(obj)
    return JsonResponse(context.data, safe=False)


def jsonplacement(request):
    email = request.user.email
    obj = placement.objects.get(email_id=email)
    context = placementSer(obj)
    return JsonResponse(context.data, safe=False)


def updateIntership(request):
    email = request.user.email
    doji = request.POST['doji']
    hremail = request.POST['hremail']
    hrname = request.POST['hrname']
    hrcontact = request.POST['hrcontact']
    intern = request.POST['internship']
    ipackage = request.POST['ipackage']
    projectname = request.POST['projectname']
    seminar = request.POST['seminar']
    status = request.POST['status']

    internship.objects.filter(email_id=email).update(internship=intern,doji=doji,hremail=hremail,hrname = hrname,
                                                     hrcontact=hrcontact,ipackage=ipackage,projectname=projectname,
                                                     seminar=seminar,status=status)
    return HttpResponse("Updated!")

def updatePlacement(request):
    email = request.user.email

    dojp = request.POST['dojp']
    hremail = request.POST['hremail']
    hrname = request.POST['hrname']
    hrcontact = request.POST['hrcontact']
    place = request.POST['placement']
    ppackage = request.POST['ppackage']
    status = request.POST['status']

    placement.objects.filter(email_id=email).update(placement=place,dojp=dojp,hremail=hremail,hrname=hrname,
                                                    hrcontact=hrcontact,ppackage=ppackage,status=status)
    return render(request,"System/StudentHome.html")


def genInternshipList(request):
    filename = request.POST['filename']
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="cpms"
    )

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + filename + '.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['First name', 'Middle name', 'Last name', 'Email', 'Internship Company','Stipend','Project Name','Seminar Topic','Date Of Joining','Hr Name','Hr Contact','Hr Email','Status'])
    mycursor = mydb.cursor()

    query = "select p.first_name, p.middle_name, p.last_name, p.email_id, i.internship, i.ipackage, i.projectname, i.seminar, i.doji, i.hrname, i.hrcontact, i.hremail, i.status from personal p INNER  JOIN internship i on p.email_id = i.email_id where i.status = 'On Campus' UNION ALL select p.first_name, p.middle_name, p.last_name, p.email_id, i.internship, i.ipackage, i.projectname, i.seminar, i.doji, i.hrname, i.hrcontact, i.hremail, i.status from personal p INNER  JOIN internship i on p.email_id = i.email_id where i.status = 'Off Campus'"
    mycursor.execute(query)
    myresult = mycursor.fetchall()

    for i in myresult:
        writer.writerow(i)

    return response

def getPlacementList(request):
    filename = request.POST['filename']
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="cpms"
    )

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + filename + '.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ['First name', 'Middle name', 'Last name', 'Email', 'Placement Company', 'Salary', 'Date Of Joining', 'Hr Name', 'Hr Contact', 'Hr Email', 'Status'])
    mycursor = mydb.cursor()

    query = "select p.first_name, p.middle_name, p.last_name, p.email_id, i.placement, i.ppackage, i.dojp, i.hrname, i.hrcontact, i.hremail, i.status from personal p INNER  JOIN placement i on p.email_id = i.email_id where i.status = 'On Campus' UNION ALL select p.first_name, p.middle_name, p.last_name, p.email_id,  i.placement, i.ppackage, i.dojp, i.hrname, i.hrcontact, i.hremail, i.status  from personal p INNER  JOIN placement i on p.email_id = i.email_id where i.status = 'Off Campus'"
    mycursor.execute(query)
    myresult = mycursor.fetchall()

    for i in myresult:
        writer.writerow(i)

    return response
