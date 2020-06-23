from django.http import JsonResponse
from django.shortcuts import render

from django.views import View

from apps.organizations.forms import AddAskForm
from apps.organizations.models import CourseOrg, City

from pure_pagination import Paginator, PageNotAnInteger


class OrgTeacherView(View):
    """
    机构老师
    """

    def get(self, request, org_id, *args, **kwargs):
        current_page = "teacher"
        course_org = CourseOrg.objects.filter(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        all_teacher = course_org.teacher_set.all()

        return render(request, "org-detail-teachers.html", {
            "all_teacher": all_teacher,
            "course_org": course_org,
            "current_page": current_page
        })


class OrgHomeView(View):
    """
    机构
    """

    def get(self, request, org_id, *args, **kwargs):
        current_page = "home"
        course_org = CourseOrg.objects.filter(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        all_courses = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()[:1]

        return render(request, "org-detail-homepage.html", {
            "all_courses": all_courses,
            "all_teacher": all_teacher,
            "course_org": course_org,
            "current_page": current_page
        })


class AddAskView(View):
    """
    处理用户咨询
    """

    def post(self, request, *args, **kwargs):
        userask_form = AddAskForm(request.POST)
        if userask_form.is_valid():
            # 保存到数据库，save为form自带方法
            userask_form.save(commit=True)
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "添加出错"
            })


class OrgView(View):
    """
    机构
    """

    def get(self, request, *args, **kwargs):
        # 从数据库中获取数据
        all_orgs = CourseOrg.objects.all()
        all_citys = City.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        # 通过机构类别对课程机构进行筛选
        category = request.GET.get("ct", "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 通过所在城市对课程机构进行筛选
        city_id = request.GET.get("city", "")
        if city_id:
            if city_id.isdigit():
                all_orgs = all_orgs.filter(city_id=int(city_id))

        # 对机构进行排序
        sort = request.GET.get("sort", "")
        if sort == "students":
            all_orgs = all_orgs.order_by("-students")

        elif sort == "courses":
            all_orgs = all_orgs.order_by("-course_nums")

        org_nums = all_orgs.count()

        # 对课程机构数据进行分页
        try:
            page = request.GET.get('page', 10)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, per_page=5, request=request)
        orgs = p.page(page)
        return render(request, "org-list.html",
                      {"all_orgs": orgs,
                       "org_nums": org_nums,
                       "all_citys": all_citys,
                       "category": category,
                       "city_id": city_id,
                       "sort": sort,
                       "hot_orgs": hot_orgs
                       })
