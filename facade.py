import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


class InsuranceApp:
    def __init__(self, root, role):
        self.root = root
        self.role = role
        self.root.title("Insurance CRM Pro")
        self.root.configure(bg="#f0f2f5")

        w, h = 1100, 700  # Немного увеличим окно для новых данных
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry(f"{w}x{h}+{int(sw / 2 - w / 2)}+{int(sh / 2 - h / 2)}")

        # --- ЛЕВАЯ ПАНЕЛЬ ---
        side_panel = tk.Frame(root, bg="#ffffff", width=280, bd=0, highlightthickness=1, highlightbackground="#dcdfe6")
        side_panel.pack(side="left", fill="y", padx=20, pady=20)
        side_panel.pack_propagate(False)

        tk.Label(side_panel, text="Карточка клиента", bg="#ffffff", font=("Segoe UI", 12, "bold")).pack(pady=10)

        def create_entry(label_text):
            tk.Label(side_panel, text=label_text, bg="#ffffff", fg="#606266", font=("Segoe UI", 8)).pack(anchor="w",
                                                                                                         padx=20)
            entry = tk.Entry(side_panel, font=("Segoe UI", 10), bd=0, bg="#f4f4f5", highlightthickness=1,
                             highlightbackground="#dcdfe6")
            entry.pack(fill="x", padx=20, pady=(2, 8), ipady=3)
            return entry

        self.entry_name = create_entry("ФИО")
        self.entry_policy = create_entry("№ Полис")
        self.entry_address = create_entry("Адрес")
        self.entry_phone = create_entry("Телефон")
        self.entry_email = create_entry("Email")
        self.entry_level = create_entry("Уровень (Diamond/Platinum/Gold/Silver)")
        self.entry_start = create_entry("Дата начала (ДД.ММ.ГГГГ)")
        self.entry_end = create_entry("Дата окончания")

        btn_style = {"font": ("Segoe UI", 9, "bold"), "bd": 0, "cursor": "hand2", "fg": "white"}
        tk.Button(side_panel, text="Добавить", command=self.add_item, bg="#67c23a", **btn_style).pack(fill="x", padx=20,
                                                                                                      pady=5, ipady=5)
        tk.Button(side_panel, text="Изменить", command=self.edit_item, bg="#e6a23c", **btn_style).pack(fill="x",
                                                                                                       padx=20, pady=5,
                                                                                                       ipady=5)
        tk.Button(side_panel, text="Удалить", command=self.delete_item, bg="#f56c6c", **btn_style).pack(fill="x",
                                                                                                        padx=20, pady=5,
                                                                                                        ipady=5)

        # --- ТАБЛИЦА ---
        main_frame = tk.Frame(root, bg="#f0f2f5")
        main_frame.pack(side="right", fill="both", expand=True, padx=(0, 20), pady=20)

        cols = ('ID', 'Имя', 'Полис', 'Адрес', 'Телефон', 'Email', 'Уровень', 'Начало', 'Конец')
        self.tree = ttk.Treeview(main_frame, columns=cols, show='headings')

        for col in cols:
            self.tree.heading(col, text=col)
            width = 40 if col == 'ID' else 100
            self.tree.column(col, width=width)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.refresh_table()

    def refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        conn = sqlite3.connect('insurance.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients")
        for row in cursor.fetchall():
            self.tree.insert('', 'end', values=row)
        conn.close()

    def get_inputs(self):
        return (self.entry_name.get(), self.entry_policy.get(), self.entry_address.get(),
                self.entry_phone.get(), self.entry_email.get(), self.entry_level.get(),
                self.entry_start.get(), self.entry_end.get())

    def add_item(self):
        if self.role != 'a': return messagebox.showwarning("Доступ", "Нет прав")
        conn = sqlite3.connect('insurance.db')
        conn.execute("""INSERT INTO clients (name, policy, address, phone, email, level, start_date, end_date) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", self.get_inputs())
        conn.commit()
        conn.close()
        self.refresh_table()
        self.clear_entries()
        return None

    def edit_item(self):
        if self.role != 'a': return messagebox.showwarning("Доступ", "Нет прав")
        sel = self.tree.focus()
        if not sel: return None
        item_id = self.tree.item(sel)['values'][0]
        conn = sqlite3.connect('insurance.db')
        conn.execute("""UPDATE clients SET name=?, policy=?, address=?, phone=?, email=?, level=?, start_date=?, end_date=? 
                        WHERE id=?""", (*self.get_inputs(), item_id))
        conn.commit()
        conn.close()
        self.refresh_table()
        return None

    def delete_item(self):
        if self.role != 'a': return messagebox.showwarning("Доступ", "Нет прав")
        sel = self.tree.focus()
        if not sel: return None
        if messagebox.askyesno("Confirm", "Удалить?"):
            item_id = self.tree.item(sel)['values'][0]
            conn = sqlite3.connect('insurance.db')
            conn.execute("DELETE FROM clients WHERE id=?", (item_id,))
            conn.commit()
            conn.close()
            self.refresh_table()
            self.clear_entries()
        return None

    def on_select(self, _):
        sel = self.tree.focus()
        if sel:
            v = self.tree.item(sel)['values']
            self.clear_entries()
            entries = [self.entry_name, self.entry_policy, self.entry_address, self.entry_phone,
                       self.entry_email, self.entry_level, self.entry_start, self.entry_end]
            for i, entry in enumerate(entries):
                entry.insert(0, v[i + 1])

    def clear_entries(self):
        for e in [self.entry_name, self.entry_policy, self.entry_address, self.entry_phone,
                  self.entry_email, self.entry_level, self.entry_start, self.entry_end]:
            e.delete(0, tk.END)
