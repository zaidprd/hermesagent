from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_project_language_project_niche_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='wp_site_url',
            field=models.URLField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='project',
            name='wp_username',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='project',
            name='wp_app_password',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
