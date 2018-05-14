__author__ = 'zhang'
__date__ = '2018/5/3 18:05'

from .models import EmailVerifyRecord,Banner
import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin
from .models import UserProfile


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = '慕学后台管理系统'
    site_footer = '慕学在线网'
    menu_style = 'accordion'


class EmailVerifyRecordAdmin(object):
    list_display = ['code','email','send_type','send_time']
    search_fields = ['code','email','send_type']
    list_filter = ['code','email','send_type','send_time']
    model_icon = 'fa fa-envelope-open'


class BannerAdmin(object):
#不能对时间进行search
    list_display = ['title','url','index','add_time','image']
    search_fields = ['title','url','index','image']
    list_filter = ['title','url','index','add_time','image']

    model_icon = 'fa fa-angle-double-right'


xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
#主题的注册
xadmin.site.register(views.BaseAdminView,BaseSetting)
#后台的左上角的文字和正下的中间的位置的文字
xadmin.site.register(views.CommAdminView,GlobalSettings)