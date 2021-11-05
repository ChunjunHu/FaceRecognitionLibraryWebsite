from __future__ import unicode_literals
from django.shortcuts import render
from app01.tools import PermissionManager
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# 导入所需模块库及对象
import datetime # 获取时间
import random # 获取随机数
from itertools import chain
# 引用app01中的models.py脚本DevGroup类、Developer类
from app01.models import DevGroup, Developer
# 引用django框架中分页器类
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import os, base64, json
# 导入AipFace模块库
from aip import AipFace

#博客模块的引入
from app01.models import Register,teacherRegister
from app01.models import GetDataCss,GetDataHtml,GetDataJavaScript
from app01.models import CustomerCss,CustomerHtml,CustomerJavaScript

#进行数据抓取需要的模块
import urllib.request
from bs4 import BeautifulSoup
import sys
utf8 = 'utf-8'
if sys.getdefaultencoding() != utf8:
    reload(sys)
    sys.setdefaultencoding(utf8)
    pass

#设定全局变量
flag = 0
bookSelect = '2'
currentStuID = ""
fee = 0
_pageSizeData = "2"

def gotoIndex(request):
    return render(request,'index.html')

def login(request):
    if request.POST:
        account = request.POST.get('account', None)
        password = request.POST.get('password', None)
    permissionManager = PermissionManager()
    flag = permissionManager.login(account, password)
    if flag:
        # 将登陆账号存放到session会话当中
        request.session['account'] = account
        # 跳转至home.html
        return HttpResponseRedirect('/gotoHome/')
    else:
        # 跳转回登陆界面，并提示报错信息
        return render(request, 'login.html', {'msg':'登陆失败'})

def gotoLogin(request):
    # 跳转至静态模板login.html
    return render(request, 'login.html')

def gotoHome(request):
    # 获取session中的登陆账号
    account = request.session.get('account', None)
    # 判断account是否存在
    if not account:  
        # 跳转至登陆页面
        return render(request ,'login.html')
    # 跳转至静态模板login.html
    return render(request, 'home.html', {'account':account})

# 定义一个退出的业务处理视图渲染控制器函数
def logout(request):
    # 删除session中的account
    del request.session['account']
    # 响应客户端跳转至网站首页index.html
    return HttpResponseRedirect('/')

# 定义一个跳转至上传页面的视图渲染控制器函数
def gotoUpload(request):
    # 跳转至静态模板upload.html
    return render(request, 'upload.html')

# 定义一个文件上传的业务处理视图渲染控制器函数
def upload(request):
    # 动态创建客户端上传数据的文件夹
    upload_folder = 'upload'
    # 判断是否存在该文件夹
    if not os.path.exists(upload_folder):
        # 动态创建文件夹
        os.mkdir(upload_folder)
    
    # 获取客户端上传的文件并写入到服务器指定的文件夹中
    # 判断post参数是否存在
    if request.POST:
        # 获取客户端上传的文件
        upload_file = request.FILES.get('uploadFile', None)
        # 判断上传文件是否正常获取
        if not upload_file:
            return HttpResponse('错误！没有解析到上传的文件数据……')
        # 打开文件二进制写操作
        destination = open(os.path.join(upload_folder, upload_file.name), 'wb+')
        # 分块写入数据
        for chunk in upload_file.chunks():
            destination.write(chunk)  # 写入文件块数据
        # 关闭文件操作指针
        destination.close()
        # 响应客户端
        return HttpResponse('恭喜，文件上传成功!')

def takePhoto(request):
    return render(request,'take_photo.html')





# 配置项目的 APP_ID, API_KEY（AK）, SECRET_KEY（SK）
# 通过百度AI控制台创建项目后查看得到
APP_ID = "10772115"
API_KEY = "Ss94IcGfZqBczc4kdkHBXW4y"
SECRET_KEY = "gjjK6t8IEmxQPToBcqm0qaxq3KXYWqdi"

# 创建client客户端对象
# 语法：AipFace(APP_ID, API_KEY, SECRET_KEY)
client = AipFace(APP_ID, API_KEY, SECRET_KEY)

# 通过装饰器设置函数URLs访问路径
# 定义设置网站首页的处理函数
def gotoFaceFind(request):
    # 浏览器输出
        return render(request,'faceRecognition.html')

def gotoindex(request):
    return render(request, "gotoindex.html")

def sample01(request):
    if request.POST:
        pass
    else:
        return render(request, 'faceRecognition.html')

'''
 定义读取人像图片函数
'''
def get_file_content(filePath):
    try:
        with open(filePath, 'rb') as fp:
            return fp.read()
    except IOError:
        print('读取图片数据失败!')

''' 
定义实现人脸查找函数
'''
def faceSearchDetection(group_id,file_path):
    groupId = group_id
    image = get_file_content(file_path)
    """ 调用人脸识别 """
    client.identifyUser(groupId, image);
    """ 如果有可选参数 """
    options = {}
    #options["ext_fields"] = "faceliveness"
    """ 带参数调用人脸识别 """
    data=client.identifyUser(groupId, image, options)
    print(data)
    if data['result'][0]['scores'][0]>80:
        print("识别通过",data)
    else:
        print("识别失败",data)

