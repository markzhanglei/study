__author__ = 'zhang'
__date__ = '2018/5/3 18:54'

from .models import CityDict,CourseOrg,Teacher
import xadmin


class CityDictAdmin(object):
    #不能查找时间相关的信息
    list_display = ['name','desc','add_time']
    search_fields = ['name','desc']
    list_filter = ['name','desc','add_time']
    model_icon = 'fa fa-address-book'


class CourseOrgAdmin(object):
    list_display = ['name','desc','click_nums','fav_nums','image','address','city','add_time']
    search_fields = ['name','desc','click_nums','fav_nums','image','address','city']
    list_filter = ['name','desc','click_nums','fav_nums','image','address','city','add_time']
#以ajax加载来用
    relfield_style = 'fk-ajax'


class TeacherAdmin(object):
    list_display = ['org','name','work_years','work_company','work_position','points','click_nums','fav_nums','add_time']
    search_fields =  ['org','name','work_years','work_company','work_position','points','click_nums','fav_nums']
    list_filter =  ['org','name','work_years','work_company','work_position','points','click_nums','fav_nums','add_time']

xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)

