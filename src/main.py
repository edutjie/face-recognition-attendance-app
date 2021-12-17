import tkinter as tk
import tkinter.messagebox as tkmsg
from tkinter.font import Font
from tkinter import ttk
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3, string, os, face, train
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(os.path.dirname(BASE_DIR), "images")

# connect sqlite database
con = sqlite3.connect(os.path.join(os.path.dirname(BASE_DIR), "face.db"))


class Login(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.title("Log in")
        self.font_settings = Font(family="Helvetica", size=12, weight="bold")
        self.create_widget()

    def create_widget(self):
        self.label = tk.Label(self, text="LOG IN", font=self.font_settings).grid(
            row=0, column=0, columnspan=2, padx=10, pady=5
        )

        # fields
        self.label = tk.Label(self, text="Username  :", font=self.font_settings).grid(
            row=1, column=0, padx=10, pady=5
        )
        self.label = tk.Label(self, text="Password  :", font=self.font_settings).grid(
            row=2, column=0, padx=10, pady=5
        )

        # entry
        self.username = tk.StringVar()
        self.ent_username = tk.Entry(self, textvariable=self.username, width=20)
        self.ent_username.grid(row=1, column=1, padx=10, pady=5)
        self.password = tk.StringVar()
        self.ent_password = tk.Entry(
            self, textvariable=self.password, width=20, show="*"
        )
        self.ent_password.grid(row=2, column=1, padx=10, pady=5)

        # cancel button
        self.cancel_btn = tk.Button(
            self, text="Cancel", font=self.font_settings, command=self.destroy, fg="red"
        ).grid(row=3, column=0, padx=10, pady=5)

        # log in button
        self.login_btn = tk.Button(
            self,
            text="Log In",
            font=self.font_settings,
            command=self.validate_user,
            fg="green",
        ).grid(row=3, column=1, padx=10, pady=5)

    def validate_user(self):
        username = self.username.get()
        password = self.password.get()
        cur = con.cursor()
        user_password = [
            hash_pass[0]
            for hash_pass in cur.execute(
                "SELECT hash FROM users WHERE username = ?", [username]
            )
        ]
        # validation
        if not (username and password):
            is_retry = tkmsg.askretrycancel(
                title="EmptyInput",
                message="You must provide your username, password!",
            )
            if not is_retry:
                self.destroy()
        elif not user_password:
            # check if username exists
            is_retry = tkmsg.askretrycancel(
                title="WrongUsername",
                message="You must provide the correct username!",
            )
            if not is_retry:
                self.destroy()
        elif not check_password_hash(user_password[0], password):
            is_retry = tkmsg.askretrycancel(
                title="WrongPassword",
                message="You must provide the correct password!",
            )
            if not is_retry:
                self.destroy()
        else:
            dirs = [
                os.path.basename(root).replace(" ", "-").lower()
                for root, dirs, files in os.walk(image_dir)
                if files
            ]
            if username not in dirs:
                tkmsg.showwarning(
                    title="TakingPicture",
                    message="We don't face your face in our database so we will take your picture shortly, so please stay in front of your camera until the process is complete!",
                )
                # have to register the face again if user's image dir doesn't exists
                Signup.register_face(self, username)
            tkmsg.showwarning(
                title="TakingPicture",
                message="We will scan your face shortly, so please stay in front of your camera until the process is complete!",
            )
            self.scan_face(username)

    def scan_face(self, username):
        is_success = face.scan_face(username)
        if is_success:
            tkmsg.showinfo(
                title="LoginSuccess",
                message="You have logged in!",
            )
            self.destroy()

            # redirect to logged in session
            App.create_logged_widget(self.master, username)

        else:
            tkmsg.showerror(
                title="LogInFailed",
                message="We cannot indentify your face!",
            )


class Signup(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.font_settings = Font(family="Helvetica", size=12, weight="bold")
        self.create_widget()

    def create_widget(self):
        self.label = tk.Label(self, text="SIGN UP", font=self.font_settings).grid(
            row=0, column=0, columnspan=2, padx=10, pady=5
        )

        # fields
        self.label = tk.Label(
            self, text="Username                  :", font=self.font_settings
        ).grid(row=1, column=0, padx=10, pady=5)
        self.label = tk.Label(
            self, text="Password                  :", font=self.font_settings
        ).grid(row=2, column=0, padx=10, pady=5)
        self.label = tk.Label(
            self, text="Confirm Password  :", font=self.font_settings
        ).grid(row=3, column=0, padx=10, pady=5)

        # entry
        self.username = tk.StringVar()
        self.ent_username = tk.Entry(self, textvariable=self.username, width=20)
        self.ent_username.grid(row=1, column=1, padx=10, pady=5)
        self.password = tk.StringVar()
        self.ent_password = tk.Entry(
            self, textvariable=self.password, width=20, show="*"
        )
        self.ent_password.grid(row=2, column=1, padx=10, pady=5)
        self.confirm = tk.StringVar()
        self.ent_confirm = tk.Entry(self, textvariable=self.confirm, width=20, show="*")
        self.ent_confirm.grid(row=3, column=1, padx=10, pady=5)

        # cancel button
        self.cancel_btn = tk.Button(
            self, text="Cancel", font=self.font_settings, command=self.destroy, fg="red"
        ).grid(row=4, column=0, padx=10, pady=5)

        # log in button
        self.login_btn = tk.Button(
            self,
            text="Sign Up",
            font=self.font_settings,
            command=self.validate_input,
            fg="green",
        ).grid(row=4, column=1, padx=10, pady=5)

    def validate_input(self):
        allowed_username = set(
            "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-"
        )
        username = self.username.get()
        password = self.password.get()
        confirm = self.confirm.get()

        # get rows to check if username already exists
        cur = con.cursor()
        rows = [
            row
            for row in cur.execute("SELECT * FROM users WHERE username = ?", [username])
        ]

        # validation
        if not (username and password and confirm):
            is_retry = tkmsg.askretrycancel(
                title="EmptyInput",
                message="You must provide your username, password and confirmation password!",
            )
            if not is_retry:
                self.destroy()
        elif len(rows) > 0:
            is_retry = tkmsg.askretrycancel(
                title="UsernameAlreadyExists",
                message="Username already exists!",
            )
            if not is_retry:
                self.destroy()
        elif not set(username).issubset(allowed_username):
            is_retry = tkmsg.askretrycancel(
                title="InvalidUsername", message="Your username is invalid!"
            )
            if not is_retry:
                self.destroy()
        elif not (
            set(password) & set(string.ascii_lowercase)
            and set(password) & set(string.ascii_uppercase)
            and set(password) & set(string.digits)
        ):
            is_retry = tkmsg.askretrycancel(
                title="InvalidPassword",
                message="Your password must contain atleast 1 uppercase, 1 lowercase and 1 number!",
            )
            if not is_retry:
                self.destroy()
        elif confirm != password:
            is_retry = tkmsg.askretrycancel(
                title="PasswordDoesNotMatch",
                message="Your confirmation password doesn't match!",
            )
            if not is_retry:
                self.destroy()
        else:
            # if input passed the validation
            # encode password to hash
            hash = generate_password_hash(password)

            # store username and hash to the database
            self.store_db(username, hash)

            # warning
            tkmsg.showwarning(
                title="TakingPicture",
                message="We will take your picture shortly, so please stay in front of your camera until the process is complete!",
            )

            # register user's face to be trained
            self.register_face(username)

            # show info that the sign up is successful
            tkmsg.showinfo(
                title="SignUpSuccessful",
                message="You have successfully registered your account.",
            )

            # close the window
            self.destroy()

    def store_db(self, username, hash):
        cur = con.cursor()
        # insert to the database
        cur.execute("INSERT INTO users (username, hash) VALUES(?, ?)", (username, hash))
        con.commit()

    def register_face(self, username):
        cur = con.cursor()
        user_id = [
            id[0]
            for id in cur.execute("SELECT id FROM users WHERE username = ?", [username])
        ][0]
        # take 200 pictures of the user
        face.take_pictures(username)
        # train model
        train.train_face()


class AttendanceList(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.font_settings = Font(family="Helvetica", size=12, weight="bold")
        self.create_widget()

    def create_widget(self):
        self.label = tk.Label(
            self, text="ATTENDANCE LIST", font=self.font_settings
        ).pack(padx=10, pady=5)

        # scrollbar
        scroll = tk.Scrollbar(self)
        scroll.pack(side="right", fill="y")

        table = ttk.Treeview(
            self,
            column=("no_col", "username_col", "dt_col"),
            show="headings",
            yscrollcommand=scroll.set,
        )

        scroll.config(command=table.yview)

        cur = con.cursor()
        cur.execute("SELECT username, datetime FROM attendance")
        rows = cur.fetchall()

        for index, row in enumerate(rows):
            row = (index + 1, *row)
            table.insert("", tk.END, values=row)

        table.column("#1", anchor=tk.CENTER)
        table.heading("#1", text="No")
        table.column("#2", anchor=tk.CENTER)
        table.heading("#2", text="Username")
        table.column("#3", anchor=tk.CENTER)
        table.heading("#3", text="Date and Time")

        table.pack()


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.font_settings = Font(family="Helvetica", size=12, weight="bold")
        self.setup_db()
        self.create_log_widget()

    def create_log_widget(self):
        self.label = tk.Label(text="FACE RECOGNITION APP", font=self.font_settings)
        self.label.pack(padx=10, pady=5)
        self.login_btn = tk.Button(
            text="Log in", font=self.font_settings, command=self.login
        )
        self.login_btn.pack(padx=10, pady=5)
        self.signup_btn = tk.Button(
            text="Sign up", font=self.font_settings, command=self.signup
        )
        self.signup_btn.pack(padx=10, pady=5)

    def create_logged_widget(self, username):
        self.clear_log_widget()
        self.username = username
        self.attendance_status_btn = tk.Label(
            text=f"Your logged in as {self.username}", font=self.font_settings
        )
        self.attendance_status_btn.pack(padx=10, pady=5)
        self.submit_attendance_btn = tk.Button(
            text="Submit Attendance",
            font=self.font_settings,
            command=self.store_attendance,
        )
        self.submit_attendance_btn.pack(padx=10, pady=5)
        self.attendance_list_btn = tk.Button(
            text="Attendance List",
            font=self.font_settings,
            command=self.attendance_list,
        )
        self.attendance_list_btn.pack(padx=10, pady=5)
        self.logout_btn = tk.Button(
            text="Log Out", font=self.font_settings, command=self.logout
        )
        self.logout_btn.pack(padx=10, pady=5)

    def setup_db(self):
        cur = con.cursor()
        # create sql table
        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS users
                    (
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL,
                        hash TEXT NOT NULL
                    )
            """
        )
        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS attendance
                    (
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL,
                        datetime TEXT NOT NULL
                    )
            """
        )
        con.commit()

    def login(self):
        Login(self)

    def signup(self):
        Signup(self)

    def logout(self):
        self.clear_logged_widget()
        self.username = ""
        self.label.pack()
        self.login_btn.pack()
        self.signup_btn.pack()

    def store_attendance(self):
        cur = con.cursor()
        # insert to the database
        cur.execute(
            "INSERT INTO attendance (username, datetime) VALUES(?, ?)",
            (self.username, datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
        )
        con.commit()

        tkmsg.showinfo(
            title="SumbitAttendanceSuccess",
            message="You're attendance has been recorded!",
        )

    def attendance_list(self):
        AttendanceList()

    def clear_log_widget(self):
        self.label.forget()
        self.login_btn.forget()
        self.signup_btn.forget()

    def clear_logged_widget(self):
        self.attendance_status_btn.destroy()
        self.submit_attendance_btn.destroy()
        self.attendance_list_btn.destroy()
        self.logout_btn.destroy()


if __name__ == "__main__":
    app = App()
    app.master.title("FACE RECOGNITION ATTENDANCE APP")
    app.master.geometry("250x175")
    app.master.mainloop()
    con.close()
