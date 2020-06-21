from django.db import models

from apps.users.models import BaseModel


class City(BaseModel):
    name = models.CharField(max_length=20, verbose_name="城市")
    desc = models.CharField(max_length=200, verbose_name="描述")

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name


class CourseOrg(BaseModel):
    name = models.CharField(verbose_name="机构名称", max_length=50)
    desc = models.TextField(verbose_name="描述")
    tag = models.CharField(verbose_name="机构标签", max_length=10, default="全国知名")
    category = models.CharField(default="pxjg", verbose_name="机构类别", choices=(("pxjg", "培训机构"),
                                                                              ("gr", "个人"), ("gx", "高校")),
                                max_length=4)
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name="logo", max_length=100)
    students = models.IntegerField(default=0, verbose_name="学习人数")
    address = models.CharField(verbose_name="机构地址", max_length=150)
    course_nums = models.IntegerField(default=0, verbose_name="课程数")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="所在城市")

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name


class Teacher(BaseModel):
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="所属机构")
    name = models.CharField(max_length=50, verbose_name="教师名")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=50, verbose_name="就职公司")
    work_position = models.CharField(max_length=50, verbose_name="公司职位")
    points = models.CharField(max_length=50, verbose_name="教学特点")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    age = models.IntegerField(default=18, verbose_name="年龄")
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name="头像", max_length=100)

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name
