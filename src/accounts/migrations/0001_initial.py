# # Generated by Django 3.0 on 2022-06-13 11:22
#
# from django.db import migrations, models
# import django.db.models.deletion
#
#
# class Migration(migrations.Migration):
#
#     initial = True
#
#     dependencies = [
#         ('scraping', '0001_initial'),
#     ]
#
#     operations = [
#         migrations.CreateModel(
#             name='MyUser',
#             fields=[
#                 ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
#                 ('password', models.CharField(max_length=128, verbose_name='password')),
#                 ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
#                 ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
#                 ('is_active', models.BooleanField(default=True)),
#                 ('is_admin', models.BooleanField(default=False)),
#                 ('send_email', models.BooleanField(default=True)),
#                 ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scraping.City')),
#                 ('program_language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scraping.ProgramLanguage')),
#             ],
#             options={
#                 'abstract': False,
#             },
#         ),
#     ]
