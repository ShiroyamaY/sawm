from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('is_hashed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'user',
                'ordering': ['-created_at'],
            },
        ),
    ]


