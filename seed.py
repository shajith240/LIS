"""
seed.py -- Populate the database with realistic demo data.

Run:
    python seed.py

On the local SQLite database (lis.db) this resets everything and loads a
fresh demo, so run it again right before a demo: due dates and fines are
worked out from today's date.

On Vercel with no DATABASE_URL, the app fills a temporary SQLite database
with this same data by itself when it starts (see app.py).

On a remote database (Supabase / PostgreSQL) it only adds rows that are
missing, unless you ask for a reset:
    python seed.py --reset     # asks you to type "yes" first
"""

import sys

from datetime import date, timedelta
from models import db, Member, Book, Issue, Reservation

today = date.today()


def ago(days):
    return today - timedelta(days=days)


# -- Members -----------------------------------------------------------------
# (code, name, category, joined)
MEMBERS = [
    # Original demo members -- the presentation guide refers to these
    ("U001", "Arjun Mehta",          "UG", date(2024, 7, 1)),
    ("U002", "Priya Nair",           "UG", date(2024, 7, 1)),
    ("U003", "Rahul Singh",          "UG", date(2024, 8, 1)),
    ("P001", "Sneha Rao",            "PG", date(2023, 6, 15)),
    ("P002", "Vikram Joshi",         "PG", date(2023, 6, 15)),
    ("R001", "Dr. Kavita Desai",     "RS", date(2022, 1, 10)),
    ("R002", "Anand Krishnan",       "RS", date(2022, 3, 20)),
    ("F001", "Prof. Sharma",         "FA", date(2018, 4, 1)),
    ("F002", "Prof. Iyer",           "FA", date(2019, 6, 1)),
    # Undergraduates
    ("U004", "Aditya Kumar",         "UG", date(2024, 7, 15)),
    ("U005", "Ananya Iyer",          "UG", date(2024, 7, 15)),
    ("U006", "Rohan Gupta",          "UG", date(2024, 8, 5)),
    ("U007", "Kavya Reddy",          "UG", date(2025, 7, 20)),
    ("U008", "Siddharth Patil",      "UG", date(2023, 8, 1)),
    ("U009", "Ishita Banerjee",      "UG", date(2025, 8, 1)),
    ("U010", "Harsh Vardhan",        "UG", date(2023, 8, 1)),
    ("U011", "Pooja Hegde",          "UG", date(2025, 7, 25)),
    ("U012", "Karthik Subramanian",  "UG", date(2024, 8, 10)),
    ("U013", "Nikhil Chauhan",       "UG", date(2025, 8, 3)),
    ("U014", "Shreya Ghosh",         "UG", date(2023, 7, 28)),
    # Postgraduates
    ("P003", "Meera Pillai",         "PG", date(2024, 7, 10)),
    ("P004", "Arvind Menon",         "PG", date(2024, 7, 10)),
    ("P005", "Neha Kulkarni",        "PG", date(2025, 7, 12)),
    ("P006", "Farhan Qureshi",       "PG", date(2024, 7, 18)),
    ("P007", "Divya Sharma",         "PG", date(2025, 7, 18)),
    # Research scholars
    ("R003", "Lakshmi Narayanan",    "RS", date(2021, 9, 1)),
    ("R004", "Sanjay Verma",         "RS", date(2023, 1, 16)),
    ("R005", "Fatima Sheikh",        "RS", date(2024, 1, 8)),
    # Faculty
    ("F003", "Dr. Ramesh Chandra",   "FA", date(2015, 6, 1)),
    ("F004", "Dr. Sunita Rao",       "FA", date(2017, 7, 1)),
    ("F005", "Prof. Abhishek Mishra", "FA", date(2020, 1, 6)),
]

