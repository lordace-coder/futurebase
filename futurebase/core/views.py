from django.shortcuts import render,redirect
from django.http import HttpRequest
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from core.models import Collection, Column, Project
# Create your views here.

def index(request:HttpRequest):
    # authenticate user
    if request.method == 'POST':
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username,password = password)
            if user:
                messages.success(request,'logged in succesfully')
                login(request,user)
            
            else:
                messages.error(request,'invalid credentials')
        except Exception as e:
            messages.error(request,"error occured "+str(e))
    return render(request,'index.html')


def register(request:HttpRequest):
    if request.method == 'POST':
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = User.objects.create_user(username=username,password=password)
            user.save()
            messages.success(request,'user created succesfully')
            login(request,user)
            return redirect('home')
        except Exception as e:
            messages.error(request,"error occured "+str(e))
    return render(request,'signup.html')

def logout_view(request:HttpRequest):
    logout(request)
    messages.success(request,'logged out succesfully')
    return redirect('home')

@login_required(login_url='home')
def dashboard(request:HttpRequest):

    return render(request,'dashboard.html',context = {
    'projects': Project.objects.filter(user=request.user),
    'total_collections': Collection.objects.filter(project__user=request.user).count(),
    'total_columns': Column.objects.filter(collection__project__user=request.user).count(),
})

def create_project(request:HttpRequest):
    if request.method == 'POST':
        try:
            title = request.POST.get("title")
            description = request.POST.get("description")
            project = Project.objects.create(user=request.user,title=title,description=description)
            project.save()
            messages.success(request,'project created succesfully')
            return redirect('dashboard')
        except Exception as e:
            messages.error(request,"error occured "+str(e))
    return render(request,'dashboard.html')
