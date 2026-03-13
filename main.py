import tkinter as tk
from tkinter import messagebox
from auth import init_db, check_login
from facade import InsuranceApp


def start_app(login_win, entry_user, entry_pass):
    username = entry_user.get().strip()
    password = entry_pass.get().strip()

    if not username or not password:
        messagebox.showwarning("Внимание", "Введите логин и пароль")
        return

    role_data = check_login(username, password)
    if role_data:
        login_win.destroy()
        root = tk.Tk()
        InsuranceApp(root, role_data)
        root.mainloop()
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль")


if __name__ == "__main__":
    init_db()

    # Настройка главного окна логина
    login_win = tk.Tk()
    login_win.title("Авторизация")
    login_win.configure(bg="#f0f2f5")

    # Размеры и центрирование
    window_width = 350
    window_height = 400
    screen_width = login_win.winfo_screenwidth()
    screen_height = login_win.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    login_win.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    login_win.resizable(False, False)

    # Стилизация контейнера
    main_frame = tk.Frame(login_win, bg="#ffffff", bd=0, highlightthickness=1, highlightbackground="#dcdfe6")
    main_frame.place(relx=0.5, rely=0.5, anchor="center", width=300, height=320)

    # Заголовок
    tk.Label(main_frame, text="Вход в систему", bg="#ffffff", fg="#303133",
             font=("Segoe UI", 16, "bold")).pack(pady=(30, 20))

    # Поле Логин
    tk.Label(main_frame, text="Имя пользователя", bg="#ffffff", fg="#606266", font=("Segoe UI", 9)).pack(anchor="w",
                                                                                                         padx=30)
    entry_user = tk.Entry(main_frame, font=("Segoe UI", 11), bd=0, bg="#f4f4f5", highlightthickness=1,
                          highlightbackground="#dcdfe6")
    entry_user.pack(fill="x", padx=30, pady=(5, 15), ipady=5)
    entry_user.insert(0, "admin")

    # Поле Пароль
    tk.Label(main_frame, text="Пароль", bg="#ffffff", fg="#606266", font=("Segoe UI", 9)).pack(anchor="w", padx=30)
    entry_pass = tk.Entry(main_frame, font=("Segoe UI", 11), show="*", bd=0, bg="#f4f4f5", highlightthickness=1,
                          highlightbackground="#dcdfe6")
    entry_pass.pack(fill="x", padx=30, pady=(5, 25), ipady=5)

    # Кнопка
    btn_login = tk.Button(main_frame, text="Войти", command=lambda: start_app(login_win, entry_user, entry_pass),
                          bg="#409eff", fg="white", font=("Segoe UI", 10, "bold"), bd=0, cursor="hand2")
    btn_login.pack(fill="x", padx=30, ipady=8)


    # Эффект наведения
    def on_enter(e): btn_login['bg'] = '#66b1ff'


    def on_leave(e): btn_login['bg'] = '#409eff'


    btn_login.bind("<Enter>", on_enter)
    btn_login.bind("<Leave>", on_leave)

    login_win.mainloop()
