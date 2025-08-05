import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Function to insert new patient into the database
def add_patient():
    name = name_var.get()
    age = age_var.get()
    disease = disease_var.get()

    if name == "" or age == "" or disease == "":
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sushu2729#",
            database="hospital_db"
        )
        cursor = conn.cursor()
        query = "INSERT INTO patients (Name, Age, Disease) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, age, disease))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Patient added successfully.")
        fetch_data()
        name_var.set("")
        age_var.set("")
        disease_var.set("")
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# Function to fetch and display data
def fetch_data():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sushu2729#",
            database="hospital_db"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients")
        rows = cursor.fetchall()

        for row in tree.get_children():
            tree.delete(row)

        for row in rows:
            tree.insert("", tk.END, values=row)

        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to delete a patient
def delete_patient():
    selected_item = tree.focus()  # Get selected row
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a patient to delete.")
        return

    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this patient?")
    if not confirm:
        return

    try:
        patient_id = tree.item(selected_item)["values"][0]  # ID is the first column
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sushu2729#",
            database="hospital_db"
        )
        cursor = conn.cursor()
        cursor.execute("DELETE FROM patients WHERE ID = %s", (patient_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Deleted", "Patient record deleted.")
        fetch_data()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to load selected patient into entry fields
def load_selected_patient():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Select a patient", "Please select a patient to edit.")
        return

    values = tree.item(selected_item, "values")
    if values:
        name_entry.delete(0, tk.END)
        name_entry.insert(0, values[1])

        age_entry.delete(0, tk.END)
        age_entry.insert(0, values[2])

        disease_entry.delete(0, tk.END)
        disease_entry.insert(0, values[3])

# Function to update selected patient
def update_patient():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showwarning("Select a patient", "Please select a patient to update.")
        return

    values = tree.item(selected_item, "values")
    patient_id = values[0]
    name = name_entry.get()
    age = age_entry.get()
    disease = disease_entry.get()

    if name == "" or age == "" or disease == "":
        messagebox.showerror("Error", "All fields are required.")
        return

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="sushu2729#",
            database="hospital_db"
        )
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE patients SET Name=%s, Age=%s, Disease=%s WHERE ID=%s",
            (name, age, disease, patient_id)
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Patient record updated.")
        fetch_data()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("Hospital Management System")
root.geometry("600x550")

tk.Label(root, text="Patient Records", font=("Arial", 16)).pack(pady=10)

# Treeview
columns = ("ID", "Name", "Age", "Disease")
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(pady=10)

tk.Button(root, text="Load Data", command=fetch_data).pack(pady=5)

# --- Entry form for adding/updating patient ---
form_frame = tk.Frame(root)
form_frame.pack(pady=20)

name_var = tk.StringVar()
age_var = tk.StringVar()
disease_var = tk.StringVar()

tk.Label(form_frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(form_frame, textvariable=name_var)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Age").grid(row=1, column=0, padx=5, pady=5)
age_entry = tk.Entry(form_frame, textvariable=age_var)
age_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(form_frame, text="Disease").grid(row=2, column=0, padx=5, pady=5)
disease_entry = tk.Entry(form_frame, textvariable=disease_var)
disease_entry.grid(row=2, column=1, padx=5, pady=5)

# Buttons
tk.Button(root, text="Add Patient", command=add_patient).pack(pady=5)
tk.Button(root, text="Load Selected", command=load_selected_patient).pack(pady=5)
tk.Button(root, text="Update Patient", command=update_patient).pack(pady=5)
tk.Button(root, text="Delete Patient", command=delete_patient).pack(pady=5)

root.mainloop()


# Hospital Management System
# --------------------------
# Language: Python
# GUI: Tkinter
# Database: MySQL
#
# Features:
# - Add, View, Update, Delete patient records
# - Integrated with MySQL
#
# How to Run:
# 1. Make sure MySQL is installed and running.
# 2. Create database `hospital_db` with table `patients`.
# 3. Run the script using: python hospital_management.py
#
# Author: [Sushma Karlakunta]