# -- Books -------------------------------------------------------------------
# (isbn, title, author, publisher, rack, copies, added)
BOOKS = [
    # Original demo books
    ("978-0-13-110362-7", "The C Programming Language", "Kernighan & Ritchie", "Prentice Hall", "CS-A1", 4, date(2020, 1, 15)),
    ("978-0-13-468599-1", "Clean Code", "Robert C. Martin", "Prentice Hall", "CS-A2", 3, date(2021, 3, 10)),
    ("978-0-201-63361-0", "Design Patterns", "Gang of Four", "Addison-Wesley", "CS-B1", 2, date(2019, 6, 5)),
    ("978-0-13-235088-4", "Introduction to Algorithms", "Cormen et al.", "MIT Press", "CS-B2", 5, date(2020, 8, 20)),
    ("978-0-596-51774-8", "Learning Python", "Mark Lutz", "O'Reilly", "CS-C1", 3, date(2022, 2, 1)),
    ("978-1-491-91205-8", "Flask Web Development", "Miguel Grinberg", "O'Reilly", "CS-C2", 2, date(2023, 5, 15)),
    ("978-0-07-352332-3", "Database System Concepts", "Silberschatz et al.", "McGraw-Hill", "CS-D1", 4, date(2018, 9, 1)),
    ("978-0-13-292401-7", "Computer Networks", "Andrew S. Tanenbaum", "Pearson", "CS-D2", 3, date(2017, 11, 1)),
    ("978-0-321-12521-7", "Domain-Driven Design", "Eric Evans", "Addison-Wesley", "CS-E1", 1, date(2016, 4, 10)),
    ("978-0-13-110362-0", "Operating System Concepts", "Silberschatz et al.", "Wiley", "CS-E2", 3, date(2021, 7, 1)),
    # Computer science
    ("978-0-13-461099-3", "Artificial Intelligence: A Modern Approach", "Stuart Russell & Peter Norvig", "Pearson", "CS-F1", 2, date(2022, 7, 4)),
    ("978-0-12-820109-1", "Computer Organization and Design", "Patterson & Hennessy", "Morgan Kaufmann", "CS-F2", 3, date(2021, 1, 12)),
    ("978-1-985-08659-3", "Operating Systems: Three Easy Pieces", "Remzi & Andrea Arpaci-Dusseau", "Arpaci-Dusseau Books", "CS-E3", 2, date(2022, 1, 20)),
    ("978-0-13-595705-9", "The Pragmatic Programmer", "David Thomas & Andrew Hunt", "Addison-Wesley", "CS-A3", 2, date(2021, 9, 14)),
    ("978-0-13-475759-9", "Refactoring", "Martin Fowler", "Addison-Wesley", "CS-A4", 1, date(2021, 9, 14)),
    ("978-0-13-394303-0", "Software Engineering", "Ian Sommerville", "Pearson", "SE-A1", 4, date(2020, 6, 2)),
    ("978-1-259-87297-6", "Software Engineering: A Practitioner's Approach", "Roger S. Pressman", "McGraw-Hill", "SE-A2", 3, date(2020, 6, 2)),
    ("978-0-321-48681-3", "Compilers: Principles, Techniques, and Tools", "Aho, Lam, Sethi & Ullman", "Pearson", "CS-G1", 2, date(2019, 2, 18)),
    ("978-1-133-18779-0", "Introduction to the Theory of Computation", "Michael Sipser", "Cengage", "CS-G2", 2, date(2022, 1, 20)),
    ("978-0-19-809930-7", "Data Structures Using C", "Reema Thareja", "Oxford University Press", "CS-B3", 4, date(2023, 7, 3)),
    ("978-0-262-03561-3", "Deep Learning", "Goodfellow, Bengio & Courville", "MIT Press", "CS-H1", 2, date(2023, 1, 9)),
    ("978-1-098-12597-4", "Hands-On Machine Learning", "Aurelien Geron", "O'Reilly", "CS-H2", 1, date(2023, 8, 21)),
    ("978-1-718-50270-3", "Python Crash Course", "Eric Matthes", "No Starch Press", "CS-C3", 3, date(2023, 8, 21)),
    ("978-1-260-46341-5", "Java: The Complete Reference", "Herbert Schildt", "McGraw-Hill", "CS-C4", 3, date(2022, 7, 4)),
    ("978-93-89845-68-5", "Let Us C", "Yashavant Kanetkar", "BPB Publications", "CS-A5", 5, date(2023, 7, 3)),
    ("978-0-13-668155-7", "Computer Networking: A Top-Down Approach", "Kurose & Ross", "Pearson", "CS-D3", 3, date(2022, 7, 4)),
    ("978-0-13-444428-4", "Cryptography and Network Security", "William Stallings", "Pearson", "CS-D4", 2, date(2021, 1, 12)),
    # Electronics
    ("978-0-13-454989-7", "Digital Design", "M. Morris Mano", "Pearson", "EC-A1", 3, date(2020, 2, 10)),
    ("978-0-19-085346-4", "Microelectronic Circuits", "Sedra & Smith", "Oxford University Press", "EC-A2", 2, date(2021, 2, 8)),
    ("978-0-13-814757-0", "Signals and Systems", "Oppenheim & Willsky", "Pearson", "EC-B1", 2, date(2019, 8, 5)),
    # Mathematics
    ("978-81-933284-9-1", "Higher Engineering Mathematics", "B. S. Grewal", "Khanna Publishers", "MA-A1", 6, date(2021, 7, 19)),
    ("978-1-259-67651-2", "Discrete Mathematics and Its Applications", "Kenneth H. Rosen", "McGraw-Hill", "MA-A2", 3, date(2020, 7, 13)),
    ("978-0-321-98238-4", "Linear Algebra and Its Applications", "David C. Lay", "Pearson", "MA-B1", 2, date(2020, 7, 13)),
    ("978-0-13-411585-6", "Probability and Statistics for Engineers", "Walpole, Myers & Ye", "Pearson", "MA-B2", 2, date(2021, 7, 19)),
    # Physics and mechanical
    ("978-81-7709-187-8", "Concepts of Physics, Vol. 1", "H. C. Verma", "Bharati Bhawan", "PH-A1", 5, date(2022, 7, 25)),
    ("978-1-119-80119-0", "Fundamentals of Physics", "Halliday, Resnick & Walker", "Wiley", "PH-A2", 2, date(2022, 7, 25)),
    ("978-0-13-391542-6", "Engineering Mechanics: Statics", "R. C. Hibbeler", "Pearson", "ME-A1", 2, date(2021, 8, 2)),
    ("978-93-5260-591-5", "Engineering Thermodynamics", "P. K. Nag", "McGraw-Hill", "ME-A2", 3, date(2022, 8, 1)),
    # General reading
    ("978-81-7371-146-6", "Wings of Fire", "A. P. J. Abdul Kalam", "Universities Press", "GN-A1", 2, date(2019, 10, 15)),
    # Old stock nobody borrows any more (unused-books report)
    ("978-0-07-462222-5", "Programming in FORTRAN 77", "V. Rajaraman", "PHI Learning", "ST-A1", 2, date(2009, 3, 2)),
    ("978-81-203-0789-6", "Turbo Pascal 7.0", "Tom Swan", "PHI Learning", "ST-A2", 1, date(2010, 6, 21)),
    ("978-81-87972-88-4", "Microprocessor Architecture, Programming and Applications with the 8085", "Ramesh Gaonkar", "Penram", "ST-A3", 2, date(2011, 1, 10)),
]

