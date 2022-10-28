import re
from django.db import connection
from django.shortcuts import render, redirect
from django.utils import timezone

from web import models
from web.models import Admin,Author,Article,Reviewer,RA,AuthorM,ArticleM,ReviewerM,AdminPay,ReviewerAdmin,ArticleResult
from django.db.models import Max

# 显示日期
global time
global time1
time=timezone.now()
time=time.strftime("%Y年%m月%d日")
time1=timezone.now()
time1=time1.strftime("%Y-%m-%d")

# 主界面
def lxt1(request):
    context={}
    return render(request,"zhuye.html",context)

# 系统管理员登录界面
def lxt2(request):
    ad = models.Admin.objects.all()    # select * from admin
    err1 = err2 = ""
    flag = True
    if request.method == "POST":
        id = request.POST.get("user")
        pass1 = request.POST.get("password")
        if id == "":
            err1 = "账号不能为空"
            flag = False
        else:
            t = 0
            for i in ad:
                if id == i.admin_id:
                    t = 1
                    break
            if t == 0:
                err1 = "用户不存在"
                flag = False
            else:
                adm = models.Admin.objects.get(admin_id=id)     # select * from admin where admin_id=id
                if pass1 == "":
                    err2 = "密码不能为空"
                    flag = False
                elif pass1 != adm.admin_pass:
                    err2 = "密码错误"
                    flag = False

        if flag == True:
            request.session["admin_id"] = adm.admin_id
            request.session["admin_name"] = adm.admin_name
            request.session["admin_phone"] = adm.admin_phone

            return redirect("/guanliyuan/")

    context = {"err1": err1, "err2": err2}
    return render(request, "denglu.html", context)

# 系统管理员界面
def lxt22(request):
    admin_id = request.session.get("admin_id", default="")
    admin_name = request.session.get("admin_name", default="")
    admin_phone = request.session.get("admin_phone", default="")
    ad = models.Admin.objects.filter(admin_id=str(admin_id))        # select # from admin where admin_id='admin_id'
    if not ad.exists():
        ad = []

    statue = dict({})
    ar = models.Article.objects.all()      # select * from article
    if ar.exists():
        for i in ar:
            statue[i.article_id] = "审核中"

        for i in ar:
            r = models.ArticleResult.objects.filter(article_id=i.article_id)
            for j in r:                                   # select * from article_result where article_id=i.article_id
                if j.result == "否":
                    statue[i.article_id] = "未通过"
                else:
                    statue[i.article_id] = "通过"
    else:
        ar = []

    if request.method == "POST":
        if "submit" in request.POST:
            a_id = request.POST.get("author")
            lis = list()
            with connection.cursor() as cursor:
                cursor.callproc('selectauthor', (a_id,))      # call selectauthor(a_id)
                data = cursor.fetchall()
                for i in data:
                    lis.append(i)
                request.session["lis"] = lis
                cursor.close()

            return redirect("/zuozhexinxi/")
        else:
            idd = request.POST.get("id")
            request.session["idgla"] = idd
            return redirect("/glyckgj/")

    context = {"id": admin_id, "name": admin_name, "phone": admin_phone, "time": time, "ad": ad, "statue":statue,"ar":ar}
    return render(request, "guanliyuan.html", context)

# 投稿人登录页面
def lxt3(request):
    au = models.Author.objects.all()     # select * from author
    err1=err2=""
    flag=True
    if request.method == "POST":
        id = request.POST.get("user")
        pass1 = request.POST.get("password")
        if id=="":
            err1="账号不能为空"
            flag = False
        else:
            t=0
            for i in au:
                if id==i.author_id:
                    t=1
                    break
            if t==0:
                err1="用户不存在"
                flag = False
            else:
                aut = models.Author.objects.get(author_id=id)      # select * from author where author_id=id
                if pass1 == "":
                    err2="密码不能为空"
                    flag = False
                else:
                    if pass1!=aut.author_pass:
                        err2="密码错误"
                        flag = False

        if flag==True:
            request.session["user_id"] = aut.author_id
            request.session["user_name"] = aut.author_name
            request.session["user_phone"] = aut.author_phone
            request.session["user_email"] = aut.author_email
            request.session["user_adress"] = aut.author_adress

            return redirect("/tougaoren/")

    context = {"err1": err1, "err2": err2}
    return render(request, "denglu1.html", context)

