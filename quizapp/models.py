from django.db import models
class User(models.Model):
    unique_id=models.CharField(max_length=50)
    name=models.CharField(max_length=100)
    email=models.EmailField()

class Option(models.Model):
    option=models.CharField(max_length=100)
    def __str__(self):
        return self.option

class Question(models.Model):
    question=models.CharField(max_length=500)
    options=models.ManyToManyField(Option,related_name='options_set')
    correct_option=models.CharField(max_length=100)
    def __str__(self):
        return self.question
class Test(models.Model):
    name=models.CharField(max_length=200,null=True)
    user=models.ManyToManyField(User)
    question=models.ManyToManyField(Question)
    def __str__(self):
        return self.name
class Person(models.Model):
    name=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    num=models.CharField(max_length=10)
    lost=models.BooleanField(default=False)
    found=models.BooleanField(default=True)
    img=models.ImageField(null=True)
    
        
    
      
    

    
    