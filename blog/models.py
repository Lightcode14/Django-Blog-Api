from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
 title=models.CharField(max_length=100)
 author=models.ForeignKey(User,on_delete=models.CASCADE)
 content=models.TextField()
 created_at=models.DateTimeField(auto_now_add=True)
 updated_at=models.DateTimeField(auto_now=True)
 featured_image=models.ImageField(upload_to="post_pics",blank=True,null=True)
 published=models.BooleanField(default=False)
 slug=models.SlugField(unique=True)
 category = models.ForeignKey("Category", on_delete=models.CASCADE)


 
def __str__(self):
        return self.title


class Category(models.Model):
 name=models.CharField(max_length=100)
 slug=models.SlugField(unique=True)

 
def __str__(self):
        return self.name


class Comment(models.Model):
  post=models.ForeignKey(Post,on_delete=models.CASCADE)
  author=models.ForeignKey(User,on_delete=models.CASCADE)
  body=models.TextField()
  created_at=models.TimeField(auto_now_add=True)

  
  def __str__(self):
        return self.body
