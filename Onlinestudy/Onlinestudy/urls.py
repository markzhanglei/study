"""Onlinestudy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.views.static import serve
import xadmin
from django.views.generic import TemplateView
from users.views import LoginView,LogoutView,RegisterView,ActiveUserView,ForgetPwdView,ResetView,ModifyPwdView

from Onlinestudy.settings import MEDIA_ROOT
from users.views import IndexView

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    #验证码
    url(r'^captcha/',include('captcha.urls')),
    #media的配置，配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$',serve,{'document_root':MEDIA_ROOT}),
    #静态文件的路径问题
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),

    url(r'^$',IndexView.as_view(),name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),

    # url(r'^login/$', LoginUnsafeView.as_view(), name='login'),

    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^active/(?P<active_code>.*)/$',ActiveUserView.as_view(),name='user_active'),
    url(r'^forget/$',ForgetPwdView.as_view(),name='forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),
#课程机构url的配置
    url(r'^org/',include('organization.urls',namespace='org')),
#课程相关配置
    url(r'^course/', include('courses.urls', namespace='course')),

    url(r'^users/', include('users.urls', namespace='users')),

    #富文本相关url
    url(r'^ueditor/',include('DjangoUeditor.urls' )),

]

#全局404页面设置
handler404 = 'users.views.page_not_found'

#全局500页面设置
handler500 = 'users.views.page_error'