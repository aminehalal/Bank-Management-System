from tkinter import *
from tkinter import messagebox
import sqlite3
import hashlib
import datetime
import os

current_path = os.path.dirname(os.path.abspath(__file__))

# ── Design tokens ─────────────────────────────────────────────────────────────
BG      = "#0D1117"
CARD    = "#161B22"
CARD2   = "#1C2128"
CARD3   = "#21262D"
BORDER  = "#30363D"
GOLD    = "#D4A843"
GOLD_LT = "#F0C060"
RED     = "#F85149"
GREEN   = "#3FB950"
BLUE    = "#388BFD"
PURPLE  = "#BC8CFF"
TEXT    = "#E6EDF3"
MUTED   = "#8B949E"
FONT_H  = ("Georgia", 14, "bold")
FONT_B  = ("Courier", 11)
FONT_SM = ("Courier", 10)


def hash_password(p): return hashlib.sha256(p.encode()).hexdigest()


def get_db():
    return sqlite3.connect(os.path.join(current_path, 'bank.db'))


def style_btn(btn, color=GOLD, text_color=BG, size=12):
    btn.configure(
        bg=color, fg=text_color, font=("Georgia", size, "bold"),
        relief=FLAT, cursor="hand2", bd=0,
        activebackground=GOLD_LT, activeforeground=BG
    )


def make_entry(parent, x, y, w=200, show=None, placeholder=""):
    e = Entry(parent, font=("Courier", 12), bg=CARD2, fg=TEXT,
              insertbackground=GOLD, highlightbackground=BORDER,
              highlightthickness=1, highlightcolor=GOLD,
              relief=FLAT, bd=0)
    if show:
        e.configure(show=show)
    e.place(x=x, y=y, width=w, height=36)
    return e


