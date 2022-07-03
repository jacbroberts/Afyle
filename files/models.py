from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserStorageData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    dynamic_max = models.BooleanField(default=True)
    
    storage_used_kB = models.PositiveBigIntegerField(default=0) #upto 9,223,372,036,854,775,807 kB (~9,223,372,036 TB)
    storage_max_kB = models.PositiveBigIntegerField(default=0)
    
    bandwidth_upload_used_kB = models.PositiveIntegerField(default=0) #upto 2147483647 kB (~2 TB)
    bandwidth_upload_max_kB = models.PositiveIntegerField(default=0)
    
    bandwidth_download_used_kB = models.PositiveIntegerField(default=0)
    bandwidth_download_max_kB = models.PositiveIntegerField(default=0)

    files = models.JSONField(null=False, default=list)

    def __str__(self):
        return self.user
    

    
# files =[
#     {
#         "name": "name",
#         "upload_date": "jdl"
#         "size": "size",
#         "type": "type"
#     },
#     {
#         "name": "name",
#         "size": "size",
#         "type": "type"
#     },
#     {
#         "name": "name",
#         "size": "size",
#         "type": "type"
#     }
# ]
