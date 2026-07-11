import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('registry', '0001_initial'),
        ('reporting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confidence_score', models.FloatField()),
                ('status', models.CharField(choices=[('PENDING', 'Pending Review'), ('VERIFIED', 'Verified'), ('REJECTED', 'Rejected')], default='PENDING', max_length=20)),
                ('reviewed_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_results', to='registry.missingperson')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_results', to='reporting.sightingreport')),
            ],
            options={
                'ordering': ['-confidence_score'],
            },
        ),
    ]
