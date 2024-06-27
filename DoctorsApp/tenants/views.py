from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django_tenants.utils import schema_context
from .forms import  AddRecordForm
from DoctorsApp.calendar.models import Member, Doctor


def home(request):
    if request.user.is_authenticated:
        try:
            doctor = Doctor.objects.filter(user=request.user).first()
            members = Member.objects.filter(doctor=doctor)
        except Doctor.DoesNotExist:
            messages.error(request, "Doctor not found for the current user.")
            members = []
        return render(request, 'home.html', {'members': members, 'doctor': doctor})
    else:
        # Check to see if logging in
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            # Authenticate
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You Have Been Logged In!")
                return redirect('home')
            else:
                messages.error(request, "There Was An Error Logging In, Please Try Again...")
                return redirect('home')
        else:
            return redirect('login')


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")

@login_required
def customer_record(request, pk):
    doctor = Doctor.objects.filter(user=request.user).first()

    if request.user.is_authenticated:
        with schema_context(doctor.tenant.schema_name):
            customer_record = Member.objects.get(doctor=doctor, id=pk)
            return render(request, 'record.html', {'member': customer_record})
    else:
        messages.success(request, "You must be logged in to view that page...")
        return redirect('home')

@login_required
def delete_record(request, pk):
    doctor = Doctor.objects.filter(user=request.user).first()
    if request.user.is_authenticated:
        with schema_context(doctor.tenant.schema_name):
            delete_it = Member.objects.get(id=pk)
            delete_it.delete()
            messages.success(request, "Record deleted successfully...")
            return redirect('home')
    else:
        messages.success(request, "You must be logged in to do that...")
        return redirect('home')

@login_required
def add_record(request):
    form = AddRecordForm(request.POST or None)
    doctor = Doctor.objects.filter(user=request.user).first()
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                with schema_context(doctor.tenant.schema_name):
                    new_member = form.save(commit=False)
                    new_member.doctor = doctor
                    new_member.save()
                    messages.success(request, "Record added...")
                    return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, "You must be logged in...")
        return redirect('home')

@login_required
def update_record(request, pk):
    doctor = Doctor.objects.filter(user=request.user).first()
    if request.user.is_authenticated:
        with schema_context(doctor.tenant.schema_name):
            current_record = Member.objects.get(id=pk)
            form = AddRecordForm(request.POST or None, instance=current_record)
            if form.is_valid():
                form.save()
                messages.success(request, "Record has been updated!")
                return redirect('home')
            return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, "You must be logged in to view that page...")
        return redirect('home')