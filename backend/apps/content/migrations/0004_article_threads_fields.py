from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_article_publish_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='threads_status',
            field=models.CharField(
                choices=[
                    ('none', 'Belum dipost'),
                    ('posting', 'Sedang posting…'),
                    ('posted', 'Terpost'),
                    ('failed', 'Gagal'),
                ],
                default='none',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='article',
            name='threads_post_id',
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name='article',
            name='threads_post_url',
            field=models.URLField(blank=True, max_length=2000),
        ),
    ]
