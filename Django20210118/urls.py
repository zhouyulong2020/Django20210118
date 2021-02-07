"""Django20210118 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url,include
from django.contrib import admin

from sign import views          #导入app sign应用views文件


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.index),            #访问其它不存在地址都从登录界面进
    url(r'^index/$', views.index),      #添加index/路径配置
    url(r'^accounts/login/$', views.index),

    url(r'^login_action/$', views.login_action),  # 添加login_action路径配置
    url(r'^event_manage/$', views.event_manage),  # 添加event_manage路径配置

    url(r'^search_name/$', views.search_name),  # 添加event_manage搜索

    url(r'^guest_manage/$', views.guest_manage),  # 添加guest_manage路径配置
    url(r'^sign_index/(?P<eid>[0-9]+)/$', views.sign_index),  # 添加签到路径配置
    url(r'^sign_index_action/(?P<eid>[0-9]+)/$',views.sign_index_action),       #签到动作

    url(r'^logout/$', views.logout),  # 退出系统

    # url(r'^api/', include('sign.urls',namespace = 'sign')),  # 在APP下创建urls.py文件来配置具体接口的二级目录,django1.0版本写法
    url('^api/', include(('sign.urls','sign'),namespace = 'sign')),

]
