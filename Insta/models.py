from django.db import models
from imagekit.models import ProcessedImageField
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


# Create your models here.
# all class should inherit models.Model



class InstaUser(AbstractUser):
    profile_pic=ProcessedImageField(
        upload_to='static/images/profile',
        format='JPEG',
        options={'quality':100},
        blank=True,
        null=True
    )
    def get_connections(self):
        #get只能返回一个值，filter可以返回多个值
        connections=UserConnection.objects.filter(creator=self)
        return connections

    def get_followers(self):
        followers=UserConnection.objects.filter(following=self)
        return followers

    def is_followed_by(self,user):
        followers=UserConnection.objects.filter(following=self)
        return followers.filter(creator=user).exists()

class Post(models.Model):
    author=models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name='my_posts'
    )
    title=models.TextField(blank=True, null=True)
    image=ProcessedImageField(
        upload_to='static/images/posts',
        format='JPEG',
        options={'quality':100},
        blank=True,
        null=True,
    )
    #当有人创建新的post,或者对post进行修改，就会调用getabsoluteurl
    #当有人创建了新的post就会reverse到url.py中的name为helloworld对应的url
    #reverse:"helloworld"-->"www.hellowordl.com"将string反转成url
    def get_absolute_url(self):
        return reverse("post_detail",args=[str(self.id)])
    def get_like_count(self):
        return self.likes.count()
     




    #解释related_name='likes'
    #like1--> wentailai like post1
    #like2--> test like post1
    #当调用post1.likes-->(like1,like2)
    #wentailai.likes-->like1

class Like(models.Model):
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE,
        related_name='likes')
    user = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    class Meta:
        unique_together=("post","user")
        #同一个user和同一个post只能被定义一次
    
    def __str__(self):
        return 'Like:'+self.user.username+' likes '+self.post.title


class Comment(models.Model):
    post = models.name = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE)
    user = models.ForeignKey(InstaUser, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    posted_on = models.DateTimeField(auto_now_add=True, editable=False)
    
    def __str__(self):
        return self.comment



    #con1-->A follows B
    #A is creator
    #con2-->A follows C
    #con3-->D follows A
    #A.friendship_creator_set-->(con1,con2)
    #A.friend_set-->(con3)

class UserConnection(models.Model):
    created=models.DateTimeField(auto_now_add=True,editable=False)
    creator=models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friendship_creator_set"
    )
    following=models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="friend_set"
    )

    def __str__(self):
        return self.creator.username+' follows '+self.following.username


