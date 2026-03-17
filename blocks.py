from tkinter import *
from tkinter import ttk
import os

current_path = os.path.dirname(os.path.abspath(__file__))

# ── Shared design tokens ──────────────────────────────────────────────────────
BG       = "#0D1117"
CARD     = "#161B22"
BORDER   = "#30363D"
GOLD     = "#D4A843"
GOLD_LT  = "#F0C060"
RED      = "#F85149"
GREEN    = "#3FB950"
TEXT     = "#E6EDF3"
MUTED    = "#8B949E"
FONT_H   = ("Georgia", 14, "bold")
FONT_B   = ("Courier", 11)
FONT_SM  = ("Courier", 10)

def style_btn(btn, color=GOLD, text_color=BG):
    btn.configure(
        bg=color, fg=text_color, font=("Georgia", 12, "bold"),
        relief=FLAT, cursor="hand2", bd=0,
        activebackground=GOLD_LT, activeforeground=BG,
        padx=20, pady=10
    )

def make_card(parent, x, y, w, h):
    f = Frame(parent, bg=CARD, highlightbackground=BORDER,
              highlightthickness=1)
    f.place(x=x, y=y, width=w, height=h)
    return f

# ── Error Login ───────────────────────────────────────────────────────────────
class ErrorLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Authentication Failed")
        self.root.geometry("420x260+430+250")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        # Header strip
        hdr = Frame(self.root, bg=RED, height=5)
        hdr.pack(fill=X, side=TOP)

        card = make_card(self.root, 20, 20, 380, 220)

        # Icon area
        icon_lbl = Label(card, text="⚠", font=("Arial", 36),
                         bg=CARD, fg=RED)
        icon_lbl.place(x=0, y=20, width=380)

        Label(card, text="Authentication Failed",
              font=("Georgia", 16, "bold"), bg=CARD, fg=RED)\
            .place(x=0, y=80, width=380)

        Label(card,
              text="The account number or password\nyou entered is incorrect.",
              font=FONT_SM, bg=CARD, fg=MUTED, justify=CENTER)\
            .place(x=0, y=118, width=380)

        close_btn = Button(card, text="Try Again",
                           command=self.root.destroy)
        style_btn(close_btn, RED, TEXT)
        close_btn.place(x=130, y=168, width=120, height=36)


if __name__ == "__main__":
    root = Tk()
    obj = ErrorLogin(root)
    root.mainloop()