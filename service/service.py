import os  # For file operations
import time  # For adding delays
import json  # For working with JSON data
import logging  # For logging information and errors
from pymongo import MongoClient  # For connecting to MongoDB
from watchdog.observers import Observer  # For watching directories
from watchdog.events import FileSystemEventHandler  # For handling file events
from jsonschema import validate, ValidationError  # For validating JSON structure

# Step 1: Set up MongoDB connection
client = MongoClient('mongodb://localhost:27017/')  # Connect to MongoDB
db = client['contacts_db']  # Select the database
collection = db['contacts']  # Select the collection for contacts

# Step 2: Specify the directory to watch
WATCH_DIRECTORY = 'storage/app/contacts/'  # Directory where JSON files will be stored

# Step 3: Define the JSON structure we expect
CONTACT_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},  # Name should be a string
        "email": {"type": "string", "format": "email"},  # Email should be a valid email format
        "phone": {"type": "string"}  # Phone should be a string
    },
    "required": ["name", "email", "phone"]  # All fields are required
}

# Step 4: Set up logging to track what happens
logging.basicConfig(level=logging.INFO)

def normalize_phone(phone):
    """ Normalize phone number to a standard format. """
    # Remove non-digit characters using simple string methods
    digits = ''.join([char for char in phone if char.isdigit()])  # Keep only digits
    if len(digits) == 10:  # Check if the phone number has 10 digits
        return f"+1-{digits[:3]}-{digits[3:6]}-{digits[6:]}"  # Format it
    return phone  # If not, return it as is

def process_file(file_path):
    """ Read the JSON file and insert contacts into MongoDB. """
    with open(file_path, 'r') as file:  # Open the file
        try:
            contacts = json.load(file)  # Load JSON data from the file
            if not isinstance(contacts, list):  # Check if it's a list
                logging.error(f"File '{file_path}' does not contain a list of contacts.")
                return  # Exit if not a list

            for contact in contacts:  # Loop through each contact
                try:
                    validate(instance=contact, schema=CONTACT_SCHEMA)  # Validate the contact data
                    contact['phone'] = normalize_phone(contact['phone'])  # Normalize the phone number
                    
                    # Check if the email already exists in the database
                    if collection.find_one({"email": contact['email']}):
                        logging.warning(f"Duplicate email found: {contact['email']}. Skipping contact.")
                        continue  # Skip to the next contact if duplicate found
                    
                    # Insert the contact into MongoDB
                    collection.insert_one(contact)
                    logging.info(f"Inserted contact: {contact['name']} with email: {contact['email']}")
                
                except ValidationError as ve:  # If validation fails
                    logging.error(f"Validation error for contact {contact}: {ve.message}")

        except json.JSONDecodeError as e:  # If there's an error reading the JSON
            logging.error(f"Error decoding JSON from file '{file_path}': {e}")

    # Step 5: Clean up by removing the processed file
    os.remove(file_path)  # Delete the file after processing
    logging.info(f"Processed and cleaned up file: {file_path}")

class ContactHandler(FileSystemEventHandler):
    """ Handle new files in the watched directory. """
    def on_created(self, event):
        """ Called when a new file is created. """
        if not event.is_directory:  # Check if it's not a directory
            logging.info(f"New file detected: {event.src_path}")  # Log the new file
            process_file(event.src_path)  # Process the new file

def watch_directory():
    """ Watch the specified directory for new files. """
    event_handler = ContactHandler()  # Create an event handler
    observer = Observer()  # Create an observer to monitor the directory
    observer.schedule(event_handler, WATCH_DIRECTORY, recursive=False)  # Start watching the directory
    
    try:
        observer.start()  # Start the observer
        logging.info("Started watching directory for new contact files.")
        while True:  # Keep the script running
            time.sleep(1)  # Wait for a second before checking again
    except KeyboardInterrupt:  # Allow graceful exit
        observer.stop()  # Stop the observer when interrupted
    observer.join()  # Wait for the observer to finish

if __name__ == "__main__":
    watch_directory()  # Start watching the directory
