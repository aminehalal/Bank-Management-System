from tkinter import *
from tkinter import messagebox
from signup import SingUpPage
from bank import BankManagementSys
import sqlite3
import datetime
import hashlib
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
ORANGE  = "#E3B341"
TEXT    = "#E6EDF3"
MUTED   = "#8B949E"
FONT_H  = ("Georgia", 14, "bold")
FONT_B  = ("Courier", 11)
FONT_SM = ("Courier", 10)

ADMIN_PASS = hashlib.sha256(b"admin1234").hexdigest()  # default: admin1234


def get_db():
    return sqlite3.connect(os.path.join(current_path, 'bank.db'))


def style_btn(btn, color=GOLD, text_color=BG, size=11):
    btn.configure(
        bg=color, fg=text_color, font=("Georgia", size, "bold"),
        relief=FLAT, cursor="hand2", bd=0,
        activebackground=GOLD_LT, activeforeground=BG
    )


def make_entry(parent, x, y, w=240, show=None):
    e = Entry(parent, font=("Courier", 12), bg=CARD2, fg=TEXT,
              insertbackground=GOLD, highlightbackground=BORDER,
              highlightthickness=1, highlightcolor=GOLD,
              relief=FLAT, bd=0)
    if show:
        e.configure(show=show)
    e.place(x=x, y=y, width=w, height=36)
    return e