# 投稿人页面
def lxt33(request):
    user_id = request.session.get("user_id", default="")
    user_name = request.session.get("user_name", default="")
    user_phone = request.session.get("user_phone", default="")
    user_email = request.session.get("user_email", default="")
    user_adress = request.session.get("user_adress", default="")
    statue=dict({})
    ar = models.Article.objects.filter(author_id=str(user_id))  # select * from article where author_id=user_id
    if ar.exists():
        for i in ar:
            statue[i.article_id] = "审核中"

        for i in ar:
            r = models.ArticleResult.objects.filter(article_id=i.article_id)
            for j in r:                             # select * from article_result where article_id=i.article
                if j.result == "否":
                    statue[i.article_id] = "未通过"
                else:
                    statue[i.article_id] = "通过"
    else:
        ar=[]

    if request.method == "POST":
        if "submit1" in request.POST:
            idd = request.POST.get("id")
            arr = models.Article.objects.filter(article_id=idd)[0]   # select * from article where article_id=idd
            request.session["id_gai"] = arr.article_id
            return redirect("/genggai/")
        else:
            idd = request.POST.get("id")
            models.Article.objects.get(article_id=idd).delete()    # delete from article where article_id=idd
            return redirect("/tougaoren/")
    context={"id":user_id,"name":user_name,"phone":user_phone,"email":user_email,
             "adress":user_adress,"time":time,"ar":ar,"statue":statue}
    return render(request,"tougaoren.html",context)

# 审稿人登录页面
def lxt4(request):
    re = models.Reviewer.objects.all()    # select * from reviewer
    err1 = err2 = ""
    flag = True
    if request.method == "POST":
        id = request.POST.get("user")
        pass1 = request.POST.get("password")
        if id == "":
            err1 = "账号不能为空"
            flag = False
        else:
            t = 0
            for i in re:
                if id == i.reviewer_id:
                    t = 1
                    break
            if t == 0:
                err1 = "用户不存在"
                flag = False
            else:
                rev = models.Reviewer.objects.get(reviewer_id=id)    # select * from reviewer where reviewer_id=id
                if pass1 == "":
                    err2 = "密码不能为空"
                    flag = False
                elif pass1 != rev.reviewer_pass:
                    err2 = "密码错误"
                    flag = False

        if flag == True:
            request.session["reviewer_id"] = rev.reviewer_id
            request.session["reviewer_name"] = rev.reviewer_name
            request.session["reviewer_phone"] = rev.reviewer_phone
            return redirect("/shengaoren/")

    context = {"err1": err1, "err2": err2}
    return render(request, "denglu2.html", context)

# 审稿人页面
def lxt44(request):
    reviewer_id = request.session.get("reviewer_id", default="")
    reviewer_name = request.session.get("reviewer_name", default="")
    reviewer_phone = request.session.get("reviewer_phone", default="")
    ar = models.Article.objects.all()         # select * from article
    ll = list()
    r = models.ArticleResult.objects.all()       # select * from article_result
    if r.exists():
        for i in r:
            ll.append(int(i.article_id))

    if not ar.exists():
        ar = []

    if request.method == "POST":
        idd = request.POST.get("id")
        arr = models.Article.objects.get(article_id=idd)      # select * from article where article_id=idd
        id = arr.article_id
        title = arr.title
        content = arr.content
        request.session["arr_id"] = id
        request.session["title"] = title
        request.session["content"] = content
        return redirect("/shengao/")

    context = {"id": reviewer_id, "name": reviewer_name, "phone": reviewer_phone, "time": time, "ar": ar,"ll":ll}
    return render(request, "shengaoren.html", context)