'''
 接受客户端传入人脸数据并进行鉴定识别
'''
def commitImageData(request):
    if request.method == 'POST':
        # 将获取的data数据转化成Json数据格式
        json_data = json.loads(request.form.get('data'))
        # 获取key：data的数据（即图片base64编码）
        img_base64 = json_data['data']
        # base64转码
        imgdata=base64.b64decode(img_base64)
        # 创建临时图片文件，以写入二进制形式打开
        file=open('temp/face_tmp.png','wb')
        # 将base64编码写入
        file.write(imgdata)
        # 关闭文件操作对象  
        file.close()
        # 调用人脸特征检测函数
        result = faceFind('temp/face_tmp.png')
        print(json.dumps(result))     
        return json.dumps(result)

def upload_image(request):
    if request.POST:
        # 获取客户端传入的data数据并转化成json格式
        json_data = json.loads(request.POST.get("data"))
        print(json_data)
        # 获取key：data的数据（即图片base64编码）
        img_base64 = json_data["data"]
        # base64转码
        imgdata=base64.b64decode(img_base64)
        # 创建临时图片文件，以写入二进制形式打开
        file=open("app01/static/temp/face_tmp.png","wb")
        try:            
            # 将base64编码写入
            file.write(imgdata)
        except IOError:
            print("图片写入错误")
        finally:
            # 关闭文件操作对象  
            file.close()        
        # 调用人脸特征检测函数
        result = faceSearchDetection("group1",'app01/static/temp/face_tmp.png')
        # 向客户端返回上传处理结果(json格式)
        return JsonResponse({"result":result})





# 定义跳转添加开发者页面的控制器函数
def gotoAddDeveloper(request):
    # 获取数据库中的开发小组的数据信息
    lstDevGroups = DevGroup.objects.all()
    # 使用请求转发模式跳转至静态资源developer/adddeveloper.html
    return render(request, 'developer/adddeveloper.html', {'lstDevGroups':lstDevGroups})

# 定义实现添加开发者信息的控制器函数
def doAddDeveloper(request):
    # 接受客户端参数
    if request.POST:
        dname = request.POST.get('dname', None)
        dhiredate = request.POST.get('dhiredate', None)
        # 转化成日期类型OK（SQLite数据库中字符串可以直接转换成日期类型）
        #dhiredate = datetime.datetime.strptime(mydate,'%Y-%m-%d')
        demail = request.POST.get('demail', None)
        dsal = float(request.POST.get('dsal', 0.0))
        # # 获取外键数据信息
        # devgroup_id = int(request.POST.get('devgroup_id', 0))
        # # 通过外键id获取到对象get(xxx=xx)
        # devgroup = DevGroup.objects.get(gid=devgroup_id)
    # 处理请求
        try:
            # 创建并初始化Developer对象
            developer = Developer(dname=dname, dhiredate=dhiredate, demail=demail, dsal=dsal)
            # 执行数据库添加操作
            developer.save()
            # 跳转回添加开发者页面
            return render(request, 'developer/adddeveloper.html')
        except Exception:
            print('添加管理员信息失败!')
            return render(request, 'developer/adddeveloper.html')

# 定义实现开发者查询的控制器函数
def doDeveloperSelect(request):
    # 查询数据库
    lstDevelopers = Developer.objects.all()
    # 响应客户端
    return render(request, 'developer/showdeveloper.html', {'lstDevelopers':lstDevelopers})

# 定义实现添加测试数据的控制器函数
def doTestAddDeveopler(request):
    testAdd = TestAddDeveloper()
    testAdd.addDatas()
    return None

# 定义实现开发者分页查询显示的控制器函数
def doSelectDeveloperByPage(request):
    # 获取查询的所有记录结果（select all的操作）
    lstDevelopers = Developer.objects.all()
    # 创建Paginator类对象
    # 构造方法 Paginator(查询结果, 每页显示的个数)
    paginator = Paginator(lstDevelopers, 15) # 每页显示15条记录
    # 获取客户端传入的页数参数
    page = request.GET.get('page', 1)
    try:
        # 获取当前页的所有数据
        pageDevelopers = paginator.page(page)
    except PageNotAnInteger:
        # 如果传入的页码不是一个数字，则默认跳转到第1页
        pageDevelopers = paginator(1)
    except EmptyPage:
        # 如果传入的页面越界，则默认跳转到最后一页
        pageDevelopers = paginator.page(paginator.num_pages)
    # 响应客户端
    return render(request, 'developer/showdeveloper.html', {'pageDevelopers':pageDevelopers})

#博客界面---------------------------------------------------------------------------------

def gotoBookIndex(request):
    return render(request, 'gotoBookIndex.html')

def gotoBookRegister(request):
    return render(request, 'gotoBookRegister.html')

def top10(request):
    return render(request, 'top10.html')

