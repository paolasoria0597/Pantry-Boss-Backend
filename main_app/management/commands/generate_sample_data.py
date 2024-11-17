import random  # We need this to pick random dispenser types and current levels
from django.core.management.base import BaseCommand  # BaseCommand lets us create custom commands
from main_app.models import Floor, Pantry, Dispenser  # Importing our models from the app
from django.contrib.auth.models import User  # Importing Django's built-in User model


class Command(BaseCommand):
    help = 'Generates sample data for Floors, Pantries, and Dispensers'

    def handle(self, *args, **options):
        """
        This is the main function that runs when you execute the command.
        It generates sample data to populate the database with floors, pantries, dispensers, and a user.
        """

        # =====================================
        # STEP 1: Create or get a sample user
        # =====================================
        # This creates a new user with the username 'sampleuser' and email 'sampleuser@example.com'.
        # If the user already exists, it just retrieves it (doesn't create a new one).
        user, created = User.objects.get_or_create(
            username='sampleuser',
            email='sampleuser@example.com'
        )

        # If the user was newly created (didn't exist before), set a password for them
        if created:
            user.set_password('password123')  # Setting a password for the user
            user.save()  # Save the user to the database

        # =====================================
        # STEP 2: Clear Existing Data
        # =====================================
        # Before generating new sample data, we delete everything so we start fresh.
        self.stdout.write("Clearing existing data...")
        Floor.objects.all().delete()  # Deletes all Floor entries in the database
        Pantry.objects.all().delete()  # Deletes all Pantry entries in the database
        Dispenser.objects.all().delete()  # Deletes all Dispenser entries in the database

        # List of possible dispenser types:
        # 'DR' = Drinks, 'SN' = Snacks, 'CO' = Coffee
        dispenser_types = ['DR', 'SN', 'CO']

        # =====================================
        # STEP 3: Generate Floors, Pantries, and Dispensers
        # =====================================

        # Loop to create 5 floors (Floor 1 to Floor 5)
        for floor_number in range(1, 6):
            # Create a floor and associate it with the sample user
            floor = Floor.objects.create(
                number=floor_number,  # Set the floor number
                user=user  # Associate the floor with our sample user
            )

            # For each floor, we create 3 pantries
            for pantry_number in range(1, 4):  # 3 pantries per floor
                pantry = Pantry.objects.create(
                    name=f"Pantry {pantry_number} on Floor {floor_number}",  # Set pantry name
                    floor=floor  # Link this pantry to the current floor
                )

                # For each pantry, we create 3 dispensers
                for dispenser_number in range(1, 4):  # 3 dispensers per pantry
                    Dispenser.objects.create(
                        type=random.choice(dispenser_types),  # Randomly choose a type ('DR', 'SN', 'CO')
                        max_capacity=100,  # Set the maximum capacity to 100 units
                        current_level=random.randint(20, 100),  # Randomly set current level between 20 and 100
                        pantry=pantry  # Link this dispenser to the current pantry
                    )

        # =====================================
        # STEP 4: Print Success Message
        # =====================================
        # Once everything is done, print a success message
        self.stdout.write(self.style.SUCCESS('Successfully generated sample data!'))
