from django import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib.auth.models import User
from mainapp.models import Media, Food, Dish, CookInfo, Order
from mainapp.models import Session
import json


def generateprofilepic(email):
    import hashlib
    m = hashlib.md5()
    m.update(email.encode("utf-8"))
    return m.hexdigest()

# Create your views here.
def login(request):
    return render(request, 'mainapp/login.html')


def signup(request):
    return render(request,'mainapp/signup.html',{'form':form})

def index(request):
    if(request.method== 'GET'):
        return render(request,'mainapp/index.html')

def home(request):
    if(request.method=='GET'):
        if(not(request.user.is_authenticated())):
            return redirect('login')
        else:
            cook=CookInfo.objects.filter(cook_id=request.user.id)[0]
            if(cook):
                return render(request,'mainapp/home.html',{'cook':cook})
    else:
        data=request.POST
        cook=CookInfo.objects.filter(cook_id=data['cookid'])[0]
        if(cook):
            cook.status=data['status']
            cook.save()
            return redirect('home')

def dishes(request):
    if(request.method=='GET'):
        if(not(request.user.is_authenticated())):
            return redirect('login')
        else:
            dishes=Dish.objects.filter(cook_id=request.user.id)
            return render(request,'mainapp/dishes.html',{'dishes':dishes})
    else:
        # Dishes list to enable
        str_dishes_list=request.POST.getlist('dishes')
        int_dishes_list=[]
        for items in str_dishes_list:
            int_dishes_list.append(int(items))

        # Cook dishes list
        dishes=Dish.objects.filter(cook_id=request.user.id)

        for dish in dishes:
            if dish.id in int_dishes_list:
                dish.enabled=True
            else:
                dish.enabled=False
            dish.save()

        return redirect('dishes')

def orders(request):
    orders=Order.objects.filter(dish__cook_id=request.user.id)
    return render(request,'mainapp/orders.html',{'orders':orders})

def order(request):
    if(request.method=='POST'):
            submitButton=request.POST['submitButton']
            return HttpResponse(submitButton)

def logout(request):
    auth.logout(request)
    return redirect('index')

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
        if Dish.objects.filter(cook=cookinfo.cook, enabled=True).count() == 0:
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


def logincheck(request):

    username = request.GET.get("user",False)
    password = request.GET.get("pass",False)
    if username is False:
        raise Http404

    if password is False:
        raise Http404

    user = authenticate(username=username, password=password)
    found = True
    if user is None:
        if User.objects.filter(email=username).count() == 0:
            found = False
        else:
            user = User.objects.get(email=username)
            if not user.check_password(password):
                found = False
    if not found:
        output = {"login": "no"}
        return HttpResponse(json.dumps(output))
    # Create some session ID for the user
    session, created = Session.objects.get_or_create(user=user)
    session.generateRandom()

    output = {
        "login": "yes",
        "name": user.first_name+" "+user.last_name,
        "email": user.email,
        "username": user.username,
        "tag": session.sessionid,
        "profile_picture": generateprofilepic(user.email)
        }
    return HttpResponse(json.dumps(output))

def sessioncheck(request):
    sessionid = request.GET.get("tag", False)
    if sessionid is False:
        raise Http404
    try:
        session = Session.objects.get(sessionid=sessionid)
    except:
        output = {"login": "no"}
        return HttpResponse(json.dumps(output))

    user = session.user
    output = {
        "login": "yes",
        "name": user.first_name+" "+user.last_name,
        "email": user.email,
        "username": user.username,
        "tag": session.sessionid,
        "profile_picture": generateprofilepic(user.email)
        }
    return HttpResponse(json.dumps(output))


def makeorder(request):
    sessionid = request.GET.get("tag", False)
    if sessionid is False:
        raise Http404

    try:
        session = Session.objects.get(sessionid=sessionid)
    except:
        raise Http404

    user = session.user

    # Now try to get the food and cook ID
    try:
        cookid = request.GET.get("cookid")
        cook = User.objects.get(pk=cookid)
        cookinfo = CookInfo.objects.get(cook=cook)
        if cookinfo.status == CookInfo.BUSY:
            return HttpResponse("BUSYCOOK")
    except:
        return HttpResponse("NOCOOK")
    try:
        foodid = request.GET.get("foodid")
        food = Food.objects.get(pk=foodid)
    except:
        return HttpResponse("NOFOOD")

    quantity = request.GET.get("quantity",1)
    quantity = int(quantity)

    # Try to find dish of that cook and food
    try:
        dish = Dish.objects.get(cook=cook, food=food)
    except:
        return HttpResponse("NODISH")
    #Create a order for it
    try:
        from datetime import datetime, timedelta
        message_interval = timedelta(seconds=60)
        # find older order with similar specifications
        if Order.objects.filter(customer=user, dish=dish, quantity=quantity,order_placed__gte = datetime.now() - message_interval).count() > 0:
            return HttpResponse("DELAY")
        neworder = Order(customer=user, dish=dish, quantity=quantity)
        neworder.save()
    except:
        return HttpResponse("ORDERROR")
    return HttpResponse("YES")



def browseorder(request):
    # I have used the following lines of code 3 times in this view.
    # Maybe i should create a function instead of writing this comment
    # On second thought, Nah...

    from datetime import datetime, timedelta
    from django.utils import timezone
    from django.utils.timesince import timesince

    sessionid = request.GET.get("tag", False)
    if sessionid is False:
        raise Http404
    try:
        session = Session.objects.get(sessionid=sessionid)
    except:
        raise Http404  # Show error in case of error

    user = session.user

    # Search for orders of this user
    orders = Order.objects.filter(customer=user)
    output = []
    for order in orders:
        orderinfo = {}
        cook = order.dish.cook
        orderinfo["cook"] = cook.first_name+" "+cook.last_name
        orderinfo["food"] = order.dish.food.name
        orderinfo["status"] = order.get_status_display()

        now = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
        difference = now - order.order_placed
        if difference <= timedelta(minutes=1):
            orderinfo["ordered"] = 'just now'
        else:
            orderinfo["ordered"] = '%(time)s ago' % {'time': timesince(order.order_placed).split(', ')[0]}
            orderinfo["ordered"] = orderinfo["ordered"].replace("\u00a0"," ")
        output.append(orderinfo)
    return HttpResponse(json.dumps(output))
