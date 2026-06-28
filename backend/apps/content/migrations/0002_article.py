import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
        ('projects', '0002_project_language_project_niche_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('body', models.TextField(blank=True)),
                ('meta_description', models.CharField(blank=True, max_length=160)),
                ('featured_image_url', models.URLField(blank=True, max_length=2000)),
                ('image_prompt', models.TextField(blank=True)),
                ('word_count', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(
                    choices=[('processing', 'Processing'), ('done', 'Done'), ('failed', 'Gagal')],
                    default='processing',
                    max_length=20,
                )),
                ('title', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='article',
                    to='content.title',
                )),
                ('project', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='articles',
                    to='projects.project',
                )),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
