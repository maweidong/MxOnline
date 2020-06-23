from django.conf.urls import url
from captcha import views
from django.urls import path

from apps.organizations.views import OrgView, AddAskView, OrgHomeView, OrgTeacherView

urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name="org_list"),
    url(r'^add_ask/$', AddAskView.as_view(), name="add_ask"),
    url(r'^(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="home"),
    # path('<int:org_id>/', OrgHomeView.as_view(), name="home")
    url(r'^(?P<org_id>\d+)/teacher/$', OrgTeacherView.as_view(), name="teacher"),

]
