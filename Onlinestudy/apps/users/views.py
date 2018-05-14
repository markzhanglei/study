from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
import json
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from django.http import HttpResponse,HttpResponseRedirect

from pure_pagination import Paginator,PageNotAnInteger,EmptyPage

from .forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm,UploadImageForm,UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse,UserFavorite,UserMessage
from organization.models import CourseOrg,Teacher
from courses.models import Course
from .models import UserProfile,EmailVerifyRecord,Banner


#django自带的判断方法的使用
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


#登录业务逻辑
class LoginView(View):
    def get(self,request):
        return render(request,'login.html',{})
    def post(self,request):
        #使用表单做预判断
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username','')
            pass_word = request.POST.get('password','')
            #向数据库验证这个用户名和密码是否正确
            user = authenticate(username=user_name,password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    from django.core.urlresolvers import reverse
                    # return render(request,'index.html')
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request,'login.html',{'msg':'用户未激活！'})
            else:
                return render(request, 'login.html', {
                    'msg': '用户名或密码错误！',
                })
        else:
            return render(request, 'login.html', {
                'login_form':login_form,
            })


#退出登录
class LogoutView(View):
    def get(self,request):
        logout(request)
        # return render(request,'index.html')
        from django.core.urlresolvers import reverse
        #反向解析 用户登出
        return HttpResponseRedirect(reverse('index'))

#注册验证
class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request,'register.html',{
            'register_form':register_form,
        })
    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            #判断在数据库中是否已经注册存在，在数据库中查找
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {
                    'msg': '用户已经存在',
                    'register_form': register_form,
                })

            pass_word = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            #写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎注册慕学在线网'
            user_message.save()

            send_register_email(user_name,'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html',{
                'register_form': register_form,
            })


#注册之后的用户激活
class ActiveUserView(View):
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request,'active_fail.html')

        return render(request,'login.html')


class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email','')
            send_register_email(email,'forget')
            return render(request,'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request,'password_reset.html',{'email':email})
        else:
            return render(request, 'active_fail.html')

        return render(request, 'login.html')


class ModifyPwdView(View):
    #修改用户密码
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2','')
            email = request.POST.get('email','')
            if pwd1 != pwd2:
                return render(request,'password_reset.html',{'email':email,'msg':'两次密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email','')
            return render(request, 'password_reset.html', {'email': email, 'modify_form': 'modify_form'})


class UserInfoView(LoginRequiredMixin,View):
    #用户个人信息
    def get(self,request):
        return render(request,'usercenter-info.html',{
        })

    def post(self,request):
        user_info_form = UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            #返回错误的信息
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')




class UploadImageView(LoginRequiredMixin,View):
    #用户修改头像
    def post(self,request):
        image_form = UploadImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            # image = image_form.cleaned_data['image']
            # request.user.image = image
            # request.user.save()
            image_form.save()
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}',content_type='application/json')


class UpdatePwdView(LoginRequiredMixin,View):
    #修改用户密码
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2','')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin,View):
    #发送邮箱验证码
    def get(self,request):
        email = request.GET.get('email','')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')

        send_register_email(email,'update_email')

        return HttpResponse('{"status":"success"}', content_type='application/json')
    # def get(self, request):
    #     email = request.GET.get('email', '')
    #
    #     res = dict()
    #     if UserProfile.objects.filter(email=email):
    #         res['email'] = '邮箱已注册'
    #         return HttpResponse(json.dumps(res), content_type='application/json')
    #     send_register_email(email, 'update_email')
    #     res['status'] = 'success'
    #     res['msg'] = '发送验证码成功'
    #     return HttpResponse(json.dumps(res), content_type='application/json')


class UpdateEmailView(LoginRequiredMixin,View):
    #修改个人邮箱
    def post(self,request):
        email = request.POST.get('email','')
        code = request.POST.get('code', '')
#从数据库查询记录是否存在
        existed_records = EmailVerifyRecord.objects.filter(email=email,code=code,send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin,View):
    #我的课程
    def get(self,request):
        user_courses =UserCourse.objects.filter(user=request.user)
        return render(request,'usercenter-mycourse.html',{
            'user_courses':user_courses,

        })


class MyFavOrgView(LoginRequiredMixin,View):
    #我的收藏的课程机构
    def get(self,request):
        org_list = []
        fav_orgs =UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=int(org_id))
            org_list.append(org)
        return render(request,'usercenter-fav-org.html',{
            'org_list':org_list,
        })


class MyFavTeacherView(LoginRequiredMixin,View):
    #我的收藏的课程机构
    def get(self,request):
        teacher_list = []
        fav_teachers =UserFavorite.objects.filter(user=request.user,fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=int(teacher_id))
            teacher_list.append(teacher)
        return render(request,'usercenter-fav-teacher.html',{
            'teacher_list':teacher_list,
        })


class MyFavCourseView(LoginRequiredMixin,View):
    #我的收藏的课程机构
    def get(self,request):
        course_list = []
        fav_courses =UserFavorite.objects.filter(user=request.user,fav_type=1)
        print(fav_courses)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            try:
                course = Course.objects.get(id=int(course_id))
                course_list.append(course)
            except:
                pass
        return render(request,'usercenter-fav-course.html',{
            'course_list':course_list,
        })


class MyMessageView(View):
    #我的消息
    def get(self,request):
        #过滤获取用户所有的消息
        all_messages = UserMessage.objects.filter(user=request.user.id)
        #把未读的消息设置为已读
        #用户进入个人消息后清空未读消息的记录
        all_unread_messages = UserMessage.objects.filter(user=request.user.id,has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()
#个人消息分页
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages,1,request=request)
        messages = p.page(page)

        return render(request,'usercenter-message.html',{
            'all_messages':messages,
        })


class IndexView(View):
    def get(self,request):
        # print(1/0)  #500错误的测试代码
        #取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=False)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request,'index.html',{
            'all_banners':all_banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'course_orgs':course_orgs
        })

#
# class LoginUnsafeView(View):
#     def get(self,request):
#         return render(request,'login.html',{})
#
#     def post(self,request):
#         user_name = request.POST.get('username', '')
#         pass_word = request.POST.get('password', '')
#
#         import MySQLdb
#         conn = MySQLdb.connect(host='127.0.0.1',user='zl',passwd='123456',db='onlinestudy',charset='utf8')
#         cursor = conn.cursor()
#         sql_select = "select * from users_userprofile where email='{0}' and password='{1}'".format(user_name,pass_word)
#
#         result = cursor.execute(sql_select)
#         for row in cursor.fetchall():
#             #查询到用户   用户：' OR 1=1#  密码：任意输入
#             #会找到你的所有的用户，信息。
#             pass
#         print('1234')





#全局404配置函数
def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html',{})
    response.status_code = 404
    return response


#全局500配置函数
def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html',{})
    response.status_code = 500
    return response