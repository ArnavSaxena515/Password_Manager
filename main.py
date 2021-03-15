import json
from tkinter import *
from tkinter import messagebox

import pyperclip

BACKGROUND = "#1a1a2e"
TEXT_BOX_BG = "#0f3460"
FONT_NAME = "Calibri"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project
import random


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]

    password_list = password_letters + password_numbers + password_symbols

    random.shuffle(password_list)

    password = "".join(password_list)

    global password_entry
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_info():
    global website_entry, password_entry, email_entry
    website = website_entry.get()
    password = password_entry.get()
    email = email_entry.get()

    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if website == "" or password == "" or email == "":
        messagebox.showinfo(title='Error', message="Please do not leave any fields empty")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            # is_ok = messagebox.askokcancel(title='Password Manager',
            #                                message=f"These are the details entered\nWebsite: {website}\nEmail: {email}\nPassword: {password}\nClick OK to save")


# ---------------------------- SEARCH ------------------------------- #
def search():
    global website_entry
    website = website_entry.get()

    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showwarning(title="Error", message="You have not saved any passwords yet!")
    else:
        try:
            query_ans = data[website]
        except KeyError:
            messagebox.showinfo(title="MyPass", message="Website not found")
        else:
            site_name = website
            site_password = data[website]["password"]
            site_email = data[website]["email"]
            messagebox.showinfo(title="MyPass", message=f"Website: {site_name}\nEmail: {site_email}\nPassword: {site_password}\nYour password has been copied to clipboard")
            pyperclip.copy(site_password)
    finally:
        website_entry.delete(0, END)
        password_entry.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("My Pass")
window.config(padx=50, pady=50, bg=BACKGROUND)

canvas = Canvas(width=200, height=200, bg=BACKGROUND, highlightthickness=0)

lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img, )
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website: ", bg=BACKGROUND, fg="white", font=(FONT_NAME, 12, "bold"))
website_label.config(padx=10, pady=10)
email_label = Label(text="Email/Username: ", bg=BACKGROUND, fg="white", font=(FONT_NAME, 12, "bold"))
email_label.config(padx=10, pady=10)
password_label = Label(text="Password: ", bg=BACKGROUND, fg="white", font=(FONT_NAME, 12, "bold"))
password_label.config(padx=10, pady=10)
website_label.grid(row=1, column=0)
website_label.grid(row=1, column=0)
email_label.grid(row=2, column=0)
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(borderwidth=5, width=35, bg=BACKGROUND, fg="white", font=(FONT_NAME, 10, "bold"),
                      insertbackground="white")
website_entry.focus
email_entry = Entry(borderwidth=5, width=35, bg=BACKGROUND, fg="white", font=(FONT_NAME, 10, "bold"),
                    insertbackground="white")
password_entry = Entry(borderwidth=5, width=35, bg=BACKGROUND, fg="white", font=(FONT_NAME, 10, "bold"),
                       insertbackground="white")
website_entry.grid(row=1, column=1, columnspan=2)
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "arnavsaxena221@gmail.com")
password_entry.grid(row=3, column=1, columnspan=2)

# Buttons
generate_password = Button(text="Create Password", highlightthickness=0, font=(FONT_NAME, 11, "bold"),
                           borderwidth=2, background="#d4483b", fg="white", activebackground="#d4483b",
                           activeforeground="white", width=15, command=generate_password)
generate_password.grid(row=3, column=3, columnspan=1)

add_button = Button(text="Add", highlightthickness=0, font=(FONT_NAME, 12, "bold"), background="#d4483b",
                    fg="white", activebackground="#d4483b", activeforeground="white", width=33, command=save_info)
add_button.grid(row=4, column=1, columnspan=2, padx=20, pady=20)

search_button = Button(text="Search", highlightthickness=0, font=(FONT_NAME, 11, "bold"), borderwidth=2,
                       background="#d4483b",
                       fg="white", activebackground="#d4483b", activeforeground="white", width=15, command=search)
search_button.grid(row=1, column=3)

window.mainloop()
