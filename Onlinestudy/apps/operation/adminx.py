__author__ = 'zhang'
__date__ = '2018/5/3 19:09'

from .models import UserAsk,CourseComments,UserFavorite,UserMessage,UserCourse

import xadmin


class UserAskAdmin(object):
    #不能查找时间相关的信息
    list_display = ['name','mobile','course_name','add_time']
    search_fields = ['name','mobile','course_name']
    list_filter = ['name','mobile','course_name','add_time']
    model_icon = 'fa fa-binoculars'


class CourseCommentsAdmin(object):
    #不能查找时间相关的信息
    list_display = ['user','course','comments','add_time']
    search_fields = ['user','course','comments']
    list_filter = ['user','course','comments','add_time']

class UserFavoriteAdmin(object):
    #不能查找时间相关的信息
    list_display = ['user','fav_id','fav_type','add_time']
    search_fields = ['user','fav_id','fav_type']
    list_filter = ['user','fav_id','fav_type','add_time']


class UserMessageAdmin(object):
    #不能查找时间相关的信息
    list_display = ['user','message','has_read','add_time']
    search_fields = ['user','message','has_read']
    list_filter = ['user','message','has_read','add_time']


class UserCourseAdmin(object):
    #不能查找时间相关的信息
    list_display = ['user','course','add_time']
    search_fields = ['user','course']
    list_filter = ['user','course','add_time']

xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
