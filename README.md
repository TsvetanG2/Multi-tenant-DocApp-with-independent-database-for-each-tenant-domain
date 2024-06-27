# Doctors Multi-Tenant Management App

Welcome to the Doctors Multi-Tenant Management App repository! This application is designed to streamline the management of appointments and patient records for doctors operating in a multi-tenant environment.

## Features

- **Multi-tenancy:** Each tenant (organization or domain) has its own isolated database.
- **Multi-user dashboard, records and calendar:** Each doctor has it's own calendar, dashboard and records. Which means that for each doctor you create and assign a user, there will be an independent patients with events.
- **Doctor Appointments:** Manage appointments with a calendar view and dashboard categorizing appointments into active, archived, and completed.
- **Patient Records:** Maintain patient records, ensuring that only patients with existing records can be added to appointments.
- **User Authentication and Authorization:** Secure user authentication and role-based access control (RBAC).
- **RESTful API:** Exposes a RESTful API for integration with other services.
- **Scalable and Extendable:** Built to accommodate growth and additional features.

#### **How it works:** Each doctor creates its own patients and appointments. They are being assigned to him by their ID and cannot be viewed, changed or deleted by other users(doctors).

## Repository Structure

- **DoctorsApp/**: Main application directory containing all the core functionalities and modules.
- **manage.py**: Command-line utility for administrative tasks.
- **requirements.txt**: List of dependencies required to run the application.

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/TsvetanG2/Multi-tenant-DocApp-with-independent-database-for-each-tenant-domain.git
   cd Multi-tenant-DocApp-with-independent-database-for-each-tenant-domain

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt

3. **Set-up the database in settings.py**
   ```sh
   DATABASES = {
    "default": {
        "ENGINE": 'django_tenants.postgresql_backend',
        "NAME": "your_database",
        "USER": "your_user",
        "PASSWORD": "your_password",
        "HOST": "your_default_host",
        "PORT": "your_default_port",
    }
}

## Run App

1. **Make Migrations:**
   ```sh
   python manage.py makemigrations

2. **Migrate:**
   ```sh
   python manage.py migrate_schemas --shared
   python manage.py migrate

3. **Create a superuser, so you can add a tenant and domain:**
   ```sh
   python manage.py createsuperuser

- **How to add tenant superuser**
  ```sh
  python manage.py create_tenant_superuser

4. **Run App:**
   ```sh
   python manage.py runserver

## Usage

- Once you run the app you will be prompted to **your_default_host:your_dafault_port** . A Django default homepage will appear that installation has been completed.
Go to:
  ```sh
  your_default_host:your_dafault_port/admin

- There you can add tenant and domain. First add a tenant, then assign the tenant to the domain.
To access the domain go to:
  ```sh
   your_domain:your_default_port

- Same way you can access admin if you add **/admin** by the end of the port.
- Create a user via the admin panel, then create a doctor and assign the doctor to the user.
- Login via adding **/login** page by addmin it by the end of the port.

## Contributing and Ideas

- Contributions are welcome! Please fork the repository and create a pull request with your changes

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## App Screenshots




