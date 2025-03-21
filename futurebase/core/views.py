from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Project, Collection, Column

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'index.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')
        
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        messages.success(request, f'Welcome to FutureBase, {username}!')
        return redirect('dashboard')
    
    return render(request, 'signup.html')

@login_required
def dashboard(request):
    projects = Project.objects.filter(user=request.user)
    total_collections = Collection.objects.filter(project__user=request.user).count()
    total_columns = Column.objects.filter(collection__project__user=request.user).count()
    
    context = {
        'projects': projects,
        'total_collections': total_collections,
        'total_columns': total_columns,
    }
    return render(request, 'dashboard.html', context)

@login_required
def create_project(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        if not title:
            messages.error(request, 'Project title is required.')
            return redirect('dashboard')
        
        project = Project.objects.create(
            user=request.user,
            title=title,
            description=description
        )
        messages.success(request, 'Project created successfully!')
        return redirect('project_detail', project_id=project.id)
    
    return redirect('dashboard')

@login_required
def project_detail(request, project_id):
    try:
        project = Project.objects.get(id=project_id, user=request.user)
        collections = Collection.objects.filter(project=project)
        
        context = {
            'project': project,
            'collections': collections,
        }
        return render(request, 'project_detail.html', context)
    except Project.DoesNotExist:
        messages.error(request, 'Project not found.')
        return redirect('dashboard')

@login_required
def create_collection(request, project_id):
    try:
        project = Project.objects.get(id=project_id, user=request.user)
        
        if request.method == 'POST':
            name = request.POST.get('name')
            field_names = request.POST.getlist('field_names[]')
            field_types = request.POST.getlist('field_types[]')
            
            # Debug logging
            print("Form Data:")
            print("Name:", name)
            print("Field Names:", field_names)
            print("Field Types:", field_types)
            print("POST Data:", request.POST)
            
            if not name:
                messages.error(request, 'Collection name is required.')
                return redirect('project_detail', project_id=project_id)
            
            if not field_names or not field_types:
                messages.error(request, 'At least one field is required.')
                return redirect('project_detail', project_id=project_id)
            
            # Create collection
            collection = Collection.objects.create(
                project=project,
                name=name
            )
            
            # Create columns
            for field_name, field_type in zip(field_names, field_types):
                if field_name and field_type:
                    column = Column.objects.create(
                        name=field_name,
                        field=field_type
                    )
                    collection.columns.add(column)
            
            messages.success(request, 'Collection created successfully!')
        
        return redirect('project_detail', project_id=project_id)
    except Project.DoesNotExist:
        messages.error(request, 'Project not found.')
        return redirect('dashboard')

@login_required
def edit_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id, user=request.user)
        
        if request.method == 'POST':
            title = request.POST.get('title')
            description = request.POST.get('description')
            
            if not title:
                messages.error(request, 'Project title is required.')
                return redirect('project_detail', project_id=project_id)
            
            project.title = title
            project.description = description
            project.save()
            
            messages.success(request, 'Project updated successfully!')
            return redirect('project_detail', project_id=project_id)
        
        return JsonResponse({
            'title': project.title,
            'description': project.description or ''
        })
    except Project.DoesNotExist:
        messages.error(request, 'Project not found.')
        return redirect('dashboard')

@login_required
def edit_collection(request, project_id, collection_id):
    try:
        project = Project.objects.get(id=project_id, user=request.user)
        collection = Collection.objects.get(id=collection_id, project=project)
        
        if request.method == 'POST':
            name = request.POST.get('name')
            field_names = request.POST.getlist('field_names[]')
            field_types = request.POST.getlist('field_types[]')
            if not name:
                messages.error(request, 'Collection name is required.')
                return redirect('project_detail', project_id=project_id)
            
            if not field_names or not field_types:
                messages.error(request, 'At least one field is required.')
                return redirect('project_detail', project_id=project_id)
            
            # Update collection name
            collection.name = name
            collection.save()
            
            # Clear existing columns and create new ones
            collection.columns.all().delete()
            for field_name, field_type in zip(field_names, field_types):
                if field_name and field_type:
                    column = Column.objects.create(
                        name=field_name,
                        field=field_type
                    )
                    collection.columns.add(column)
            
            messages.success(request, 'Collection updated successfully!')
            return redirect('project_detail', project_id=project_id)
        
        return JsonResponse({
            'name': collection.name,
            'fields': [
                {'name': column.name, 'type': column.field}
                for column in collection.columns.all()
            ]
        })
    except (Project.DoesNotExist, Collection.DoesNotExist):
        messages.error(request, 'Collection not found.')
        return redirect('project_detail', project_id=project_id)

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home') 