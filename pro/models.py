from django.db import models

class UserInfo(models.Model):
    """
    用户表
    """
    nid = models.BigAutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名',max_length=32,unique=True)
    password = models.CharField(verbose_name='密码',max_length=64)
    nickname = models.CharField(verbose_name='昵称',max_length=32)
    email = models.EmailField(verbose_name='邮箱',unique=True)
    avatar = models.ImageField(verbose_name='头像')
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    """
    auto_now_add = True，字段在实例第一次保存的时候会保存当前时间，不管你在这里是否对其赋值。但是之后的save()
    是可以手动赋值的。也就是新实例化一个model，想手动存其他时间，就需要对该实例save()
    之后赋值然后再save()。
    """
    # fans = models.ManyToManyField(verbose_name='粉丝们',
    #                               to='UserInfo',
    #                               through='',
    #                               related_name='f',
    #                               through_fields=('user','follower')
    #                               )
    def __str__(self):
        return '%s-%s'%(self.nid,self.username)


class Blog(models.Model):
    """
    博客信息
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题',max_length=64)
    site = models.CharField(verbose_name='个人博客后缀',max_length=32,unique=True)
    theme = models.CharField(verbose_name='博客主题',max_length=32)
    user = models.OneToOneField(to='UserInfo',to_field='nid')    # OneToOneField就是FK+unique
    def __str__(self):
        return '%s-%s'%(self.nid,self.title)


class UserFans(models.Model):
    """
    互粉关系表
    """
    nid = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(verbose_name='博主',to='UserInfo',to_field='nid',related_name='users')
    follower = models.ForeignKey(verbose_name='粉丝',to='UserInfo',to_field='nid',related_name='followers')

    class Meta:
        unique_together = [
            ('user','follower'),
        ]
    def __str__(self):
        return '%s-%s-%s'%(self.nid,self.user,self.follower)

class Category(models.Model):
    """
    博主个人文章分类表
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题',max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客',to='Blog',to_field='nid')
    def __str__(self):
        return '%s-%s'%(self.nid,self.title)


class ArticleDetail(models.Model):
    """
    文章详细表
    """
    nid = models.AutoField(primary_key=True,max_length=255)
    content = models.TextField(verbose_name='文章内容')
    article = models.OneToOneField(verbose_name='所属文章',to='Article',to_field='nid')
    def __str__(self):
        return '%s-%s'%(self.nid,self.content)


class UpDown(models.Model):
    """
    文章顶或踩
    """
    nid = models.BigAutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='文章',to='Article',to_field='nid')
    user = models.ForeignKey(verbose_name='赞或踩用户',to='UserInfo',to_field='nid')
    up =models.BooleanField(verbose_name='是否赞')

    class Meta:
        unique_together = [
            ('article','user'),
        ]
    def __str__(self):
        return '%s-%s'%(self.nid,self.article)


class Comment(models.Model):
    """
    评论表
    """
    nid = models.BigAutoField(primary_key=True)
    content = models.CharField(verbose_name='评论内容',max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)

    reply = models.ForeignKey(verbose_name='回复评论',to='self',related_name='back',null=True)
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='nid')
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='nid')
    def __str__(self):
        return '%s'%(self.nid)


class Tag(models.Model):
    """
    标签表
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')
    def __str__(self):
        return '%s-%s'%(self.nid,self.title)


class Article(models.Model):
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='文章标题', max_length=128)
    summary = models.CharField(verbose_name='文章简介', max_length=255)
    read_count = models.IntegerField(default=0)         #阅读数量
    comment_count = models.IntegerField(default=0)      #评论数量
    up_count = models.IntegerField(default=0)           #点赞数量
    down_count = models.IntegerField(default=0)         #踩一下数量
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')
    category = models.ForeignKey(verbose_name='所属分类', to='Category', to_field='nid', null=True)

    type_choices = [
        (1, "Python"),
        (2, "Linux"),
        (3, "HTML"),
        # (4, "GoLang"),
    ]

    article_type_id = models.IntegerField(choices=type_choices, default=None)

    tags = models.ManyToManyField(
        to="Tag",
        through='Article2Tag',
        through_fields=('article', 'tag'),
    )
    def __str__(self):
        return '%s-%s'%(self.nid,self.title)

class Article2Tag(models.Model):
    """
    标签文章关系表
    """
    nid = models.CharField(primary_key=True,max_length=255)
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='nid')
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='nid')


    class Meta:
        unique_together = [
            ('tag', 'article'),
        ]

    def __str__(self):
        return '%s-%s'%(self.nid,self.tag)

