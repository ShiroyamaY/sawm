from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from portals.models import CustomerAccount


class Command(BaseCommand):
    help = "Create demo roles (admin + manager) and seed customer accounts for the lab."

    def handle(self, *args, **options):
        User = get_user_model()

        admin, created_admin = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "role": User.Role.ADMIN,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created_admin:
            admin.set_password("Admin!123")
            admin.save()
            self.stdout.write(self.style.SUCCESS("Admin user admin/Admin!123 created"))
        else:
            self.stdout.write("Admin user already exists.")

        manager, created_manager = User.objects.get_or_create(
            username="manager",
            defaults={
                "email": "manager@example.com",
                "role": User.Role.MANAGER,
                "is_staff": False,
                "is_superuser": False,
            },
        )
        if created_manager:
            manager.set_password("Manager!123")
            manager.save()
            self.stdout.write(self.style.SUCCESS("Manager user manager/Manager!123 created"))
        else:
            self.stdout.write("Manager user already exists.")

        sample_accounts = [
            {
                "full_name": "North LLC",
                "email": "contact@north.example",
                "status": CustomerAccount.Status.ACTIVE,
                "balance": 154000,
            },
            {
                "full_name": "Smirnova Sole Prop",
                "email": "anna@bizmail.example",
                "status": CustomerAccount.Status.PENDING,
                "balance": 42000,
            },
            {
                "full_name": "TechFuture Ltd",
                "email": "hello@techfuture.example",
                "status": CustomerAccount.Status.BLOCKED,
                "balance": 0,
            },
        ]

        for payload in sample_accounts:
            obj, created = CustomerAccount.objects.get_or_create(
                email=payload["email"],
                defaults=payload,
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Customer {obj.full_name} added"))
            else:
                self.stdout.write(f"Customer {obj.full_name} already present.")

        self.stdout.write(self.style.SUCCESS("Demo data ready."))
