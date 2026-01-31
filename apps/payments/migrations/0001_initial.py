
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gateway', models.CharField(default='razorpay', max_length=50)),
                ('gateway_order_id', models.CharField(blank=True, max_length=255, null=True)),
                ('gateway_payment_id', models.CharField(blank=True, max_length=255, null=True)),
                ('gateway_signature', models.CharField(blank=True, max_length=255, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('INITIATED', 'Initiated'), ('SUCCESS', 'Success'), ('FAILED', 'Failed')], default='INITIATED', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='orders.order')),
            ],
        ),
    ]