def doSelectTopData(request):
    flag = 0
    # 获取登陆者信息
    Reg = Register.objects.all().values_list('dname','borrowTimes')

    # 获取所有书籍信息~被借阅次数
    css = GetDataCss.objects.all().values_list('title','beBorrowedTimes')
    html = GetDataHtml.objects.all().values_list('title','beBorrowedTimes')
    javaScript = GetDataJavaScript.objects.all().values_list('title','beBorrowedTimes')

    # 将借阅top10信息排序并选前十传参
    topStus = sorted(Reg, key = lambda x:x[1], reverse = True)[:10]
    topBooks = sorted(chain(css, html, javaScript), key = lambda x:x[1], reverse = True)[:10]

    pageSizeData=request.GET.get("pageSizeData")
    request.session['pageSizeData']=pageSizeData
    if pageSizeData=="1":
        getDataJavaScript = topStus
        flag = 1
    elif pageSizeData=="2":
        getDataJavaScript = topBooks
        flag = 2
    # 响应客户端
    return render(request, 'top10.html', {'getDataJavaScript':getDataJavaScript})

# 密码修改跳转
def gotochangePassword(request):
    return render(request,'changePassword.html')

# 修改密码
def changePassword(request):
    if request.POST:
        dname = request.POST.get('user', None)
        dkey = request.POST.get('newPwd', None)
        Register.objects.filter(dname = dname).update(dkey = dkey)
        return render(request, 'changePassword.html',{"message":"修改密码成功","userid1":"1"})

# 挂失系统----------------------
def gotoBookLost(request):
    return render(request, 'certificateLost.html')

def recordLostPeople(request):
    if request.POST:
        lostPeople = request.POST
        if lostPeople['sex'] == '1':
            flag = Register.objects.filter(dname = lostPeople['user']).update(daccessable = 0)
            if flag:
                return render(request, 'certificateLost.html',{"message":"挂失成功","userid1":"1"})
            else:
                return render(request, 'certificateLost.html',{"message":"挂失失败","userid2":"2"})
        else:
            flag = Register.objects.filter(dname = lostPeople['user']).delete()
            if flag:
                return render(request, 'certificateLost.html',{"message":"注销成功","userid1":"1"})
            else:
                return render(request, 'certificateLost.html',{"message":"注销失败","userid2":"2"})
# -----------------------------

# 用户注册
def doAddRegister(request):
    # 接受客户端参数
    if request.POST:
        dname = request.POST.get('user', None)
        dkey = request.POST.get('psd', None)
        demail = request.POST.get('email', None)
        dsex = request.POST.get('sex', None)

        # 二维码生成，依据当前日期与学生学号
        str1 = str(datetime.datetime.now().year*datetime.datetime.now().month*datetime.datetime.now().day)
        str2 = str( int(int((int(dname)/100000000)) * (int(dname)%10000) * (( (int(dname)%100000000) - (int(dname)%10000) ) / 10000)))
        QrCode = str1 + str2

        if dsex == '1':
            try:
                # 创建并初始化Developer对象
                register = Register(dname=dname, dkey=dkey, demail=demail, dQrCode = QrCode)
                # 执行数据库添加操作
                register.save()
                # 跳转回添加开发者页面
                return render(request, 'gotoBookRegister.html',{"message":"注册成功，请去登录","userid1":"1", "QrCode":QrCode})
            except Exception:
                return render(request, 'gotoBookRegister.html',{"message":"注册失败，请重新注册","userid2":"2"})
        else:
            try:
                register = Register.objects.all().values_list('dname','daccessable')
                for reg in register:
                    if dname == reg[0] and reg[1] == 0:
                        # 补办后更新用户数据
                        Register.objects.filter(dname = dname).update(dkey = dkey)
                        Register.objects.filter(dname = dname).update(demail = demail)
                        Register.objects.filter(dname = dname).update(dQrCode = QrCode)
                        Register.objects.filter(dname = dname).update(daccessable = 1)
                        return render(request, 'gotoBookRegister.html', {"message":"补办成功，请去登录","userid1":"1", "QrCode":QrCode})
                return render(request, 'gotoBookRegister.html', {"message":"您不符合补办条件","userid2":"2"})
            except Exception:
                return render(request, 'gotoBookRegister.html',{"message":"补办失败，请重新补办","userid2":"2"})

def BookRegister(request):
    return render(request,'BookRegister.html')


