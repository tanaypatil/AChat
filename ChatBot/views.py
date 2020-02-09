import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from .forms import *


def home(request):
    if request.user.is_authenticated:
        ratings = Rating.objects.values_list('rating', flat=True)
        rating_count = Rating.objects.all().count()
        if rating_count == 0:
            average_rating = 0
        else:
            average_rating = sum(ratings)//rating_count
        context = {
            'average': average_rating,
            'ratings': Rating.objects.all()
        }
        return render(request, 'ChatBot/home.html', context=context)
    else:
        if request.POST:
            return handle_forms(request)
        context = get_default_context()
        return render(request, 'ChatBot/index.html', context=context)


def handle_forms(request):
    request_type = request.POST['submit']
    if request_type == "Sign In":
        return login_user(request)
    else:
        return signup_user(request)


def login_user(request):
    form = AuthenticationForm(request=request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        return HttpResponseRedirect('/')
    else:
        context = get_default_context(login_form=form)
        return render(request, 'ChatBot/index.html', context=context)


def logout_user(request):
    logout(request)
    context = get_default_context()
    return HttpResponseRedirect('/', context)


def signup_user(request):
    form = UserCreationForm(data=request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "User signed up successfully.")
        return HttpResponseRedirect('/')
    else:
        context = get_default_context(signup_form=form)
        context['signup'] = "signup"
        return render(request, 'ChatBot/index.html', context=context)


def get_default_context(login_form=AuthenticationForm(), signup_form=UserCreationForm()):
    return {'login_form': login_form, 'signup_form': signup_form}


@login_required
def files(request):
    if request.POST:
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            File.objects.create(name=form.cleaned_data['name'], document=form.cleaned_data['document'],
                                user=User.objects.get(username=str(request.user)))
            messages.success(request, "File uploaded successfully.")
            return HttpResponseRedirect('files', {'form': FileForm(), 'files': File.objects.all()})
        else:
            return render(request, 'ChatBot/files.html', context={'form': form, 'files': File.objects.all()})
    else:
        context = {
            'form': FileForm(),
            'files': File.objects.all()
        }
        return render(request, 'ChatBot/files.html', context=context)


@login_required
@csrf_exempt
def delete_file(request):
    if request.POST:
        file_name = request.POST['name']
        if File.objects.filter(user_id=request.user.id, name=file_name):
            file = File.objects.get(user_id=request.user.id, name=file_name)
            file.delete()
            template = render_to_string('ChatBot/_files.html', context={'files': File.objects.all()}, request=request)
            return JsonResponse({'message': 'File deleted successfully', 'status': 1,
                                 'template': template})
        else:
            return JsonResponse({'message': 'File Not Found.', 'status': 0}, content_type='application/json')


def rating(request):
    if request.POST:
        form = RatingForm(request.POST)
        if form.is_valid():
            if Rating.objects.filter(user_id=request.user.id):
                rating_obj = Rating.objects.get(user_id=request.user.id)
                rating_obj.rating = form.cleaned_data['rating']
                rating_obj.review = form.cleaned_data['review']
                rating_obj.save()
            else:
                Rating.objects.create(user_id=request.user.id, rating=form.cleaned_data['rating'],
                                      review=form.cleaned_data['review'])
            messages.success(request, "Rating & Review submitted successfully.")
            return HttpResponseRedirect('rating', {'ratings': Rating.objects.filter(user_id=request.user.id)})
        else:
            messages.error(request, form.errors)
            return render(request, 'ChatBot/rating.html',
                          context={'ratings': Rating.objects.filter(user_id=request.user.id)})
    else:
        return render(request, 'ChatBot/rating.html',
                      context={'ratings': Rating.objects.filter(user_id=request.user.id)})
