from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from logbook.models import Scan

User = get_user_model()


class Command(BaseCommand):
    help = "Import CCFP EM users and their scan data"

    def handle(self, *args, **options):
        # Data from CCFP EM 2025-26 total scans Excel file
        # Mapping Excel columns to Scan model exam types:
        # - Efast → RUQ (E-FAST hepatorenal view)
        # - 1st tri obs → OB_FIRST
        # - Aorta + AAA → AORTA
        # - Lung + PTX → LUQ (thoracic views)
        # - PSAX → PSAX
        # - PLAX + PSL → PLAX
        # - SubX + A4C → SUBXIPHOID
        # - Full Cardiac → IVC (cardiac assessment)

        users_data = [
            {
                "first_name": "Rebecca",
                "last_name": "Van Ginkel",
                "scans": {
                    "RUQ": 0,        # Efast
                    "OB_FIRST": 10,  # 1st tri obs
                    "AORTA": 0,      # Aorta + AAA
                    "LUQ": 0,        # Lung + PTX
                    "PSAX": 2,       # PSAX
                    "PLAX": 4,       # PLAX + PSL (0 + 4)
                    "SUBXIPHOID": 3, # SubX + A4C (0 + 3)
                    "IVC": 18,       # Full Cardiac
                }
            },
            {
                "first_name": "Richard",
                "last_name": "Ngo",
                "scans": {
                    "RUQ": 0,        # Efast
                    "OB_FIRST": 10,  # 1st tri obs
                    "AORTA": 0,      # Aorta + AAA
                    "LUQ": 0,        # Lung + PTX
                    "PSAX": 2,       # PSAX
                    "PLAX": 2,       # PLAX + PSL (1 + 1)
                    "SUBXIPHOID": 3, # SubX + A4C (0 + 3)
                    "IVC": 28,       # Full Cardiac
                }
            },
            {
                "first_name": "Fady",
                "last_name": "Sulailman",
                "scans": {
                    "RUQ": 24,       # Efast
                    "OB_FIRST": 13,  # 1st tri obs
                    "AORTA": 31,     # Aorta + AAA (10 + 21)
                    "LUQ": 17,       # Lung + PTX (5 + 12)
                    "PSAX": 0,       # PSAX
                    "PLAX": 0,       # PLAX + PSL
                    "SUBXIPHOID": 0, # SubX + A4C
                    "IVC": 5,        # Full Cardiac
                }
            },
            {
                "first_name": "Fadi",
                "last_name": "Bahodi",
                "scans": {
                    "RUQ": 9,        # Efast
                    "OB_FIRST": 13,  # 1st tri obs
                    "AORTA": 8,      # Aorta + AAA (0 + 8)
                    "LUQ": 5,        # Lung + PTX (5 + 0)
                    "PSAX": 0,       # PSAX
                    "PLAX": 0,       # PLAX + PSL
                    "SUBXIPHOID": 0, # SubX + A4C
                    "IVC": 5,        # Full Cardiac
                }
            },
            {
                "first_name": "Cimon",
                "last_name": "Song",
                "scans": {
                    "RUQ": 0,        # Efast
                    "OB_FIRST": 0,   # 1st tri obs
                    "AORTA": 0,      # Aorta + AAA
                    "LUQ": 0,        # Lung + PTX
                    "PSAX": 0,       # PSAX
                    "PLAX": 0,       # PLAX + PSL
                    "SUBXIPHOID": 0, # SubX + A4C
                    "IVC": 12,       # Full Cardiac
                }
            },
            {
                "first_name": "Tvisha",
                "last_name": "Ijner",
                "scans": {
                    "RUQ": 0,        # Efast
                    "OB_FIRST": 0,   # 1st tri obs
                    "AORTA": 0,      # Aorta + AAA
                    "LUQ": 0,        # Lung + PTX
                    "PSAX": 0,       # PSAX
                    "PLAX": 0,       # PLAX + PSL
                    "SUBXIPHOID": 0, # SubX + A4C
                    "IVC": 0,        # Full Cardiac
                }
            },
        ]

        password = "manitobapocus"
        today = timezone.localdate()

        for user_data in users_data:
            first_name = user_data["first_name"]
            last_name = user_data["last_name"]

            # Create username: lastname + first letter of firstname (lowercase)
            # Handle multi-word last names by removing spaces
            last_name_clean = last_name.replace(" ", "").lower()
            username = f"{last_name_clean}{first_name[0].lower()}"

            email = f"{username}@example.com"

            # Create or get user
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                }
            )

            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user: {username}"))
            else:
                self.stdout.write(self.style.WARNING(f"User already exists: {username}"))

            # Add scans for this user
            scans_to_create = []
            for exam_type, count in user_data["scans"].items():
                for i in range(count):
                    scans_to_create.append(
                        Scan(
                            user=user,
                            exam_type=exam_type,
                            performed_at=today,
                            finding="NORMAL",
                            scan_context="ACADEMIC",  # These are Academic Half Day scans
                        )
                    )

            if scans_to_create:
                Scan.objects.bulk_create(scans_to_create)
                self.stdout.write(
                    self.style.SUCCESS(f"  Added {len(scans_to_create)} scans for {username}")
                )
            else:
                self.stdout.write(f"  No scans to add for {username}")

        self.stdout.write(self.style.SUCCESS("\nImport complete!"))
        self.stdout.write("\nCreated users:")
        self.stdout.write("  Username format: lastname + first initial")
        self.stdout.write("  Password for all: manitobapocus")
        self.stdout.write("\n  vanginkler - Rebecca Van Ginkel")
        self.stdout.write("  ngor - Richard Ngo")
        self.stdout.write("  sulailmanf - Fady Sulailman")
        self.stdout.write("  bahodif - Fadi Bahodi")
        self.stdout.write("  songc - Cimon Song")
        self.stdout.write("  ijnert - Tvisha Ijner")
