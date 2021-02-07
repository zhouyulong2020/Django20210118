from django.shortcuts import render

# 控制向前端页面显示的内容
# Create your views here.

# HttpResponse 响应HTTP请求
# HttpResponseRedirect 对HTTP响应的路径进行重定向
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth     #调用Django自带的后台用户管理系统
from django.contrib.auth.decorators import login_required   #关上窗户
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger  #分页
from django.shortcuts import get_object_or_404

from sign.models import Event,Guest

# def index(request):
#     return HttpResponse("hello django")

def index(request):
    return render(request,"index.html")

#登录动作
def login_action(request):
    if request.method == "POST":
        username = request.POST.get('username',"")
        password = request.POST.get('password',"")
        # 使用django提供的authenticate()函数认证给出的用户名与密码，存在返回一个user对象，否则返回None
        user = auth.authenticate(username = username,password = password)
        # 判断authenticate()返回对象，如果不为None,则说明认证通过，调用login()函数进行登录，参数为HttpRequest对象和一个USER对象。
        if user is not None:
            auth.login(request,user)    #登录
        # if username == 'admin' and password == 'admin123':
            # return HttpResponse('login success!')
            # return HttpResponseRedirect('/event_manage/')
            response = HttpResponseRedirect('/event_manage/')
            '''
            cookie是由浏览器按照一定的规则在后台自动发送给服务器，浏览器检查所有存储的cookie，如果某个cookie所
            申明的作用范围大于等于将要请求的资源所在的位置，则把该cookie附在请求资源的HTTP请求头上发送给服务器。
            cookie固然好，但存在一定的安全隐患（相当于存折，用户信息记录在上面），session相对安全很多（相当于银行卡，用户只有ID，数据记录在服务器）。
            '''
            #response.set_cookie('user',username,3600)   #添加浏览器cookie:cookie名，参数名称，cookie保持时间
            request.session['user'] = username      #将session信息记录于浏览器
            return response
        else:
            return render(request,'index.html',{'error':'username or password error!'})

#发布会管理
# 如果想限制某个视图函数必须登录才能访问，则只需要在这个函数的前面加上@login_required的装饰即可。
@login_required
def event_manage(request):
    # username  = request.COOKIES.get('user','')  #读取浏览器cookie
    event_list = Event.objects.all()
    username = request.session.get('user','')   #读取浏览器session
    return render(request,"event_manage.html",{"user1":username,'events':event_list})

#发布会搜索
@login_required
def search_name(request):
    username = request.session.get('user','')
    search_name = request.GET.get('name','')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request,"event_manage.html",{"user":username,"events":event_list})

#嘉宾管理
@login_required
def guest_manage(request):
    username = request.session.get('user','')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list,2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)    #如果page不是整数，取第一页面数据
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)      #如果page不在范围，取最后一个页面

    return render(request,"guset_manage.html",{'user':username,"guests":contacts})

#签到页面
@login_required
def sign_index(request,eid):
    event = get_object_or_404(Event,id=eid)         #如果查询对象不存在，则会抛出一个HTTP404异常。就可以省去table.objects.get()方法的异常断言。
    return render(request,'sign_index.html',{'event':event})

#签到动作
@login_required
def sign_index_action(request,eid):
    event = get_object_or_404(Event,id=eid)
    phone = request.POST.get('phone','')
    print(phone)
    result = Guest.objects.filter(phone=phone)
    if not result:
         return render(request,'sign_index.html',{'event':event,'hint':'phone error.'})
    result = Guest.objects.filter(phone=phone,event_id=eid)
    if not result:
            return render(request, 'sign_index.html', {'event': event, 'hint': 'event id or phone error.'})
    result = Guest.objects.get(phone=phone,event_id=eid)
    if result.sign:
        return render(request,'sign_index.html',{'event':event,'hint':'user has sign in.'})
    else:
        Guest.objects.filter(phone=phone,event_id=eid).update(sign='1')
        return render(request,'sign_index.html',{'event':event,'hint':'sign in success!','guest':result})


# 退出登录
@login_required
def logout(request):
    auth.logout(request) #退出登录
    response = HttpResponseRedirect('/index/')
    return response