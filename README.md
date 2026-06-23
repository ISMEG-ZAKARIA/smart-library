# Smart Library — Academic Library Management System

A professional, multi-role academic library management system built with Django, featuring user authentication, book cataloging, reservations, loans, penalties, notifications, and an audit trail. Implements transactional workflows, role-based access control, and database integrity guarantees.

## Features

- **Role-Based Access Control (RBAC):** Three distinct user roles:
  - **Administrator:** Full system access, user management, library settings
  - **Librarian:** Manage catalog, process loans/returns, handle reservations
  - **Client:** Browse catalog, make reservations, track loans
- **Book Cataloging:** Comprehensive book management with authors, categories, covers, and visibility controls
- **Reservations System:** With automatic expiration, quota checks, and conflict resolution
- **Loans Management:** QR code support, return processing, and overdue tracking
- **Penalties System:** Automated penalty creation, tracking, and settlement
- **Notifications:** Real-time in-app alerts with context processors
- **Audit Trail:** Immutable audit log for all critical operations
- **Database Integrity:** MySQL triggers for stock and status synchronization
- **Demo Data Seeding:** Reproducible demo environment with sample books and users

## Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Django 4.x (Python 3.10+) |
| Database | MySQL 8.x (with SQLite fallback for testing) |
| Authentication | Django's built-in auth system with custom user model |
| Templates | Django MVT (Model-View-Template) |
| Security | CSRF protection, password hashing, atomic transactions |

## System Architecture

Smart Library follows a clean **MVT (Model-View-Template)** architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (Templates)                  │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │
│  │  Admin UI    │ │ Librarian UI │ │  Client UI   │        │
│  └──────────────┘ └──────────────┘ └──────────────┘        │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                      Backend (Django)                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Views: HTTP handlers, permission checks              │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Services: Transactional business logic               │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Models: ORM, data validation, triggers               │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│                      Database (MySQL)                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Tables: Users, Books, Reservations, Loans, Penalties │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Triggers: Stock sync, status updates, integrity      │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Technical Highlights

- **Atomic Transactions:** All critical workflows (reservation → loan → penalty) wrapped in `transaction.atomic()`
- **Row-Level Locking:** Uses `select_for_update()` to prevent race conditions on books, reservations, and loans
- **Database Triggers:** MySQL triggers for automatic stock and book status synchronization
- **Custom Managers:** Specialized querysets for active loans, overdue items, and audit logs
- **Management Commands:**
  - `seed_demo`: Populate with sample data for testing
  - `expire_reservations`: Periodic expiration of old reservations
  - `audit_database_integrity`: Validate database consistency

## Installation

### Prerequisites
- Python 3.10 or higher
- MySQL 8.x (running locally)

### Setup Instructions

1. Clone the repository
```bash
cd PFA-project-Smart-Library
```

2. Install dependencies
```powershell
python -m pip install -r requirements.txt
```

3. Configure environment variables (copy `.env.example` to `.env` and edit)
```bash
cp .env.example .env
# Edit .env with your MySQL credentials
```

4. Run migrations (automatically creates the `PFA_3IIR` database)
```powershell
python manage.py migrate
```

5. Create a superuser
```powershell
python manage.py createsuperuser
```

6. Seed demo data (optional)
```powershell
python manage.py seed_demo
```

7. Run the development server
```powershell
python manage.py runserver
```

## Demo Users

After running `seed_demo`, use these credentials:

| Role | Email | Password |
|------|-------|----------|
| Administrator | admin@smartlibrary.local | AdminSmart2026! |
| Librarian | bibliothecaire@smartlibrary.local | BiblioSmart2026! |
| Client | client@smartlibrary.local | ClientSmart2026! |

## Project Structure

```
PFA-project-Smart-Library/
├── accounts/               # User management, authentication, profiles
├── catalog/                # Book catalog, authors, categories
├── reservations/           # Reservation system, expiration, validation
├── loans/                  # Loan processing, returns, overdue tracking
├── penalties/              # Penalty creation, settlement, tracking
├── alerts/                 # Notifications system
├── audit/                  # Audit trail, integrity checks
├── abuse/                  # Abuse reporting, restrictions
├── dashboard/              # Dashboard statistics and views
├── templates/              # Django templates (admin, librarian, client UIs)
├── static/                 # Static files (CSS, JS, images)
├── assets/                 # Project assets (book covers, logos)
├── sql/                    # Database setup scripts
├── smart_library/          # Django project configuration
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
└── .env.example            # Environment variables template
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DJANGO_SECRET_KEY | Django secret key | (development placeholder) |
| DJANGO_DEBUG | Debug mode | 1 |
| DJANGO_ALLOWED_HOSTS | Allowed hosts | localhost,127.0.0.1 |
| MYSQL_HOST | MySQL host | localhost |
| MYSQL_PORT | MySQL port | 3306 |
| MYSQL_USER | MySQL username | root |
| MYSQL_PASSWORD | MySQL password | (empty) |
| USE_SQLITE_FOR_TESTS | Use SQLite instead of MySQL for tests | 0 |

## Future Improvements

- [ ] API integration with external library systems
- [ ] Email notifications for reservations and loans
- [ ] Advanced search and filtering
- [ ] Book recommendation engine
- [ ] Containerization with Docker
- [ ] CI/CD pipeline for automated testing and deployment

## License

MIT License - see LICENSE file for details.

## Author

Zakaria Ismeg
