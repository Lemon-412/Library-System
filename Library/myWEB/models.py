from django.db import models
# Create your models here.


class dzTable(models.Model):  # 读者信息
    dzid = models.AutoField(primary_key=True)  # 读者ID
    psw = models.CharField(max_length=256, default='passw0rd')  # 读者密码
    xm = models.CharField(max_length=10, blank=False)  # 姓名
    dh = models.CharField(max_length=20)
    email = models.CharField(max_length=50)


class tsglyTable(models.Model):  # 图书管理员信息
    gh = models.CharField(max_length=10, primary_key=True)  # 工号，格式：gh001
    psw = models.CharField(max_length=256, default='passw0rd')  # 管理员密码
    xm = models.CharField(max_length=10, blank=False)  # 姓名


class smTable(models.Model):  # 书目信息
    isbn = models.CharField(max_length=50, primary_key=True)  # ISBN号
    sm = models.CharField(max_length=50, blank=False)  # 书名
    zz = models.CharField(max_length=50)  # 作者
    cbs = models.CharField(max_length=50)  # 出版商
    cbny = models.DateTimeField()  # 出版年月
    cs = models.IntegerField()   # 册数
    jbr = models.ForeignKey(tsglyTable, on_delete=models.CASCADE)  # 经办人


class tsTable(models.Model):  # 图书信息
    tsid = models.CharField(max_length=20, primary_key=True)  # 图书id
    isbn = models.ForeignKey(smTable, on_delete=models.CASCADE)  # ISBN号
    cfwz = models.CharField(max_length=20)  # 存放位置
    zt = models.CharField(max_length=20, blank=False)  # 状态
    jbr = models.ForeignKey(tsglyTable, on_delete=models.CASCADE)  # 经办人


class jsTable(models.Model):  # 借书信息
    dzid = models.ForeignKey(dzTable, on_delete=models.CASCADE)  # 读者ID
    tsid = models.ForeignKey(tsTable, on_delete=models.CASCADE)  # 图书ID
    jysj = models.DateTimeField()  # 借阅时间
    yhsj = models.DateTimeField()  # 应还时间
    ghsj = models.DateTimeField()  # 归还时间

    class Meta:
        unique_together = ("dzid", "tsid")


class yyTable(models.Model):  # 预约信息
    dzid = models.ForeignKey(dzTable, on_delete=models.CASCADE)  # 读者ID
    isbn = models.ForeignKey(smTable, on_delete=models.CASCADE)  # ISBN号
    yysj = models.DateTimeField()

    class Meta:
        unique_together = ("dzid", "isbn")
