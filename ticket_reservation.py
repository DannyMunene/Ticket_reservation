import tkinter as tk
from tkinter import messagebox

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password 
        self.booked_tickets = []

class Event:
    def __init__(self, event_id, name, seats):
        self.event_id = event_id
        self.name = name 
        self.available_seats = seats 

class Ticket:
    def __init__(self, event, seat_number, user):
        self.event = event 
        self.seat_number = seat_number
        self.user = user 

class ReservationSystem:
    def __init__(self, root):
        self.root = root 
        self.users = {}
        self.events = []
        self.current_user = None 
        self._load_sample_events()
        self.build_login_ui()

    def _load_sample_events(self):
        self.events = [
            Event(1, "Movie: Interstellar", 5),
            Event(2, "Concert: Coldplay", 3),
            Event(3, "Play: Hamlet", 4)
        ]

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def build_login_ui(self):
        self.clear_window()
        self.root.title("Tickets Reservation System")

        tk.Label(self.root, text="Login or Register", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        def login():
            username = username_entry.get() 
            password = password_entry.get()
            user = self.users.get(username)
            if user and user.password == password:
                self.current_user = user
                self.build_main_ui()
            else:
                messagebox.showerror("Error", "Invalid credentials")
        def register():
            username = username_entry.get()
            password = password_entry.get()
            if username in self.users:
                messagebox.showerror("Error", "Username already exists")
            else:
                self.users[username] = User(username, password)
                messagebox.showinfo("Success", "Registration successful")


        tk.Button(self.root, text="Login", command=login).pack(pady=5)
        tk.Button(self.root, text="Register", command=register).pack()

    def build_main_ui(self):
        self.clear_window()

        tk.Label(self.root, text=f"welcome {self.current_user.username}", font=("Arial", 14)).pack(pady=10)
        tk.Button(self.root, text="View events", command=self.build_event_ui).pack(pady=5)
        tk.Button(self.root, text="View my Tickets", command=self.build_my_tickets_ui).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.build_login_ui).pack(pady=5)

    def build_event_ui(self):
        self.clear_window()
        tk.Label(self.root, text="Available Events", font=("Arial", 14)).pack(pady=10)
        for event in self.events:
            frame = tk.Frame(self.root)
            frame.pack(pady=5)
            tk.Label(frame, text=f"{event.name} - Seats Left: {event.available_seats}").pack(side=tk.LEFT)

            def make_booking_func(e=event):
                return lambda: self.book_ticket(e)
            tk.Button(frame, text="Book", command=make_booking_func()).pack(side=tk.RIGHT)

        tk.Button(self.root, text="Back", command=self.build_main_ui).pack(pady=10)

    def build_my_tickets_ui(self):
        self.clear_window()
        tk.Label(self.root, text="My Tickets", font=("Arial", 14)).pack(pady=10)

        if not self.current_user.booked_tickets:
            tk.Label(self.root, text="No tickets booked yet").pack()
        else:
            for ticket in self.current_user.booked_tickets:
                frame = tk.Frame(self.root)
                frame.pack(pady=5)
                tk.Label(frame, text=f"{ticket.event.name} - Seat {ticket.seat_number}").pack(side=tk.LEFT)

                def make_cancel_func(t=ticket):
                    return lambda: self.cancel_ticket(t)
                
                tk.Button(frame, text="Cancel", command=make_cancel_func()).pack(side=tk.RIGHT)

                tk.Button(self.root, text="Back", command=self.build_main_ui).pack(pady=10)

    def book_ticket(self, event):
        if event.available_seats <= 0:
            messagebox.showerror("Error", "No seats available")
            return 
        seat_number = event.available_seats
        ticket = Ticket(event, seat_number, self.current_user)
        self.current_user.booked_tickets.append(ticket)
        event.available_seats -= 1
        messagebox.showinfo("Success", f"ticket booked! Seatnumber: {seat_number}")
        self.build_event_ui()

    def cancel_ticket(self, ticket):
        self.current_user.booked_tickets.remove(ticket)
        ticket.event.available_seats += 1 
        messagebox.showinfo("Success", "Ticket Canceled.")
        self.build_my_tickets_ui()

if __name__=="__main__":
    root = tk.Tk()
    root.geometry("400x400")
    app = ReservationSystem(root)
    root.mainloop()