# Generated by Django 2.1.5 on 2019-02-27 22:01

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompradeBultos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_bultos', models.PositiveSmallIntegerField()),
                ('responsable', models.CharField(blank=True, max_length=100, null=True)),
                ('fecha_registro', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_update', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Concentrado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('proteina', models.PositiveSmallIntegerField()),
                ('kilos', models.PositiveSmallIntegerField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=8)),
                ('total_kg', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.AddField(
            model_name='compradebultos',
            name='concentrado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.Concentrado'),
        ),
    ]