# 审稿页面
def lxt444(request):
    id = request.session.get("arr_id", default="")
    title = request.session.get("title", default="")
    content = request.session.get("content", default="")
    r_id = request.session.get("reviewer_id", default="")
    if request.method == "POST":
        r = RA()
        pas = request.POST.get("pass")
        if pas=="是":
            request.session["statue"] = "审查通过"

            rr = models.Article.objects.filter(article_id=id)[0]       # select * from article where article_id=id
            user_id=rr.author_id
            money = len(rr.content) * 0.05
            money2 = len(rr.content) * 0.01
            au = AuthorM()               # insert into author_m values(user_id,id,money)
            au.author_id = user_id
            au.article_id = id
            au.article_money = money
            au.save()

            money1=money*0.3
            ar=ArticleM()               # insert into article_m values(id,money1)
            ar.article_id=id
            ar.article_money = money1
            ar.save()


        else:
            request.session["statue"] = "审查未通过"
            rr = models.Article.objects.filter(article_id=id)[0]     # select * from article where article_id=id
            money2 = len(rr.content) * 0.01
        r.article_id = id          # insert into r_a values(id,r_id,time1,pas)
        r.reviewer_id = r_id
        r.time=time1
        r.result = pas
        r.save()

        rv=ReviewerM()              # insert into reviewer_m values(r_id,id,money2,get)
        rv.reviewer_id=r_id
        rv.article_id=id
        rv.reviewer_money=money2
        rv.get="否"
        rv.save()

        ad=AdminPay()               # insert into admin_pay values(r_id,id,pay)
        ad.reviewer_id = r_id
        ad.article_id = id
        ad.pay = "未支付"
        ad.save()

        aar=ArticleResult()         # insert into article_result values(id,pas)
        aar.article_id=id
        aar.result=pas
        aar.save()

        return redirect("/shengaoren/")
    context={"id":id,"title":title,"content":content}
    return render(request,"shengao.html",context)

# 系统管理员注册界面
def lxt5(request):
    ad=models.Admin.objects.all()           # select * from admin
    err1=err2=err3=err4=err5=err6=""
    if request.method=="POST":
        flag=True
        id=request.POST.get("user1")
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        admin = Admin()
        if id=="":
            err1="账号不能为空"
            flag=False
        if pass1=="":
            err2 = "密码不能为空"
            flag = False
        if pass2=="":
            err3="确认密码是必填的"
            flag = False
        else:
            if pass1!=pass2:
                err3="密码不一致"
                flag = False
        if name=="":
            err4 = "姓名不能为空"
            flag = False
        if phone=="":
            err5 = "联系电话不能为空"
            flag = False

        if flag==True:
            t=1
            for i in ad:
                if id==i.admin_id:
                    t=0
                    break
            if t==1:
                admin.admin_id=id        # insert into admin values(id,pass1,name,phone)
                admin.admin_pass=pass1
                admin.admin_name=name
                admin.admin_phone=phone
                admin.save()
                return redirect('/denglu/')
            else:
                err1="用户已存在"
    context = {"err1": err1, "err2": err2, "err3": err3, "err4": err4, "err5": err5, "err6": err6}
    return render(request, "zhuce.html", context)

