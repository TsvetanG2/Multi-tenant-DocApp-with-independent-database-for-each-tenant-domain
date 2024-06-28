# Multi-tenant Doctor Appointments with Independent Databases
## Overview
This repository contains a multi-tenant doctor appointments application with independent databases for each tenant domain. It is designed to provide a scalable and secure solution for managing appointments across multiple tenants while ensuring data isolation and privacy.

## Features

- **Multi-tenancy:** Each tenant (organization or domain) has its own isolated database.
- **Multi-user dashboard, records and calendar:** Each doctor has it's own calendar, dashboard and records. Which means that for each doctor you create and assign a user, there will be an independent patients with events.
- **Doctor Appointments:** Manage appointments with a calendar view and dashboard categorizing appointments into active, archived, and completed.
- **Patient Records:** Maintain patient records, ensuring that only patients with existing records can be added to appointments.
- **User Authentication and Authorization:** Secure user authentication and role-based access control (RBAC).
- **RESTful API:** Exposes a RESTful API for integration with other services.
- **Scalable and Extendable:** Built to accommodate growth and additional features.

## How it works:
- For each created tenant with domain, there will be a seperated database independent from the other tenants. You can create users and doctors. Assign the user to the doctor and assign the doctor to the domain(tenant) via the admin panel.
- Each doctor creates its own patients and appointments. Each element is being assigned to him by their id in the database and cannot be viewed, changed or deleted by other users(doctors).

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
- Create a user via the admin panel, then create a doctor and assign the doctor to the user and the domain.
- Login via adding **/login** page by adding it by the end of the port.
- Use the user's credentials to access the app.

## Contributing and Ideas

- Contributions are welcome! Please fork the repository and create a pull request with your changes

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## App Screenshots
**Django Default Page**
![Django_default_page](https://github.com/TsvetanG2/Multi-tenant-DocApp-with-independent-database-for-each-tenant-domain/assets/106432651/f2b90ef0-94c2-4e56-b20e-b7b69815fb4a)

**Django Admin Panel**
![Default_admin_to_add_tenants_and_domains](https://github.com/TsvetanG2/Multi-tenant-DocApp-with-independent-database-for-each-tenant-domain/assets/106432651/d42ca25d-63fb-4a9d-829d-03fcf0ba9c0b)

**Tenant-Domain Admin Panel**
![Tenant_domain_admin_panel](https://github.com/TsvetanG2/Multi-tenant-DocApp-with-independent-database-for-each-tenant-domain/assets/106432651/daa4cffc-50ee-4091-8219-d6b791eeccce)

**Tenant-Domain Login Page**
![Tenant_users_login_page](https://github.com/TsvetanG2/Multi-tenant-DocApp-with-independent-database-for-each-tenant-domain/assets/106432651/36cfacd2-da1e-4900-b4fa-aa2f89da1c9f)

**Tenant-Domain Home Page**
![Records_display_on_default_page](https://github.com/TsvetanG2/Multi-tenant-DocApp-with-independent-database-for-each-tenant-domain/assets/106432651/36099824-3518-4407-8e7e-8d9193fe6dbf)

**Tenant-Domain Add Record Page**
![Add_record_of_patient_page](https://github.com/TsvetanG2/Multi-tenant-DocApp-with-independent-database-for-each-tenant-domain/assets/106432651/20c752b8-497a-4773-81e5-137c2d59acaa)

**Tenant-Domain Calendar Page**
![Calendar_page](https://github.com/TsvetanG2/Multi-tenant-DocApp-with-independent-database-for-each-tenant-domain/assets/106432651/dfedb3e1-d3a3-415b-b45d-eced8c250c0d)

**Tenant-Domain Dashboard Page**
![Dashboard_page](https://github.com/TsvetanG2/Multi-tenant-DocApp-with-independent-database-for-each-tenant-domain/assets/106432651/3e969669-bacc-4219-b49a-e3b77a77cd92)







