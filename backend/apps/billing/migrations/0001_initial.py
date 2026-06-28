import datetime

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tenants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('plan', models.CharField(
                    choices=[('free', 'Free'), ('pro', 'Pro')],
                    default='free',
                    max_length=20,
                )),
                ('valid_until', models.DateField(blank=True, null=True)),
                ('articles_this_month', models.PositiveIntegerField(default=0)),
                ('quota_month', models.DateField(default=datetime.date.today)),
                ('mayar_order_id', models.CharField(blank=True, max_length=255)),
                ('tenant', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='subscription',
                    to='tenants.tenant',
                )),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
