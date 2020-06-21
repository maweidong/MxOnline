from datetime import datetime

from django.db import models

from apps.users.models import BaseModel

# 1、设计表结构
"""
课程、章节、视频、课程资源
"""


# 2、实体的具体字段

# 3、每个字段的类型是否必填

class Course(BaseModel):
    name = models.CharField(verbose_name="课程名", max_length=50)
    desc = models.CharField(verbose_name="课程描述", max_length=300)
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    degree = models.CharField(verbose_name="难度", choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), max_length=2)
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    category = models.CharField(verbose_name="课程类别", max_length=20, default="后端开发")
    tag = models.CharField(verbose_name="课程标签", max_length=10, default="")
    youneed_know = models.CharField(verbose_name="课程须知", max_length=300, default="")
    teacher_tell = models.CharField(verbose_name="老师告诉你", max_length=300, default="")

    detail = models.TextField(verbose_name="课程详情")
    image = models.IntegerField(upload_to="courses/%Y/%m", verbose_name="封面图", max_length=100)

    class Meta:
        verbose_name = "课程信息"
        verbose_name_plural = verbose_name


class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # 级联删除
    name = models.CharField(max_length=100, verbose_name="章节名")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")

    class Meta:
        verbose_name = "课程章节"
        verbose_name_plural = verbose_name


class Video(BaseModel):
    lesson = models.ForeignKey(Lesson, verbose_name="章节", on_delete=models.CASCADE)  # 级联删除
    name = models.CharField(max_length=100, verbose_name="视频名")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    url = models.CharField(max_length=200, verbose_name="访问地址")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name


class CourseResource(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")  # 级联删除
    name = models.CharField(max_length=100, verbose_name="名称")
    file = models.FileField(upload_to="course/resourse/%Y/%m", verbose_name="下载地址", max_length=200)

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name