# -- Loans -------------------------------------------------------------------
# (isbn, member, issued N days ago, returned N days ago or None)
# Due dates and fines follow the member's category, exactly as the app does.
LOANS = [
    # Still out, on time
    ("978-0-13-394303-0", "U001", 12, None),
    ("978-93-89845-68-5", "U003", 8, None),
    ("978-1-718-50270-3", "U005", 3, None),
    ("978-0-13-468599-1", "U005", 25, None),     # due in 5 days
    ("978-81-7709-187-8", "U007", 6, None),
    ("978-1-260-46341-5", "U010", 15, None),
    ("978-81-933284-9-1", "U011", 4, None),
    ("978-0-13-668155-7", "U012", 19, None),
    ("978-0-13-235088-4", "P001", 10, None),
    ("978-0-321-48681-3", "P002", 20, None),
    ("978-0-13-468599-1", "P003", 18, None),
    ("978-0-262-03561-3", "P003", 28, None),     # due in 2 days
    ("978-1-133-18779-0", "P005", 9, None),
    ("978-0-13-454989-7", "P006", 14, None),
    ("978-0-596-51774-8", "R001", 5, None),
    ("978-0-321-98238-4", "R001", 30, None),
    ("978-0-19-085346-4", "R002", 40, None),
    ("978-0-262-03561-3", "R003", 60, None),
    ("978-0-13-461099-3", "R003", 70, None),
    ("978-1-985-08659-3", "R004", 22, None),
    ("978-0-13-110362-0", "F001", 20, None),
    ("978-1-259-87297-6", "F001", 60, None),
    ("978-0-12-820109-1", "F002", 90, None),
    ("978-0-13-391542-6", "F002", 45, None),
    ("978-93-5260-591-5", "F003", 30, None),
    ("978-0-13-444428-4", "F004", 15, None),
    ("978-0-201-63361-0", "F004", 12, None),
    ("978-0-13-595705-9", "F005", 33, None),

    # Still out, overdue (overdue reminders report)
    ("978-0-13-468599-1", "U002", 50, None),     # 20 days late
    ("978-0-201-63361-0", "U002", 35, None),     # 5 days late; U002 is at the UG limit
    ("978-0-19-809930-7", "U004", 41, None),     # 11 days late
    ("978-0-13-454989-7", "U006", 33, None),     # 3 days late
    ("978-81-933284-9-1", "U008", 44, None),     # 14 days late
    ("978-0-13-411585-6", "U014", 38, None),     # 8 days late
    ("978-1-098-12597-4", "P004", 52, None),     # 22 days late
    ("978-0-13-411585-6", "P004", 52, None),     # 22 days late
    ("978-0-13-814757-0", "R002", 100, None),    # 10 days late (90-day loan)
    ("978-1-119-80119-0", "F003", 200, None),    # 20 days late (180-day loan)

    # Returned (history, some with fines paid)
    ("978-0-13-110362-7", "U001", 40, 12),
    ("978-0-596-51774-8", "U003", 70, 38),       # 2 days late
    ("978-93-89845-68-5", "U005", 100, 65),      # 5 days late
    ("978-1-718-50270-3", "U004", 120, 95),
    ("978-0-13-235088-4", "P003", 90, 50),       # 10 days late
    ("978-0-07-352332-3", "P001", 150, 125),
    ("978-1-985-08659-3", "R002", 200, 150),
    ("978-0-13-595705-9", "F002", 300, 200),
    ("978-0-13-454989-7", "U007", 80, 45),
    ("978-81-7709-187-8", "U008", 140, 100),
    ("978-0-321-98238-4", "P004", 110, 70),
    ("978-1-259-67651-2", "U010", 70, 28),
    ("978-0-13-668155-7", "U006", 90, 45),
    ("978-81-7371-146-6", "U009", 60, 22),
    ("978-0-13-475759-9", "R003", 400, 330),
    ("978-1-098-12597-4", "U005", 200, 160),
    ("978-0-13-110362-7", "U012", 75, 41),       # 4 days late
    ("978-0-07-352332-3", "P006", 66, 30),
    ("978-0-13-292401-7", "F003", 2400, 2300),   # 2019: only loan of this book in years
    # Returned yesterday, 9 days late; a reservation turned it into a hold (see below)
    ("978-0-13-461099-3", "U008", 40, 1),
]

