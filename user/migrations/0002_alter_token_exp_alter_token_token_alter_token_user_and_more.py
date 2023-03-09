# Generated by Django 4.1.1 on 2023-03-09 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="token",
            name="exp",
            field=models.FloatField(default=1678371531.804228),
        ),
        migrations.AlterField(
            model_name="token", name="token", field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name="token",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="user.user"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]