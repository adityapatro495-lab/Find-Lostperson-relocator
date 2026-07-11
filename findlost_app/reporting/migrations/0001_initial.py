import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SightingReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=255)),
                ('sighted_date', models.DateField()),
                ('sighted_time', models.TimeField(blank=True, null=True)),
                ('photo', models.ImageField(upload_to='reports/')),
                ('encoding', models.BinaryField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sighting_reports', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
