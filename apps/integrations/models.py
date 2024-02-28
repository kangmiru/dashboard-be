from django.db import models
from apps.institutions.models import institutions, pic_institutions
from apps.schools.models import schools

class institution_schools(models.Model):
    id = models.AutoField(primary_key=True)
    institution_id = models.ForeignKey(institutions, on_delete=models.CASCADE, null=False)
    school_id = models.ForeignKey(schools, on_delete=models.CASCADE, null=True, default=None, blank=False)
    created_by = models.ForeignKey(pic_institutions, on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(null=True, auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    def __str__(self):
        return self.institution_id.name

    class Meta:
        db_table = 'institution_schools'

class institution_school_verifications(models.Model):
    id = models.AutoField(primary_key=True)
    institution_school_id = models.ForeignKey(institution_schools, on_delete=models.CASCADE, null=False)
    status_choices = [
        ("1", "pending"),
        ("2", "accepted"),
        ("3", "rejected")
    ]
    status = models.CharField(max_length=1, null=False, default="1",choices=status_choices, db_index=True)
    verified_by = models.BigIntegerField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    def __str__(self):
        return self.institution_school_id.institution_id.name

    class Meta:
        db_table = 'institution_school_verification'

class integrations(models.Model):
    id = models.AutoField(primary_key=True)
    pic_id = models.ForeignKey(pic_institutions, on_delete=models.CASCADE, null=False)
    school_id = models.ForeignKey(schools, on_delete=models.CASCADE, null=True, default=None, blank=False)
    status_choices = [
        ("1", "pending"),
        ("2", "accepted"),
        ("3", "rejected")
    ]
    status = models.CharField(max_length=1, null=False, default="1",choices=status_choices, db_index=True)
    status_read_choices = [
        ("0", "not read yet"),
        ("1", "has been read")
    ]
    status_read = models.CharField(max_length=1, null=False, default='0',choices=status_read_choices, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(null=True,  auto_now=True)
    
    def __str__(self):
        return self.school_id.name

    class Meta:
        db_table = 'integrations'