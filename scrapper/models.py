from django.db import models


class Segment(models.Model):
    class Meta:
        db_table = 'scrapper_segment'

    name = models.CharField(max_length=255)


class Keyword(models.Model):
    class Meta:
        db_table = 'scrapper_keyword'

    segment = models.ForeignKey(Segment, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)


class Site(models.Model):
    class Meta:
        db_table = 'scrapper_site'

    url = models.URLField(max_length=1023)
    title = models.CharField(max_length=255)
    password = models.CharField(null=True, default=None, max_length=255)
    login = models.CharField(null=True, default=None, max_length=255)
    app_id = models.CharField(null=True, default=None, max_length=255)
    app_secret = models.CharField(null=True, default=None, max_length=255)
    limit = models.IntegerField(default=10)


class Task(models.Model):
    class Meta:
        db_table = 'scrapper_task'

    STATUS_IN_QUEUE = 0
    STATUS_PROCESSING = 1
    STATUS_COMPLETED = 2
    STATUS_ERROR = 3

    id = models.BigAutoField(primary_key=True)
    segment = models.CharField(max_length=255)
    keyword = models.CharField(max_length=255)
    status = models.SmallIntegerField(default=0)
    site = models.ForeignKey(Site, on_delete=models.PROTECT)
    limit = models.IntegerField(default=10)
    errors = models.TextField()
    total_found = models.IntegerField(default=0)
    search_params = models.TextField(null=True, default=None)
    scanned_at = models.DateTimeField(null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    class Meta:
        db_table = 'scrapper_profile'

    id = models.BigAutoField(primary_key=True)
    link = models.URLField(max_length=1023)
    name = models.CharField(null=True, default=None, max_length=255)
    lastname = models.CharField(null=True, default=None, max_length=255)
    email = models.EmailField(null=True, default=None)
    email_provider = models.CharField(null=True, default=None, max_length=255)
    phone = models.CharField(null=True, default=None, max_length=255)
    city = models.CharField(max_length=255)
    info = models.TextField(null=True, default=None, )
    segment = models.CharField(max_length=255)
    keyword = models.CharField(max_length=255)
    resume_id = models.CharField(null=True, default=None, max_length=1023)
    outer_id = models.CharField(null=True, default=None, max_length=1023)
    scanned_at = models.DateTimeField(null=True, default=None)
    scan_errors = models.TextField(null=True, default=None)
    duplicate = models.SmallIntegerField(default=0)

    task = models.ForeignKey(Task, on_delete=models.PROTECT)
    site = models.ForeignKey(Site, on_delete=models.PROTECT)


class RegionDict(models.Model):
    class Meta:
        db_table = 'scrapper_region_dict'

    id = models.BigAutoField(primary_key=True)
    site = models.ForeignKey(Site, on_delete=models.PROTECT)
    country_id = models.BigIntegerField()
    country_name = models.CharField(max_length=255)
    region_id = models.BigIntegerField()
    region_name = models.CharField(max_length=255)
    town_id = models.BigIntegerField()
    town_name = models.CharField(max_length=255)
