from django.db import models

# Create your models here.
# 创建一个实体类DevGroup（自动生成一张数据表 app01_devgroup）
class DevGroup(models.Model):
    # 定义该类的成员属性
    # 属性与表的字段一一对应
    # gid是对应的数据表的主键并且需要自增长
    gid = models.AutoField(primary_key=True)
    # gname是小组名称字符串类型(初始化必须携带一个参数max_length)
    gname = models.CharField(max_length=30)

    # 重写__str__方法 (Python2 __unicode__)
    def __str__(self):
        return self.gname
    pass

# 创建一个实体类Developer（存在一个外键DevGroup）
class Developer(models.Model):
    # did 开发者编号
    did = models.AutoField(primary_key=True)
    # dname 开发者的姓名
    dname = models.CharField(max_length=30)
    # dhiredate 入职时间
    dhiredate = models.DateField()
    # demail 电子邮箱
    demail = models.EmailField(max_length=50)
    # dsal 薪资
    dsal = models.FloatField()
    # # 注意：devgroup 开发者所在的小组(外键)
    # devgroup = models.ForeignKey(DevGroup,on_delete=models.CASCADE)
    pass

#博客的注册表
class Register(models.Model):
    # did 开发者编号
    did = models.AutoField(primary_key=True)
    # dname 开发者的姓名
    dname = models.CharField(max_length=30)
    # dhiredate 入职时间
    dkey = models.CharField(max_length=30)
    # demail 电子邮箱
    demail = models.EmailField(max_length=50)
    # dQrCode 学生二维码
    dQrCode = models.CharField(max_length = 200, default = "")
    # daccessable 学生卡的可用性
    daccessable = models.IntegerField(default = 1)
    # borrowTimes 学生借阅次数
    borrowTimes = models.IntegerField(default = 0)
    # fee 学生欠款金额
    fee = models.IntegerField(default = 0)
    # # 注意：devgroup 开发者所在的小组(外键)
    # devgroup = models.ForeignKey(DevGroup,on_delete=models.CASCADE)
    pass

class teacherRegister(models.Model):
    # did 开发者编号
    did = models.AutoField(primary_key=True)
    # dname 开发者的姓名
    dname = models.CharField(max_length=30)
    # dhiredate 入职时间
    dkey = models.CharField(max_length=30)
    # demail 电子邮箱
    demail = models.EmailField(max_length=50)
    # dsal 薪资
    dsex = models.CharField(max_length=30)
    # daccessable 教师卡的可用性
    daccessable = models.IntegerField(default = 1)
    # # 注意：devgroup 开发者所在的小组(外键)
    # devgroup = models.ForeignKey(DevGroup,on_delete=models.CASCADE)
    pass

# 图书库中CSS书籍Moels表单
class GetDataCss(models.Model):
    Jsid=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    imgUrl=models.CharField(max_length=100)
    details=models.CharField(max_length=200)
    copyBook = models.IntegerField(default= 1)
    beBorrowedTimes = models.IntegerField(default = 1)
    pass

# 图书库中HTML书籍Moels表单
class GetDataHtml(models.Model):
    Jsid=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    imgUrl=models.CharField(max_length=100)
    details=models.CharField(max_length=200)
    copyBook = models.IntegerField(default= 1)
    beBorrowedTimes = models.IntegerField(default = 1)
    pass

# 图书库中JS书籍Moels表单
class GetDataJavaScript(models.Model):
    Jsid=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    imgUrl=models.CharField(max_length=100)
    details=models.CharField(max_length=200)
    copyBook = models.IntegerField(default= 1)
    beBorrowedTimes = models.IntegerField(default = 1)
    pass




# 所有被借阅的CSS相关书籍Models表单
class CustomerCss(models.Model):
    Sid = models.AutoField(primary_key = True)
    Jsid=models.IntegerField(default= 0)
    title=models.CharField(max_length=100)
    imgUrl=models.CharField(max_length=100)
    details=models.CharField(max_length=200)
    borrowTime = models.CharField(max_length=100, default = "")
    whoBorrow = models.CharField(max_length=100, default = "")

# 所有被借阅的HTML相关书籍Models表单
class CustomerHtml(models.Model):
    Sid = models.AutoField(primary_key = True)
    Jsid=models.IntegerField(default= 0)
    title=models.CharField(max_length=100)
    imgUrl=models.CharField(max_length=100)
    details=models.CharField(max_length=200)
    borrowTime = models.CharField(max_length=100, default = "")
    whoBorrow = models.CharField(max_length=100, default = "")

# 所有被借阅的JS相关书籍Models表单
class CustomerJavaScript(models.Model):
    Sid = models.AutoField(primary_key = True)
    Jsid=models.IntegerField(default= 0)
    title=models.CharField(max_length=100)
    imgUrl=models.CharField(max_length=100)
    details=models.CharField(max_length=200)
    borrowTime = models.CharField(max_length=100, default = "")
    whoBorrow = models.CharField(max_length=100, default = "")


