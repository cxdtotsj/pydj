from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


# Create your views here.

def index(request):
    return render(request,"index.html")

# 登陆操作
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user) # 登陆
            request.session['user'] = username # 将 session 记录到浏览器
            response = HttpResponseRedirect('/event_manage/')
            # response.set_cookie('user',username,3600) # 添加浏览器 cookie
            return response
            
        else:
            return render(request,'index.html',{'error':'username or password error'})
    else:
        return HttpResponse("Method Not Allowed")

# 发布会管理
@login_required
def event_manage(request):
    # username = request.COOKIES.get('user','') # 读取浏览器 cookie

    event_list = Event.objects.all()
    username = request.session.get('user','') # 读取浏览器 session
    return render(request,"event_manage.html",{"user":username,"events":event_list})

# 发布会名称搜索
@login_required
def eventName_search(request):
    username = request.session.get('user','')
    search_name = request.GET.get('name','')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request,"event_manage.html",{"user":username,"events":event_list})

# 嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user','') # 读取浏览器 session
    guest_list = Guest.objects.all()
    page_guest = Paginator(guest_list,2)
    page = request.GET.get('page')
    try:
        contacts = page_guest.page(page)
    except PageNotAnInteger:
        contacts = page_guest.page(1)
    except EmptyPage:
        contacts = page_guest.page(Paginator.num_pages)
    return render(request,"guest_manage.html",{"user":username,"guests":contacts})

# 嘉宾名称、手机搜索
@login_required
def guestRP_search(request):
    username = request.session.get('user','')
    search_name = request.GET.get('name','')
    search_phone = request.GET.get('phone','')
    guest_list = Guest.objects.filter(realname__contains=search_name).filter(phone__contains=search_phone)
    return render(request,"guest_manage.html",{"user":username,"guests":guest_list})

# 签到页面
@login_required
def sign_index(request,event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request,'sign_index.html',{'event':event})

# 签到动作
@login_required
def sign_index_action(request,event_id):
    event = get_object_or_404(Event,id=event_id)
    phone = request.POST.get('phone','')

    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html',{'event':event,'hint':'phone error.'})
    result = Guest.objects.filter(phone=phone,event_id=event_id)
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':'event_id or phone error.'})
    result = Guest.objects.get(phone=phone,event_id=event_id)
    if result.sign:
        return render(request,'sign_index.html',{'event':event,'hint':"user has sign in."})
    else:
        Guest.objects.filter(phone=phone,event_id=event_id).update(sign='1')
        return render(request,'sign_index.html',{'event':event,'hint':'sign in success!','guest':result})

# 退出登录
@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response