# ── Admin Portal ──────────────────────────────────────────────────────────────
class BankManagementAdmin:

    def __init__(self, root):
        self.root = root
        self.root.title("SecureBank — Admin Console")
        self.root.geometry("1020x700+80+10")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self._build_header()
        self._build_admin_login()

    # ── Header ────────────────────────────────────────────────────────────────
    def _build_header(self):
        Frame(self.root, bg=ORANGE, height=4).pack(fill=X, side=TOP)

        hdr = Frame(self.root, bg=CARD, height=70,
                    highlightbackground=BORDER, highlightthickness=1)
        hdr.pack(fill=X)

        Label(hdr, text="◈  SECUREBANK",
              font=("Georgia", 22, "bold"), bg=CARD, fg=GOLD)\
            .place(x=20, y=12)
        Label(hdr, text="Admin Console",
              font=("Courier", 11), bg=CARD, fg=ORANGE)\
            .place(x=26, y=46)

        self.time_lbl = Label(hdr, text="", font=("Courier", 10),
                              bg=CARD, fg=MUTED)
        self.time_lbl.place(x=760, y=28)
        self._tick()

    def _tick(self):
        now = datetime.datetime.now().strftime("%d %b %Y  %H:%M:%S")
        self.time_lbl.configure(text=now)
        self.root.after(1000, self._tick)

    # ── Admin Login ───────────────────────────────────────────────────────────
    def _build_admin_login(self):
        self._login_frame = Frame(self.root, bg=BG)
        self._login_frame.place(x=0, y=74, width=1020, height=626)

        card = Frame(self._login_frame, bg=CARD,
                     highlightbackground=ORANGE, highlightthickness=1)
        card.place(x=310, y=100, width=400, height=340)

        Label(card, text="Admin Access",
              font=("Georgia", 20, "bold"), bg=CARD, fg=ORANGE)\
            .place(x=0, y=30, width=400)
        Label(card, text="Restricted — Authorised Personnel Only",
              font=("Courier", 10), bg=CARD, fg=MUTED)\
            .place(x=0, y=62, width=400)

        Frame(card, bg=BORDER, height=1).place(x=30, y=92, width=340)

        Label(card, text="Admin Password", font=("Courier", 10),
              bg=CARD, fg=MUTED).place(x=30, y=108)
        self._admin_pass = make_entry(card, 30, 132, 340, show="●")

        self._login_status = Label(card, text="", font=("Courier", 10),
                                    bg=CARD, fg=RED)
        self._login_status.place(x=30, y=180)

        btn = Button(card, text="Enter Console", command=self._do_admin_login)
        style_btn(btn, ORANGE, BG)
        btn.place(x=30, y=200, width=340, height=42)

        Label(card, text="Default password: admin1234",
              font=("Courier", 9), bg=CARD, fg=BORDER)\
            .place(x=30, y=258)

        Label(card, text="⚠  All actions are logged.",
              font=("Courier", 9), bg=CARD, fg=MUTED)\
            .place(x=30, y=280)

        btn2 = Button(card, text="→ User Mode", command=self.usermode,
                      font=("Courier", 10), bg=CARD, fg=BLUE,
                      relief=FLAT, cursor="hand2", activebackground=CARD)
        btn2.place(x=130, y=305)

        self._admin_pass.bind('<Return>', lambda e: self._do_admin_login())

    def _do_admin_login(self):
        pw = self._admin_pass.get().strip()
        if hashlib.sha256(pw.encode()).hexdigest() == ADMIN_PASS:
            self._login_frame.destroy()
            self._build_console()
        else:
            self._login_status.configure(text="⚠  Incorrect admin password.")
            self._admin_pass.delete(0, END)

    # ── Main Console ──────────────────────────────────────────────────────────
    def _build_console(self):
        console = Frame(self.root, bg=BG)
        console.place(x=0, y=74, width=1020, height=626)
        self._console = console

        # ── Sidebar ──
        sidebar = Frame(console, bg=CARD,
                        highlightbackground=BORDER, highlightthickness=1)
        sidebar.place(x=20, y=20, width=220, height=570)

        Label(sidebar, text="ADMIN",
              font=("Georgia", 14, "bold"), bg=CARD, fg=ORANGE)\
            .place(x=0, y=20, width=220)
        Label(sidebar, text="SecureBank Console",
              font=("Courier", 9), bg=CARD, fg=MUTED)\
            .place(x=0, y=46, width=220)

        Frame(sidebar, bg=BORDER, height=1).place(x=20, y=72, width=180)

        nav_items = [
            ("◈  Dashboard",      self._show_dashboard),
            ("＋  Add Account",    self.signupdetail),
            ("✕  Delete Account",  self._show_delete),
            ("⊟  View Account",    self._show_check),
            ("≡  All Accounts",    self._show_all_accounts),
        ]
        self._nav_btns = []
        for i, (lbl, cmd) in enumerate(nav_items):
            b = Button(sidebar, text=lbl, command=cmd,
                       font=("Courier", 11), bg=CARD, fg=TEXT,
                       relief=FLAT, anchor=W, cursor="hand2",
                       activebackground=CARD2, activeforeground=ORANGE,
                       padx=16)
            b.place(x=0, y=90 + i * 46, width=220, height=42)
            self._nav_btns.append(b)

        Frame(sidebar, bg=BORDER, height=1).place(x=20, y=328, width=180)

        Button(sidebar, text="→ User Mode", command=self.usermode,
               font=("Courier", 11), bg=CARD, fg=BLUE,
               relief=FLAT, anchor=W, cursor="hand2",
               activebackground=CARD2, activeforeground=BLUE,
               padx=16).place(x=0, y=346, width=220, height=42)

        Button(sidebar, text="⎋  Logout", command=self._logout,
               font=("Courier", 11), bg=CARD, fg=RED,
               relief=FLAT, anchor=W, cursor="hand2",
               activebackground=CARD2, activeforeground=RED,
               padx=16).place(x=0, y=524, width=220, height=42)

        # ── Content ──
        self.content = Frame(console, bg=BG)
        self.content.place(x=260, y=20, width=740, height=570)

        self._show_dashboard()

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _highlight_nav(self, idx):
        for i, b in enumerate(self._nav_btns):
            b.configure(bg=CARD2 if i == idx else CARD,
                        fg=ORANGE if i == idx else TEXT)

    # ── Dashboard ─────────────────────────────────────────────────────────────
    def _show_dashboard(self):
        self._clear_content()
        self._highlight_nav(0)

        Label(self.content, text="Admin Dashboard",
              font=("Georgia", 18, "bold"), bg=BG, fg=TEXT).place(x=0, y=0)

        with get_db() as db:
            cr = db.cursor()
            cr.execute("SELECT COUNT(*) FROM accounts")
            n_accounts = cr.fetchone()[0]
            cr.execute("SELECT COALESCE(SUM(amount),0) FROM accounts")
            total_balance = cr.fetchone()[0]
            cr.execute("SELECT COUNT(*) FROM operations")
            n_txns = cr.fetchone()[0]
            cr.execute(
                "SELECT cin, firstname, lastname, amount FROM accounts "
                "ORDER BY amount DESC LIMIT 5"
            )
            top = cr.fetchall()
            cr.execute(
                "SELECT cin, type, amount, datetime FROM operations "
                "ORDER BY datetime DESC LIMIT 6"
            )
            recent_ops = cr.fetchall()

        # Stat cards
        stats = [
            ("Total Accounts",  str(n_accounts),        BLUE),
            ("Total Deposits",  f"{total_balance:,.0f} DH", GOLD),
            ("Transactions",    str(n_txns),             GREEN),
        ]
        for i, (label, value, color) in enumerate(stats):
            sc = Frame(self.content, bg=CARD,
                       highlightbackground=BORDER, highlightthickness=1)
            sc.place(x=i * 245, y=40, width=230, height=100)
            Label(sc, text=label, font=("Courier", 9, "bold"),
                  bg=CARD, fg=MUTED).place(x=15, y=15)
            Label(sc, text=value, font=("Georgia", 20, "bold"),
                  bg=CARD, fg=color).place(x=15, y=45)

        # Top accounts
        Label(self.content, text="Top Accounts by Balance",
              font=("Georgia", 13, "bold"), bg=BG, fg=TEXT).place(x=0, y=162)

        for i, (cin, fn, ln, amt) in enumerate(top):
            row = Frame(self.content, bg=CARD,
                        highlightbackground=BORDER, highlightthickness=1)
            row.place(x=0, y=192 + i * 44, width=360, height=38)
            Label(row, text=f"  #{cin}", font=("Courier", 10),
                  bg=CARD, fg=MUTED, anchor=W).place(x=0, y=8, width=130)
            Label(row, text=f"{fn} {ln}", font=("Courier", 10),
                  bg=CARD, fg=TEXT, anchor=W).place(x=130, y=8, width=140)
            Label(row, text=f"{amt:,.0f} DH",
                  font=("Courier", 10, "bold"), bg=CARD,
                  fg=GOLD, anchor=E).place(x=250, y=8, width=100)

        # Recent ops
        Label(self.content, text="Recent Transactions",
              font=("Georgia", 13, "bold"), bg=BG, fg=TEXT)\
            .place(x=380, y=162)

        for i, (cin, typ, amt, dt) in enumerate(recent_ops):
            color = GREEN if typ in ("Deposit", "Transfer In") else RED
            row = Frame(self.content, bg=CARD,
                        highlightbackground=BORDER, highlightthickness=1)
            row.place(x=380, y=192 + i * 57, width=355, height=50)
            Label(row, text=f"  #{cin}", font=("Courier", 9),
                  bg=CARD, fg=MUTED, anchor=W).place(x=0, y=4, width=130)
            Label(row, text=typ, font=("Courier", 9),
                  bg=CARD, fg=color, anchor=W).place(x=130, y=4, width=100)
            Label(row, text=f"{float(amt):,.0f} DH",
                  font=("Courier", 9, "bold"), bg=CARD,
                  fg=color).place(x=240, y=4, width=100)
            Label(row, text=str(dt)[:16], font=("Courier", 8),
                  bg=CARD, fg=MUTED).place(x=10, y=28, width=200)

    # ── Delete Account ────────────────────────────────────────────────────────
    def _show_delete(self):
        self._clear_content()
        self._highlight_nav(2)

        Label(self.content, text="Delete Account",
              font=("Georgia", 18, "bold"), bg=BG, fg=TEXT).place(x=0, y=0)

        card = Frame(self.content, bg=CARD,
                     highlightbackground=BORDER, highlightthickness=1)
        card.place(x=0, y=50, width=500, height=280)

        Label(card, text="⚠  This action is irreversible.",
              font=("Courier", 10), bg=CARD, fg=ORANGE).place(x=30, y=20)

        Label(card, text="Account CIN / Number",
              font=("Courier", 10), bg=CARD, fg=MUTED).place(x=30, y=55)
        self._del_cin = make_entry(card, 30, 78, 340)

        self._del_status = Label(card, text="", font=("Courier", 10),
                                  bg=CARD, fg=RED, wraplength=440)
        self._del_status.place(x=30, y=130)

        btn = Button(card, text="Delete Account", command=self._do_delete)
        style_btn(btn, RED, TEXT)
        btn.place(x=30, y=130, width=200, height=38)

        # Result area
        self._del_result = Frame(card, bg=CARD)
        self._del_result.place(x=30, y=185, width=440, height=80)

    def _do_delete(self):
        cin = self._del_cin.get().strip().upper()
        if not cin:
            self._del_status.configure(text="⚠  Enter an account number.")
            return

        if not messagebox.askyesno(
            "Confirm Deletion",
            f"Permanently delete account {cin} and all its records?\n\nThis cannot be undone.",
            parent=self.root
        ):
            return

        with get_db() as db:
            cr = db.cursor()
            cr.execute("SELECT firstname, lastname FROM accounts WHERE cin=?", (cin,))
            row = cr.fetchone()
            if row:
                cr.execute("DELETE FROM operations WHERE cin=?", (cin,))
                cr.execute("DELETE FROM accounts WHERE cin=?", (cin,))
                db.commit()
                self._del_status.configure(
                    text=f"✔  Account {cin} ({row[0]} {row[1]}) has been deleted.",
                    fg=GREEN
                )
            else:
                self._del_status.configure(
                    text=f"⚠  Account {cin} not found.", fg=RED)

        self._del_cin.delete(0, END)

    # ── View Account ──────────────────────────────────────────────────────────
    def _show_check(self):
        self._clear_content()
        self._highlight_nav(3)

        Label(self.content, text="View Account",
              font=("Georgia", 18, "bold"), bg=BG, fg=TEXT).place(x=0, y=0)

        top = Frame(self.content, bg=CARD,
                    highlightbackground=BORDER, highlightthickness=1)
        top.place(x=0, y=50, width=740, height=80)

        Label(top, text="Account CIN / Number",
              font=("Courier", 10), bg=CARD, fg=MUTED).place(x=20, y=12)
        self._check_cin = make_entry(top, 20, 36, 340)

        btn = Button(top, text="Lookup →", command=self._do_check)
        style_btn(btn, BLUE, TEXT)
        btn.place(x=380, y=30, width=140, height=38)

        self._check_area = Frame(self.content, bg=BG)
        self._check_area.place(x=0, y=148, width=740, height=420)

        self._check_cin.bind('<Return>', lambda e: self._do_check())

    def _do_check(self):
        for w in self._check_area.winfo_children():
            w.destroy()

        cin = self._check_cin.get().strip().upper()
        if not cin:
            return

        with get_db() as db:
            cr = db.cursor()
            cr.execute(
                "SELECT firstname, lastname, birthday, email, adress, amount "
                "FROM accounts WHERE cin=?", (cin,)
            )
            acct = cr.fetchone()
            if not acct:
                Label(self._check_area,
                      text=f"⚠  Account {cin} not found.",
                      font=FONT_B, bg=BG, fg=RED).place(x=0, y=10)
                return

            cr.execute(
                "SELECT type, amount, datetime, note FROM operations "
                "WHERE cin=? ORDER BY datetime DESC LIMIT 8", (cin,)
            )
            ops = cr.fetchall()

        fn, ln, bd, email, adress, balance = acct

        # Account info card
        info = Frame(self._check_area, bg=CARD,
                     highlightbackground=BORDER, highlightthickness=1)
        info.place(x=0, y=0, width=340, height=200)

        Label(info, text=f"{fn} {ln}",
              font=("Georgia", 14, "bold"), bg=CARD, fg=TEXT)\
            .place(x=15, y=15)
        Label(info, text=f"#{cin}",
              font=("Courier", 10), bg=CARD, fg=MUTED).place(x=15, y=44)

        for i, (lbl, val) in enumerate([
            ("Balance",  f"{balance:,.2f} DH"),
            ("Birthday", str(bd)),
            ("Email",    str(email)),
            ("Address",  str(adress)),
        ]):
            Label(info, text=lbl, font=("Courier", 9),
                  bg=CARD, fg=MUTED, anchor=W).place(x=15, y=75 + i * 28)
            Label(info, text=val, font=("Courier", 10),
                  bg=CARD, fg=(GOLD if lbl == "Balance" else TEXT), anchor=W)\
                .place(x=105, y=75 + i * 28, width=220)

        # Transactions
        Label(self._check_area, text="Recent Transactions",
              font=("Georgia", 12, "bold"), bg=BG, fg=TEXT)\
            .place(x=360, y=0)

        if not ops:
            Label(self._check_area, text="No transactions.",
                  font=FONT_SM, bg=BG, fg=MUTED).place(x=360, y=30)
        else:
            for i, (typ, amt, dt, note) in enumerate(ops):
                color = (GREEN if typ in ("Deposit", "Transfer In")
                         else RED if typ in ("Withdrawal", "Transfer Out")
                         else BLUE)
                row = Frame(self._check_area, bg=CARD,
                            highlightbackground=BORDER, highlightthickness=1)
                row.place(x=360, y=28 + i * 46, width=376, height=40)
                Label(row, text=f"  {typ}", font=("Courier", 9),
                      bg=CARD, fg=color, anchor=W).place(x=0, y=6, width=120)
                Label(row, text=f"{float(amt):,.0f} DH",
                      font=("Courier", 10, "bold"), bg=CARD,
                      fg=color).place(x=125, y=6, width=100)
                Label(row, text=str(dt)[:16], font=("Courier", 8),
                      bg=CARD, fg=MUTED).place(x=235, y=10, width=130)

    # ── All Accounts ──────────────────────────────────────────────────────────
    def _show_all_accounts(self):
        self._clear_content()
        self._highlight_nav(4)

        Label(self.content, text="All Accounts",
              font=("Georgia", 18, "bold"), bg=BG, fg=TEXT).place(x=0, y=0)

        with get_db() as db:
            cr = db.cursor()
            cr.execute(
                "SELECT cin, firstname, lastname, email, amount "
                "FROM accounts ORDER BY lastname"
            )
            rows = cr.fetchall()

        # Table header
        hdr = Frame(self.content, bg=CARD2,
                    highlightbackground=BORDER, highlightthickness=1)
        hdr.place(x=0, y=40, width=730, height=32)
        for lbl, xp, wp in [
            ("CIN", 10, 110), ("Name", 130, 160),
            ("Email", 300, 220), ("Balance (DH)", 530, 140)
        ]:
            Label(hdr, text=lbl, font=("Courier", 9, "bold"),
                  bg=CARD2, fg=MUTED, anchor=W).place(x=xp, y=6, width=wp)

        if not rows:
            Label(self.content, text="No accounts in database.",
                  font=FONT_SM, bg=BG, fg=MUTED).place(x=0, y=90)
            return

        for i, (cin, fn, ln, email, amt) in enumerate(rows[:11]):
            bg_row = CARD if i % 2 == 0 else CARD2
            row = Frame(self.content, bg=bg_row,
                        highlightbackground=BORDER, highlightthickness=1)
            row.place(x=0, y=74 + i * 44, width=730, height=38)
            Label(row, text=f"  {cin}", font=("Courier", 10),
                  bg=bg_row, fg=MUTED, anchor=W).place(x=0, y=8, width=120)
            Label(row, text=f"{fn} {ln}", font=("Courier", 10),
                  bg=bg_row, fg=TEXT, anchor=W).place(x=130, y=8, width=160)
            Label(row, text=(email or "—"), font=("Courier", 9),
                  bg=bg_row, fg=MUTED, anchor=W).place(x=300, y=10, width=220)
            Label(row, text=f"{float(amt):,.2f}", font=("Courier", 10, "bold"),
                  bg=bg_row, fg=GOLD, anchor=E).place(x=530, y=8, width=180)

    # ── Other Pages ───────────────────────────────────────────────────────────
    def signupdetail(self):
        self._highlight_nav(1)
        win = Toplevel(self.root)
        SingUpPage(win)

    def usermode(self):
        win = Toplevel(self.root)
        BankManagementSys(win)

    def _logout(self):
        self._console.destroy()
        self._build_admin_login()


if __name__ == "__main__":
    root = Tk()
    obj = BankManagementAdmin(root)
    root.mainloop()