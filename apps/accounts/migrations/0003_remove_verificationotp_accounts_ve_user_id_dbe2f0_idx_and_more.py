

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_usermodel_auth_provider_alter_usermodel_email'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='verificationotp',
            name='accounts_ve_user_id_dbe2f0_idx',
        ),
        migrations.AddIndex(
            model_name='verificationotp',
            index=models.Index(fields=['user', 'purpose', 'created_at'], name='accounts_ve_user_id_dd3e7f_idx'),
        ),
    ]
