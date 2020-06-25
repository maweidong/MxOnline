from django.conf.urls import url

from apps.users.views import UserInfoView, ChangeMobileView

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name="list"),
    url(r'^image/upload/$', UserInfoView.as_view(), name="image"),
    url(r'^update/mobile/$', ChangeMobileView.as_view(), name="update_mobile"),

]
