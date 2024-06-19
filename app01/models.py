from django.db import models

# Create your models here.

class Academy(models.Model):
    academyname = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'academy'
        db_table_comment = '学院表'


class Course(models.Model):
    coursename = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'course'
        db_table_comment = '学生课程表'


class CourseAcademy(models.Model):
    academyid = models.ForeignKey(Academy, models.DO_NOTHING, db_column='academyid')
    courseid = models.ForeignKey(Course, models.DO_NOTHING, db_column='courseid')

    class Meta:
        managed = True
        db_table = 'course_academy'
        db_table_comment = '连接学院表和课程表'


class StuCours(models.Model):
    studentid = models.IntegerField()
    courseid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stu_cours'
        db_table_comment = '连接学生表和课程表'


class Student(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True, db_comment='学生学号')  # Field name made lowercase.
    name = models.CharField(unique=True, max_length=5)
    gender = models.CharField(max_length=1, db_comment='性别')
    academyid = models.IntegerField(blank=True, null=True, db_comment='所属学院,与学院表的id建立连接')
    entrydate = models.DateField(db_comment='入学日期')
    password = models.CharField(db_comment='登陆密码', max_length=8)

    class Meta:
        managed = True
        db_table = 'student'
        db_table_comment = '学生表'