# 投稿人注册界面
def lxt6(request):
    au = models.Author.objects.all()          # select * from author
    err1 = err2 = err3 = err4 = err5 = err6 = err7 = ""
    if request.method == "POST":
        flag = True
        id = request.POST.get("user")
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        adress = request.POST.get("adress")
        author = Author()
        if id == "":
            err1 = "账号不能为空"
            flag = False
        if pass1 == "":
            err2 = "密码不能为空"
            flag = False
        if pass2 == "":
            err3 = "确认密码是必填的"
            flag = False
        else:
            if pass1 != pass2:
                err3 = "密码不一致"
                flag = False
        if name == "":
            err4 = "姓名不能为空"
            flag = False
        if phone == "":
            err5 = "联系电话不能为空"
            flag = False
        if email == "":
            err6 = "邮箱不能为空"
            flag = False
        else:
            ret = re.findall(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{2,3}$', str(email))
            if not ret:
                err6="邮箱格式错误"
                flag=False
        if adress == "":
            err7 = "地址不能为空"
            flag = False

        if flag == True:
            t = 1
            for i in au:
                if id == i.author_id:
                    t = 0
                    break
            if t == 1:
                author.author_id = id       # insert into author values(id,pass1,name,phone,email,adress)
                author.author_pass = pass1
                author.author_name = name
                author.author_phone = phone
                author.author_email = email
                author.author_adress = adress
                author.save()
                return redirect('/denglu1/')
            else:
                err1 = "用户已存在"
    context = {"err1": err1, "err2": err2, "err3": err3, "err4": err4, "err5": err5, "err6": err6,"err7":err7}
    return render(request, "zhuce1.html", context)

# 投稿人修改密码
def lxt7(request):
    err1 = err2 = err3 = ""
    user_id=request.session.get("user_id",default="")
    au=models.Author.objects.get(author_id=user_id)      # select * from author where author_id=user_id
    if request.method == "POST":
        flag = True
        passs = request.POST.get("password")
        pass11 = request.POST.get("password1")
        pass22 = request.POST.get("password2")

        if passs=="":
            err1="密码不能为空"
            flag = False
        else:
            if passs!=au.author_pass:
                err1="密码错误"
                flag = False
            else:
                if pass11 == "":
                    err2 = "新密码不能为空"
                    flag = False
                else:
                    if pass22 != pass11:
                        err3 = "确认密码错误"
                        flag = False
        if flag == True:
            au.author_pass = pass11          # update author set author_pass where author_id=user_id
            au.save()
            return redirect('/denglu1/')

    context = {"err1": err1, "err2": err2, "err3": err3}
    return render(request, "gai1.html", context)

# 投稿人修改个人信息
def lxt8(request):
    err1 = err2 = err3 = err4=""
    user_id = request.session.get("user_id", default="")
    au = models.Author.objects.get(author_id=user_id)    # select * from author where author_id=user_id
    if request.method == "POST":
        flag = True
        name = request.POST.get("name")
        phone= request.POST.get("phone")
        email = request.POST.get("email")
        adress = request.POST.get("adress")

        if name=="":
            err1="姓名不能为空"
            flag = False
        if phone=="":
            err2="联系电话不能为空"
            flag = False

        if email=="":
            err3="邮箱不能为空"
            flag = False
        else:
            ret = bool(re.match("^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", email))
            if ret == False:
                err3 = "邮箱格式错误"
                flag = False

        if adress=="":
            err4="地址不能为空"
            flag = False

        if flag == True:
            au.author_name = name                # update author
            au.author_phone= phone               # set author_name=name,author_phone=phone,
            au.author_email = email              # author_email=email,author_adress=adress
            au.author_adress = adress            # where author_id=user_id
            au.save()
            request.session["user_name"] = name
            request.session["user_phone"] = phone
            request.session["user_email"] = email
            request.session["user_adress"] = adress
            return redirect('/tougaoren/')

    context = {"err1": err1, "err2": err2, "err3": err3,"err4":err4}
    return render(request, "gai2.html", context)

# 投稿界面
def lxt9(request):
    err1 = err2 = ""
    flag = True
    if request.method == "POST":
        title = request.POST.get("title")
        type = request.POST.get("type")
        content = request.POST.get("content")
        if title == "":
            err1 = "标题不能为空"
            flag = False
        if content=="":
            err2="内容是必写的"
            flag = False
        else:
            if len(content)>10000:
                err2="字数最多为10000字"
                flag = False

        if flag == True:
            user_id = request.session.get("user_id", default="")
            article=Article()
            k = models.Article.objects.all().aggregate(Max('article_id'))
            if k['article_id__max'] is None:                              # select max(article_id) from article
                article.article_id = 1
            else:
                article.article_id = k['article_id__max'] + 1

            article.title= title
            article.type= type           # insert into article values(title,type,content,user_id,time1)
            article.content= content
            article.author_id= user_id
            article.time = time1
            article.save()

            return redirect("/tougaoren/")
    context = {"err1": err1, "err2": err2}
    return render(request,"tougao.html",context)

# 系统管理员修改密码
def lxt10(request):
    err1 = err2 = err3 = ""
    admin_id = request.session.get("admin_id", default="")
    ad = models.Admin.objects.get(admin_id=admin_id)           # select * from admin where admin_id='admin_id'
    if request.method == "POST":
        flag = True
        passs = request.POST.get("password")
        pass11 = request.POST.get("password1")
        pass22 = request.POST.get("password2")

        if passs == "":
            err1 = "密码不能为空"
            flag = False
        else:
            if passs != ad.admin_pass:
                err1 = "密码错误"
                flag = False
            else:
                if pass11 == "":
                    err2 = "新密码不能为空"
                    flag = False
                else:
                    if pass22 != pass11:
                        err3 = "确认密码错误"
                        flag = False
        if flag == True:
            ad.admin_pass = pass11        # update admin set admin_pass=pass11 where admin_id='admin_id'
            ad.save()
            return redirect('/denglu/')

    context = {"err1": err1, "err2": err2, "err3": err3}
    return render(request, "gai3.html", context)

# 系统管理员修改个人信息
def lxt11(request):
    err1 = err2 = err3 = err4=""
    admin_id = request.session.get("admin_id", default="")
    ad = models.Admin.objects.get(admin_id=admin_id)      # select * from admin where admin_id='admin_id'
    if request.method == "POST":
        flag = True
        name = request.POST.get("name")
        phone= request.POST.get("phone")

        if name=="":
            err1="姓名不能为空"
            flag = False
        if phone=="":
            err2="联系电话不能为空"
            flag = False

        if flag == True:
            ad.admin_name = name        # update admin set admin_name=name,admin_phone=phone where admin_id='admin_id'
            ad.admin_phone = phone
            ad.save()
            request.session["admin_name"] = name
            request.session["admin_phone"] = phone
            return redirect('/guanliyuan/')

    context = {"err1": err1, "err2": err2, "err3": err3,"err4":err4}
    return render(request, "gai4.html", context)

# 审稿人注册页面
def lxt12(request):
    re=models.Reviewer.objects.all()        # select * from reviewer
    err1=err2=err3=err4=err5=err6=""
    if request.method=="POST":
        flag=True
        id=request.POST.get("user1")
        pass1 = request.POST.get("password1")
        pass2 = request.POST.get("password2")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        reviewer = Reviewer()
        ra=ReviewerAdmin()
        if id=="":
            err1="账号不能为空"
            flag=False
        if pass1=="":
            err2 = "密码不能为空"
            flag = False
        if pass2=="":
            err3="确认密码是必填的"
            flag = False
        else:
            if pass1!=pass2:
                err3="密码不一致"
                flag = False
        if name=="":
            err4 = "姓名不能为空"
            flag = False
        if phone=="":
            err5 = "联系电话不能为空"
            flag = False

        if flag==True:
            t=1
            for i in re:
                if id==i.reviewer_id:
                    t=0
                    break
            if t==1:
                admin_id = request.session.get("admin_id",default="")
                reviewer.reviewer_id=id
                reviewer.reviewer_pass=pass1         # insert into reviewer values(id,pass1,name,phone)
                reviewer.reviewer_name=name
                reviewer.reviewer_phone=phone
                reviewer.save()

                ra.admin_id=admin_id                # insert into reviewer_admin values(admin_id,id)
                ra.reviewer_id=id
                ra.save()
                return redirect('/guanliyuan/')
            else:
                err1="用户已存在"
    context = {"err1": err1, "err2": err2, "err3": err3, "err4": err4, "err5": err5, "err6": err6}
    return render(request, "zhuce2.html", context)

# 审稿人修改密码
def lxt13(request):
    err1 = err2 = err3 = ""
    reviewer_id = request.session.get("reviewer_id", default="")
    re = models.Reviewer.objects.get(reviewer_id=reviewer_id)  # select * from reviewer where reviewer_id='reviewer_id'
    if request.method == "POST":
        flag = True
        passs = request.POST.get("password")
        pass11 = request.POST.get("password1")
        pass22 = request.POST.get("password2")

        if passs == "":
            err1 = "密码不能为空"
            flag = False
        else:
            if passs != re.reviewer_pass:
                err1 = "密码错误"
                flag = False
            else:
                if pass11 == "":
                    err2 = "新密码不能为空"
                    flag = False
                else:
                    if pass22 != pass11:
                        err3 = "确认密码错误"
                        flag = False
        if flag == True:
            re.reviewer_pass = pass11    # update reviewer set reviewer_pass=pass11 where reviewer_id='reviewer_id'
            re.save()
            return redirect('/denglu2/')

    context = {"err1": err1, "err2": err2, "err3": err3}
    return render(request, "gai5.html", context)

# 审稿人修改个人信息
def lxt14(request):
    err1 = err2 = err3 = err4=""
    reviewer_id = request.session.get("reviewer_id", default="")
    re = models.Reviewer.objects.get(reviewer_id=reviewer_id)  # select * from reviewer where reviewer_id='reviewer_id'
    if request.method == "POST":
        flag = True
        name = request.POST.get("name")
        phone= request.POST.get("phone")

        if name=="":
            err1="姓名不能为空"
            flag = False
        if phone=="":
            err2="联系电话不能为空"
            flag = False

        if flag == True:
            re.reviewer_name = name
            re.reviewer_phone = phone
            re.save()     # update reviewer set reviewer_name=name,reviewer_phone=phone where reviewer_id='reviewer_id'
            request.session["reviewer_name"] = name
            request.session["reviewer_phone"] = phone
            return redirect('/shengaoren/')

    context = {"err1": err1, "err2": err2, "err3": err3,"err4":err4}
    return render(request, "gai6.html", context)

# 管理员审阅信息
def lxt15(request):
    admin_id = request.session.get("admin_id", default="")
    ree = models.ReviewerAdmin.objects.filter(admin_id=admin_id)
    ll=list()                                    # select * from reviewer_admin where admin_id='admin_id'
    for i in ree:
        ra = models.RA.objects.filter(reviewer_id=i.reviewer_id)
        for j in ra:                             # select * from r_a where reviewer_id=i.reviewer_id
            if j.result=="否":
                j.result="审核未通过"
            if j.result=="是":
                j.result="审核通过"
            ll.append(j)
    return render(request,"shenyuexinxi.html",{"ll":ll})

# 管理员审稿人信息
def lxt16(request):
    admin_id = request.session.get("admin_id", default="")
    ree = models.ReviewerAdmin.objects.filter(admin_id=admin_id)
    ll = list()                                    # select * from reviewer_admin where admin_id='admin_id'
    for i in ree:
        rev = models.Reviewer.objects.filter(reviewer_id=i.reviewer_id)[0]
        ll.append(rev)                           # select * from reviewer where reviewer_id=i.reviewer_id

    if request.method == "POST":
        idd = request.POST.get("id")
        models.Reviewer.objects.get(reviewer_id=idd).delete()     # delete from reviewer where reviewer_id=idd
        models.ReviewerAdmin.objects.get(reviewer_id=idd).delete()   # delete from reviewer_admin where reviewer_id=idd
        return redirect("/shenxinxi/")

    return render(request,"shenxinxi.html",{"ll":ll})

# 存储过程查看作者信息
def lxt17(request):
    lis = request.session.get("lis", default="")
    rr = models.Article.objects.all()        # select * from article
    for i in lis:
        for j in rr:
            if str(i[1]) == str(j.article_id):
                i.append(str(j.time))
                continue
    return render(request,"zuozhexinxi.html",{"lis":lis})

# 稿费和版面费
def lxt18(request):
    user_id = request.session.get("user_id", default="")
    au = models.AuthorM.objects.filter(author_id=user_id)   # select * from author_m where author_id=user_id
    ar = models.ArticleM.objects.all()                      # select * from article_m
    return render(request,"gaofei.html",{"au":au,"ar":ar})

# 审稿人费用
def lxt19(request):
    reviewer_id = request.session.get("reviewer_id", default="")
    rr = models.ReviewerM.objects.filter(reviewer_id=reviewer_id)
    return render(request,"shenf.html",{"rr":rr})           # select * from reviewer_m where reviewer_id='reviewer_id'

# 系统管理员查看投稿人费用
def lxt20(request):
    ar = models.AuthorM.objects.all()            # select * from author_m
    return render(request,"sgf.html",{"ar":ar})

# 系统管理员查看稿件版面费
def lxt21(request):
    ar = models.ArticleM.objects.all()           # select * from article_m
    return render(request,"gf.html",{"ar":ar})

# 系统管理员查看审稿人费用
def lxt23(request):
    if request.method == "POST":
        idd = request.POST.get("id")
        add = models.AdminPay.objects.filter(article_id=idd)[0]     # select * from admin_pay where article_id=idd
        a_id = add.article_id
        pay = add.pay
        if pay=="未支付":                                     # update admin_pay set pay='已支付' where article_id=a_id
            models.AdminPay.objects.filter(article_id=a_id).update(pay="已支付")

        admin_id = request.session.get("admin_id", default="")
        ree = models.ReviewerAdmin.objects.filter(admin_id=admin_id)
        k = list()  # select * from reviewer_admin where admin_id='admin_id'
        for i in ree:
            k.append(i.reviewer_id)

        admin_id = request.session.get("admin_id", default="")
        ree = models.ReviewerAdmin.objects.filter(admin_id=admin_id)
        k = list()                                      # select * from reviewer_admin where admin_id='admin_id'
        for i in ree:
            r = models.ReviewerM.objects.filter(reviewer_id=i.reviewer_id)
            for j in r:                                 # select * from reviewer_m where reviewer_id=i.reviewer_id
                k.append(j)

        r = models.ReviewerM.objects.all()                  # select * from reviewer_m
        ll=list()
        for i in r:
            if i.get=="是":
                ll.append(i.article_id)
        return render(request, "sss.html", {"k": k, "ll": ll})

    admin_id = request.session.get("admin_id", default="")
    ree = models.ReviewerAdmin.objects.filter(admin_id=admin_id)
    k=list()                       # select * from reviewer_admin where admin_id='admin_id'
    for i in ree:
        r = models.ReviewerM.objects.filter(reviewer_id=i.reviewer_id)
        for j in r:                          # select * from reviewer_m where reviewer_id=i.reviewer_id
            k.append(j)

    ll = list()
    r = models.ReviewerM.objects.all()         # select * from reviewer_m
    for i in r:
        if i.get == "是":
            ll.append(i.article_id)
    return render(request,"sss.html",{"k":k,"ll": ll})

#投稿人更改稿件信息
def lxt24(request):
    id = request.session.get("id_gai", default="")
    arr = models.Article.objects.filter(article_id=id)[0]    # select * from article where article_id=id
    title = arr.title
    content = arr.content
    err1 = err2 = ""
    flag = True
    if request.method == "POST":
        title1 = request.POST.get("title")
        type1 = request.POST.get("type")
        content1 = request.POST.get("content")
        if title1 == "":
            err1 = "标题不能为空"
            flag = False
        if content1 == "":
            err2 = "内容是必写的"
            flag = False
        else:
            if len(content1) > 10000:
                err2 = "字数最多为10000字"
                flag = False

        if flag == True:   # update article set title=title1,type=type1,aontent=content1,time=time1 where article_id=id
            models.Article.objects.filter(article_id=id).update(title=title1)
            models.Article.objects.filter(article_id=id).update(type=type1)
            models.Article.objects.filter(article_id=id).update(content=content1)
            models.Article.objects.filter(article_id=id).update(time=time1)
            return redirect("/tougaoren/")

    return render(request,"genggai.html",{"id":id,"title":title,"content":content,"type":type,"err1":err1,"err2":err2})

# 审核结果
def lxt25(request):
    au = models.Author.objects.all()      # select * from author
    return render(request,"txx.html",{"au":au})

# 系统管理员查看稿件
def lxt26(request):
    idd = request.session.get("idgla", default="")
    axa=models.Article.objects.filter(article_id=idd)[0]    # select * from article where article_id=idd
    return render(request,"glyckgj.html",{"axa":axa.content})

def lxt27(request):
    r1 = models.RA.objects.filter(reviewer_id='111', article_id=1)[0]
    r2 = models.RA.objects.get(reviewer_id='111' , article_id=1)
    return render(request,"x.html",{"r":r})
