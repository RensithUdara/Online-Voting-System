import tkinter as tk
from tkinter import ttk, messagebox
from users import User
from votes import VotingSystem

class VotingAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Voting System")
        self.root.geometry("600x500")
        self.root.configure(bg="#2E3440")  # Dark background
        self.voting_system = VotingSystem()
        self.current_user = None

        # Custom Fonts
        self.title_font = ("Arial", 24, "bold")
        self.label_font = ("Arial", 14)
        self.button_font = ("Arial", 12, "bold")

        # Custom Colors
        self.bg_color = "#2E3440"  # Dark background
        self.fg_color = "#D8DEE9"  # Light text (for labels and buttons)
        self.button_bg = "#4C566A"  # Button background
        self.button_fg = "black"  # White button text (changed here)
        self.hover_bg = "#5E81AC"  # Button hover background
        self.success_color = "#A3BE8C"  # Success messages
        self.error_color = "#BF616A"  # Error messages
        self.entry_bg = "#3B4252"  # Entry widget background
        self.entry_fg = "#ECEFF4"  # Entry widget text color

        # Configure ttk styles
        self.style = ttk.Style()
        self.style.configure("TButton", font=self.button_font, background=self.button_bg, foreground=self.button_fg)
        self.style.map("TButton", background=[("active", self.hover_bg)])

        # Main Menu Frame
        self.main_frame = tk.Frame(self.root, bg=self.bg_color)
        self.main_frame.pack(pady=20)

        # Title Label
        tk.Label(self.main_frame, text="Voting System", font=self.title_font, bg=self.bg_color, fg=self.fg_color).pack(pady=20)

        # Buttons for Main Menu
        buttons = [
            ("Register", self.show_register),
            ("Login", self.show_login),
            ("Vote", self.show_vote),
            ("View Results", self.show_results),
            ("Exit", self.root.quit)
        ]

        for text, command in buttons:
            ttk.Button(self.main_frame, text=text, command=command, style="TButton").pack(pady=10, padx=20, fill=tk.X)

    def clear_frame(self):
        """Clear all widgets from the current frame."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_register(self):
        """Display the registration form."""
        self.clear_frame()
        tk.Label(self.root, text="Register", font=self.title_font, bg=self.bg_color, fg=self.fg_color).pack(pady=20)

        # Username
        tk.Label(self.root, text="Username:", font=self.label_font, bg=self.bg_color, fg=self.fg_color).pack()
        self.register_username = tk.Entry(self.root, font=self.label_font, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg)
        self.register_username.pack(pady=10)

        # Password
        tk.Label(self.root, text="Password:", font=self.label_font, bg=self.bg_color, fg=self.fg_color).pack()
        self.register_password = tk.Entry(self.root, show="*", font=self.label_font, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg)
        self.register_password.pack(pady=10)

        # Buttons
        ttk.Button(self.root, text="Register", command=self.register_user, style="TButton").pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.show_main_menu, style="TButton").pack()

    def show_login(self):
        """Display the login form."""
        self.clear_frame()
        tk.Label(self.root, text="Login", font=self.title_font, bg=self.bg_color, fg=self.fg_color).pack(pady=20)

        # Username
        tk.Label(self.root, text="Username:", font=self.label_font, bg=self.bg_color, fg=self.fg_color).pack()
        self.login_username = tk.Entry(self.root, font=self.label_font, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg)
        self.login_username.pack(pady=10)

        # Password
        tk.Label(self.root, text="Password:", font=self.label_font, bg=self.bg_color, fg=self.fg_color).pack()
        self.login_password = tk.Entry(self.root, show="*", font=self.label_font, bg=self.entry_bg, fg=self.entry_fg, insertbackground=self.entry_fg)
        self.login_password.pack(pady=10)

        # Buttons
        ttk.Button(self.root, text="Login", command=self.login_user, style="TButton").pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.show_main_menu, style="TButton").pack()

    def show_vote(self):
        """Display the voting form."""
        if not self.current_user:
            messagebox.showwarning("Login Required", "You need to login first.")
            return

        self.clear_frame()
        tk.Label(self.root, text="Vote", font=self.title_font, bg=self.bg_color, fg=self.fg_color).pack(pady=20)

        # Party Selection
        tk.Label(self.root, text="Select a party:", font=self.label_font, bg=self.bg_color, fg=self.fg_color).pack()
        self.party_var = tk.StringVar()
        parties = ["PTI", "MQM", "PMLN", "PPP", "JI"]

        for party in parties:
            tk.Radiobutton(
                self.root, text=party, variable=self.party_var, value=party,
                font=self.label_font, bg=self.bg_color, fg=self.fg_color, selectcolor=self.bg_color
            ).pack(pady=5)

        # Buttons
        ttk.Button(self.root, text="Submit Vote", command=self.submit_vote, style="TButton").pack(pady=10)
        ttk.Button(self.root, text="Back", command=self.show_main_menu, style="TButton").pack()

    def show_results(self):
        """Display the voting results."""
        self.clear_frame()
        tk.Label(self.root, text="Voting Results", font=self.title_font, bg=self.bg_color, fg=self.fg_color).pack(pady=20)

        # Results Table
        results_frame = tk.Frame(self.root, bg=self.bg_color)
        results_frame.pack()

        results = self.voting_system.get_results()
        for party, votes in results:
            tk.Label(
                results_frame, text=f"{party}: {votes} votes", font=self.label_font,
                bg=self.bg_color, fg=self.fg_color
            ).pack(pady=5)

        # Back Button
        ttk.Button(self.root, text="Back", command=self.show_main_menu, style="TButton").pack(pady=10)

    def show_main_menu(self):
        """Return to the main menu."""
        self.clear_frame()
        self.__init__(self.root)

    def register_user(self):
        """Handle user registration."""
        username = self.register_username.get()
        password = self.register_password.get()

        if User.add_user(username, password):
            messagebox.showinfo("Success", "User registered successfully!", icon="info")
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Registration failed. Username may already exist.", icon="error")

    def login_user(self):
        """Handle user login."""
        username = self.login_username.get()
        password = self.login_password.get()

        self.current_user = User.authenticate_user(username, password)
        if self.current_user:
            messagebox.showinfo("Success", f"Welcome, {username}!", icon="info")
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid username or password.", icon="error")

    def submit_vote(self):
        """Handle voting submission."""
        party = self.party_var.get()
        if not party:
            messagebox.showwarning("Error", "Please select a party to vote.", icon="warning")
            return

        if self.voting_system.vote(self.current_user["id"], party):
            messagebox.showinfo("Success", "Vote cast successfully!", icon="info")
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "You have already voted.", icon="error")