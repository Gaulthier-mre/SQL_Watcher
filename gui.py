# gui.py

from export_html import export_to_html
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv

DB_PATH = "alerts.db"

def get_alerts(ip_filter="", method_filter="", date_filter=""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    query = "SELECT ip, method, uri, date, timestamp FROM alerts WHERE 1=1"
    params = []

    if ip_filter:
        query += " AND ip LIKE ?"
        params.append(f"%{ip_filter}%")
    if method_filter:
        query += " AND method LIKE ?"
        params.append(f"%{method_filter}%")
    if date_filter:
        query += " AND date LIKE ?"
        params.append(f"%{date_filter}%")

    query += " ORDER BY timestamp DESC"
    cursor.execute(query, params)
    data = cursor.fetchall()
    conn.close()
    return data

def export_to_csv(data):
    if not data:
        messagebox.showwarning("Aucune alerte", "Aucune alerte à exporter.")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("Fichier CSV", "*.csv")],
        title="Enregistrer les alertes en CSV"
    )

    if not file_path:
        return

    try:
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["IP", "Méthode", "URI", "Date", "Détectée à"])
            writer.writerows(data)
        messagebox.showinfo("Export réussi", f"Les alertes ont été exportées vers\n{file_path}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'export : {e}")

def clear_alerts(tree):
    confirm = messagebox.askyesno("Confirmation", "Es-tu sûr de vouloir supprimer toutes les alertes ?")
    if confirm:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alerts")
        conn.commit()
        conn.close()
        update_tree(tree)
        messagebox.showinfo("Succès", "Toutes les alertes ont été supprimées.")

def update_tree(tree, ip="", method="", date=""):
    for item in tree.get_children():
        tree.delete(item)
    alerts = get_alerts(ip, method, date)
    for alert in alerts:
        tree.insert("", "end", values=alert)

def show_gui():
    root = tk.Tk()
    root.title("SQLWatcher - Alertes SQL")
    root.geometry("1000x520")
    root.configure(bg="#1e1e1e")

    # Zone de recherche multiple
    search_frame = tk.Frame(root, bg="#1e1e1e")
    search_frame.pack(fill="x", padx=10, pady=(10, 0))

    tk.Label(search_frame, text="IP :", fg="white", bg="#1e1e1e").grid(row=0, column=0, padx=5)
    ip_entry = tk.Entry(search_frame, width=20)
    ip_entry.grid(row=0, column=1)

    tk.Label(search_frame, text="Méthode :", fg="white", bg="#1e1e1e").grid(row=0, column=2, padx=5)
    method_entry = tk.Entry(search_frame, width=10)
    method_entry.grid(row=0, column=3)

    tk.Label(search_frame, text="Date (AAAA-MM-JJ) :", fg="white", bg="#1e1e1e").grid(row=0, column=4, padx=5)
    date_entry = tk.Entry(search_frame, width=15)
    date_entry.grid(row=0, column=5)

    def filter_results():
        update_tree(tree, ip_entry.get().strip(), method_entry.get().strip(), date_entry.get().strip())

    tk.Button(search_frame, text="Filtrer", command=filter_results, bg="#444", fg="white").grid(row=0, column=6, padx=10)

    # Tableau
    columns = ("IP", "Méthode", "URI", "Date", "Détectée à")
    tree = ttk.Treeview(root, columns=columns, show="headings")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b")
    style.configure("Treeview.Heading", background="#3c3c3c", foreground="red")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="w", width=180)

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Boutons
    button_frame = tk.Frame(root, bg="#1e1e1e")
    button_frame.pack(pady=(0, 10))

    tk.Button(
        button_frame,
        text="Exporter en CSV",
        command=lambda: export_to_csv(get_alerts(ip_entry.get().strip(), method_entry.get().strip(), date_entry.get().strip())),
        bg="#8b0000",
        fg="white",
        activebackground="#aa0000",
        font=("Helvetica", 11, "bold")
    ).pack(side="left", padx=10)

    tk.Button(
        button_frame,
        text="Exporter en HTML",
        command=lambda: export_to_html(get_alerts(ip_entry.get().strip(), method_entry.get().strip(), date_entry.get().strip())),
        bg="#005f73",
        fg="white",
        activebackground="#0a9396",
        font=("Helvetica", 11, "bold")
    ).pack(side="left", padx=10)

    tk.Button(
        button_frame,
        text="Vider les alertes",
        command=lambda: clear_alerts(tree),
        bg="#222222",
        fg="orange",
        activebackground="#aa3300",
        font=("Helvetica", 11, "bold")
    ).pack(side="left", padx=10)

    update_tree(tree)
    root.mainloop()

if __name__ == "__main__":
    show_gui()
