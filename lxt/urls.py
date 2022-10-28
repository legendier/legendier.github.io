"""lxt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import re_path
from . import view
urlpatterns = [
    re_path('lxt/',view.lxt1),
    re_path('denglu/',view.lxt2),
    re_path('guanliyuan/',view.lxt22),
    re_path('denglu1/',view.lxt3),
    re_path('tougaoren/',view.lxt33),
    re_path('denglu2/',view.lxt4),
    re_path('shengaoren/',view.lxt44),
    re_path('shengao/',view.lxt444),
    re_path('zhuce/',view.lxt5),
    re_path('zhuce1/',view.lxt6),
    re_path('gai1/',view.lxt7),
    re_path('gai2/',view.lxt8),
    re_path('tougao/',view.lxt9),
    re_path('gai3/',view.lxt10),
    re_path('gai4/',view.lxt11),
    re_path('zhuce2/',view.lxt12),
    re_path('gai5/',view.lxt13),
    re_path('gai6/',view.lxt14),
    re_path('shenyuexinxi/',view.lxt15),
    re_path('shenxinxi/',view.lxt16),
    re_path('zuozhexinxi/', view.lxt17),
    re_path('gaofei/', view.lxt18),
    re_path('shenf/', view.lxt19),
    re_path('sgf/', view.lxt20),
    re_path('gf/', view.lxt21),
    re_path('sss/', view.lxt23),
    re_path('genggai/', view.lxt24),
    re_path('txx/', view.lxt25),
    re_path('glyckgj/', view.lxt26),
    re_path('x/', view.lxt27),
]