# -- Reservations ------------------------------------------------------------
# (isbn, member, reserved N days ago, status, hold_until)
RESERVATIONS = [
    # Clean Code: all 3 copies out, two people waiting
    ("978-0-13-468599-1", "U003", 3, "Waiting", None),
    ("978-0-13-468599-1", "U013", 2, "Waiting", None),
    # Design Patterns: both copies out
    ("978-0-201-63361-0", "R001", 6, "Waiting", None),
    ("978-0-201-63361-0", "U009", 4, "Waiting", None),
    # AI: A Modern Approach: one copy out, the other just returned and held for P002
    ("978-0-13-461099-3", "P002", 14, "Hold", "held since yesterday"),
    ("978-0-13-461099-3", "U006", 9, "Waiting", None),
    # Deep Learning: both copies out
    ("978-0-262-03561-3", "U010", 7, "Waiting", None),
    # Hands-On Machine Learning: the only copy is overdue
    ("978-1-098-12597-4", "P005", 12, "Waiting", None),
    ("978-1-098-12597-4", "U007", 5, "Waiting", None),
    ("978-1-098-12597-4", "R005", 2, "Waiting", None),
    # Past reservations, kept for history
    ("978-0-13-235088-4", "P001", 40, "Fulfilled", None),
    ("978-0-321-48681-3", "U001", 60, "Expired", None),
    ("978-0-13-475759-9", "P007", 30, "Cancelled", None),
]


