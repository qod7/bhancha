from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib import auth

from django.contrib.auth.models import User
from mainapp.models import Media, Food, Dish, CookInfo, Order

# Create your views here.
class LoginForm(forms.Form):
    username=forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(max_length=30,widget=forms.PasswordInput(attrs={'class':'form-control'}))

def login(request):
    if(request.method== 'POST'):
        form=LoginForm(request.POST)
        if(form.is_valid()):
            user=auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    auth.login(request,user)
                    return redirect('mainapp:home')
                else:
                    # Disabled account
                    pass
            else:
                new_form=LoginForm()
                return render(request, 'mainapp/login.html',{'form':form,'message':'Wrong Username or password'})
    else:
        form=LoginForm()
        return render(request, 'mainapp/login.html',{'form':form})

class SignupForm(forms.ModelForm):
    class Meta:
        model= auth.models.User
        fields= ['username','email','first_name','last_name','password']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'password': forms.PasswordInput(attrs={'class':'form-control'}),
        }

    repassword=forms.CharField(max_length=30,widget=forms.PasswordInput(attrs={'class':'form-control'}))

def signup(request):
    if (request.method== 'POST'):
        form=SignupForm(request.POST)
        if (form.is_valid()):
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            repassword=form.cleaned_data['repassword']
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']

            if(password!=repassword):
                return render(request,'mainapp/signup.html',{'form':form})

            user = auth.models.User.objects.create_user(username, email, password)
            user.first_name=first_name
            user.last_name=last_name
            user.save()

            new_form=SignupForm()
            user=auth.authenticate(username=username, password=password)
            return redirect('mainapp:home')

        else:
            return render(request,'mainapp/signup.html',{'form':form,'message':'Invalid form'})
    form=SignupForm()
    return render(request,'mainapp/signup.html',{'form':form})

def index(request):
    if(request.method== 'GET'):
        return render(request,'mainapp/index.html')

def home(request):
        if(request.method=='GET'):
                # Getting the orders for the cook which are ordered
                orders=Order.objects.filter(dish__cook_id=request.user.id,status='ORD')
                if(orders):
                        # Only a single order is show at a time
                        order=orders[0]
                        return render(request,'mainapp/home.html',{'order':order})
                else:
                        return render(request,'mainapp/home.html')

def order(request):
        if(request.method=='POST'):
                submitButton=request.POST['submitButton']
                return HttpResponse(submitButton)

def logout(request):
    auth.logout(request)
    return redirect('mainapp:index')

def browsefood(request):
    import json
    import hashlib

    #get all the food items
    food = Food.objects.all()
    output = []
    for fooditem in food:
        if Dish.objects.filter(food=fooditem, enabled=True).count() == 0:
            continue
        item = {}
        item['id'] = fooditem.pk
        item['name'] = fooditem.name
        item['image_id'] = 'http://bhancha.com/media/'+fooditem.image.image.name
        item['cooks']=[]
        # find all the cooks for the food
        dishes = Dish.objects.filter(food=fooditem, enabled=True)
        for dish in dishes:
            cook = {}
            cook['id'] = dish.cook.pk
            cook['name'] = dish.cook.first_name+" "+dish.cook.last_name
            cook['rating'] = 3.5

            m = hashlib.md5()
            m.update(dish.cook.email.encode("utf-8"))

            cook['image_id'] = m.hexdigest()
            item['cooks'].append(cook)
        output.append(item)
    return HttpResponse(json.dumps(output))


def browsecook(request):
    import json
    import hashlib

    '''
    Browse by cook
    '''
    # get the cook list by cookinfo as not all users are cooks
    cookinfos = CookInfo.objects.filter(status=CookInfo.FREE)
    output = []
    for cookinfo in cookinfos:
        if Dish.objects.filter(cook=cook, enabled=True).count() == 0:
            continue
        cook = cookinfo.cook
        item = {}
        item['id'] = cook.pk
        item['name'] = cook.first_name+" "+cook.last_name
        m = hashlib.md5()
        m.update(cook.email.encode("utf-8"))

        item['image_id'] = m.hexdigest()

        #get the items cooked by the cook
        dishes = Dish.objects.filter(cook=cook, enabled=True)
        item['foods'] = []
        for dish in dishes:
            food = {}
            food['id'] = dish.food.pk
            food['name'] = dish.food.name
            food['image_id'] = 'http://bhancha.com/media/'+dish.food.image.image.name
            item['foods'].append(food)
        output.append(item)
    return HttpResponse(json.dumps(output))

def browseorder(request):
    import json
    import hashlib

    output = []
    #first of all, try to validate the user
    try:
        username = request.GET.get("user")
        password = request.GET.get("password")
    except:
        return HttpResponse("Permission denied")
    return HttpResponse(json.dumps(output))
