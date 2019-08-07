# Generated by Django 2.2.4 on 2019-08-02 23:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.FloatField(default=50.0)),
                ('peopleMax', models.IntegerField(default=1)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.IntegerField(default=1)),
                ('startingDate', models.DateField()),
                ('creationDate', models.DateField(auto_now=True)),
                ('status', models.CharField(choices=[('conf', 'confirmada'), ('cIn', 'checkin'), ('cOut', 'checkout')], default='conf', max_length=4)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.Room')),
            ],
        ),
    ]