def populate(category_limits, fine_per_day, hold_days):
    """Add the demo rows. Needs an app context and existing tables.

    The app also calls this on Vercel to fill its temporary database.
    """
    for code, name, cat, joined in MEMBERS:
        if not db.session.get(Member, code):
            db.session.add(Member(code=code, name=name, category=cat, join_date=joined))

    for isbn, title, author, pub, rack, copies, added in BOOKS:
        if not db.session.get(Book, isbn):
            db.session.add(Book(isbn=isbn, title=title, author=author, publisher=pub,
                                rack_no=rack, total_copies=copies,
                                available_copies=copies, date_added=added))
    db.session.commit()

    categories = {code: cat for code, _, cat, _ in MEMBERS}
    for isbn, code, issued_ago, returned_ago in LOANS:
        issued = ago(issued_ago)
        due = issued + timedelta(days=category_limits[categories[code]]["days"])
        returned = ago(returned_ago) if returned_ago is not None else None
        fine = max(0, (returned - due).days) * fine_per_day if returned else 0.0
        if not Issue.query.filter_by(book_isbn=isbn, member_code=code, issue_date=issued).first():
            db.session.add(Issue(book_isbn=isbn, member_code=code, issue_date=issued,
                                 due_date=due, return_date=returned, penalty_paid=fine))

    for isbn, code, reserved_ago, status, hold in RESERVATIONS:
        # The copy came back yesterday, so the hold runs for hold_days from then
        hold_until = ago(1) + timedelta(days=hold_days) if hold else None
        if not Reservation.query.filter_by(book_isbn=isbn, member_code=code, status=status).first():
            db.session.add(Reservation(book_isbn=isbn, member_code=code,
                                       reservation_date=ago(reserved_ago),
                                       status=status, hold_until=hold_until))
    db.session.commit()

    # Copies on the shelf = total - copies on loan - copies held for a reservation
    for book in Book.query.all():
        on_loan = Issue.query.filter_by(book_isbn=book.isbn, return_date=None).count()
        held = Reservation.query.filter_by(book_isbn=book.isbn, status="Hold").count()
        book.available_copies = max(0, book.total_copies - on_loan - held)
    db.session.commit()


def seed():
    from app import app, CATEGORY_LIMITS, FINE_PER_DAY, HOLD_DAYS

    with app.app_context():
        if db.engine.url.get_backend_name() == "sqlite":
            db.drop_all()
            print("[..] Local SQLite database: cleared for a fresh demo.")
        elif "--reset" in sys.argv:
            host = db.engine.url.host
            answer = input(f"This deletes ALL library data on {host}. Type yes to continue: ")
            if answer.strip().lower() != "yes":
                print("Cancelled. Nothing was changed.")
                return
            db.drop_all()
            print("[..] Remote database: cleared for a fresh demo.")
        else:
            print("[..] Remote database: adding missing rows only, nothing is deleted.")
        db.create_all()

        populate(CATEGORY_LIMITS, FINE_PER_DAY, HOLD_DAYS)

        overdue = Issue.query.filter(Issue.return_date.is_(None), Issue.due_date < today).count()
        print("[OK] Seed complete.")
        print("   Members      :", Member.query.count())
        print("   Books        :", Book.query.count())
        print("   Loans        :", Issue.query.count(), f"({Issue.query.filter_by(return_date=None).count()} out, {overdue} overdue)")
        print("   Reservations :", Reservation.query.filter(Reservation.status.in_(["Waiting", "Hold"])).count(), "active")


if __name__ == "__main__":
    seed()
