
import mysql.connector
import csv

from django.shortcuts import render,HttpResponseRedirect
from rest_framework.views import APIView
from .models import register,profile
from django.http import HttpResponse
from .serializer import signupSer

# Create your views here.


def loadSignup(request):
    return render(request, "System/signup.html")


def loadLogin(request):
    return render(request, "System/Index.html")


def loadCriteria(request):
    return render(request, "System/Criteria.html")

class reg(APIView):
    def post(self,request):
        email = request.POST['email']
        fnm = request.POST['fnm']
        mnm = request.POST['mnm']
        lnm = request.POST['lnm']
        year = request.POST['year']
        password = request.POST['password']

        reg = register()
        reg.email = email
        reg.first_name = fnm
        reg.middle_name = mnm
        reg.last_name = lnm
        reg.year = year
        reg.password = password
        reg.save()
        return HttpResponse('Saved')

class login(APIView):
    def post(self,request):
        email = request.POST['email']
        password = request.POST['password']
        try:
            register.objects.get(email=email,password=password)
            return HttpResponse("Logged in successfully")
        except:

            return HttpResponseRedirect("/system/")


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
        writer.writerow(['First name', 'Last name', 'ssc', 'hsc', 'ug', 'pg', 'Email address'])
        mycursor = mydb.cursor()

        query = "select r.first_name , r.last_name, p.ssc, p.hsc, p.ug, p.pg, p.email_id from register r inner join profile p on r.email= p.email_id where "

        if count == 1:

            first = selecttype[0]
            val = checkit(first)
            cond1 = request.POST.get(val)


            query += "p." + first + " > " + cond1 + " AND r.year = '" + Year +"'"


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

            query += "p."+ first + " > " + cond1 + " AND " + "p." + second + " > " + cond2 + " AND r.year = '" + Year +"'"

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

            query += "p." + first + " > " + cond1 + " AND " + "p." + second + " > " + cond2 + " AND " + "p." + third + " > " + cond3 + " AND r.year = '" + Year +"'"

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

            query += "p." + first + " > " + cond1 + " AND " + "p." + second + " > " + cond2 + " AND " + "p." + third + " > " + cond3 + " AND " + "p." + fourth + " > " + cond4 + " AND r.year = '" + Year +"'"
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


