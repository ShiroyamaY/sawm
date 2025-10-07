from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('e_mail', models.EmailField(max_length=254)),
                ('text_message', models.TextField()),
                ('data_time_message', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]



