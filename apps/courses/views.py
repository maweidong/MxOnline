from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.courses.models import Course


class CourseListView(View):
    def get(self, request, *args, **kwargs):
        """获取课程列表信息"""
        all_courses = Course.objects.order_by("-add_time")
        return render(request, "course-list.html", {
            "all_courses": all_courses
        })
