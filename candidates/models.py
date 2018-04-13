from django.db import models


class Candidate(models.Model):
    name = models.CharField(max_length=250)
    key = models.IntegerField(primary_key=True)
    state = models.CharField(max_length=50)
    abbr = models.CharField(max_length=2)
    office = models.CharField(max_length=10)
    party = models.CharField(max_length=50)
    campaign_url = models.CharField(max_length=250)
    bp_url = models.CharField(max_length=250)
    emails = models.CharField(max_length=250, blank=True, null=True)
    facebook = models.CharField(max_length=100, blank=True, null=True)
    twitter = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'candidate'


class Primarydate(models.Model):
    key = models.IntegerField(primary_key=True)
    state = models.CharField(max_length=50)
    abbr = models.CharField(max_length=2)
    date = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'primarydate'
