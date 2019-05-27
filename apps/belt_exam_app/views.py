from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Job, Category
import bcrypt

# Create your views here.
def index(request):
    return render(request,'belt_exam_app/login_reg.html')

def register(request):
    reg_errors = User.objects.reg_validator(request.POST)
    if len(reg_errors) > 0:
        for key,value in reg_errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(index)
    user = User.objects.create(fname=request.POST['fname'],lname=request.POST['lname'],birthday=request.POST['birthday'],email=request.POST['email_r'],password=bcrypt.hashpw(request.POST['password_r'].encode(), bcrypt.gensalt()))
    request.session['fname']=request.POST['fname']
    request.session['user_id']=user.id
    return redirect('/dashboard')

def login(request):
    login_errors = User.objects.login_validator(request.POST)
    if len(login_errors) > 0:
        for key,value in login_errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(index)

    user = User.objects.filter(email=request.POST['email']).values()
    for e in user:
        request.session['fname']=e['fname']
        request.session['user_id']=e['id']
    return redirect('/dashboard')

def dashboard(request):
    if 'fname' in request.session:
        context = {
            "name": request.session['fname'],
            "user_id": request.session['user_id'],
            "jobs": Job.objects.exclude(user=request.session['user_id']).order_by('-created_at'),
            "user_jobs": Job.objects.filter(user=request.session['user_id']),
        }
        return render(request,'belt_exam_app/dashboard.html',context)
    return redirect ('/')

def add_job(request):
    if 'fname' in request.session:
        context = {
            "categories": Category.objects.all()
        }
        return render(request,'belt_exam_app/add_job.html', context)

def addjobDB(request):
    if 'fname' in request.session:
        errors = Job.objects.validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/jobs/new')
        user = User.objects.get(id=request.session['user_id'])
        job = Job.objects.create(owner=user,title=request.POST['title'],location=request.POST['location'],description=request.POST['description'])
        if request.POST['other']:
            category = Category.objects.create(title=request.POST['other'])
            job.category.add(category)
            job.save()
        else:
            category = request.POST.getlist('category')
            for i in range(len(category)):
                add_category = Category.objects.get(id=category[i])
                job.category.add(add_category)
                job.save()
        return redirect(view_job,job.id)
    return redirect ('/')

def add_job_to_user(request,job_id):
    user = User.objects.get(id=request.session['user_id'])
    job = Job.objects.get(id=job_id)
    job.user = user
    job.save()
    return redirect('/dashboard')

def remove_job_from_user(request,job_id):
    job = Job.objects.get(id=job_id)
    job.user = None
    job.save()
    return redirect('/dashboard')

def edit_job(request, job_id):
    if 'fname' in request.session:
        context = {
            "user_id":request.session['user_id'],
            "name": request.session['fname'],
            "job": Job.objects.get(id=job_id)
        }
        return render(request,'belt_exam_app/edit_job.html',context)
    return redirect ('/')

def editjob(request,job_id):
    errors = Job.objects.validator(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(edit_job,job_id)
    job = Job.objects.get(id=job_id)
    job.title = request.POST['title']
    job.description = request.POST['description']
    job.location = request.POST['location']
    job.save()
    return redirect(view_job,job_id)

def view_job(request,job_id):
    if 'fname' in request.session:
        context = {
            "user_id":request.session['user_id'],
            "name": request.session['fname'],
            "job": Job.objects.get(id=job_id)
        }
        return render(request,'belt_exam_app/view_job.html',context)
    return redirect ('/')

def remove_job(request,job_id):
    if 'fname' in request.session:
        job = Job.objects.get(id=job_id)
        job.delete()
        return redirect('/dashboard')
    return redirect ('/')

def logout(request):
    request.session.clear()
    return redirect('/')