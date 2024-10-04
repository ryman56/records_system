#views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import FileResponse, Http404, HttpResponse
from django.db import IntegrityError, transaction
from django.urls import reverse
from django.utils import timezone
from django.db.models import Q
from django.views.decorators.http import require_http_methods
import logging
from .forms import UserRegistrationForm, DocumentUploadForm
from .models import Department, Record, User
import mimetypes


User = get_user_model()


#index.html(homepage) render
def index(request):
    return render(request, 'index.html')


#log out function
def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('index')


#dashboard view function
@login_required
def dashboard_view(request):
    total_departments = Department.objects.count()
    total_records = Record.objects.count()
    recent_activities = Record.objects.order_by('-last_accessed')[:5]
    
    context = {
        'total_departments': total_departments,
        'total_records': total_records,
        'recent_activities': recent_activities,
    }
    return render(request, 'dashboard.html', context)


#upload document function
@login_required
def upload_document_view(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            
            # Debug information
            print(f"Current user ID: {request.user.id}")
            print(f"User authenticated: {request.user.is_authenticated}")
            print(f"User exists in database: {User.objects.filter(id=request.user.id).exists()}")
            print(f"User type: {type(request.user)}")
            print(f"Form data: {form.cleaned_data}")
            
            document.created_by = request.user
            try:
                with transaction.atomic():
                    document.save()
                    print(f"Document saved with created_by_id: {document.created_by_id}")
                messages.success(request, 'Document uploaded successfully.')
                return redirect('dashboard')
            except IntegrityError as e:
                print(f"Error saving document: {str(e)}")
                messages.error(request, 'Error saving document. Please try again.')
        else:
            print(f"Form errors: {form.errors}")
            messages.error(request, 'Error uploading document. Please check the form and try again.')
    else:
        form = DocumentUploadForm()

    return render(request, 'upload_document.html', {'form': form})

#document view function
@login_required
def view_document(request, record_id):
    record = get_object_or_404(Record, id=record_id)

    # Update last accessed time
    record.last_accessed = timezone.now()
    record.save()

    try:
        # Open the document and determine its content type dynamically
        file_path = record.document.path
        content_type, _ = mimetypes.guess_type(file_path)

        # Use a default content type if one cannot be guessed
        if content_type is None:
            content_type = 'application/octet-stream'

        return FileResponse(open(file_path, 'rb'), content_type=content_type)
    
    except FileNotFoundError:
        # Handle the case where the file does not exist
        raise Http404("Document not found")


#department records function
@login_required
def department_records(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    records = Record.objects.filter(department=department).order_by('title')
    return render(request, 'department_records.html', {'department': department, 'records': records})


#view records function
@login_required
def records_view(request):
    records = Record.objects.all().select_related('department', 'created_by').order_by('title')
    return render(request, 'records.html', {'records': records})


#department_view
@login_required
def departments_view(request):
    departments = Department.objects.all()
    return render(request, 'departments.html', {'departments': departments})


#log in page
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Debugging: Print the values of username and password
        print(f"Attempting login with username: {username}, password: {password}")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            logger.info(f"User {username} logged in successfully.")
            messages.success(request, 'You have successfully logged in.')
            return redirect('dashboard')
        else:
            logger.warning(f"Failed login attempt for username: {username}")
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')




# Set up logging
logger = logging.getLogger(__name__)


#registercfuntion
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()  # Save the user
                    logger.info(f"User {user.username} created successfully.")  # Log success
                    messages.success(request, 'Account created successfully! Please log in.')
                    return redirect('login')  # Redirect to login page
            except Exception as e:
                logger.error(f"Error creating user: {str(e)}")  # Log error
                messages.error(request, f'An error occurred while creating your account: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


#document download function
@login_required
def download_document(request, record_id):
    record = get_object_or_404(Record, id=record_id)
    response = FileResponse(record.document.open('rb'), as_attachment=True)
    response['Content-Disposition'] = f'attachment; filename="{record.document.name}"'
    return response


#user profile section
@login_required
def profile_view(request):
    return render(request, 'profile.html')


#profile view section
@login_required
def profile_view(request):
    profile_form = UserRegistrationForm(instance=request.user)  # Assuming you're using this for profile updates
    password_form = PasswordChangeForm(user=request.user)
    
    if request.method == 'POST':
        profile_form = UserRegistrationForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')

    return render(request, 'profile.html', {
        'profile_form': profile_form,
        'password_form': password_form,
    })


#change password function
@login_required
def profile_view(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        password_form = PasswordChangeForm(user=request.user)

    return render(request, 'profile.html', {
        'password_form': password_form,
    })
