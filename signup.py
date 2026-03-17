from tkinter import *
from tkcalendar import DateEntry
import sqlite3
import hashlib
import secrets
import os
import re

current_path = os.path.dirname(os.path.abspath(__file__))

# ── Design tokens (shared) ────────────────────────────────────────────────────
BG      = "#0D1117"
CARD    = "#161B22"
CARD2   = "#1C2128"
BORDER  = "#30363D"
GOLD    = "#D4A843"
GOLD_LT = "#F0C060"
RED     = "#F85149"
GREEN   = "#3FB950"
TEXT    = "#E6EDF3"
MUTED   = "#8B949E"
BLUE    = "#388BFD"
FONT_H  = ("Georgia", 14, "bold")
FONT_B  = ("Courier", 11)
FONT_SM = ("Courier", 10)


def make_label(parent, text, x, y, w=None, color=MUTED, font=FONT_SM):
    lbl = Label(parent, text=text, font=font, bg=CARD, fg=color, anchor=W)
    if w:
        lbl.place(x=x, y=y, width=w)
    else:
        lbl.place(x=x, y=y)
    return lbl


def make_entry(parent, x, y, w=200, show=None):
    e = Entry(parent, font=("Courier", 12), bg=CARD2,
              fg=TEXT, insertbackground=GOLD,
              highlightbackground=BORDER, highlightthickness=1,
              highlightcolor=GOLD, relief=FLAT, bd=0)
    if show:
        e.configure(show=show)
    e.place(x=x, y=y, width=w, height=36)
    return e


def style_btn(btn, color=GOLD, text_color=BG):
    btn.configure(
        bg=color, fg=text_color, font=("Georgia", 12, "bold"),
        relief=FLAT, cursor="hand2", bd=0,
        activebackground=GOLD_LT, activeforeground=BG,
        padx=20, pady=8
    )


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def init_db():
    db = sqlite3.connect(os.path.join(current_path, 'bank.db'))
    cr = db.cursor()
    cr.execute("""CREATE TABLE IF NOT EXISTS accounts (
        cin       TEXT PRIMARY KEY,
        firstname TEXT NOT NULL,
        lastname  TEXT NOT NULL,
        birthday  DATE,
        email     TEXT,
        adress    TEXT,
        password  TEXT NOT NULL,
        amount    REAL DEFAULT 0
    )""")
    cr.execute("""CREATE TABLE IF NOT EXISTS operations (
        id       INTEGER PRIMARY KEY AUTOINCREMENT,
        cin      TEXT NOT NULL,
        type     TEXT NOT NULL,
        amount   REAL NOT NULL,
        datetime TEXT NOT NULL,
        note     TEXT,
        FOREIGN KEY (cin) REFERENCES accounts(cin)
    )""")
    db.commit()
    return db


