import tkinter as tk
from tkinter import messagebox
from users import User
from votes import VotingSystem

class VotingAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Voting System")
        self.root.geometry("500x400")
        self.root.configure(bg="#f0f0f0")
        self.voting_system = VotingSystem()
        self.current_user = None

        # Custom Fonts
        self.title_font = ("Arial", 18, "bold")
        self.label_font = ("Arial", 12)
        self.button_font = ("Arial", 12, "bold")

        # Main Menu Frame
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(pady=20)

        # Title Label
        tk.Label(self.main_frame, text="Voting System", font=self.title_font, bg="#f0f0f0").pack(pady=10)

        # Buttons for Main Menu
        buttons = [
            ("Register", self.show_register),
            ("Login", self.show_login),
            ("Vote", self.show_vote),
            ("View Results", self.show_results),
            ("Exit", self.root.quit)
        ]

        for text, command in buttons:
            tk.Button(self.main_frame, text=text, command=command, font=self.button_font, bg="#4CAF50", fg="white", width=20).pack(pady=5)

    def clear_frame(self):
        """Clear all widgets from the current frame."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_register(self):
        """Display the registration form."""
        self.clear_frame()
        tk.Label(self.root, text="Register", font=self.title_font, bg="#f0f0f0").pack(pady=10)

        # Username
        tk.Label(self.root, text="Username:", font=self.label_font, bg="#f0f0f0").pack()
        self.register_username = tk.Entry(self.root, font=self.label_font)
        self.register_username.pack(pady=5)

        # Password
        tk.Label(self.root, text="Password:", font=self.label_font, bg="#f0f0f0").pack()
        self.register_password = tk.Entry(self.root, show="*", font=self.label_font)
        self.register_password.pack(pady=5)

        # Buttons
        tk.Button(self.root, text="Register", command=self.register_user, font=self.button_font, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_main_menu, font=self.button_font, bg="#f44336", fg="white").pack()

    def show_login(self):
        """Display the login form."""
        self.clear_frame()
        tk.Label(self.root, text="Login", font=self.title_font, bg="#f0f0f0").pack(pady=10)

        # Username
        tk.Label(self.root, text="Username:", font=self.label_font, bg="#f0f0f0").pack()
        self.login_username = tk.Entry(self.root, font=self.label_font)
        self.login_username.pack(pady=5)

        # Password
        tk.Label(self.root, text="Password:", font=self.label_font, bg="#f0f0f0").pack()
        self.login_password = tk.Entry(self.root, show="*", font=self.label_font)
        self.login_password.pack(pady=5)

        # Buttons
        tk.Button(self.root, text="Login", command=self.login_user, font=self.button_font, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_main_menu, font=self.button_font, bg="#f44336", fg="white").pack()

    def show_vote(self):
        """Display the voting form."""
        if not self.current_user:
            messagebox.showwarning("Login Required", "You need to login first.")
            return

        self.clear_frame()
        tk.Label(self.root, text="Vote", font=self.title_font, bg="#f0f0f0").pack(pady=10)

        # Party Selection
        tk.Label(self.root, text="Select a party:", font=self.label_font, bg="#f0f0f0").pack()
        self.party_var = tk.StringVar()
        parties = ["PTI", "MQM", "PMLN", "PPP", "JI"]

        for party in parties:
            tk.Radiobutton(self.root, text=party, variable=self.party_var, value=party, font=self.label_font, bg="#f0f0f0").pack()

        # Buttons
        tk.Button(self.root, text="Submit Vote", command=self.submit_vote, font=self.button_font, bg="#4CAF50", fg="white").pack(pady=10)
        tk.Button(self.root, text="Back", command=self.show_main_menu, font=self.button_font, bg="#f44336", fg="white").pack()

    def show_results(self):
        """Display the voting results."""
        self.clear_frame()
        tk.Label(self.root, text="Voting Results", font=self.title_font, bg="#f0f0f0").pack(pady=10)

        # Results Table
        results_frame = tk.Frame(self.root, bg="#f0f0f0")
        results_frame.pack()

        results = self.voting_system.get_results()
        for party, votes in results:
            tk.Label(results_frame, text=f"{party}: {votes} votes", font=self.label_font, bg="#f0f0f0").pack()

        # Back Button
        tk.Button(self.root, text="Back", command=self.show_main_menu, font=self.button_font, bg="#f44336", fg="white").pack(pady=10)

    def show_main_menu(self):
        """Return to the main menu."""
        self.clear_frame()
        self.__init__(self.root)

    def register_user(self):
        """Handle user registration."""
        username = self.register_username.get()
        password = self.register_password.get()

        if User.add_user(username, password):
            messagebox.showinfo("Success", "User registered successfully!")
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Registration failed. Username may already exist.")

    def login_user(self):
        """Handle user login."""
        username = self.login_username.get()
        password = self.login_password.get()

        self.current_user = User.authenticate_user(username, password)
        if self.current_user:
            messagebox.showinfo("Success", f"Welcome, {username}!")
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def submit_vote(self):
        """Handle voting submission."""
        party = self.party_var.get()
        if not party:
            messagebox.showwarning("Error", "Please select a party to vote.")
            return

        if self.voting_system.vote(self.current_user["id"], party):
            messagebox.showinfo("Success", "Vote cast successfully!")
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "You have already voted.")