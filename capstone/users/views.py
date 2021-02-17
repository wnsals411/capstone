from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, LogInForm

def main(request):
    if request.method == 'GET':
        form = LogInForm()
        return render(request, 'users/main.html', {'form': form})

    elif request.method == 'POST':
        form = LogInForm(request.POST)

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('users:index'))
        else:
            return HttpResponse("등록되지 않은 사용자입니다.")    
    return render(request, 'users/main.html')

def signup(request):
    if request.method == 'GET':
        form = SignUpForm()

        return render(request, 'users/signup.html', {'form':form})
    elif request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('users:index'))
            
        return render(request, 'users/main.html')

def sucess(request):
    return HttpResponse("로그인 성공!")