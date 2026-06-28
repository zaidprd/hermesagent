from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("content", "0004_article_threads_fields"),
    ]

    operations = [
        migrations.RemoveField(model_name="article", name="threads_status"),
        migrations.RemoveField(model_name="article", name="threads_post_id"),
        migrations.RemoveField(model_name="article", name="threads_post_url"),
    ]