def getCSSData(request):
    getDataCss = GetDataCss.objects.all()
    if len(getDataCss)>0:
        if flag == 1:
            return render(request,'BookRegister.html',{"success1":"跳过数据更新，进入系统","userid1":"1","message":"Student Page"})
        else:
            return render(request,'BookRegister.html',{"success1":"跳过数据更新，进入系统","userid1":"1","message":"Welcome, teacher"})
    else:
        list1=['http://web.jobbole.com/category/css/','http://web.jobbole.com/category/css/page/2/']
        for i in list1:
            res = urllib.request.urlopen(i)
            soup = BeautifulSoup(res,"html.parser")
            items = soup.find_all('div',{'class':'post floated-thumb'})   
            obj={}
            for item in items:
                obj['title'] = item.find('a',{"class":"archive-title"}).get_text()
                obj['details'] = item.find('span',{"class":"excerpt"}).find("p").get_text()
                obj['imgUrl'] = item.find("div",{"class":"post-thumb"}).find("a").find("img").get("src")
                obj['copyBook'] = random.randint(2, 11)
                obj['beBorrowedTimes'] = random.randint(2, 50)
                etJsData=GetDataCss(title=obj['title'],imgUrl=obj['imgUrl'],details=obj['details'],copyBook = obj['copyBook'], beBorrowedTimes = obj['beBorrowedTimes'])
                etJsData.save()
        if flag == 1:
            return render(request,'BookRegister.html',{"success1":"跳过数据更新，进入系统","userid":"1","message":"Student Page"})
        else:
            return render(request,'BookRegister.html',{"success1":"跳过数据更新，进入系统","userid":"1","message":"Welcome, teacher"})

def getHtmlData(request):
    getDataHtml=GetDataHtml.objects.all()
    if len(getDataHtml)>0:
        if flag == 1:
            return render(request,'BookRegister.html',{"success2":"跳过数据更新，进入系统","userid1":"1","message":"Student Page"})
        else:
            return render(request,'BookRegister.html',{"success2":"跳过数据更新，进入系统","userid1":"1","message":"Welcome, teacher"})
    else:
        list1=['http://web.jobbole.com/category/html5/','http://web.jobbole.com/category/html5/page/2/']
        for i in list1:
            res = urllib.request.urlopen(i)
            soup = BeautifulSoup(res,"html.parser")
            items = soup.find_all('div',{'class':'post floated-thumb'})   
            obj={}
            for item in items:
                obj['title'] = item.find('a',{"class":"archive-title"}).get_text()
                obj['details']=item.find('span',{"class":"excerpt"}).find("p").get_text()
                obj['imgUrl']=item.find("div",{"class":"post-thumb"}).find("a").find("img").get("src")
                obj['copyBook']=random.randint(2, 11)
                obj['beBorrowedTimes'] = random.randint(2, 50)
                getDataHtml=GetDataHtml(title=obj['title'],imgUrl=obj['imgUrl'],details=obj['details'],copyBook = obj['copyBook'], beBorrowedTimes = obj['beBorrowedTimes'])
                getDataHtml.save()
        if flag == 1:
            return render(request,'BookRegister.html',{"success2":"跳过数据更新，进入系统","userid1":"1","message":"Student Page"})
        else:
            return render(request,'BookRegister.html',{"success2":"跳过数据更新，进入系统","userid1":"1","message":"Welcome, teacher"})

def getJavaScriptData(request):
    getDataJavaScript=GetDataJavaScript.objects.all()
    if len(getDataJavaScript)>0:
        if flag == 1:
            return render(request,'BookRegister.html',{"success3":"跳过数据更新，进入系统","userid1":"1","message":"Student Page"})
        else:
            return render(request,'BookRegister.html',{"success3":"跳过数据更新，进入系统","userid1":"1","message":"Welcome, teacher"})
    else:
        list1=['http://web.jobbole.com/category/javascript-2/','http://web.jobbole.com/category/javascript-2/page/2/']
        for i in list1:
            res = urllib.request.urlopen(i)
            soup = BeautifulSoup(res,"html.parser")
            items = soup.find_all('div',{'class':'post floated-thumb'})   
            obj={}
            for item in items:
                obj['title'] = item.find('a',{"class":"archive-title"}).get_text()
                obj['details']=item.find('span',{"class":"excerpt"}).find("p").get_text()
                obj['imgUrl']=item.find("div",{"class":"post-thumb"}).find("a").find("img").get("src")
                obj['copyBook']=random.randint(2, 11)
                obj['beBorrowedTimes'] = random.randint(2, 50)
                getDataJavaScript=GetDataJavaScript(title=obj['title'],imgUrl=obj['imgUrl'],details=obj['details'], copyBook = obj['copyBook'], beBorrowedTimes = obj['beBorrowedTimes'])
                getDataJavaScript.save()
        if flag == 1:
            return render(request,'BookRegister.html',{"success3":"跳过数据更新，进入系统","userid1":"1","message":"Student Page"})
        else:
            return render(request,'BookRegister.html',{"success3":"跳过数据更新，进入系统","userid1":"1","message":"Welcome, teacher"})


