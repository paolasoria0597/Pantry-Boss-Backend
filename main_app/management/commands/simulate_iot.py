from django.core.management.base import BaseCommand
import requests
import random
import time

# ====================
# CONFIGURATION SECTION
# ====================

# Base URL of our local Django server
BASE_URL = 'http://localhost:8000'

# API endpoint to interact with dispensers
DISPENSER_URL = f'{BASE_URL}/api/dispensers/'

# API endpoint to authenticate and get a token
AUTH_URL = f'{BASE_URL}/api/auth/jwt/create/'

# Replace with your actual username and password that you set in generate_sample_data script
USERNAME = 'sampleuser'
PASSWORD = 'password123'


class Command(BaseCommand):
    help = 'Simulate IoT devices updating dispenser levels'

    def handle(self, *args, **options):
        """
        This is the main function that runs when you execute the command.
        It continuously updates the dispenser levels to simulate real-life usage.
        """

        # Step 1: Authenticate and get an access token
        token = self.get_access_token()
        if not token:  # If token is None, authentication failed
            self.stdout.write("Authentication failed. Exiting...")
            return

        # Step 2: Fetch the latest dispenser IDs from the server
        dispenser_ids = self.get_dispenser_ids(token)
        if not dispenser_ids:  # If no dispensers are found, exit
            self.stdout.write("No dispensers found. Exiting...")
            return

        # Step 3: Simulate dispenser usage in an infinite loop
        while True:
            try:
                # Randomly pick a dispenser to update
                dispenser_id = random.choice(dispenser_ids)

                # Update the selected dispenser's current level
                success = self.simulate_dispenser_usage(dispenser_id, token)

                # If the token expired, get a new one
                if not success:
                    self.stdout.write("Token expired, refreshing...")
                    token = self.get_access_token()
                    if not token:  # If we can't get a new token, exit
                        self.stdout.write("Re-authentication failed. Exiting...")
                        return

                # Pause for a random amount of time between 2 to 5 seconds
                time.sleep(random.uniform(2, 5))

            except KeyboardInterrupt:
                # If the user presses Ctrl+C, gracefully stop the simulation
                self.stdout.write("Simulation interrupted. Exiting...")
                break

    def get_access_token(self):
        """
        Authenticate the user and obtain a JWT token for authorization.
        Without this token, we can't access the protected API endpoints.
        """
        payload = {
            'username': USERNAME,
            'password': PASSWORD
        }
        try:
            # Make a POST request to the authentication endpoint
            response = requests.post(AUTH_URL, json=payload)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Return the token from the response
                return response.json().get('access')
            else:
                # Print an error message if authentication fails
                self.stdout.write(f"Failed to obtain access token: {response.status_code} {response.text}")
                return None
        except requests.RequestException as e:
            # Handle network errors (e.g., server down, no internet)
            self.stdout.write(f"Error during authentication: {e}")
            return None

    def get_dispenser_ids(self, token):
        """
        Fetch the list of all dispenser IDs from the API.
        This ensures we're always using the correct IDs, even if the data changes.
        """
        headers = {
            'Authorization': f'Bearer {token}'
        }
        try:
            # Make a GET request to fetch all dispensers
            response = requests.get(DISPENSER_URL, headers=headers)

            if response.status_code == 200:
                # Convert the response to a list of dispensers and extract their IDs
                dispensers = response.json()
                return [dispenser['id'] for dispenser in dispensers]
            else:
                # Print an error message if fetching dispensers fails
                self.stdout.write(f"Failed to fetch dispensers: {response.status_code} {response.text}")
                return []
        except requests.RequestException as e:
            # Handle network errors
            self.stdout.write(f"Error fetching dispenser data: {e}")
            return []

    def simulate_dispenser_usage(self, dispenser_id, token):
        """
        Simulate the consumption of items in a dispenser by reducing its current level.
        """
        # Endpoint to update the dispenser's current level
        url = f"{DISPENSER_URL}{dispenser_id}/update-level/"

        # Headers for the request, including the authentication token
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        # Generate a random consumption value (how much the dispenser is used)
        consumption = random.randint(1, 10)

        # Create the payload (data) to send in the request
        payload = {'current_level': consumption}

        try:
            # Make a POST request to update the dispenser's current level
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                # Print success message if update was successful
                self.stdout.write(f"Dispenser {dispenser_id} updated with {consumption} units.")
                return True
            elif response.status_code == 401:  # Unauthorized, possibly token expired
                self.stdout.write("Token expired or invalid.")
                return False
            else:
                # Handle other errors and print the response message
                try:
                    error_message = response.json()
                    self.stdout.write(f"Failed to update dispenser {dispenser_id}: {error_message}")
                except requests.exceptions.JSONDecodeError:
                    self.stdout.write(f"Failed to update dispenser {dispenser_id}: Non-JSON response")
                return False

        except requests.RequestException as e:
            # Handle network errors (like server down)
            self.stdout.write(f"Network error: {e}")
            return False
