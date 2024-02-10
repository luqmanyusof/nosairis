# Generated by Django 5.0.2 on 2024-02-10 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PingData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('switch_label', models.CharField(max_length=3)),
                ('t1', models.IntegerField()),
                ('t2', models.IntegerField()),
                ('t3', models.IntegerField()),
                ('t4', models.IntegerField()),
                ('t5', models.IntegerField()),
                ('ping_status', models.IntegerField()),
                ('ping_time', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=20)),
            ],
        ),
    ]