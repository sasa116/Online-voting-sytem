from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from phe import paillier
from .models import party
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
import base64
import pickle
from django.db import connection
l1=[]
l2=[]
l3=[]
pu = open("C:/Users/Administrator/Desktop/main_project/voting/pu.pk", 'rb')
pr = open("C:/Users/Administrator/Desktop/main_project/voting/pri.pk", 'rb')
public_key = pickle.load(pu)
private_key = pickle.load(pr) 


def votingpage(request):
    if request.method=="POST":
        print('in votepage')
        return render(request,'voting/votepage.html')
    else:
        return HttpResponse("<H1>Error 404</H1> <BR> <H2>YOU MUST LOGIN</H2>")

def choose(request):
    # if request.method=="POST":
        return render(request,'voting/choose.html')
    # else:
    #     return HttpResponse("<H1>Error 404</H1> <BR> <H2>YOU MUST LOGIN</H2>")

# def logout(request):
#     # if request.method == "POST":
#         logout(request)
#         messages.success(request,"Successfully logged out")
#         return redirect('/')





def thanks(request):
    if(request.method == 'POST'):
        print("-----------------")
        value=request.POST['par_a']
        # print("-----------------")
        # print(value)
        # print(type(value))
        if(value == "1"):
            l1.append(public_key.encrypt(1))
            l2.append(public_key.encrypt(0))
            l3.append(public_key.encrypt(0))
            
            update()
        elif(value == "2"):
            l2.append(public_key.encrypt(1))
            l3.append(public_key.encrypt(0))
            l1.append(public_key.encrypt(0))
            
            update()
        elif(value == "3"):
            l3.append(public_key.encrypt(1))
            l1.append(public_key.encrypt(0))
            l2.append(public_key.encrypt(0))
            
            update()
    else:
        return HttpResponse('404 - Not Found') 
    messages.success(request,'Thanks for voting')
    return render(request,'voting/thank.html')


def update():
    print("We are in update")
    cursor=connection.cursor()
    # cursor.execute('INSERT INTO regis(voted) VALUE(%s)',(int(1)
    cursor.execute('INSERT INTO party(party_A, party_B, party_C) VALUES(%s,%s,%s)',(base64.b64encode(pickle.dumps(l1[-1])),base64.b64encode(pickle.dumps(l2[-1])),base64.b64encode(pickle.dumps(l3[-1]))))
    

def result(request):
    cursor=connection.cursor()
    cursor.execute("SELECT party_A FROM party")
    data = cursor.fetchall()
    out = [item for t in data for item in t]
    l=[]
    total = 0
    for i in range(len(out)):
        print(base64.b64decode(out[i]))
        l.append(pickle.loads(base64.b64decode(out[i])))
    
    for i in range(0,len(l)):
        total= total + l[i]
    A=private_key.decrypt(total)

    cursor.execute("SELECT party_B FROM party")
    data1 = cursor.fetchall()
    out1 = [item for t in data1 for item in t] 
    j=[]
    to = 0
    for k in range(len(out1)):
        j.append(pickle.loads(base64.b64decode(out1[k])))
    
    for k in range(0,len(j)):
        to= to + j[k]
    B=private_key.decrypt(to)


    cursor.execute("SELECT party_C FROM party")
    data2 = cursor.fetchall()
    out2 = [item for t in data2 for item in t] 
    k=[]
    tol = 0
    for x in range(len(out2)):
        k.append(pickle.loads(base64.b64decode(out2[x])))
    
    
    for x in range(0,len(k)):
        tol= tol + k[x]
    C=private_key.decrypt(tol)

    param={'partya' :A ,'partyb' :B,'partyc' :C}
    
    return render(request, 'voting/result.html' ,param)