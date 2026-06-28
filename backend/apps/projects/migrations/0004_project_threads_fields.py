from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_project_wp_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='threads_user_id',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name='project',
            name='threads_access_token',
            field=models.TextField(blank=True),
        ),
    ]
