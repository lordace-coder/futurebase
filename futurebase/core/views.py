from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse

from collections_manager import manager
from .models import Project, Collection, Column
import json

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
            
            # Debug logging
            print("Edit Collection POST Data:")
            print("Name:", name)
            print("Field Names:", field_names)
            print("Field Types:", field_types)
            print("Raw POST Data:", request.POST)
            
            if not name:
                messages.error(request, 'Collection name is required.')
                return redirect('project_detail', project_id=project_id)
            
            # Update collection name
            collection.name = name
            collection.save()
            
            # Clear existing columns and create new ones
            collection.columns.clear()  # Use clear() instead of delete() to maintain referential integrity
            
            # Validate and create fields
            if len(field_names) != len(field_types):
                messages.error(request, 'Field names and types must match.')
                return redirect('project_detail', project_id=project_id)
            
            fields_created = False
            for field_name, field_type in zip(field_names, field_types):
                if field_name.strip() and field_type.strip():  # Check for non-empty strings
                    column = Column.objects.create(
                        name=field_name.strip(),
                        field=field_type.strip()
                    )
                    collection.columns.add(column)
                    fields_created = True
            
            if not fields_created:
                messages.error(request, 'At least one valid field is required.')
                return redirect('project_detail', project_id=project_id)
            
            messages.success(request, 'Collection updated successfully!')
            return redirect('project_detail', project_id=project_id)
        
        # GET request - return current collection data
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


def collection_detail_view(request:HttpRequest,collection_id:str):
    if request.method == 'POST':
        try:
            data = request.POST.dict()
            data.pop("csrfmiddlewaretoken")
            print(data)
            print("Received data for collection", collection_id, ":", data)  # Debug log
            collection = Collection.objects.get(id=collection_id, project__user=request.user)
            # TODO: Add your data storage logic here

            manager.insertData(collection.dbName(),data)
            # For now, just return success
            messages.info(request,"Updated succesfully")

        except json.JSONDecodeError as e:
            messages.error(request,"Invalid json data")
        # except Exception as e:
        #     print(e)
        #     messages.error(request,str(e))

    try:
        collection = Collection.objects.get(id=collection_id, project__user=request.user)
        fields = collection.columns.all()
        collection_data = manager.fetchAllData(collection.dbName())
        context = {
            "collection": collection,
            "collection_data": collection_data,
            "fields": fields  # Get all columns/fields for this collection
        }
 
        return render(request, 'collection_detail.html', context=context)
    except Collection.DoesNotExist:
        messages.error(request, 'Collection not found.')
        return redirect('dashboard')


@login_required(login_url='home')
def delete_collection_item(request,collection_id,item_id):
    collection = Collection.objects.get(id=collection_id, project__user=request.user)
    manager.deleteData(collection.dbName(),{"_id":item_id})
    return redirect('collection_detail',collection_id=collection_id)


@login_required(login_url='home')
def edit_collection_item(request, collection_id, item_id):
    try:
        collection = Collection.objects.get(id=collection_id, project__user=request.user)
        if request.method == 'POST':
            try:
                data = {}

                # Process form data
                for key, value in request.POST.items():
                    if key not in ['csrfmiddlewaretoken', '_id']:
                        data[key] = value

                try:
                    # Ensure _id is passed as a string that can be converted to ObjectId
                    manager.updateData(collection.dbName(), filter={"_id": str(item_id)}, update={"$set": data})
                    messages.success(request, 'Record updated successfully!')
                except ValueError as e:
                    messages.error(request, str(e))
                except Exception as e:
                    messages.error(request, f'Error updating record: {str(e)}')
                return redirect('collection-detail', collection_id=collection_id)
            except Exception as e:
                messages.error(request, f'Error updating record: {str(e)}')
                return redirect('collection-detail', collection_id=collection_id)
        return redirect('collection-detail', collection_id=collection_id)
    except Collection.DoesNotExist:
        messages.error(request, 'Collection not found')
        return redirect('dashboard')
