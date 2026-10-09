import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
import unittest
import tempfile
import sys


DB_NAME = 'flowershop.db'






def get_connection():
    return sqlite3.connect(DB_NAME)




def init_db():
    conn = get_connection()
    cur = conn.cursor()


    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            total REAL NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)


    cur.execute("SELECT COUNT(*) FROM products")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO products (name, category, price, quantity) VALUES (?, ?, ?, ?)",
            [
                ('Роза красная', 'Цветы', 250.0, 100),
                ('Тюльпан жёлтый', 'Цветы', 150.0, 80),
                ('Букет «Весенний»', 'Букеты', 1500.0, 20),
                ('Композиция «Нежность»', 'Композиции', 2200.0, 15),
            ],
        )
        cur.executemany(
            "INSERT INTO customers (full_name, phone) VALUES (?, ?)",
            [
                ('Иванова Анна', '+7-900-111-22-33'),
                ('Петров Сергей', '+7-900-444-55-66'),
            ],
        )


    conn.commit()
    conn.close()






def add_product(name, category, price, quantity):
    conn = get_connection()
    conn.execute(
        "INSERT INTO products (name, category, price, quantity) VALUES (?, ?, ?, ?)",
        (name, category, price, quantity),
    )
    conn.commit()
    conn.close()




def get_products(search=None):
    conn = get_connection()
    cur = conn.cursor()
    if search:
        cur.execute(
            "SELECT id, name, category, price, quantity FROM products "
            "WHERE name LIKE ? ORDER BY name",
            (f'%{search}%',),
        )
    else:
        cur.execute("SELECT id, name, category, price, quantity FROM products ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return rows






def add_customer(full_name, phone):
    conn = get_connection()
    conn.execute("INSERT INTO customers (full_name, phone) VALUES (?, ?)", (full_name, phone))
    conn.commit()
    conn.close()




def get_customers():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, full_name, phone FROM customers ORDER BY full_name")
    rows = cur.fetchall()
    conn.close()
    return rows






def add_order(customer_id, product_id, quantity, total):
    conn = get_connection()
    conn.execute(
        "INSERT INTO orders (customer_id, product_id, quantity, total) VALUES (?, ?, ?, ?)",
        (customer_id, product_id, quantity, total),
    )
    conn.commit()
    conn.close()




def get_orders():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT o.id, c.full_name, p.name, o.quantity, o.total, o.created_at
        FROM orders o
        JOIN customers c ON c.id = o.customer_id
        JOIN products p ON p.id = o.product_id
        ORDER BY o.id DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows






class FlowerShopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FlowerShop — Цветочный магазин")
        self.root.geometry("950x600")


        notebook = ttk.Notebook(root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)


        self.tab_products = tk.Frame(notebook)
        self.tab_customers = tk.Frame(notebook)
        self.tab_orders = tk.Frame(notebook)
        self.tab_search = tk.Frame(notebook)


        notebook.add(self.tab_products, text='Товары')
        notebook.add(self.tab_customers, text='Покупатели')
        notebook.add(self.tab_orders, text='Заказы')
        notebook.add(self.tab_search, text='Поиск')


        self.build_products()
        self.build_customers()
        self.build_orders()
        self.build_search()


 
    def build_products(self):
        form = tk.LabelFrame(self.tab_products, text="Добавить товар")
        form.pack(fill=tk.X, padx=8, pady=8)


        tk.Label(form, text="Название:").grid(row=0, column=0, padx=4, pady=4, sticky='w')
        self.p_name = tk.Entry(form, width=25)
        self.p_name.grid(row=0, column=1, padx=4, pady=4)


        tk.Label(form, text="Категория:").grid(row=0, column=2, padx=4, pady=4, sticky='w')
        self.p_category = ttk.Combobox(form, values=["Цветы", "Букеты", "Композиции", "Аксессуары"], width=18)
        self.p_category.grid(row=0, column=3, padx=4, pady=4)
        self.p_category.set("Цветы")


        tk.Label(form, text="Цена:").grid(row=1, column=0, padx=4, pady=4, sticky='w')
        self.p_price = tk.Entry(form, width=25)
        self.p_price.grid(row=1, column=1, padx=4, pady=4)


        tk.Label(form, text="Количество:").grid(row=1, column=2, padx=4, pady=4, sticky='w')
        self.p_qty = tk.Entry(form, width=18)
        self.p_qty.grid(row=1, column=3, padx=4, pady=4)


        tk.Button(form, text="Добавить", command=self.add_product_click).grid(
            row=2, column=0, columnspan=4, pady=6
        )


        cols = ('ID', 'Название', 'Категория', 'Цена', 'Остаток')
        self.tree_products = ttk.Treeview(self.tab_products, columns=cols, show='headings')
        for c in cols:
            self.tree_products.heading(c, text=c)
            self.tree_products.column(c, width=150, anchor='center')
        self.tree_products.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)


        self.refresh_products()


    def add_product_click(self):
        try:
            name = self.p_name.get().strip()
            if not name:
                raise ValueError("Введите название")
            price = float(self.p_price.get())
            qty = int(self.p_qty.get())
            if price <= 0 or qty < 0:
                raise ValueError("Цена > 0, количество ≥ 0")
            add_product(name, self.p_category.get(), price, qty)
            self.p_name.delete(0, tk.END)
            self.p_price.delete(0, tk.END)
            self.p_qty.delete(0, tk.END)
            self.refresh_products()
            messagebox.showinfo("Готово", "Товар добавлен")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except sqlite3.IntegrityError:
            messagebox.showerror("Ошибка", "Такой товар уже есть")


    def refresh_products(self):
        for row in self.tree_products.get_children():
            self.tree_products.delete(row)
        for row in get_products():
            self.tree_products.insert('', 'end', values=row)


   
    def build_customers(self):
        form = tk.LabelFrame(self.tab_customers, text="Добавить покупателя")
        form.pack(fill=tk.X, padx=8, pady=8)


        tk.Label(form, text="ФИО:").grid(row=0, column=0, padx=4, pady=4, sticky='w')
        self.c_name = tk.Entry(form, width=30)
        self.c_name.grid(row=0, column=1, padx=4, pady=4)


        tk.Label(form, text="Телефон:").grid(row=0, column=2, padx=4, pady=4, sticky='w')
        self.c_phone = tk.Entry(form, width=20)
        self.c_phone.grid(row=0, column=3, padx=4, pady=4)


        tk.Button(form, text="Добавить", command=self.add_customer_click).grid(
            row=1, column=0, columnspan=4, pady=6
        )


        cols = ('ID', 'ФИО', 'Телефон')
        self.tree_customers = ttk.Treeview(self.tab_customers, columns=cols, show='headings')
        for c in cols:
            self.tree_customers.heading(c, text=c)
            self.tree_customers.column(c, width=200, anchor='center')
        self.tree_customers.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)


        self.refresh_customers()


    def add_customer_click(self):
        try:
            name = self.c_name.get().strip()
            phone = self.c_phone.get().strip()
            if not name or not phone:
                raise ValueError("Заполните ФИО и телефон")
            add_customer(name, phone)
            self.c_name.delete(0, tk.END)
            self.c_phone.delete(0, tk.END)
            self.refresh_customers()
            messagebox.showinfo("Готово", "Покупатель добавлен")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except sqlite3.IntegrityError:
            messagebox.showerror("Ошибка", "Такой телефон уже есть")


    def refresh_customers(self):
        for row in self.tree_customers.get_children():
            self.tree_customers.delete(row)
        for row in get_customers():
            self.tree_customers.insert('', 'end', values=row)


   
    def build_orders(self):
        form = tk.LabelFrame(self.tab_orders, text="Оформить заказ")
        form.pack(fill=tk.X, padx=8, pady=8)


        tk.Label(form, text="Покупатель:").grid(row=0, column=0, padx=4, pady=4, sticky='w')
        self.o_customer = ttk.Combobox(form, width=30, state='readonly')
        self.o_customer.grid(row=0, column=1, padx=4, pady=4)


        tk.Label(form, text="Товар:").grid(row=0, column=2, padx=4, pady=4, sticky='w')
        self.o_product = ttk.Combobox(form, width=30, state='readonly')
        self.o_product.grid(row=0, column=3, padx=4, pady=4)


        tk.Label(form, text="Количество:").grid(row=1, column=0, padx=4, pady=4, sticky='w')
        self.o_qty = tk.Entry(form, width=10)
        self.o_qty.grid(row=1, column=1, padx=4, pady=4, sticky='w')


        tk.Button(form, text="Оформить", command=self.add_order_click).grid(
            row=2, column=0, columnspan=2, pady=6
        )
        tk.Button(form, text="Обновить списки", command=self.load_order_lists).grid(
            row=2, column=3, padx=4, pady=6, sticky='e'
        )


        cols = ('ID', 'Покупатель', 'Товар', 'Кол-во', 'Сумма', 'Дата')
        self.tree_orders = ttk.Treeview(self.tab_orders, columns=cols, show='headings')
        for c in cols:
            self.tree_orders.heading(c, text=c)
            self.tree_orders.column(c, width=130, anchor='center')
        self.tree_orders.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)


        self.load_order_lists()
        self.refresh_orders()


    def load_order_lists(self):
        self.customers_data = get_customers()
        self.products_data = get_products()
        self.o_customer['values'] = [f"{c[0]} — {c[1]}" for c in self.customers_data]
        self.o_product['values'] = [
            f"{p[0]} — {p[1]} ({p[3]} руб., ост. {p[4]})" for p in self.products_data
        ]


    def add_order_click(self):
        try:
            if not self.o_customer.get() or not self.o_product.get():
                raise ValueError("Выберите покупателя и товар")
            customer_id = int(self.o_customer.get().split(' — ')[0])
            product_id = int(self.o_product.get().split(' — ')[0])
            qty = int(self.o_qty.get())
            if qty <= 0:
                raise ValueError("Количество > 0")


            product = next(p for p in self.products_data if p[0] == product_id)
            total = qty * product[3]


            add_order(customer_id, product_id, qty, total)
            self.o_qty.delete(0, tk.END)
            self.refresh_orders()
            messagebox.showinfo("Готово", f"Заказ оформлен. Сумма: {total:.2f} руб.")
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))


    def refresh_orders(self):
        for row in self.tree_orders.get_children():
            self.tree_orders.delete(row)
        for row in get_orders():
            self.tree_orders.insert('', 'end', values=row)


   
    def build_search(self):
        form = tk.LabelFrame(self.tab_search, text="Поиск товара по названию")
        form.pack(fill=tk.X, padx=8, pady=8)


        tk.Label(form, text="Название:").grid(row=0, column=0, padx=4, pady=4, sticky='w')
        self.s_query = tk.Entry(form, width=40)
        self.s_query.grid(row=0, column=1, padx=4, pady=4)


        tk.Button(form, text="Найти", command=self.do_search).grid(row=0, column=2, padx=4, pady=4)
        tk.Button(form, text="Сбросить", command=lambda: self.do_search(clear=True)).grid(
            row=0, column=3, padx=4, pady=4
        )


        cols = ('ID', 'Название', 'Категория', 'Цена', 'Остаток')
        self.tree_search = ttk.Treeview(self.tab_search, columns=cols, show='headings')
        for c in cols:
            self.tree_search.heading(c, text=c)
            self.tree_search.column(c, width=150, anchor='center')
        self.tree_search.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)


        self.do_search(clear=True)


    def do_search(self, clear=False):
        query = '' if clear else self.s_query.get().strip()
        if clear:
            self.s_query.delete(0, tk.END)
        for row in self.tree_search.get_children():
            self.tree_search.delete(row)
        for row in get_products(query or None):
            self.tree_search.insert('', 'end', values=row)






if __name__ == '__main__':
    init_db()
    root = tk.Tk()
    app = FlowerShopApp(root)
    root.mainloop()

