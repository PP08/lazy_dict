from django.db import models

# Create your models here.
# class Dictionary(models.Model):
#     word = models.CharField(max_length=200)
#     definition = models.TextField()
#     def __str__(self):
#         return self.word

class KeyWord(models.Model):
    keyWord = models.CharField(max_length=200)
    def __str__(self):
        return  self.keyWord