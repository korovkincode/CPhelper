from django.db import models

class Users(models.Model):
	username = models.CharField(max_length = 20)
	password = models.CharField(max_length = 50)
	codeforces = models.CharField(max_length = 1)
	atcoder = models.CharField(max_length = 1)
	codechef = models.CharField(max_length = 1)