# ── Sign Up Page ──────────────────────────────────────────────────────────────
class SingUpPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Open New Account")
        self.root.geometry("600x620+320+30")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        # Top accent bar
        Frame(self.root, bg=GOLD, height=4).pack(fill=X, side=TOP)

        # Title bar
        title_bar = Frame(self.root, bg=BG, height=55)
        title_bar.pack(fill=X)
        Label(title_bar, text="✦  Open New Account",
              font=("Georgia", 17, "bold"), bg=BG, fg=GOLD)\
            .place(x=20, y=12)

        # Card
        card = Frame(self.root, bg=CARD,
                     highlightbackground=BORDER, highlightthickness=1)
        card.place(x=20, y=70, width=560, height=530)

        # ── Section: Personal Info ──
        Label(card, text="PERSONAL INFORMATION",
              font=("Courier", 9, "bold"), bg=CARD, fg=MUTED)\
            .place(x=20, y=18)
        Frame(card, bg=BORDER, height=1).place(x=20, y=36, width=520)

        make_label(card, "First Name", 20, 50)
        self.firstnamea = make_entry(card, 20, 70, 240)

        make_label(card, "Last Name", 300, 50)
        self.lastnamea = make_entry(card, 300, 70, 240)

        make_label(card, "CIN / National ID", 20, 120)
        self.cina = make_entry(card, 20, 140, 240)

        make_label(card, "Date of Birth", 300, 120)
        self.birthdaya = DateEntry(
            card, font=("Courier", 11), background=CARD2,
            foreground=TEXT, borderwidth=0, date_pattern='yyyy-mm-dd'
        )
        self.birthdaya.place(x=300, y=140, width=240, height=36)

        # ── Section: Contact ──
        Label(card, text="CONTACT DETAILS",
              font=("Courier", 9, "bold"), bg=CARD, fg=MUTED)\
            .place(x=20, y=195)
        Frame(card, bg=BORDER, height=1).place(x=20, y=213, width=520)

        make_label(card, "Email Address", 20, 225)
        self.emaila = make_entry(card, 20, 245, 520)

        make_label(card, "Home Address", 20, 295)
        self.adressa = make_entry(card, 20, 315, 520)

        # ── Initial Deposit ──
        Label(card, text="INITIAL DEPOSIT",
              font=("Courier", 9, "bold"), bg=CARD, fg=MUTED)\
            .place(x=20, y=368)
        Frame(card, bg=BORDER, height=1).place(x=20, y=386, width=520)

        make_label(card, "Opening Balance (DH)", 20, 398)
        self.initial_amount = make_entry(card, 20, 418, 200)
        self.initial_amount.insert(0, "0")

        # ── Agreement ──
        self.var = IntVar()
        chk = Checkbutton(
            card, text="  I agree to the Terms & Conditions",
            variable=self.var, font=FONT_SM,
            bg=CARD, fg=TEXT, selectcolor=CARD2,
            activebackground=CARD, activeforeground=GOLD,
            cursor="hand2"
        )
        chk.place(x=18, y=460)

        # ── Status label ──
        self.status_lbl = Label(card, text="", font=FONT_SM,
                                 bg=CARD, fg=RED, wraplength=520)
        self.status_lbl.place(x=20, y=490, width=520)

        # ── Submit ──
        btn = Button(card, text="Create Account", command=self.signup)
        style_btn(btn)
        btn.place(x=180, y=483, width=200, height=38)

    def set_status(self, msg, color=RED):
        self.status_lbl.configure(text=msg, fg=color)

    def signup(self):
        if self.var.get() != 1:
            self.set_status("⚠  Please accept the Terms & Conditions.")
            return

        firstname = self.firstnamea.get().strip()
        lastname  = self.lastnamea.get().strip()
        cin       = self.cina.get().strip().upper()
        birthday  = self.birthdaya.get_date()
        email     = self.emaila.get().strip()
        adress    = self.adressa.get().strip()
        init_amt  = self.initial_amount.get().strip()

        # Validation
        if not all([firstname, lastname, cin, email, adress]):
            self.set_status("⚠  All fields are required.")
            return
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.set_status("⚠  Please enter a valid email address.")
            return
        try:
            init_amt = float(init_amt)
            if init_amt < 0:
                raise ValueError
        except ValueError:
            self.set_status("⚠  Initial deposit must be a positive number.")
            return

        db = init_db()
        cr = db.cursor()

        cr.execute("SELECT cin FROM accounts WHERE cin = ?", (cin,))
        if cr.fetchone():
            self.set_status("⚠  An account with this CIN already exists.")
            db.close()
            return

        # Generate secure 6-digit password
        password_plain = str(secrets.randbelow(900000) + 100000)
        password_hash  = hash_password(password_plain)

        cr.execute(
            """INSERT INTO accounts
               (cin, firstname, lastname, birthday, email, adress, password, amount)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (cin, firstname, lastname, str(birthday),
             email, adress, password_hash, init_amt)
        )
        db.commit()
        db.close()

        # Clear fields
        for widget in [self.firstnamea, self.lastnamea,
                        self.cina, self.emaila, self.adressa]:
            widget.delete(0, END)
        self.initial_amount.delete(0, END)
        self.initial_amount.insert(0, "0")
        self.var.set(0)

        # Success popup
        self._show_success(cin, password_plain)

    def _show_success(self, cin, password):
        win = Toplevel(self.root)
        win.title("Account Created")
        win.geometry("400x280+370+200")
        win.configure(bg=BG)
        win.resizable(False, False)

        Frame(win, bg=GREEN, height=4).pack(fill=X)

        card = Frame(win, bg=CARD, highlightbackground=BORDER,
                     highlightthickness=1)
        card.place(x=20, y=20, width=360, height=240)

        Label(card, text="✔  Account Created!",
              font=("Georgia", 15, "bold"), bg=CARD, fg=GREEN)\
            .place(x=0, y=20, width=360)

        Label(card, text="Save your credentials below:",
              font=FONT_SM, bg=CARD, fg=MUTED)\
            .place(x=0, y=58, width=360)

        cred_frame = Frame(card, bg=CARD2,
                           highlightbackground=BORDER, highlightthickness=1)
        cred_frame.place(x=20, y=82, width=320, height=80)

        Label(cred_frame, text=f"Account Number:  {cin}",
              font=("Courier", 12, "bold"), bg=CARD2, fg=GOLD)\
            .place(x=10, y=10)
        Label(cred_frame, text=f"Password:          {password}",
              font=("Courier", 12, "bold"), bg=CARD2, fg=GOLD)\
            .place(x=10, y=42)

        Label(card, text="⚠ Store this password safely — it won't be shown again.",
              font=("Courier", 9), bg=CARD, fg=RED, wraplength=320)\
            .place(x=20, y=170)

        btn = Button(card, text="Done", command=win.destroy)
        style_btn(btn, GREEN, BG)
        btn.place(x=130, y=200, width=100, height=32)


if __name__ == "__main__":
    root = Tk()
    obj = SingUpPage(root)
    root.mainloop()