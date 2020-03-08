# Generated by Django 2.1.3 on 2020-03-08 00:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('qty', models.IntegerField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='fish',
            options={'verbose_name_plural': 'Fish'},
        ),
        migrations.AlterModelOptions(
            name='fisherman',
            options={'verbose_name_plural': 'Fishermen'},
        ),
        migrations.AlterModelOptions(
            name='retailer_inventory',
            options={'verbose_name_plural': 'Retailer Inventories'},
        ),
        migrations.AddField(
            model_name='sales',
            name='Fish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Fish'),
        ),
    ]