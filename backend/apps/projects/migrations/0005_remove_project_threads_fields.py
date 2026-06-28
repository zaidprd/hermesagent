from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0004_project_threads_fields"),
    ]

    operations = [
        migrations.RemoveField(model_name="project", name="threads_user_id"),
        migrations.RemoveField(model_name="project", name="threads_access_token"),
    ]
