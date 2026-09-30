from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_transactions_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlacklistedToken',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'token',
                    models.CharField(
                        max_length=500,
                        unique=True
                    )
                ),
                (
                    'blacklisted_at',
                    models.DateTimeField(
                        auto_now_add=True
                    )
                ),
            ],
        ),
    ]