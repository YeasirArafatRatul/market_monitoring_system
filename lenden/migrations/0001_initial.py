# Generated by Django 3.1.4 on 2020-12-18 05:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0007_auto_20201218_1137'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('quantity', models.PositiveBigIntegerField(error_messages={'required': 'Quantity must be provided'})),
                ('unit', models.CharField(blank=True, choices=[('tons', 'TON'), ('metrictons', 'METRIC TONS'), ('kilograms', 'KILOGRAMS'), ('litres', 'LITRES'), ('gallons', 'GALLONS')], default='', max_length=10, null=True)),
                ('imported_from', models.CharField(max_length=200)),
                ('customs_clearance_no', models.PositiveBigIntegerField(error_messages={'unique': 'A user with that email already exists.'}, unique=True)),
                ('import_date', models.DateField(default=django.utils.timezone.now)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
        ),
    ]
