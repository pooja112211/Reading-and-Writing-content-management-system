from django.db import models

# Create your models here.
class Types(models.Model):
    type_name=models.CharField( max_length=50)
    type_img=models.ImageField(upload_to='images/',
        null=True,
        blank=True)
    desc=models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return self.type_name
    
class Category(models.Model):
    name=models.CharField( max_length=50)
    img=models.ImageField(upload_to='cat', null=True, blank=True)
    type=models.ForeignKey(Types, on_delete=models.CASCADE, null=True, blank=True)
    desc=models.CharField( max_length=500)

    def __str__(self):
        return self.name    
    
class Novel(models.Model):
    name=models.CharField(max_length=50)
    img=models.ImageField(upload_to='novel/', null=True,blank=True)
    cat=models.ForeignKey(Types,on_delete=models.CASCADE, null=True,blank=True)
    type=models.ForeignKey(Category,on_delete=models.CASCADE, null=True,blank=True)
    desc=models.CharField(max_length=500)

    def __str__(self):
        return self.name
    

class Movies(models.Model):
    name=models.CharField(max_length=50)
    img=models.ImageField(upload_to='movies/', null=True,blank=True)
    cat=models.ForeignKey(Types, on_delete=models.CASCADE, null=True,blank=True)
    type=models.ForeignKey(Category,on_delete=models.CASCADE, null=True,blank=True)
    desc=models.CharField(max_length=500)

    def __str__(self):
        return self.name
    

class Series(models.Model):
    name=models.CharField(max_length=50)
    img=models.ImageField(upload_to='series/', null=True,blank=True)
    cat=models.ForeignKey(Types,on_delete=models.CASCADE , null=True,blank=True)
    type=models.ForeignKey(Category,on_delete=models.CASCADE, null=True,blank=True)
    desc=models.CharField(max_length=500)

    def __str__(self):
        return self.name
    

class Collection(models.Model):
    name=models.CharField(max_length=50)
    category=models.ForeignKey(Types, on_delete=models.CASCADE)
    img=models.ImageField(upload_to='coll/', null=True,blank=True)
    pdf=models.FileField(upload_to='pdfs/', null=True,blank=True)
    desc=models.CharField(max_length=500)

    def __str__(self):
        return self.name    



  