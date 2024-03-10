from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User
from blood import forms as bforms
from blood import models as bmodels


def lab_signup_view(request):
    userForm=forms.labUserForm()
    labForm=forms.labForm()
    mydict={'userForm':userForm,'labForm':labForm}
    if request.method=='POST':
        userForm=forms.labUserForm(request.POST)
        labForm=forms.labForm(request.POST,request.FILES)
        if userForm.is_valid() and labForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            lab=labForm.save(commit=False)
            lab.user=user
            lab.bloodgroup=labForm.cleaned_data['bloodgroup']
            lab.save()
            my_lab_group = Group.objects.get_or_create(name='lab')
            my_lab_group[0].user_set.add(user)
        return HttpResponseRedirect('lablogin')
    return render(request,'lab/labsignup.html',context=mydict)

def lab_dashboard_view(request):
    lab= models.lab.objects.get(user_id=request.user.id)
    dict={
        'requestpending': bmodels.BloodRequest.objects.all().filter(request_by_lab=lab).filter(status='Pending').count(),
        'requestapproved': bmodels.BloodRequest.objects.all().filter(request_by_lab=lab).filter(status='Approved').count(),
        'requestmade': bmodels.BloodRequest.objects.all().filter(request_by_lab=lab).count(),
        'requestrejected': bmodels.BloodRequest.objects.all().filter(request_by_lab=lab).filter(status='Rejected').count(),

    }
   
    return render(request,'lab/lab_dashboard.html',context=dict)

def make_request_view(request):
    request_form=bforms.RequestForm()
    if request.method=='POST':
        request_form=bforms.RequestForm(request.POST)
        if request_form.is_valid():
            blood_request=request_form.save(commit=False)
            blood_request.bloodgroup=request_form.cleaned_data['bloodgroup']
            lab= models.lab.objects.get(user_id=request.user.id)
            blood_request.request_by_lab=lab
            blood_request.save()
            return HttpResponseRedirect('my-request')  
    return render(request,'lab/makerequest.html',{'request_form':request_form})

def my_request_view(request):
    lab= models.lab.objects.get(user_id=request.user.id)
    blood_request=bmodels.BloodRequest.objects.all().filter(request_by_lab=lab)
    return render(request,'lab/my_request.html',{'blood_request':blood_request})
