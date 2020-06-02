from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import connection
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
import hashlib
from django.contrib import messages

def index(request):
    return render(request,'index.html')#you always have to pass request

    """ third argument that we can pass in render is parameters
        first we have to declare parameter as dictionary
        eg param={'name': 'saksham', 'place':'india'}
        then write ,param in render
        in html {{name}}  , {{place}}  double curly brackets.
     """
def register(request):
    return render(request,'register.html')
def login1(request):
    return render(request,'login1.html')
def About(request):
    return render(request,'about.html')
def handlesignup(request):
    if request.method == 'POST':
        user=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        passw=request.POST['password1']
        passw1=request.POST['password2']
        gender=request.POST['gender']
        vid=request.POST['voter']
        city=request.POST['city']
        state=request.POST['state']
        result = hashlib.md5(passw.encode())
        passwd=result.hexdigest()

        if not user.isalnum():
            messages.error(request, "Your username must contain only words and numbers !")
            return redirect('/registration/')

        if passw!= passw1:
            messages.error(request, "Password do not match ")
            return redirect('/registration/')




        myuser = User.objects.create_user(user,email,passw)
        myuser.first_name= fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your Account has been successfully created !")
        cursor=connection.cursor()
        cursor.execute('INSERT INTO regis(username,fname,lname,email,password,gender,voter_id,city,state) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',(user,fname,lname,email,passwd,gender,vid,city,state))
        # messages.success(request,"you have successfully registered!")
        return redirect('/')
        # messages.success(request,"you have successfully registered!")
        # return HttpResponse("thanks")
    else:
        return HttpResponse('404 - Not Found') 

def checklogin(request):
    if request.method == "POST":
        username=request.POST['name']
        pw=request.POST['pass']
        result = hashlib.md5(pw.encode())
        P = result.hexdigest()
        user = authenticate(username= username , password= pw)
        if user is not None:
           
            cursor=connection.cursor()
            qry = "SELECT username,password,voted FROM regis WHERE username = %s AND password = %s"
            cursor.execute(qry, (username, P))
            myresult = cursor.fetchall()
            if(int(myresult[0][-1]) == 1):
                print("----------------------------------------------------")
                messages.error(request, 'Already voted')
                return redirect('/')
            else:
                cursor.execute('update regis set voted = 1 where username = %s', (str(myresult[0][0]),) )
                login(request,user)
                messages.success(request," Successfully logged in ")
                return redirect('/voting/')
        else:
            messages.error(request,'Invalid credentials')
            return redirect('/')    
    else:
        return HttpResponse("Error 404")

    # cursor=connection.cursor()
    # try:
    #     qry = "SELECT username,password,voted FROM regis WHERE username = %s AND password = %s"
    #     cursor.execute(qry, (user_name, pwd))
    # except:
    #     messages.error(request, 'user not found!')
    #     return redirect('/')
    # else:
    #     myresult = cursor.fetchall()
    #     if(int(myresult[0][-1]) == 1):
    #         messages.error(request, 'Already voted')
    #         return redirect('/')
            
    #     else:
    #         cursor.execute('update regis set voted = 1 where username = %s', (str(myresult[0][0]),) )
    #         messages.success(request,'Welcome to vote page')
    #         return redirect('/voting/')
        
