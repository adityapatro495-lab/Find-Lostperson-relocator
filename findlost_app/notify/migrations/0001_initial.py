import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('matching', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('SENT', 'Sent'), ('FAILED', 'Failed')], max_length=20)),
                ('sent_time', models.DateTimeField(auto_now_add=True)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='matching.matchresult')),
            ],
        ),
    ]
