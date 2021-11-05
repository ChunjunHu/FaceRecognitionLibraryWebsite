"""myDjango02 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
#from django.urls import path
from django.conf.urls import url
from app01 import views as app01_v
from django.urls import path

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^$',app01_v.gotoIndex),
    url(r'^gotoLogin', app01_v.gotoLogin), # 定义一个跳转登录页面login.html的映射地址解析
    url(r'^post-login', app01_v.login), #定义一个处理搜登陆请求的映射地址解析
    url(r'^gotoHome', app01_v.gotoHome), # 定义一个跳转登录页面home.html的映射地址解析
    url(r'^get-logout', app01_v.logout), # 定义一个跳转网站首页index.html的映射地址解析
    url(r'^gotoUpload', app01_v.gotoUpload), # 定义一个跳转网站上传页面upload.html的映射地址解析
    url(r'^post-upload', app01_v.upload), # 定义一个处理文件上传业务的映射地址解析
    url(r'^takePhoto', app01_v.takePhoto), # 定义一个处理文件上传业务的映射地址解析
    url(r'^gotoFaceFind', app01_v.gotoFaceFind), 
    path('face_sluice/',app01_v.gotoindex),  # 进入人脸检测的首页URL地址
    path('face_sluice/sample01',app01_v.sample01),
    path('face_sluice/upload',app01_v.upload_image),
    url(r'^developer/adddeveloper', app01_v.gotoAddDeveloper), # 注册跳转到添加开发者的页面的地址映射
    url(r'^developer/doadd', app01_v.doAddDeveloper), # 注册实现开发者数据表添加操作的地址映射
    #url(r'^developer/doselect', app01_v.doDeveloperSelect), # 注册实现开发者数据表添加操作的地址映射
    path('gotoBookIndex',app01_v.gotoBookIndex),
    path('post-Booklogin',app01_v.Booklogin),
    path('gotoBookRegister',app01_v.gotoBookRegister),
    path('doAddRegister',app01_v.doAddRegister),
    path('BookRegister',app01_v.BookRegister),
    path('getCSSData',app01_v.getCSSData),
    path('getHtmlData',app01_v.getHtmlData),
    path('getJavaScriptData',app01_v.getJavaScriptData),
    path('showData',app01_v.gotoShowData),
    path('doSelectGetDataCssByPage',app01_v.doSelectGetDataCssByPage),
    path('toupdate',app01_v.toupdate),
    path('doupdate', app01_v.doUpdate),
    path('gotoshowSearchData',app01_v.gotoshowSearchData),
    path('doSelectGetDataIndexByPage',app01_v.doSelectGetDataIndexByPage),
    path('doSelectGetDataByPage',app01_v.doSelectGetDataByPage),
    path('doSelectCustomerCssByPage', app01_v.doSelectCustomerCssByPage),
    path('doSelectCustomerHtmlByPage', app01_v.doSelectCustomerHtmlByPage),
    path('doSelectGetCustomerDataByPage', app01_v.doSelectGetCustomerDataByPage),
    path('customerMainBookIndex',app01_v.gotoCustomerMainBookIndex),
    path('customerBookIndex',app01_v.gotoCustomerBookIndex),
    path('borrow',app01_v.gotoBorrow),
    path('sendBack',app01_v.gotoSendBack),
    path('certificateLost',app01_v.gotoBookLost),
    path('recordLostPeople',app01_v.recordLostPeople),
    path('gotoChangePassword',app01_v.gotochangePassword),
    path('changePassword',app01_v.changePassword),
    path('top10',app01_v.top10),
    path('doSelectTopData',app01_v.doSelectTopData),
    path('payFee',app01_v.payFee),
    path('gotoPayFee',app01_v.gotoPayFee),

]