# ── Bank User Dashboard ───────────────────────────────────────────────────────
class BankManagementSys:

    def __init__(self, root):
        self.root = root
        self.root.title("SecureBank — User Portal")
        self.root.geometry("900x650+120+30")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        # Ensure database schema is present/updated before UI actions
        ensure_db_schema()

        self._build_header()
        self._build_login_screen()

    # ── Header ────────────────────────────────────────────────────────────────
    def _build_header(self):
        Frame(self.root, bg=GOLD, height=4).pack(fill=X, side=TOP)

        hdr = Frame(self.root, bg=CARD, height=70,
                    highlightbackground=BORDER, highlightthickness=1)
        hdr.pack(fill=X)

        Label(hdr, text="◈  SECUREBANK",
              font=("Georgia", 22, "bold"), bg=CARD, fg=GOLD)\
            .place(x=20, y=12)

        Label(hdr, text="User Portal",
              font=("Courier", 11), bg=CARD, fg=MUTED)\
            .place(x=26, y=46)

        self.time_lbl = Label(hdr, text="", font=("Courier", 10),
                              bg=CARD, fg=MUTED)
        self.time_lbl.place(x=680, y=28)
        self._tick()

    def _tick(self):
        now = datetime.datetime.now().strftime("%d %b %Y  %H:%M:%S")
        self.time_lbl.configure(text=now)
        self.root.after(1000, self._tick)

    # ── Login Screen ──────────────────────────────────────────────────────────
    def _clear_main(self):
        for w in self.root.pack_slaves():
            if isinstance(w, Frame) and w.cget('bg') != GOLD:
                pass  # keep header
        for w in self.root.place_slaves():
            w.destroy()

    def _build_login_screen(self):
        # Destroy any existing placed content
        for w in list(self.root.children.values()):
            try:
                info = w.place_info()
                if info:
                    w.destroy()
            except Exception:
                pass

        outer = Frame(self.root, bg=BG)
        outer.place(x=0, y=74, width=900, height=576)
        self._login_outer = outer

        # Left panel — branding
        left = Frame(outer, bg=CARD2,
                     highlightbackground=BORDER, highlightthickness=1)
        left.place(x=40, y=60, width=340, height=420)

        Label(left, text="◈", font=("Georgia", 40), bg=CARD2, fg=GOLD)\
            .place(x=0, y=40, width=340)
        Label(left, text="SecureBank", font=("Georgia", 22, "bold"),
              bg=CARD2, fg=TEXT).place(x=0, y=110, width=340)
        Label(left, text="Your trusted financial partner",
              font=("Courier", 10), bg=CARD2, fg=MUTED)\
            .place(x=0, y=148, width=340)

        Frame(left, bg=BORDER, height=1).place(x=40, y=180, width=260)

        features = [
            ("⬡", "Secure Transactions"),
            ("⬡", "Real-time Balance"),
            ("⬡", "Transaction History"),
        ]
        for i, (icon, txt) in enumerate(features):
            Label(left, text=f" {icon}  {txt}",
                  font=("Courier", 11), bg=CARD2, fg=MUTED, anchor=W)\
                .place(x=60, y=205 + i * 40)

        Label(left, text="Protected by 256-bit encryption",
              font=("Courier", 9), bg=CARD2, fg=BORDER)\
            .place(x=0, y=380, width=340)

        # Right panel — form
        right = Frame(outer, bg=CARD,
                      highlightbackground=BORDER, highlightthickness=1)
        right.place(x=420, y=60, width=400, height=420)

        Label(right, text="Sign In", font=("Georgia", 20, "bold"),
              bg=CARD, fg=TEXT).place(x=30, y=30)
        Label(right, text="Enter your account credentials",
              font=("Courier", 10), bg=CARD, fg=MUTED)\
            .place(x=30, y=62)

        Frame(right, bg=BORDER, height=1).place(x=30, y=88, width=340)

        Label(right, text="Account Number", font=("Courier", 10),
              bg=CARD, fg=MUTED).place(x=30, y=105)
        self.username = make_entry(right, 30, 125, 340)

        Label(right, text="Password", font=("Courier", 10),
              bg=CARD, fg=MUTED).place(x=30, y=175)
        self.password = make_entry(right, 30, 195, 340, show="●")

        self.login_status = Label(right, text="", font=("Courier", 10),
                                   bg=CARD, fg=RED, wraplength=340)
        self.login_status.place(x=30, y=242)

        btn = Button(right, text="Sign In →", command=self._do_login)
        style_btn(btn)
        btn.place(x=30, y=270, width=340, height=42)

        Label(right, text="Forgot your password? Contact your branch.",
              font=("Courier", 9), bg=CARD, fg=MUTED)\
            .place(x=30, y=325)

        # Bind Enter key
        self.root.bind('<Return>', lambda e: self._do_login())

    # ── Login Logic ───────────────────────────────────────────────────────────
    def _do_login(self):
        cin   = self.username.get().strip().upper()
        passw = self.password.get().strip()

        if not cin or not passw:
            self.login_status.configure(text="⚠  All fields are required.")
            return

        # pw_hash = hash_password(passw)
        with get_db() as db:
            cr = db.cursor()
            cr.execute(
                "SELECT firstname, lastname, amount FROM accounts "
                "WHERE cin = ? AND password = ?",
                (cin, passw)
            )
            row = cr.fetchone()

        if row:
            self.root.unbind('<Return>')
            self._login_outer.destroy()
            self._build_dashboard(cin, row[0], row[1], row[2])
        else:
            self.login_status.configure(text="⚠  Invalid account number or password.")
            self.password.delete(0, END)

    # ── Dashboard ─────────────────────────────────────────────────────────────
    def _build_dashboard(self, cin, firstname, lastname, amount):
        self.cin       = cin
        self.firstname = firstname
        self.lastname  = lastname

        dash = Frame(self.root, bg=BG)
        dash.place(x=0, y=74, width=900, height=576)
        self._dash = dash

        # ── Left sidebar ──
        sidebar = Frame(dash, bg=CARD,
                        highlightbackground=BORDER, highlightthickness=1)
        sidebar.place(x=20, y=20, width=220, height=520)

        # Avatar
        av = Frame(sidebar, bg=GOLD, width=60, height=60)
        av.place(x=80, y=20)
        Label(av, text=firstname[0].upper() + lastname[0].upper(),
              font=("Georgia", 20, "bold"), bg=GOLD, fg=BG)\
            .place(x=0, y=8, width=60)

        Label(sidebar, text=f"{firstname} {lastname}",
              font=("Georgia", 12, "bold"), bg=CARD, fg=TEXT)\
            .place(x=0, y=100, width=220)
        Label(sidebar, text=f"#{cin}",
              font=("Courier", 10), bg=CARD, fg=MUTED)\
            .place(x=0, y=124, width=220)

        Frame(sidebar, bg=BORDER, height=1).place(x=20, y=155, width=180)

        # Nav buttons
        nav_items = [
            ("◈  Overview",    self._show_overview),
            ("↑  Deposit",     self._show_deposit),
            ("↓  Withdraw",    self._show_withdraw),
            ("↔  Transfer",    self._show_transfer),
            ("⊟  History",     self._show_history),
        ]
        self._nav_btns = []
        for i, (label, cmd) in enumerate(nav_items):
            b = Button(sidebar, text=label, command=cmd,
                       font=("Courier", 11), bg=CARD, fg=TEXT,
                       relief=FLAT, anchor=W, cursor="hand2",
                       activebackground=CARD2, activeforeground=GOLD,
                       padx=16)
            b.place(x=0, y=175 + i * 46, width=220, height=42)
            self._nav_btns.append(b)

        Frame(sidebar, bg=BORDER, height=1).place(x=20, y=415, width=180)

        logout_btn = Button(sidebar, text="⎋  Logout",
                            command=self._logout,
                            font=("Courier", 11), bg=CARD, fg=RED,
                            relief=FLAT, anchor=W, cursor="hand2",
                            activebackground=CARD2, activeforeground=RED,
                            padx=16)
        logout_btn.place(x=0, y=430, width=220, height=42)

        # ── Main content area ──
        self.content = Frame(dash, bg=BG)
        self.content.place(x=260, y=20, width=620, height=520)

        self._show_overview()

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _highlight_nav(self, idx):
        for i, b in enumerate(self._nav_btns):
            b.configure(bg=CARD2 if i == idx else CARD,
                        fg=GOLD if i == idx else TEXT)

    # ── Overview ──────────────────────────────────────────────────────────────
    def _show_overview(self):
        self._clear_content()
        self._highlight_nav(0)

        with get_db() as db:
            cr = db.cursor()
            cr.execute("SELECT amount FROM accounts WHERE cin = ?", (self.cin,))
            amount = cr.fetchone()[0]
            cr.execute(
                "SELECT type, amount, datetime FROM operations "
                "WHERE cin = ? ORDER BY datetime DESC LIMIT 5",
                (self.cin,)
            )
            recent = cr.fetchall()

        Label(self.content, text="Account Overview",
              font=("Georgia", 18, "bold"), bg=BG, fg=TEXT)\
            .place(x=0, y=0)

        # Balance card
        bal_card = Frame(self.content, bg=CARD,
                         highlightbackground=GOLD, highlightthickness=1)
        bal_card.place(x=0, y=40, width=300, height=130)

        Label(bal_card, text="AVAILABLE BALANCE",
              font=("Courier", 9, "bold"), bg=CARD, fg=MUTED)\
            .place(x=20, y=18)
        Label(bal_card, text=f"{amount:,.2f} DH",
              font=("Georgia", 24, "bold"), bg=CARD, fg=GOLD)\
            .place(x=20, y=45)
        Label(bal_card, text=f"Account  #{self.cin}",
              font=("Courier", 10), bg=CARD, fg=MUTED)\
            .place(x=20, y=95)

        # Stats cards
        with get_db() as db:
            cr = db.cursor()
            cr.execute(
                "SELECT COALESCE(SUM(amount),0) FROM operations "
                "WHERE cin=? AND type='Deposit'", (self.cin,)
            )
            total_dep = cr.fetchone()[0]
            cr.execute(
                "SELECT COALESCE(SUM(amount),0) FROM operations "
                "WHERE cin=? AND type='Withdrawal'", (self.cin,)
            )
            total_wd = cr.fetchone()[0]

        for i, (label, value, color) in enumerate([
            ("Total Deposited",  f"{total_dep:,.0f} DH", GREEN),
            ("Total Withdrawn",  f"{total_wd:,.0f} DH",  RED),
        ]):
            sc = Frame(self.content, bg=CARD,
                       highlightbackground=BORDER, highlightthickness=1)
            sc.place(x=320 + i * 155, y=40, width=140, height=130)
            Label(sc, text=label, font=("Courier", 9), bg=CARD, fg=MUTED,
                  wraplength=120).place(x=10, y=15)
            Label(sc, text=value, font=("Georgia", 14, "bold"),
                  bg=CARD, fg=color).place(x=10, y=60)

        # Recent transactions
        Label(self.content, text="Recent Transactions",
              font=("Georgia", 13, "bold"), bg=BG, fg=TEXT)\
            .place(x=0, y=192)

        if not recent:
            Label(self.content, text="No transactions yet.",
                  font=FONT_SM, bg=BG, fg=MUTED).place(x=0, y=225)
        else:
            for i, (typ, amt, dt) in enumerate(recent):
                row = Frame(self.content, bg=CARD,
                            highlightbackground=BORDER, highlightthickness=1)
                row.place(x=0, y=222 + i * 52, width=610, height=44)

                color = GREEN if typ == "Deposit" else (RED if typ == "Withdrawal" else BLUE)
                sym   = "+" if typ == "Deposit" else ("−" if typ == "Withdrawal" else "↔")

                Label(row, text=f"  {typ}", font=("Courier", 11, "bold"),
                      bg=CARD, fg=color, anchor=W).place(x=0, y=4, width=180)
                Label(row, text=f"{sym}{float(amt):,.2f} DH",
                      font=("Georgia", 12, "bold"), bg=CARD,
                      fg=color).place(x=180, y=4, width=180)
                Label(row, text=str(dt)[:19], font=("Courier", 9),
                      bg=CARD, fg=MUTED).place(x=370, y=10)

    # ── Deposit ───────────────────────────────────────────────────────────────
    def _show_deposit(self):
        self._clear_content()
        self._highlight_nav(1)
        self._build_transaction_form(
            "Deposit Funds", GREEN,
            "Amount to Deposit (DH)", self._do_deposit
        )

    def _show_withdraw(self):
        self._clear_content()
        self._highlight_nav(2)
        self._build_transaction_form(
            "Withdraw Funds", RED,
            "Amount to Withdraw (DH)", self._do_withdraw
        )

    def _build_transaction_form(self, title, color, label_text, action):
        Label(self.content, text=title,
              font=("Georgia", 18, "bold"), bg=BG, fg=TEXT)\
            .place(x=0, y=0)

        card = Frame(self.content, bg=CARD,
                     highlightbackground=BORDER, highlightthickness=1)
        card.place(x=0, y=50, width=500, height=300)

        with get_db() as db:
            cr = db.cursor()
            cr.execute("SELECT amount FROM accounts WHERE cin = ?", (self.cin,))
            amount = cr.fetchone()[0]

        Label(card, text="Current Balance",
              font=("Courier", 10), bg=CARD, fg=MUTED).place(x=30, y=25)
        Label(card, text=f"{amount:,.2f} DH",
              font=("Georgia", 20, "bold"), bg=CARD, fg=GOLD)\
            .place(x=30, y=50)

        Frame(card, bg=BORDER, height=1).place(x=30, y=90, width=440)

        Label(card, text=label_text, font=("Courier", 10),
              bg=CARD, fg=MUTED).place(x=30, y=108)
        self._txn_entry = make_entry(card, 30, 132, 300)

        Label(card, text="Note (optional)", font=("Courier", 10),
              bg=CARD, fg=MUTED).place(x=30, y=182)
        self._note_entry = make_entry(card, 30, 202, 440)

        self._txn_status = Label(card, text="", font=("Courier", 10),
                                  bg=CARD, fg=RED, wraplength=440)
        self._txn_status.place(x=30, y=245)

        btn = Button(card, text="Confirm", command=action)
        style_btn(btn, color, BG if color != RED else TEXT)
        btn.place(x=30, y=245, width=150, height=38)

    def _do_deposit(self):
        self._process_txn("Deposit")

    def _do_withdraw(self):
        self._process_txn("Withdrawal")

    def _process_txn(self, txn_type):
        raw = self._txn_entry.get().strip()
        note = self._note_entry.get().strip()
        try:
            amt = float(raw)
            if amt <= 0:
                raise ValueError
        except ValueError:
            self._txn_status.configure(text="⚠  Enter a valid positive amount.")
            return

        with get_db() as db:
            cr = db.cursor()
            cr.execute("SELECT amount FROM accounts WHERE cin = ?", (self.cin,))
            balance = cr.fetchone()[0]

            if txn_type == "Withdrawal" and amt > balance:
                self._txn_status.configure(
                    text=f"⚠  Insufficient funds. Balance: {balance:,.2f} DH")
                return

            if txn_type == "Deposit":
                cr.execute("UPDATE accounts SET amount = amount + ? WHERE cin = ?",
                           (amt, self.cin))
            else:
                cr.execute("UPDATE accounts SET amount = amount - ? WHERE cin = ?",
                           (amt, self.cin))

            cr.execute(
                "INSERT INTO operations (cin, type, amount, datetime, note) "
                "VALUES (?, ?, ?, ?, ?)",
                (self.cin, txn_type, amt,
                 str(datetime.datetime.now())[:19], note)
            )
            db.commit()

        self._txn_entry.delete(0, END)
        self._note_entry.delete(0, END)
        sym = "+" if txn_type == "Deposit" else "−"
        color = GREEN if txn_type == "Deposit" else RED
        self._txn_status.configure(
            text=f"✔  {txn_type} of {sym}{amt:,.2f} DH successful!",
            fg=color
        )
        # Refresh overview after a moment
        self.root.after(1500, self._show_overview)

    # ── Transfer ──────────────────────────────────────────────────────────────
    def _show_transfer(self):
        self._clear_content()
        self._highlight_nav(3)

        Label(self.content, text="Transfer Funds",
              font=("Georgia", 18, "bold"), bg=BG, fg=TEXT).place(x=0, y=0)

        card = Frame(self.content, bg=CARD,
                     highlightbackground=BORDER, highlightthickness=1)
        card.place(x=0, y=50, width=500, height=340)

        with get_db() as db:
            cr = db.cursor()
            cr.execute("SELECT amount FROM accounts WHERE cin=?", (self.cin,))
            balance = cr.fetchone()[0]

        Label(card, text="Your Balance",
              font=("Courier", 10), bg=CARD, fg=MUTED).place(x=30, y=22)
        Label(card, text=f"{balance:,.2f} DH",
              font=("Georgia", 20, "bold"), bg=CARD, fg=GOLD).place(x=30, y=46)
        Frame(card, bg=BORDER, height=1).place(x=30, y=88, width=440)

        Label(card, text="Recipient Account Number",
              font=("Courier", 10), bg=CARD, fg=MUTED).place(x=30, y=105)
        self._to_cin = make_entry(card, 30, 128, 300)

        Label(card, text="Amount (DH)",
              font=("Courier", 10), bg=CARD, fg=MUTED).place(x=30, y=178)
        self._tr_amount = make_entry(card, 30, 200, 200)

        Label(card, text="Note (optional)",
              font=("Courier", 10), bg=CARD, fg=MUTED).place(x=30, y=248)
        self._tr_note = make_entry(card, 30, 268, 440)

        self._tr_status = Label(card, text="", font=("Courier", 10),
                                 bg=CARD, fg=RED, wraplength=440)
        self._tr_status.place(x=30, y=310)

        btn = Button(card, text="Transfer →", command=self._do_transfer)
        style_btn(btn, BLUE, TEXT)
        btn.place(x=30, y=300, width=160, height=38)

    def _do_transfer(self):
        to_cin = self._to_cin.get().strip().upper()
        raw    = self._tr_amount.get().strip()
        note   = self._tr_note.get().strip()

        if not to_cin:
            self._tr_status.configure(text="⚠  Enter recipient account number.")
            return
        if to_cin == self.cin:
            self._tr_status.configure(text="⚠  Cannot transfer to your own account.")
            return
        try:
            amt = float(raw)
            if amt <= 0:
                raise ValueError
        except ValueError:
            self._tr_status.configure(text="⚠  Enter a valid positive amount.")
            return

        with get_db() as db:
            cr = db.cursor()
            cr.execute("SELECT firstname, lastname, amount FROM accounts WHERE cin=?",
                       (to_cin,))
            recipient = cr.fetchone()
            if not recipient:
                self._tr_status.configure(
                    text=f"⚠  Account {to_cin} not found.")
                return

            cr.execute("SELECT amount FROM accounts WHERE cin=?", (self.cin,))
            my_balance = cr.fetchone()[0]
            if amt > my_balance:
                self._tr_status.configure(
                    text=f"⚠  Insufficient funds. Balance: {my_balance:,.2f} DH")
                return

            ts = str(datetime.datetime.now())[:19]
            cr.execute("UPDATE accounts SET amount = amount - ? WHERE cin=?",
                       (amt, self.cin))
            cr.execute("UPDATE accounts SET amount = amount + ? WHERE cin=?",
                       (amt, to_cin))
            cr.execute(
                "INSERT INTO operations (cin,type,amount,datetime,note) VALUES (?,?,?,?,?)",
                (self.cin, "Transfer Out", amt, ts,
                 f"To {to_cin}" + (f": {note}" if note else ""))
            )
            cr.execute(
                "INSERT INTO operations (cin,type,amount,datetime,note) VALUES (?,?,?,?,?)",
                (to_cin, "Transfer In", amt, ts,
                 f"From {self.cin}" + (f": {note}" if note else ""))
            )
            db.commit()

        rname = f"{recipient[0]} {recipient[1]}"
        self._tr_status.configure(
            text=f"✔  Transferred {amt:,.2f} DH to {rname} ({to_cin})", fg=GREEN)
        self._to_cin.delete(0, END)
        self._tr_amount.delete(0, END)
        self._tr_note.delete(0, END)
        self.root.after(2000, self._show_overview)

    # ── History ───────────────────────────────────────────────────────────────
    def _show_history(self):
        self._clear_content()
        self._highlight_nav(4)

        Label(self.content, text="Transaction History",
              font=("Georgia", 18, "bold"), bg=BG, fg=TEXT).place(x=0, y=0)

        with get_db() as db:
            cr = db.cursor()
            cr.execute(
                "SELECT type, amount, datetime, note FROM operations "
                "WHERE cin=? ORDER BY datetime DESC LIMIT 20",
                (self.cin,)
            )
            rows = cr.fetchall()

        # Header row
        hdr = Frame(self.content, bg=CARD2,
                    highlightbackground=BORDER, highlightthickness=1)
        hdr.place(x=0, y=40, width=610, height=32)
        for txt, xp, wp in [("Type", 10, 120), ("Amount", 140, 140),
                              ("Date & Time", 290, 180), ("Note", 480, 120)]:
            Label(hdr, text=txt, font=("Courier", 9, "bold"),
                  bg=CARD2, fg=MUTED, anchor=W).place(x=xp, y=6, width=wp)

        if not rows:
            Label(self.content, text="No transactions recorded.",
                  font=FONT_SM, bg=BG, fg=MUTED).place(x=0, y=90)
            return

        # Scrollable-ish: show up to 9 rows
        for i, (typ, amt, dt, note) in enumerate(rows[:9]):
            color = (GREEN if typ in ("Deposit", "Transfer In")
                     else RED if typ in ("Withdrawal", "Transfer Out")
                     else BLUE)
            bg_row = CARD if i % 2 == 0 else CARD2
            row = Frame(self.content, bg=bg_row,
                        highlightbackground=BORDER, highlightthickness=1)
            row.place(x=0, y=74 + i * 46, width=610, height=40)
            sym = "+" if typ in ("Deposit", "Transfer In") else "−"
            Label(row, text=f"  {typ}", font=("Courier", 10),
                  bg=bg_row, fg=color, anchor=W).place(x=0, y=8, width=130)
            Label(row, text=f"{sym}{float(amt):,.2f} DH",
                  font=("Courier", 10, "bold"), bg=bg_row,
                  fg=color, anchor=W).place(x=140, y=8, width=140)
            Label(row, text=str(dt)[:19], font=("Courier", 9),
                  bg=bg_row, fg=MUTED, anchor=W).place(x=290, y=10, width=180)
            Label(row, text=(note or "—"), font=("Courier", 9),
                  bg=bg_row, fg=MUTED, anchor=W).place(x=480, y=10, width=120)

    # ── Logout ────────────────────────────────────────────────────────────────
    def _logout(self):
        self._dash.destroy()
        self._build_login_screen()


if __name__ == "__main__":
    root = Tk()
    obj = BankManagementSys(root)
    root.mainloop()