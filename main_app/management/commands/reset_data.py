import random
from django.core.management.base import BaseCommand
from main_app.models import Floor, Pantry, Dispenser
from django.contrib.auth.models import User
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Resets the database and regenerates sample data'

    def handle(self, *args, **options):
        """
        This is the main function that runs when you execute the command.
        It deletes existing data from the database and regenerates fresh sample data.
        """

        # Step 1: Delete all existing Floors, Pantries, and Dispensers
        self.stdout.write("Deleting all Floors, Pantries, and Dispensers...")
        # Removes all records of Floor, Pantry, and Dispenser from the database.
        # This is like clearing everything so you can start fresh.
        Floor.objects.all().delete()
        Pantry.objects.all().delete()
        Dispenser.objects.all().delete()

        # Step 2: Delete the sample user if it exists
        self.stdout.write("Deleting sample user...")
        try:
            # Tries to find a user with the username 'sampleuser'
            user = User.objects.get(username='sampleuser')

            # If found, delete the user
            user.delete()
            self.stdout.write(self.style.SUCCESS('Sample user deleted'))
        except User.DoesNotExist:
            # If the user doesn't exist, print a message
            self.stdout.write("Sample user not found")

        # Step 3: Regenerate all the sample data
        self.stdout.write("Regenerating sample data...")
        # Calls another management command called 'generate_sample_data'
        # This command will create new Floors, Pantries, Dispensers, and a sample user.
        call_command('generate_sample_data')

        # Step 4: Print a success message once everything is done
        self.stdout.write(self.style.SUCCESS('Successfully reset and regenerated sample data!'))
