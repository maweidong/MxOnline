from django.conf.urls import url

from apps.users.views import UserInfoView

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name="list"),
    url(r'^image/upload/$', UserInfoView.as_view(), name="image"),

]
