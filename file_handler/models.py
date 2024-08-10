from django.db import models
from users.models import UserAccount  
#from django.contrib.postgres.fields import JSONField # FOR POSTGRES


class UserProjects(models.Model):
    title = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class UserProjectsData(models.Model):
    project_id = models.ForeignKey(UserProjects, on_delete=models.CASCADE)
    Data_Id = models.CharField(max_length=255)
    Label = models.CharField(max_length=255)
    Modularity_Class = models.CharField(max_length=255)
    Pageranks = models.CharField(max_length=255)
    Custom_Filter = models.CharField(max_length=255)
    X = models.CharField(max_length=255)
    Y = models.CharField(max_length=255)
    Size = models.CharField(max_length=255)
    Color = models.CharField(max_length=255)
    Level1 = models.CharField(max_length=255)  # Yeni sütun

    def __str__(self):
        return f"{self.project_id.title} - {self.Data_Id}"



class UserProjectShapes(models.Model):
    project = models.ForeignKey(UserProjects, on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    shape_data = models.JSONField()

    def __str__(self):
        return f"{self.project.title} - {self.user.email}"
    


class AllLabels(models.Model):
    data_id = models.CharField(max_length=255)  # Benzersiz bir tanımlayıcı
    label = models.CharField(max_length=255)  # Etiket, benzersiz olmalı