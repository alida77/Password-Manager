from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- Search Function ------------------------------- #
def search():
    with open("data.json") as data_file:
        try:
            data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showinfo(title="Error: No File", message="No data file found")
        else:
            website = website_entry.get()
            if website in data:
                email = data[website]["email"]
                password = data[website]["password"]
                messagebox.showinfo(title=website, message=f"Email: {email} \nPassword: {password}")
            else:
                messagebox.showinfo(title="No Result", message="No details found")


# --------------------------- PASSWORD GENERATOR ------------------------------ #
def pwd_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    letters_list = [random.choice(letters) for char in range(nr_letters)]
    symbols_list = [random.choice(symbols) for char in range(nr_symbols)]
    numbers_list = [random.choice(numbers) for char in range(nr_numbers)]
    password_list = letters_list + symbols_list + numbers_list

    random.shuffle(password_list)

    password = ""
    for char in password_list:
        password += char
    pwd_entry.delete(0, END)
    pwd_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = pwd_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) < 1 or len(email) < 1 or len(password) < 1:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered:\nEmail: {email}"
                                                              f"\nPassword: {password}"
                                                              f"\nIs it ok to save?")
        if is_ok:
            # with open("data.txt", mode="a") as data:
            #     data.write(f"{website} | {email} | {password}\n")
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                pwd_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
email_label = Label(text="Email/Username::")
email_label.grid(column=0, row=2)
pwd_label = Label(text="Password:")
pwd_label.grid(column=0, row=3)

website_entry = Entry(width=33)
website_entry.grid(column=1, row=1)
website_entry.focus()
email_entry = Entry(width=52)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "alih@gmail.com")
pwd_entry = Entry(width=33)
pwd_entry.grid(column=1, row=3)

generate_pwd_button = Button(text="Generate Password", width=15, command=pwd_generator)
generate_pwd_button.grid(column=2, row=3)
add_button = Button(text="Add", width=44, command=save)
add_button.grid(column=1, row=4, columnspan=2)
search_button = Button(text="Search", width=15, command=search)
search_button.grid(column=2, row=1)

window.mainloop()