# 定义实现开发者分页查询显示的控制器函数
def doSelectGetDataCssByPage(request):
    # 获取查询的所有记录结果（select all的操作）
    getDataCss = GetDataCss.objects.all()
    # 创建Paginator类对象
    # 构造方法 Paginator(查询结果, 每页显示的个数)
    paginator = Paginator(getDataCss, 5) # 每页显示5条记录
    # 获取客户端传入的页数参数
    page = request.GET.get('page', 1)
    try:
        # 获取当前页的所有数据
        pageDevelopers = paginator.page(page)
    except PageNotAnInteger:
        # 如果传入的页码不是一个数字，则默认跳转到第1页
        pageDevelopers = paginator(1)
    except EmptyPage:
        # 如果传入的页面越界，则默认跳转到最后一页
        pageDevelopers = paginator.page(paginator.num_pages)
    # 响应客户端
    return render(request, 'showData.html', {'pageDevelopers':pageDevelopers, "message":flag})


def doSelectGetDataIndexByPage(request):
    # 获取查询的所有记录结果（select all的操作）
    getDataHtml = GetDataHtml.objects.all()
    # 创建Paginator类对象
    # 构造方法 Paginator(查询结果, 每页显示的个数)
    paginator = Paginator(getDataHtml, 5) # 每页显示5条记录
    # 获取客户端传入的页数参数
    page = request.GET.get('page', 1)
    try:
        # 获取当前页的所有数据
        pageDevelopers = paginator.page(page)
    except PageNotAnInteger:
        # 如果传入的页码不是一个数字，则默认跳转到第1页
        pageDevelopers = paginator(1)
    except EmptyPage:
        # 如果传入的页面越界，则默认跳转到最后一页
        pageDevelopers = paginator.page(paginator.num_pages)
    # 响应客户端
    return render(request, 'showData.html', {'pageDevelopers':pageDevelopers, "message":flag})



def doSelectGetDataByPage(request):
    # 获取查询的所有记录结果（select all的操作）
    pageSizeData=request.GET.get("pageSizeData")
    global bookSelect, _pageSizeData
    if not pageSizeData == None:
        _pageSizeData = pageSizeData
    bookSelect = _pageSizeData
    request.session['pageSizeData']=pageSizeData
    if _pageSizeData=="1":
        getDataJavaScript = GetDataJavaScript.objects.all()
    elif _pageSizeData=="2":
        getDataJavaScript = GetDataHtml.objects.all()
    elif _pageSizeData=="3":
        getDataJavaScript = GetDataCss.objects.all()
    # 创建Paginator类对象
    # 构造方法 Paginator(查询结果, 每页显示的个数)
    paginator = Paginator(getDataJavaScript, 5) # 每页显示15条记录
    # 获取客户端传入的页数参数
    page = request.GET.get('page', 1)
    try:
        # 获取当前页的所有数据
        pageDevelopers = paginator.page(page)
    except PageNotAnInteger:
        # 如果传入的页码不是一个数字，则默认跳转到第1页
        pageDevelopers = paginator(1)
    except EmptyPage:
        # 如果传入的页面越界，则默认跳转到最后一页
        pageDevelopers = paginator.page(paginator.num_pages)
    # 响应客户端
    return render(request, 'showData.html', {'pageDevelopers':pageDevelopers, "message":flag})

    
#获取顾客登录借书页面的数据并分页展示
def doSelectCustomerCssByPage(request):
    # 获取查询的所有记录结果（select all的操作）
    customerCss = CustomerCss.objects.all()
    # 创建Paginator类对象
    # 构造方法 Paginator(查询结果, 每页显示的个数)
    paginator = Paginator(customerCss, 5) # 每页显示15条记录
    # 获取客户端传入的页数参数
    page = request.GET.get('page', 1)
    try:
        # 获取当前页的所有数据
        pageDevelopers = paginator.page(page)
    except PageNotAnInteger:
        # 如果传入的页码不是一个数字，则默认跳转到第1页
        pageDevelopers = paginator(1)
    except EmptyPage:
        # 如果传入的页面越界，则默认跳转到最后一页
        pageDevelopers = paginator.page(paginator.num_pages)
    # 响应客户端
    return render(request, 'customerBookIndex.html', {'pageDevelopers':pageDevelopers})

def doSelectCustomerHtmlByPage(request):
    global currentStuID
    # 获取查询的所有记录结果（select all的操作）
    customerHtml = CustomerHtml.objects.filter(whoBorrow = currentStuID)
    # 创建Paginator类对象
    # 构造方法 Paginator(查询结果, 每页显示的个数)
    paginator = Paginator(customerHtml, 5) # 每页显示15条记录
    # 获取客户端传入的页数参数
    page = request.GET.get('page', 1)
    try:
        # 获取当前页的所有数据
        pageDevelopers = paginator.page(page)
    except PageNotAnInteger:
        # 如果传入的页码不是一个数字，则默认跳转到第1页
        pageDevelopers = paginator(1)
    except EmptyPage:
        # 如果传入的页面越界，则默认跳转到最后一页
        pageDevelopers = paginator.page(paginator.num_pages)
    # 响应客户端
    return render(request, 'customerBookIndex.html', {'pageDevelopers':pageDevelopers})

