from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='publish_status',
            field=models.CharField(
                choices=[
                    ('none', 'Belum dipublish'),
                    ('publishing', 'Sedang publish…'),
                    ('published', 'Published'),
                    ('failed', 'Gagal'),
                ],
                default='none',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='article',
            name='wp_post_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='wp_post_url',
            field=models.URLField(blank=True, max_length=2000),
        ),
    ]
