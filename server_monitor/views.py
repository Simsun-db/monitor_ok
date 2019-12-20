from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpRequest
from . import models
from django import forms
from . import forms
import hashlib

# @transaction.atomic
# def dbo_update():
#     with connection.cursor() as cursor:
#         sql2 = """UPDATE  ms_user_list u
#         SET u.user_sqr='testsqr233332'
#            WHERE u.user_id=:userid """
#         parameters2 = {'userid': '1'}
#         cursor.execute(sql2, parameters2)

# Create your views here.

#密码加密
def hash_code(s, salt='simsun'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


# 执行SQL函数
def my_custom_sql(sql, parameters={}):
    with connection.cursor() as cursor:
        cursor.execute(sql, parameters)
        cols = [item[0] for item in cursor.description]
        rows = cursor.fetchall()
    return cols, rows


def server_list(request):
    sql = "select * from ms_server_list where server_name like :x"
    parameters = {'x': '%服务器1%'}
    cols, rows = my_custom_sql(sql, parameters)
    return render(
        request, 'serverlist.html', {
            'serverlist': rows, "cols": cols})


def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    sql = "select * from ms_server_list where server_name like :x"
    parameters = {'x': '%服务器1%'}
    cols, rows = my_custom_sql(sql, parameters)
    return render(request, 'login/index.html',
                  {'serverlist': rows, "cols": cols})


def login(request: HttpRequest):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        message = '请检查填写的内容！'
        if username.strip() and password:
            # 用户名字符合法性验证
            # 密码长度验证
            # 更多的其它验证.....
            try:
                user = models.MsUsers.objects.get(username=username)
            except BaseException:
                message = '用户不存在！'
                return render(request, 'login/login.html', locals())
            if user.password == hash_code(password):
                request.session['is_login'] = True
                request.session['cn_name'] = user.cn_name
                request.session['user_name'] = user.username
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())

    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            cn_name = register_form.cleaned_data.get('cn_name')
            if len(password1) < 6:
                    message = '密码长度应大于6位,请重新填写！'
                    return render(request, 'login/register.html', locals())
            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.MsUsers.objects.filter(
                    username=username)
                if same_name_user:
                    message = '用户账号已经存在！'
                    return render(request, 'login/register.html', locals())
                # same_email_user = models.MsUsers.objects.filter(email=email)
                # if same_email_user:
                #     message = '该邮箱已经被注册了！'
                #     return render(request, 'login/register.html', locals())

                new_user = models.MsUsers()
                new_user.username = username
                new_user.password = hash_code(password1)
                new_user.cn_name = cn_name
                new_user.save()

                return redirect('/login/')
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    request.session.flush()
    return redirect("/login/")
