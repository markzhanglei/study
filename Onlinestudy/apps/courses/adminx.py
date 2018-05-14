__author__ = 'zhang'
__date__ = '2018/5/3 18:44'

from .models import Course,Lesson,Video,CourseResource,BannerCourse
import xadmin
from organization.models import CourseOrg


#可以在课程里面直接添加章节的信息
class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    #不能查找时间相关的信息
    list_display = ['name','desc','detail','degree','learn_times','students','fav_nums','click_nums','get_zj_nums','go_to']
    search_fields = ['name','desc','detail','degree','students','fav_nums','click_nums']
    list_filter = ['name','desc','detail','degree','learn_times','students','fav_nums','click_nums']
    #在列表页可以直接对它进行编辑
    list_editable = ['degree','desc']
    #更改图标
    model_icon = 'fa fa-handshake-o'
    #按照给的字段排序
    ordering = ['-click_nums']
    #字段设置为只读
    readonly_fields = ['click_nums']
    #隐藏这个字段。排除这个字段
    exclude = ['fav_nums']
    #把章节信息放进来，可以收起来  只能嵌套一层，不能嵌套两层。  但是可以放多个的信息。
    inlines = [LessonInline,CourseResourceInline]

    style_fields = {'detail':'ueditor'}
#导入文件
    import_excel = True
    #在页面的生成刷新的图标，可以选择刷新的方式
    refresh_times = [3,5]

    def queryset(self):
        qs = super(CourseAdmin,self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        #在保存课程的时候统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    def post(self,request,*args,**kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin,self).post(request,*args,**kwargs)


class BannerCourseAdmin(object):
    #不能查找时间相关的信息
    list_display = ['name','desc','detail','degree','learn_times','students','fav_nums','click_nums']
    search_fields = ['name','desc','detail','degree','students','fav_nums','click_nums']
    list_filter = ['name','desc','detail','degree','learn_times','students','fav_nums','click_nums']
    #更改图标
    model_icon = 'fa fa-handshake-o'
    #按照给的字段排序
    ordering = ['-click_nums']
    #字段设置为只读
    readonly_fields = ['click_nums']
    #隐藏这个字段。排除这个字段
    exclude = ['fav_nums']
    #把章节信息放进来，可以收起来  只能嵌套一层，不能嵌套两层。  但是可以放多个的信息。
    inlines = [LessonInline,CourseResourceInline]

    def queryset(self):
        qs = super(BannerCourseAdmin,self).queryset()
        qs = qs.filter(is_banner=True)
        return qs




class LessonAdmin(object):
    #不能查找时间相关的信息
    list_display = ['course','name','add_time']
    search_fields = ['course','name']
    list_filter = ['course__name','name','add_time']


class VideoAdmin(object):
    #不能查找时间相关的信息
    list_display = ['lesson','name','add_time']
    search_fields = ['lesson','name']
    list_filter = ['lesson__name','name','add_time']


class CourseResourceAdmin(object):
    #不能查找时间相关的信息
    list_display = ['course','name','download','add_time']
    search_fields = ['course','name','download']
    list_filter = ['course','name','download','add_time']


xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(BannerCourse,BannerCourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)
