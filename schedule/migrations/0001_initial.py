# Generated by Django 2.0.3 on 2018-03-22 02:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=300)),
                ('suite', models.CharField(blank=True, max_length=20, null=True)),
                ('stretcher', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='MedicalProvider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('specialty', models.CharField(max_length=100)),
                ('destinations', models.ManyToManyField(blank=True, related_name='medical_providers', to='schedule.Destination')),
            ],
        ),
        migrations.CreateModel(
            name='Resident',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=35)),
                ('last_name', models.CharField(max_length=35)),
                ('date_of_birth', models.DateField()),
                ('medicaid_number', models.CharField(blank=True, max_length=8, null=True)),
                ('room_number', models.CharField(blank=True, max_length=5, null=True)),
                ('ride_to_care_eligble', models.BooleanField(default=False)),
                ('can_transfer', models.BooleanField(default=False)),
                ('wheelchair_van', models.BooleanField(default=True)),
                ('bariatric', models.BooleanField(default=False)),
                ('wheechair_size', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transport_provider', models.CharField(choices=[('M', 'Metro West'), ('R', 'Ride to Care'), ('T', 'Trimet Lift'), ('F', 'Family/Friend'), ('C', 'Cab')], max_length=1)),
                ('trip_date', models.DateField()),
                ('pick_up_time', models.DateTimeField()),
                ('return_time', models.DateTimeField()),
                ('will_call', models.BooleanField(default=False)),
                ('wait_and_return', models.BooleanField(default=False)),
                ('strecher', models.BooleanField(default=False)),
                ('oxygen', models.BooleanField(default=False)),
                ('oxygen_liters', models.IntegerField(blank=True, null=True)),
                ('representative_notified', models.CharField(blank=True, max_length=40, null=True)),
                ('tripID', models.CharField(blank=True, max_length=40, null=True)),
                ('notes', models.CharField(blank=True, max_length=200, null=True)),
                ('procedure', models.CharField(max_length=200)),
                ('door_to_door', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('trip_scheduled_status', models.BooleanField(default=False)),
                ('arranged_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips', to=settings.AUTH_USER_MODEL)),
                ('desination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination', to='schedule.Destination')),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resident', to='schedule.Resident')),
            ],
        ),
        migrations.AddField(
            model_name='medicalprovider',
            name='residents',
            field=models.ManyToManyField(blank=True, related_name='medical_providers', to='schedule.Resident'),
        ),
    ]