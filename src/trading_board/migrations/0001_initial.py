# Generated by Django 3.1.3 on 2020-11-21 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Trade",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                (
                    "type",
                    models.CharField(
                        choices=[("Buy", "ACHAT"), ("Sell", "VENTE")], max_length=128
                    ),
                ),
                ("open_price", models.FloatField(default=0.0)),
                ("close_price", models.FloatField(default=0.0)),
            ],
        )
    ]
