from gui import VotingAppGUI
import tkinter as tk
from database import initialize_database

if __name__ == "__main__":
    # Initialize the database
    initialize_database()

    # Start the GUI
    root = tk.Tk()
    app = VotingAppGUI(root)
    root.mainloop()