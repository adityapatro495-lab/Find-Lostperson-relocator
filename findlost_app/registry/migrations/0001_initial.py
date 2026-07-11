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
            name='MissingPerson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('age', models.PositiveIntegerField()),
                ('gender', models.CharField(max_length=20)),
                ('last_seen_location', models.CharField(max_length=255)),
                ('contact_email', models.EmailField(max_length=254)),
                ('contact_phone', models.CharField(blank=True, max_length=15)),
                ('photo', models.ImageField(upload_to='missing_photos/')),
                ('encoding', models.BinaryField(blank=True, null=True)),
                ('status', models.CharField(choices=[('OPEN', 'Open'), ('MATCH_FOUND', 'Match Found'), ('CLOSED', 'Closed')], default='OPEN', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reported_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='missing_persons', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