def doSelectGetCustomerDataByPage(request):
    global bookSelect, _pageSizeData
    # 获取查询的所有记录结果（select all的操作）
    pageSizeData=request.GET.get("pageSizeData")
    if not pageSizeData == None:
        _pageSizeData = pageSizeData
    bookSelect = _pageSizeData
    request.session['pageSizeData']=pageSizeData
    if _pageSizeData=="1":
        getDataJavaScript = CustomerJavaScript.objects.filter(whoBorrow = currentStuID)
    elif _pageSizeData=="2":
        getDataJavaScript = CustomerHtml.objects.filter(whoBorrow = currentStuID)
    elif _pageSizeData=="3":
        getDataJavaScript = CustomerCss.objects.filter(whoBorrow = currentStuID)
    # 创建Paginator类对象
    # 构造方法 Paginator(查询结果, 每页显示的个数)
    paginator = Paginator(getDataJavaScript, 5) # 每页显示15条记录
    # 获取客户端传入的页数参数
    page = request.GET.get('page', 1)
    try:
        # 获取当前页的所有数据
        pageDevelopers = paginator.page(page)
    except PageNotAnInteger:
        # 如果传入的页码不是一个数字，则默认跳转到第1页
        pageDevelopers = paginator(1)
    except EmptyPage:
        # 如果传入的页面越界，则默认跳转到最后一页
        pageDevelopers = paginator.page(paginator.num_pages)
    # 响应客户端
    return render(request, 'customerBookIndex.html', {'pageDevelopers':pageDevelopers})

def gotoShowData(request):
    return render(request,'showData.html')

def gotoShowCustomerData(request):
    return render(request,'customerBookIndex.html')

def gotoCustomerMainBookIndex(request):
    return render(request,'customerMainBookIndex.html')

def gotoCustomerBookIndex(request):
    return render(request,'customerBookIndex.html')

