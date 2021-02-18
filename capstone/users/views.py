from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, LogInForm, UserSearchForm
from django.views.generic.edit import FormView
from .models import User
from django.db.models import Q

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

class SearchFormView(FormView):
    form_class = UserSearchForm
    template_name = 'users/search.html'

    def form_valid(self, form):
        searchWord = form.cleaned_data['search_word']
        user_list = User.objects.filter(Q(name__icontains=searchWord) | Q(email__icontains=searchWord) | Q(bio__icontains=searchWord)).distinct()

        context = {'form': form, 'search_term': searchWord, 'object_list': user_list}
        return render(self.request, self.template_name, context)