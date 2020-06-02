from django.db import models

# Create your models here.

class party(models.Model):
    party_a = models.CharField(db_column='party_A', max_length=512)  # Field name made lowercase.
    party_b = models.CharField(db_column='party_B', max_length=512)  # Field name made lowercase.
    party_c = models.CharField(db_column='party_C', max_length=512)  # Field name made lowercase.

    class Meta:
        ##managed = False
        db_table = 'party'
