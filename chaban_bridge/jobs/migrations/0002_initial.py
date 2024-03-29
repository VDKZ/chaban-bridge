# Generated by Django 5.0.3 on 2024-03-15 16:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("jobs", "0001_initial"),
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="jobs",
                to="user.organization",
            ),
        ),
        migrations.AddField(
            model_name="execution",
            name="job",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="executions",
                to="jobs.job",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="job",
            unique_together={("organization", "name")},
        ),
    ]
