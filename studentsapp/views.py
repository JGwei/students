from django.shortcuts import render, redirect
from studentsapp.models import student, Visit
from studentsapp.forms import PostForm

from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
import datetime

def set_session(request,key=None,value=None):
	response = HttpResponse('')
	request.session[key]=value
	return response

def set_cookie(request,key=None,value=None):
	response = HttpResponse('Cookie 儲存完畢!')
	response.set_cookie(key,value)
	return response

def showSession(request):
	if "Logins" in request.session:
		request.session["Logins"] = int(request.session["Logins"]) + 1
	else:
		request.session["Logins"] = 1
	response = HttpResponse(request.session["Logins"])	
	return response

def show(request):
	if "counter" in request.COOKIES:
		counter=int(request.COOKIES["counter"])
		counter+=1
	else:		
		counter=1
	response = HttpResponse(counter)		
	tomorrow = datetime.datetime.now() + datetime.timedelta(days = 1)
	tomorrow = datetime.datetime.replace(tomorrow, hour=0, minute=0, second=0)
	expires = datetime.datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT") 
	response.set_cookie("counter",counter,expires=expires)
	return response

def index(request):
	if request.user.is_authenticated:
		name=request.session['username']
		data=request.session['Logins']
	students = student.objects.all().order_by('id')  #讀取資料表, 依 id 遞增排序

	return render(request, "index.html", locals())

def login(request):
	if request.method == 'POST':
		name = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=name, password=password)
		if user is not None:
			if user.is_active:
				auth.login(request,user)
				request.session['username'] = name
				showSession(request)
				
				return redirect('/index/')
				message = '登入成功！'
			else:
				message = '帳號尚未啟用！'
		else:
			message = '登入失敗！'
	return render(request, "login.html", locals())
	
def logout(request):
	auth.logout(request)
	response = HttpResponseRedirect('/index/')
	response.delete_cookie("counter")
	response.delete_cookie("Logins")
	return response


# 使用到的
def post2(request):  #新增資料，資料必須驗證
	if not  request.user.is_authenticated:
		return redirect('/login/')
	else:
		if request.method == "POST":  #如果是以POST方式才處理
			postform = PostForm(request.POST)  #建立forms物件
			if postform.is_valid():			#通過forms驗證
				cName = postform.cleaned_data['cName'] #取得表單輸入資料
				cSex =  postform.cleaned_data['cSex']
				cBirthday =  postform.cleaned_data['cBirthday']
				cEmail = postform.cleaned_data['cEmail']
				cPhone =  postform.cleaned_data['cPhone']
				cAddr =  postform.cleaned_data['cAddr']
				#新增一筆記錄
				unit = student.objects.create(cName=cName, cSex=cSex, cBirthday=cBirthday, cEmail=cEmail,cPhone=cPhone, cAddr=cAddr) 
				unit.save()  #寫入資料庫
				message = '已儲存...'
				return redirect('/logout/')	
			else:
				message = '驗證碼錯誤！'	
		else:
			message = '姓名、性別、生日必須輸入！'
			postform = PostForm()

		if request.user.is_authenticated:
			name=request.session['username']
		return render(request, "post2.html", locals())		
# 使用到的	
def delete(request,id=None):  #刪除資料
	if not  request.user.is_authenticated:
		
		return redirect('/login/')
	else:
		if id!=None:
			if request.method == "POST":  #如果是以POST方式才處理
				id=request.POST['cId'] #取得表單輸入的編號
			try:
				unit = student.objects.get(id=id)  
				unit.delete()
				return redirect('/logout/')
			except:
				message = "讀取錯誤!"
		if request.user.is_authenticated:
			name=request.session['username']	
		return render(request, "delete.html", locals())
# 使用到的		
def edit2(request,id=None,mode=None):
	if not request.user.is_authenticated:
		return redirect('/login/')
	else:
		if mode == "load":  # 由 index.html 按 編輯二 鈕
			unit = student.objects.get(id=id)  #取得要修改的資料記
			strdate=str(unit.cBirthday)
			strdate2=strdate.replace("年","-")
			strdate2=strdate.replace("月","-")
			strdate2=strdate.replace("日","-")
			unit.cBirthday = strdate2
			if request.user.is_authenticated:
				name=request.session['username']	
			return render(request, "edit2.html", locals())
		elif mode == "save": # 由 edit2.html 按 submit		
			unit = student.objects.get(id=id)  #取得要修改的資料記錄	
			unit.cName=request.POST['cName']
			unit.cSex=request.POST['cSex']
			unit.cBirthday=request.POST['cBirthday']
			unit.cEmail=request.POST['cEmail']
			unit.cPhone=request.POST['cPhone']
			unit.cAddr=request.POST['cAddr']		
			unit.save()  #寫入資料庫
			message = '已修改...'
		return redirect('/logout/')
	 	



def listone(request): 
	try: 
		unit = student.objects.get(cName="李采茜") #讀取一筆資料
	except:
		errormessage = " (讀取錯誤!)"
	return render(request, "listone.html", locals())

def listall(request):  
    students = student.objects.all().order_by('id')  #讀取資料表, 依 id 遞增排序
    return render(request, "listall.html", locals())
	
def post(request):
	if request.method == "POST":		#如果是以POST方式才處理
		mess = request.POST['username'] #取得表單輸入資料
	else:
		mess="表單資料尚未送出!"	
	return render(request, "post.html", locals())
	
def post1(request):  #新增資料，資料不作驗證
	if not  request.user.is_authenticated:
		return redirect('/login/')
	else:
		if request.method == "POST":	  #如果是以POST方式才處理
			cName = request.POST['cName'] #取得表單輸入資料
			cSex =  request.POST['cSex']
			cBirthday =  request.POST['cBirthday']
			cEmail = request.POST['cEmail']
			cPhone =  request.POST['cPhone']
			cAddr =  request.POST['cAddr']
			#新增一筆記錄
			unit = student.objects.create(cName=cName, cSex=cSex, cBirthday=cBirthday, cEmail=cEmail,cPhone=cPhone, cAddr=cAddr) 
			unit.save()  #寫入資料庫
			return redirect('/index/')	
		else:
			message = '請輸入資料(資料不作驗證)'
		return render(request, "post1.html", locals())	

def edit(request,id=None,mode=None):  
	if mode == "edit":  # 由 edit.html 按 submit
		unit = student.objects.get(id=id)  #取得要修改的資料記錄	
		unit.cName=request.GET['cName']
		unit.cSex=request.GET['cSex']
		unit.cBirthday=request.GET['cBirthday']
		unit.cEmail=request.GET['cEmail']
		unit.cPhone=request.GET['cPhone']
		unit.cAddr=request.GET['cAddr']		
		unit.save()  #寫入資料庫
		message = '已修改...'
		return redirect('/index/')	
	else: # 由網址列
		try:
			unit = student.objects.get(id=id)  #取得要修改的資料記錄
			strdate=str(unit.cBirthday)
			strdate2=strdate.replace("年","-")
			strdate2=strdate.replace("月","-")
			strdate2=strdate.replace("日","-")
			unit.cBirthday = strdate2
		except:
			message = "此 id不存在！"	
		return render(request, "edit.html", locals())	
 
def postform(request):  #新增資料，資料必須驗證
	postform = PostForm()  #建立PostForm物件
	return render(request, "postform.html", locals())		  
