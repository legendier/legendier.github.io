# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Admin(models.Model):
    admin_id = models.CharField(primary_key=True, max_length=20)
    admin_pass = models.CharField(max_length=10)
    admin_name = models.CharField(max_length=10)
    admin_phone = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'admin'


class AdminPay(models.Model):
    reviewer = models.ForeignKey('Reviewer', models.DO_NOTHING)
    article_id = models.IntegerField(primary_key=True)
    pay = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'admin_pay'


class Article(models.Model):
    article_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=20)
    type = models.CharField(max_length=10)
    content = models.CharField(max_length=10000)
    author = models.ForeignKey('Author', models.DO_NOTHING)
    time = models.DateField()

    class Meta:
        managed = False
        db_table = 'article'


class ArticleM(models.Model):
    article_id = models.IntegerField(primary_key=True)
    article_money = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'article_m'


class ArticleResult(models.Model):
    article_id = models.CharField(primary_key=True, max_length=20)
    result = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'article_result'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Author(models.Model):
    author_id = models.CharField(primary_key=True, max_length=20)
    author_pass = models.CharField(max_length=20)
    author_name = models.CharField(max_length=10)
    author_phone = models.IntegerField()
    author_email = models.CharField(max_length=20)
    author_adress = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'author'


class AuthorM(models.Model):
    author = models.ForeignKey(Author, models.DO_NOTHING)
    article_id = models.IntegerField(primary_key=True)
    article_money = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'author_m'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class RA(models.Model):
    article_id = models.IntegerField(primary_key=True)
    reviewer = models.ForeignKey('Reviewer', models.DO_NOTHING)
    time = models.DateField()
    result = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'r_a'


class Reviewer(models.Model):
    reviewer_id = models.CharField(primary_key=True, max_length=20)
    reviewer_pass = models.CharField(max_length=20)
    reviewer_name = models.CharField(max_length=10)
    reviewer_phone = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'reviewer'


class ReviewerAdmin(models.Model):
    admin = models.ForeignKey(Admin, models.DO_NOTHING)
    reviewer_id = models.CharField(primary_key=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'reviewer_admin'


class ReviewerM(models.Model):
    reviewer = models.ForeignKey(Reviewer, models.DO_NOTHING)
    article_id = models.IntegerField(primary_key=True)
    reviewer_money = models.IntegerField()
    get = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'reviewer_m'