def Booklogin(request):
    global fee, currentStuID, flag
    # func计算借阅天数
    def days_increase(borrowDate, currentYear, currentMonth, currentDay):
        monthDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        borYear = int(borrowDate.split('-')[0])
        borMonth = int(borrowDate.split('-')[1])
        borDay = int(borrowDate.split('-')[2])

        count = 0
        while not (borYear == currentYear and borMonth == currentMonth and borDay == currentDay):
            borDay+=1
            count += 1
            if(borMonth == 2 and borYear % 4 == 0): 
                monthDays[1] = 29
            else:  
                monthDays[1] = 28
            if monthDays[borMonth-1] < borDay:
                borMonth+=1
                borDay = 1
                if borMonth == 13:
                    borMonth = 1
                    borYear += 1
        return count

    account = ""
    password = ""
    if request.POST:
        account = request.POST.get('account', None)
        password = request.POST.get('password', None)
    currentStuID = account
    # 获取当前学生所借阅的书籍
    lcss = CustomerCss.objects.filter(whoBorrow = currentStuID)
    lhtml = CustomerHtml.objects.filter(whoBorrow = currentStuID)
    ljavascript = CustomerJavaScript.objects.filter(whoBorrow = currentStuID)
    borrowedBooks = chain(lcss, lhtml, ljavascript)

    fee = 0
    for obj in borrowedBooks:
        days = days_increase(obj.borrowTime, datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
        if days >= 30:
            if (days-30) * 0.1 >= 10:
                fee += 10
            else:
                fee += (days-30) * 0.1
    teaRegisterName = Register.objects.all().values_list('dname')
    if currentStuID in teaRegisterName:
        reg = Register.objects.get(dname = currentStuID)
        reg.fee = fee
        reg.save()
    register = Register.objects.all().values_list('dname','dkey','daccessable')
    teachRegister = teacherRegister.objects.all().values_list('dname','dkey','daccessable')
    for mesage in register:
        if account == mesage[0] and password == mesage[1]:
            flag = 1
            if mesage[2] == 0:
                flag = 3
            break
    for mesage in teachRegister:
        if account == mesage[0] and password == mesage[1]:
            flag = 2
            if mesage[2] == 0:
                flag = 3
            break
    if fee >= 10:
        flag = 4
    print(flag)
    if flag == 1 :
        # 将登陆账号存放到session会话当中
        request.session['account'] = account
        # 跳转至home.html
        return render(request, 'BookRegister.html',{"message":"Student Page","userid1":"1"})
    elif flag == 2 :
        # 将登陆账号存放到session会话当中
        request.session['account'] = account
        # 跳转至home.html
        return render(request, 'BookRegister.html',{"message":"Welcome, teacher","userid1":"1"})
    elif flag == 3:
        # 将登陆账号存放到session会话当中
        request.session['account'] = account
        # 跳转至home.html
        return render(request, 'gotoBookIndex.html',{"msg":"证件已挂失，请去补办"})
    elif flag == 4:
        # 将登陆账号存放到session会话当中
        request.session['account'] = account
        # 跳转至home.html
        return render(request, 'gotoBookIndex.html',{"flag":flag, "fee":fee})
    else:
        # 跳转回登陆界面，并提示报错信息
        return render(request, 'gotoBookIndex.html', {'msg':'登陆失败'})

def payFee(request):
    def days_increase(borrowDate, currentYear, currentMonth, currentDay):
        monthDays = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        borYear = int(borrowDate.split('-')[0])
        borMonth = int(borrowDate.split('-')[1])
        borDay = int(borrowDate.split('-')[2])

        count = 0
        while not (borYear == currentYear and borMonth == currentMonth and borDay == currentDay):
            borDay+=1
            count += 1
            if(borMonth == 2 and borYear % 4 == 0): 
                monthDays[1] = 29
            else:  
                monthDays[1] = 28
            if monthDays[borMonth-1] < borDay:
                borMonth+=1
                borDay = 1
                if borMonth == 13:
                    borMonth = 1
                    borYear += 1
        return count
    global fee
    dname = request.POST.get('user')
    dsex = request.POST.get('sex')
    print(dsex)
    if dsex == '1':
        Register.objects.filter(dname = dname).update(fee = 0)
        fee = 0
        lcss = CustomerCss.objects.filter(whoBorrow = dname)
        for obj in lcss:
            days = days_increase(obj.borrowTime, datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
            if days > 30:
                obj.delete()
        lhtml = CustomerHtml.objects.filter(whoBorrow = dname)
        for obj in lhtml:
            days = days_increase(obj.borrowTime, datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
            if days > 30:
                obj.delete()
        ljs = CustomerJavaScript.objects.filter(whoBorrow = dname)
        for obj in ljs:
            days = days_increase(obj.borrowTime, datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
            if days > 30:
                obj.delete()
        return render(request, 'gotoBookIndex.html')
    else:
        return render(request, 'gotoBookIndex.html')

def gotoPayFee(request):
    return render(request, 'payFee.html', {'fee':fee})

def gotoBorrow(request):
    global bookSelect, currentStuID
    jsId=request.GET.get("jsId")
    # 查询待更新的数据对象
    if bookSelect == '3':
        getDataCss = GetDataCss.objects.get(Jsid=jsId)
        if getDataCss.copyBook <= 0:
            return render(request,'showData.html',{"message":flag})
        obj = CustomerCss(Jsid = getDataCss.Jsid, title = getDataCss.title, imgUrl = getDataCss.imgUrl, details = getDataCss.details, whoBorrow = currentStuID)
        obj.save()
        css = GetDataCss.objects.get(Jsid=jsId)
        GetDataCss.objects.filter(Jsid=jsId).update(copyBook= css.copyBook - 1)
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().month)
        day = str(datetime.datetime.now().day)
        CustomerCss.objects.filter(Jsid=jsId).update(borrowTime = year + '-' + month + '-' + day)
        #记录用户的借阅次数和书籍的借阅次数
        GetDataCss.objects.filter(Jsid=jsId).update(beBorrowedTimes= css.beBorrowedTimes + 1)
        reg = Register.objects.get(dname = currentStuID)
        Register.objects.filter(dname = currentStuID).update(borrowTimes= reg.borrowTimes + 1)
        bookSelect = '2'
    elif bookSelect == '2':
        getDataHtml = GetDataHtml.objects.get(Jsid=jsId)
        if getDataHtml.copyBook <= 0:
            return render(request,'showData.html',{"message":flag})
        obj = CustomerHtml(Jsid = getDataHtml.Jsid, title = getDataHtml.title, imgUrl = getDataHtml.imgUrl, details = getDataHtml.details, whoBorrow = currentStuID)
        obj.save()
        html = GetDataHtml.objects.get(Jsid=jsId)
        GetDataHtml.objects.filter(Jsid=jsId).update(copyBook= html.copyBook - 1)
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().month)
        day = str(datetime.datetime.now().day)
        CustomerHtml.objects.filter(Jsid=jsId).update(borrowTime = year + '-' + month + '-' + day)
        #记录用户的借阅次数和书籍的借阅次数
        GetDataHtml.objects.filter(Jsid=jsId).update(beBorrowedTimes= html.beBorrowedTimes + 1)
        reg = Register.objects.get(dname = currentStuID)
        Register.objects.filter(dname = currentStuID).update(borrowTimes= reg.borrowTimes + 1)
        bookSelect = '2'
    elif bookSelect == '1':
        getDataJavaScript = GetDataJavaScript.objects.get(Jsid=jsId)
        if getDataJavaScript.copyBook <= 0:
            return render(request,'showData.html',{"message":flag})
        obj = CustomerJavaScript(Jsid = getDataJavaScript.Jsid, title = getDataJavaScript.title, imgUrl = getDataJavaScript.imgUrl, details = getDataJavaScript.details, whoBorrow = currentStuID)
        obj.save()
        javaScript = GetDataJavaScript.objects.get(Jsid=jsId)
        GetDataJavaScript.objects.filter(Jsid=jsId).update(copyBook= javaScript.copyBook - 1)
        year = str(datetime.datetime.now().year)
        month = str(datetime.datetime.now().month)
        day = str(datetime.datetime.now().day)
        CustomerJavaScript.objects.filter(Jsid=jsId).update(borrowTime = year + '-' + month + '-' + day)
        #记录用户的借阅次数和书籍的借阅次数
        GetDataJavaScript.objects.filter(Jsid=jsId).update(beBorrowedTimes= javaScript.beBorrowedTimes + 1)
        reg = Register.objects.get(dname = currentStuID)
        Register.objects.filter(dname = currentStuID).update(borrowTimes= reg.borrowTimes + 1)
        bookSelect = '2'
    #使用请求转发跳转到指定的更新页面并展示待更新的数据
    return render(request,'showData.html',{"message":flag})

def gotoSendBack(request):
    global bookSelect, currentStuID
    jsId=request.GET.get("jsId")
    print(jsId)
    # 查询待更新的数据对象
    if bookSelect == '3':
        CustomerCss.objects.filter(Jsid = jsId, whoBorrow = currentStuID).delete()
        css = GetDataCss.objects.get(Jsid=jsId)
        GetDataCss.objects.filter(Jsid=jsId).update(copyBook= css.copyBook + 1)
        bookSelect = '2'
    elif bookSelect == '2':
        CustomerHtml.objects.filter(Jsid = jsId, whoBorrow = currentStuID).delete()
        html = GetDataHtml.objects.get(Jsid=jsId)
        GetDataHtml.objects.filter(Jsid=jsId).update(copyBook= html.copyBook + 1)
        bookSelect = '2'
    elif bookSelect == '1':
        CustomerJavaScript.objects.filter(Jsid = jsId, whoBorrow = currentStuID).delete()
        javaScript = GetDataJavaScript.objects.get(Jsid=jsId)
        GetDataJavaScript.objects.filter(Jsid=jsId).update(copyBook= javaScript.copyBook + 1)
        bookSelect = '2'
    #使用请求转发跳转到指定的更新页面并展示待更新的数据
    return render(request,'customerBookIndex.html',{"message":flag})

def toupdate(request):
    jsId=request.GET.get("jsId")
    # 获取查询的所有记录结果（select all的操作）
    pageSizeData=request.GET.get("pageSizeData")
    global bookSelect, _pageSizeData
    if not pageSizeData == None:
        _pageSizeData = pageSizeData
    # 查询待更新的数据对象
    if _pageSizeData=="1":
        getDataJavaScript = GetDataJavaScript.objects.get(Jsid=jsId)
    elif _pageSizeData=="2":
        getDataJavaScript = GetDataHtml.objects.get(Jsid=jsId)
    elif _pageSizeData=="3":
        getDataJavaScript = GetDataCss.objects.get(Jsid=jsId)
    #使用请求转发跳转到指定的更新页面并展示待更新的数据
    return render(request,'updatedata.html',{"getDataCss":getDataJavaScript})

def doUpdate(request):
    # 获取客户端参数
    global _pageSizeData
    if request.POST:
        Jsid = int(request.POST.get('Jsid', 0))
        title = request.POST.get('title', None)
        details = request.POST.get('details', 0.0)
        # 更新数据
        # 查询待更新的数据对象
        if _pageSizeData=="1":
            GetDataJavaScript.objects.filter(Jsid=Jsid).update(title=title,details=details)
            _pageSizeData = "2"
        elif _pageSizeData=="2":
            GetDataHtml.objects.filter(Jsid=Jsid).update(title=title,details=details)
            _pageSizeData = "2"
        elif _pageSizeData=="3":
            GetDataCss.objects.filter(Jsid=Jsid).update(title=title,details=details)
            _pageSizeData = "2"
        return HttpResponseRedirect('doSelectGetDataIndexByPage')

def gotoshowSearchData(request):
    pageSizeData=request.session['pageSizeData']
    if pageSizeData=="1":
        getDataAll = GetDataJavaScript.objects.all()
    elif pageSizeData=="2":
        getDataAll = GetDataHtml.objects.all()
    elif pageSizeData=="3":
        getDataAll = GetDataCss.objects.all()
    txt=request.GET.get('txt')
    if txt:
        list1=[]
        for i in getDataAll:
            if txt in i.title:
                list1.append(i)
        if len(list1)>0:     
            paginator = Paginator(list1, 5) # 每页显示15条记录
            # 获取客户端传入的页数参数
            page = request.GET.get('page', 1)
            try:
                # 获取当前页的所有数据
                pageDevelopers = paginator.page(page)
            except PageNotAnInteger:
                # 如果传入的页码不是一个数字，则默认跳转到第1页
                pageDevelopers = paginator(1)
            except EmptyPage:
                # 如果传入的页面越界，则默认跳转到最后一页
                pageDevelopers = paginator.page(paginator.num_pages)
            
            return render(request,'showData.html',{"pageDevelopers":pageDevelopers,"txt":txt, "message":flag})
        else:
            return render(request,'showData.html',{"msg2":"您的搜索的数据不存在!!!", "message":flag})   
    else:
        return render(request,'showData.html',{"msg1":"您的搜索框为空!!!", "message":flag})        
        


        
    
    








    