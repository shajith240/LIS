# Library Information System (LIS)

A single-branch library management web application built with **Python · Flask · SQLAlchemy · Supabase (PostgreSQL) / SQLite · Bootstrap 5**.

---

## Features

| Module | What it does |
|---|---|
| **Authentication** | Three roles — Librarian, Clerk, Member (sign-in by member code) |
| **Book Catalogue** | Add, search (ISBN / title / author), delete with loan guard |
| **Member Management** | Register and remove members across 4 categories (UG, PG, RS, FA) |
| **Issue & Return** | Enforce per-category limits; compute overdue fines at Rs. 2/day |
| **Reservations** | FIFO queue; 7-day hold on return; auto-expire cascade |
| **Reports** | Printable overdue reminders and unused-books (5-year) report |

---

## Quick Start

### Prerequisites
- Python 3.10+

### Setup

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd lis-swe

# 2. Create and activate a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment (optional — defaults work for dev)
copy .env.example .env   # Windows
# cp .env.example .env   # macOS/Linux
# Edit .env and set LIS_SECRET to a strong random string

# 5. Seed demo data (optional but recommended)
python seed.py

# 6. Run the development server
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

---

## Sign-in Guide

| Role | How to sign in |
|---|---|
| Librarian | Click the **Librarian** photo |
| Clerk | Click the **Clerk** photo |
| Member | Type your member code (e.g. `U001`) and press **Sign in** |

### Demo member codes (after running `seed.py`)

`seed.py` loads 31 members, 42 books, 38 current loans (10 overdue), a year of returns
and 10 active reservations. Due dates and fines are worked out from today's date, so
run it again before a demo.

| Code | Name | Category | Notes |
|---|---|---|---|
| `U001` | Arjun Mehta | UG | 1 book out, can borrow 1 more |
| `U002` | Priya Nair | UG | **2 overdue books** (at limit) |
| `U003` | Rahul Singh | UG | First in the queue for *Clean Code* |
| `U011` | Pooja Hegde | UG | No reservations |
| `P002` | Vikram Joshi | PG | *AI: A Modern Approach* is on hold for him |
| `P004` | Arvind Menon | PG | 2 books, 22 days overdue |
| `R001` | Dr. Kavita Desai | RS | First in the queue for *Design Patterns* |
| `F001` | Prof. Sharma | FA | 2 books out |

---

## Project Structure

```
Library-Information-System/
├── app.py              # Flask app: all routes and business logic
├── models.py           # SQLAlchemy ORM models
├── seed.py             # Demo data loader
├── requirements.txt    # Python dependencies
├── vercel.json         # Vercel deployment config
├── .env.example        # Environment variable template
├── docs/               # Project report and presentation guide (PDF)
├── static/img/         # Images used by the pages
└── templates/
    ├── base.html           # Layout, sidebar, library rules panel, shared styles
    ├── login.html
    ├── issue.html
    ├── return.html         # + printable return receipt
    ├── slip.html           # Printable reservation hold slip
    ├── reserve.html        # Member: my reservations
    ├── books/              # search, add, delete
    ├── members/index.html  # Member list and registration
    ├── reservations/index.html  # Reservation queue (staff)
    └── reports/            # Overdue reminders, unused books
```

---

## Business Rules

| Rule | Value |
|---|---|
| UG book limit | 2 books / 30-day loan |
| PG book limit | 4 books / 30-day loan |
| RS book limit | 6 books / 90-day loan |
| FA book limit | 10 books / 180-day loan |
| Overdue fine | Rs. 2 per day |
| Reservation hold | 7 days |
| Unused-book threshold | No issue in 5 years |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Web framework | Flask 3.x |
| ORM | Flask-SQLAlchemy 3.x |
| Database | SQLite (`lis.db`) locally, PostgreSQL (Supabase) when deployed |
| Frontend | Bootstrap 5.3 + Bootstrap Icons |
| Templating | Jinja2 (server-side rendering) |

---

## Deploy to Vercel

**Quickest (no database setup):** import the repo in Vercel, add `LIS_SECRET`
(below) and deploy. Without `DATABASE_URL` the app keeps a temporary SQLite
database in `/tmp` and loads the demo data itself. Changes made on the site last
while it is active; after it has been idle, Vercel starts it fresh with clean
demo data.

**Permanent data (Supabase):**

1. **Database.** In Supabase, open *Project Settings > Database > Connection string*,
   choose **Transaction pooler**, and copy the URI (replace `[YOUR-PASSWORD]`).
2. **Load the demo data** into Supabase from your computer:
   ```bash
   DATABASE_URL="postgresql://..." python seed.py --reset
   ```
3. **Import the repo** in Vercel (*Add New > Project*). No build settings are needed;
   `vercel.json` tells Vercel to run `app.py` with Python.
4. **Environment variables** (*Settings > Environment Variables*):

   | Name | Value |
   |---|---|
   | `DATABASE_URL` | the Supabase URI from step 1 |
   | `LIS_SECRET` | a long random string (`python -c "import secrets; print(secrets.token_hex(32))"`) |

5. **Deploy.** Open the site; `/` goes to the sign-in page.

To reset the live demo later, run step 2 again.

---

## Security

- All database queries go through SQLAlchemy (parameterized — no SQL injection)
- Role checks enforced server-side; unauthorized access returns HTTP 403
- Secret key loaded from `LIS_SECRET` environment variable

---

## License

This project was built as a software engineering coursework submission.
