"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from pro import views
urlpatterns = [

    url(r'^myblog.html$', views.myblog),##主站
    url(r'^myblog/big-classify/(?P<type_id>\d+).html$', views.myblog),##大分类
    url(r'^myblog/big-classify.html$', views.myblog),
    url(r'^asaka/article/(?P<article_id>\d+).html$', views.article),##个人文章页
    url(r'^updown/', views.updown),##点赞，踩
    url(r'^asaka/(?P<type>\w+)/(?P<id>\w+-*\w*).html$', views.type),###个人首页
    url(r'^myblog/asaka.html$', views.type),
    url(r'^myblog/manager.html$', views.manager),##后台管理
    url(r'^myblog/manager/article.html$', views.article_manage),  ##后台文章管理
    url(r'^myblog/manager/article-(?P<article_type_id>\d+)-(?P<tags__nid>\d+)-(?P<category_id>\d+).html$', views.article_manage),#后台筛选
    url(r'^myblog/edit/(?P<num>\d+).html$', views.edit),###编辑文本内容
    url(r'^myblog/article_edit/(?P<nid>\d+).html$', views.edit_sub),##刷新页面，重新跳转



    url(r'^admin/', admin.site.urls),
]
