from django.db import models

# Create your models here.

class education_levels(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'education_levels'

class schools(models.Model):
    id = models.AutoField(primary_key=True)
    education_level_id = models.ForeignKey('education_levels', on_delete=models.CASCADE, null=False)
    npsn = models.CharField(max_length=50, null=False, db_index=True, unique=True)
    name = models.CharField(max_length=255,null=False)
    dns = models.CharField(max_length=255,null=False, unique=True, db_index= True)
    link_maps = models.CharField(max_length=255, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'schools'