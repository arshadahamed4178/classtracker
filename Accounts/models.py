from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Classe(models.Model):
    name = models.CharField(max_length=30)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        teacher_email = self.teacher.user.email if self.teacher else "<no-teacher>"
        return self.name + " : " + teacher_email

class Topic(models.Model):
    title = models.CharField(max_length=30)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        classe_name = self.classe.name if self.classe else "<no-class>"
        teacher_email = self.classe.teacher.user.email if (self.classe and self.classe.teacher) else "<no-teacher>"
        return self.title + " : " + classe_name + " : " + teacher_email
    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username + " : " + self.text[:20]