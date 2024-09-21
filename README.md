# Contact Management API

This project contains two main components:
1. A **Laravel API** for uploading and managing contacts.
2. A **Python service** that processes JSON files with contact data and inserts them into MongoDB.

## Requirements

### Laravel API
- PHP >= 7.3
- Composer
- MongoDB
- XAMPP (or another web server)

### Python Service
- Python >= 3.6
- MongoDB
- Required Python packages:
  - `pymongo`
  - `watchdog`
  - `jsonschema`

## Setup Instructions

### Laravel API

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd <your-project-folder>
   ```

2. **Install dependencies**:
   ```bash
   composer install
   ```

3. **Configure environment variables** in `.env` file:
   ```env
   DB_CONNECTION=mysql
   DB_HOST=127.0.0.1
   DB_PORT=3306
   DB_DATABASE=contacts_db
   DB_USERNAME=root
   DB_PASSWORD=
   ```

4. **Run migrations**:
   ```bash
   php artisan migrate
   ```

5. **Start the Laravel server**:
   ```bash
   php artisan serve
   ```

### Python Service

1. **Install required Python packages**:
   ```bash
   pip install pymongo watchdog jsonschema
   ```

2. **Run the Python service**:
   ```bash
   python service.py
   ```

## API Endpoints

1. **Upload Contacts**
   - `POST /upload`
   - Upload a JSON file containing contacts.
   
2. **Get Contacts (Paginated)**
   - `GET /contacts`
   - Optional filters: `name`, `email`.
   
3. **Get Single Contact**
   - `GET /contacts/{id}`
   
4. **Update Contact**
   - `PUT /contacts/{id}`
   
5. **Delete Contact**
   - `DELETE /contacts/{id}`

## Python Service Overview

- **Monitors** the `storage/app/contacts/` directory.
- **Processes** new JSON files.
- **Validates** JSON structure (name, email, phone).
- **Normalizes** phone numbers.
- **Inserts** contacts into MongoDB.
- **Removes** processed files.

---