from django.shortcuts import render,HttpResponse,redirect
from pro import models
from static.utils import pager
from django.db.models import Count
from django.db.models import F
###主站
def myblog(request,*args,**kwargs):
    condition={}
    type_id=int(kwargs.get('type_id'))if kwargs.get('type_id') else None
    if type_id:
        condition['article_type_id']=type_id
    type_choice=models.Article.type_choices
    all_counts=models.Article.objects.all().count()
    page_info=pager.Pager(request.GET.get('page'),all_counts,5,request.path_info)
    article=models.Article.objects.filter(**condition).values(
        'title','summary','comment_count','read_count','blog__user__username','up_count','down_count',
        'create_time','nid'
    )[page_info.start_index():page_info.stop_index()]
    top_post=models.Article.objects.values('read_count','title','nid').order_by('-read_count')
    comment_post=models.Article.objects.values('comment_count','title','nid').order_by('-comment_count')
    return render(request,'blog.html',{'type_choice':type_choice,'article':article,
                                       'page_info':page_info,'top_post':top_post,
                                       'comment_post':comment_post,'type_id':type_id})

###个人文章页
def article(request,*args,**kwargs):
    blog=models.Blog.objects.filter(user__nid=1)
    article_id=kwargs.get('article_id')
    user=models.UserInfo.objects.filter(blog=blog).values('nickname','email')
    ##关注
    bozhu=models.UserFans.objects.filter(user__nid=1).values('user').annotate(c=Count('nid')).first()
    ##粉丝
    fan=models.UserFans.objects.filter(follower__nid=1).values('follower').annotate(c=Count('nid')).first()
    ##标签
    tag=models.Article2Tag.objects.filter(article__blog=blog).values('tag__title','tag__nid').annotate(c=Count('nid'))
    ##分类
    category=models.Article.objects.filter(blog=blog).values('category__title','category__nid').annotate(c=Count('nid'))
    ##时间
    ctime=models.Article.objects.filter(blog=blog).extra(select={'ctime':"date_format(create_time,'%%Y-%%m')"}).values('ctime').annotate(c=Count('nid'))
    ##获取文章内容
    content=models.ArticleDetail.objects.filter(article__nid=article_id).values('article__title','content','article__up_count','article__down_count','article__nid').first()
    return render(request,'article.html',{'user':user,'fan':fan,'bozhu':bozhu,'tag':tag,
                                          'category':category,'ctime':ctime,'content':content})

##点赞，踩
def updown(request):
    article_id=request.GET.get('article')
    val=request.POST.get('val')
    obj=models.UpDown.objects.filter(user__nid=1,article__nid=article_id)
    if obj:
        return HttpResponse('不能重复点')
    else:
        from django.db import transaction
        with transaction.atomic():
            if val == '1':
                models.UpDown.objects.create(user_id=1,article_id=article_id,up=1)
                models.Article.objects.filter(nid=article_id).update(up_count=F('up_count')+1)
            else:
                models.UpDown.objects.create(user_id=1,article_id=article_id,up=0)
                models.Article.objects.filter(nid=article_id).update(down_count=F('down_count')+1)
    return HttpResponse('ok')

##个人主页
def type(request,*args,**kwargs):
    blog=models.Blog.objects.filter(user__nid=1)
    type=kwargs.get('type')
    id=kwargs.get('id')
    user=models.UserInfo.objects.filter(blog=blog).values('nickname','email')
    ##关注
    bozhu=models.UserFans.objects.filter(user__nid=1).values('user').annotate(c=Count('nid')).first()
    ##粉丝
    fan=models.UserFans.objects.filter(follower__nid=1).values('follower').annotate(c=Count('nid')).first()
    # ##标签
    tag=models.Article2Tag.objects.filter(article__blog=blog).values('tag__title','tag__nid').annotate(c=Count('nid'))
    ##分类
    category=models.Article.objects.filter(blog=blog).values('category__title','category__nid').annotate(c=Count('nid'))
    ##时间
    ctime=models.Article.objects.filter(blog=blog).extra(select={'ctime':"date_format(create_time,'%%Y-%%m')"}).values('ctime').annotate(c=Count('nid'))
    ##获取文章内容
    if type == 'tag':
        count = models.Article.objects.filter(blog=blog, article2tag__tag_id=id).count()
        page_info = pager.Pager(request.GET.get('page'), count, 5, request.path_info)
        content=models.Article.objects.filter(blog=blog,article2tag__tag_id=id).values('title','summary','comment_count','read_count','nid')[page_info.start_index():page_info.stop_index()]

    elif type == 'category':
        count = models.Article.objects.filter(blog=blog, category_id=id).count()
        page_info = pager.Pager(request.GET.get('page'), count, 5, request.path_info)
        content=models.Article.objects.filter(blog=blog,category_id=id).values('title','summary','comment_count','read_count','nid')[page_info.start_index():page_info.stop_index()]

    elif type == 'ctime':
        count = models.Article.objects.filter(blog=blog, create_time__startswith=id).count()
        page_info = pager.Pager(request.GET.get('page'), count, 5, request.path_info)
        content=models.Article.objects.filter(blog=blog,create_time__startswith=id).values('title','summary','comment_count','read_count','nid')[page_info.start_index():page_info.stop_index()]

    else:
        count = models.ArticleDetail.objects.all().count()
        page_info=pager.Pager(request.GET.get('page'),count,5,request.path_info)
        content=models.Article.objects.filter(blog=blog).values('title','summary','comment_count','read_count','nid')[page_info.start_index():page_info.stop_index()]



    ##分页

    return render(request,'type.html',{'user':user,'bozhu':bozhu,
                                          'category':category,'ctime':ctime,'content':content,'fan':fan,'tag':tag,
                                       'page_info':page_info
                                       })

##后台管理
def manager(request):
    return render(request,'manager.html')
##后台文章管理
def article_manage(request,*args,**kwargs):
    blog = models.Blog.objects.filter(user__nid=1)
    condition = {}
    for k, v in kwargs.items():
        kwargs[k] = int(v)
        if v != '0':
            condition[k] = v
    ##大分类
    type_list = models.Article.type_choices
    ##个人标签
    tag_list = models.Tag.objects.filter(blog=blog)
    ##个人分类
    category_list = models.Category.objects.filter(blog=blog)
    ##有以上分类的全部文章
    all_counts = models.Article.objects.filter(**condition).count()
    page_info=pager.Pager(request.GET.get('page'),all_counts,3,request.path_info)
    article_list = models.Article.objects.filter(**condition)[page_info.start_index():page_info.stop_index()]

    return render(request,'article_manage.html',{'type_list':type_list,'category_list':category_list,'tag_list':tag_list,
                                                 'article_list':article_list,'kwargs':kwargs,'page_info':page_info})

##后台文章编辑
def edit(request,**kwargs):
    num=kwargs.get('num')
    print(num)
    article_list=models.Article.objects.filter(nid=num).values('nid','title','summary','articledetail__content')
    return render(request,'edit.html',{'article_list':article_list})

def edit_sub(request,**kwargs):
    nid=kwargs.get('nid')
    print(nid)
    title=request.POST.get('title')
    content=request.POST.get('content')
    print(title)
    print(content)
    models.Article.objects.filter(nid=nid).update(title=title)
    models.ArticleDetail.objects.filter(nid=nid).update(content=content)
    return redirect('/myblog/manager/article.html')