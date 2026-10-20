import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import os
from calculate_method import calculate_products

def init_db():
    if os.path.exists("aroma_dom.db"): return
    db = sqlite3.connect("aroma_dom.db")
    c = db.cursor()
    c.executescript("""
    CREATE TABLE MaterialTypes (Id INT, Name TEXT, Loss REAL);
    CREATE TABLE ProductTypes (Id INT, Name TEXT, Coef REAL);
    CREATE TABLE Materials (Id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, TypeId INT, Price REAL, Min REAL, Stock REAL, Pack REAL, Unit TEXT);
    CREATE TABLE Products (Id INT, Name TEXT, TypeId INT);
    CREATE TABLE ProductMaterials (MatId INT, ProdId INT, Qty REAL);
    
    INSERT INTO MaterialTypes VALUES (1,'Соевый воск',0.12),(2,'Пчелиный воск',0.18),(3,'Ароматическое масло',0.25),(4,'Краситель',0.08),(5,'Фитиль',0.03),(6,'Стеклянная тара',0.04),(7,'Керамическая тара',0.06),(8,'Декор',0.10),(9,'Упаковка',0.05),(10,'Этикетка',0.02);
    INSERT INTO ProductTypes VALUES (1,'Классическая свеча',1.00),(2,'Премиальная свеча',1.15),(3,'Подарочный набор',1.30),(4,'Интерьерная свеча',1.20),(5,'Мини-свеча',0.80),(6,'Сезонная коллекция',1.25);
    INSERT INTO Materials (Name, TypeId, Price, Min, Stock, Pack, Unit) VALUES 
    ('Соевый воск премиум',1,890,40,120,20,'кг'),('Соевый воск EcoBlend',1,760,30,95,25,'кг'),('Пчелиный воск натуральный',2,1450,15,48,10,'кг'),('Масло лаванды',3,3200,6,18.5,1,'л'),('Масло ванили',3,2950,8,22,1,'л'),('Масло цитрусовое',3,2870,5,16.7,1,'л'),('Краситель янтарный',4,640,2,6.2,0.5,'кг'),('Краситель розовый',4,615,1.5,5.1,0.5,'кг'),('Фитиль хлопковый 8 см',5,4.5,800,2500,500,'шт'),('Фитиль хлопковый 12 см',5,5.8,600,1800,400,'шт'),('Стакан прозрачный 200 мл',6,28,300,950,100,'шт'),('Стакан матовый 250 мл',6,34,200,620,60,'шт'),('Чаша керамическая белая',7,72,80,280,40,'шт'),('Сухоцветы лаванды',8,520,1.5,4.8,0.3,'кг'),('Лента сатиновая бежевая',9,12,120,340,50,'м'),('Коробка подарочная малая',9,18,150,420,50,'шт'),('Этикетка фирменная круглая',10,3.2,500,1800,250,'шт'),('Наклейка предупреждающая',10,2.1,400,1600,200,'шт');
    INSERT INTO Products VALUES (1,'Свеча «Лавандовый вечер»',1),(2,'Свеча «Ванильный крем»',1),(3,'Свеча «Цитрусовый сад»',1),(4,'Свеча «Белый мускус»',2),(5,'Свеча «Дикая орхидея»',2),(6,'Свеча «Теплый янтарь»',4),(7,'Свеча «Сандаловое дерево»',4),(8,'Мини-свеча «Лаванда»',5),(9,'Мини-свеча «Ваниль»',5),(10,'Мини-свеча «Цитрус»',5),(11,'Набор «Уютный дом»',3),(12,'Набор «Теплый вечер»',3),(13,'Свеча «Зимние специи»',6),(14,'Свеча «Хвойный лес»',6);
    INSERT INTO ProductMaterials VALUES (1,1,0.18),(4,1,0.009),(9,1,1),(11,1,1),(17,1,1),(1,2,0.18),(5,2,0.01),(9,2,1),(11,2,1),(17,2,1),(2,3,0.175),(6,3,0.011),(9,3,1),(11,3,1),(17,3,1),(1,4,0.22),(5,4,0.006),(10,4,1),(12,4,1),(17,4,1),(1,5,0.225),(4,5,0.004),(10,5,1),(12,5,1),(17,5,1),(3,6,0.28),(7,6,0.004),(10,6,1),(13,6,1),(17,6,1),(3,7,0.285),(5,7,0.003),(10,7,1),(13,7,1),(17,7,1),(2,8,0.07),(4,8,0.003),(9,8,1),(11,8,1),(2,9,0.07),(5,9,0.003),(9,9,1),(11,9,1),(2,10,0.07),(6,10,0.003),(9,10,1),(11,10,1),(1,11,0.18),(4,11,0.009),(9,11,1),(11,11,1),(15,11,1.2),(16,11,1),(17,11,1),(1,12,0.225),(5,12,0.01),(10,12,1),(12,12,1),(15,12,1.5),(16,12,1),(17,12,1),(1,13,0.21),(5,13,0.008),(7,13,0.003),(10,13,1),(12,13,1),(18,13,1),(1,14,0.215),(6,14,0.004),(7,14,0.002),(10,14,1),(12,14,1),(18,14,1);
    """)
    db.commit()
    db.close()

BG_MAIN, BG_CARD, ACCENT, FONT = "#FFFFFF", "#F4E6D4", "#8A5A44", "Georgia"

def load_cards():
    for widget in scroll_frame.winfo_children(): widget.destroy()
    db = sqlite3.connect("aroma_dom.db")
    c = db.cursor()
    c.execute("""
        SELECT m.Id, mt.Name, m.Name, m.Price, m.Min, m.Stock, m.Unit, COALESCE(SUM(pm.Qty), 0)
        FROM Materials m JOIN MaterialTypes mt ON mt.Id = m.TypeId
        LEFT JOIN ProductMaterials pm ON pm.MatId = m.Id
        GROUP BY m.Id ORDER BY mt.Name, m.Name
    """)
    for row in c.fetchall():
        card = tk.Frame(scroll_frame, bg=BG_CARD, padx=10, pady=8, highlightbackground=ACCENT, highlightthickness=1)
        card.pack(fill="x", padx=15, pady=4)
        text = f"{row[1]} | {row[2]}\nМинимальное количество: {row[4]} {row[6]}\nКоличество на складе: {row[5]} {row[6]}\nЦена: {row[3]:.2f} р / Единица измерения: {row[6]}\nТребуемое количество: {row[7]:.2f} {row[6]}"
        lbl = tk.Label(card, text=text, font=(FONT, 10), bg=BG_CARD, justify="left")
        lbl.pack(side="left", anchor="w")
        
        btn_prod = tk.Button(card, text="Продукция ➔", font=(FONT, 9), bg="#FFFFFF", fg=ACCENT, 
                             command=lambda m_id=row[0], m_name=row[2]: show_products_window(m_id, m_name))
        btn_prod.pack(side="right", padx=10)
        
        for widget in (card, lbl):
            widget.bind("<Button-1>", lambda e, m_id=row[0]: open_form(m_id))
    db.close()

def show_products_window(material_id, material_name):
    win = tk.Toplevel(root)
    win.title(f"Продукция: {material_name}")
    win.geometry("400x500")
    win.configure(bg=BG_MAIN)
    tk.Label(win, text=f"Где используется:\n{material_name}", font=(FONT, 12, "bold"), bg=ACCENT, fg="white", pady=10).pack(fill="x")
    
    db = sqlite3.connect("aroma_dom.db")
    c = db.cursor()
    c.execute("SELECT p.Name, pm.Qty, m.Unit FROM ProductMaterials pm JOIN Products p ON p.Id = pm.ProdId JOIN Materials m ON m.Id = pm.MatId WHERE pm.MatId = ?", (material_id,))
    for row in c.fetchall():
        f = tk.Frame(win, bg=BG_CARD, pady=5, padx=10)
        f.pack(fill="x", padx=10, pady=5)
        tk.Label(f, text=row[0], font=(FONT, 10, "bold"), bg=BG_CARD).pack(anchor="w")
        tk.Label(f, text=f"Требуется: {row[1]} {row[2]}", font=(FONT, 9), bg=BG_CARD).pack(anchor="w")
    db.close()
    
    tk.Button(win, text="⬅ Назад", bg=ACCENT, fg="white", font=(FONT, 10, "bold"), command=win.destroy).pack(pady=15)

def open_form(material_id=None):
    form = tk.Toplevel(root)
    form.title("Редактирование" if material_id else "Добавление")
    form.geometry("350x500")
    form.configure(bg=BG_MAIN)
    
    db = sqlite3.connect("aroma_dom.db")
    c = db.cursor()
    c.execute("SELECT Id, Name FROM MaterialTypes")
    types = c.fetchall()
    
    tk.Label(form, text="Тип материала", bg=BG_MAIN).pack(pady=(5,0))
    cb_type = ttk.Combobox(form, values=[t[1] for t in types], state="readonly"); cb_type.pack()
    
    tk.Label(form, text="Наименование", bg=BG_MAIN).pack(pady=(5,0))
    ent_name = tk.Entry(form); ent_name.pack()
    
    tk.Label(form, text="Цена (руб)", bg=BG_MAIN).pack(pady=(5,0))
    ent_price = tk.Entry(form); ent_price.pack()
    
    tk.Label(form, text="Ед. изм.", bg=BG_MAIN).pack(pady=(5,0))
    cb_unit = ttk.Combobox(form, values=["кг", "л", "м", "шт"], state="readonly"); cb_unit.pack()
    
    tk.Label(form, text="В упаковке", bg=BG_MAIN).pack(pady=(5,0))
    ent_pack = tk.Entry(form); ent_pack.pack()
    
    tk.Label(form, text="Мин. количество", bg=BG_MAIN).pack(pady=(5,0))
    ent_min = tk.Entry(form); ent_min.pack()
    
    tk.Label(form, text="На складе", bg=BG_MAIN).pack(pady=(5,0))
    ent_stock = tk.Entry(form); ent_stock.pack()
    
    if material_id:
        c.execute("SELECT TypeId, Name, Price, Min, Stock, Pack, Unit FROM Materials WHERE Id=?", (material_id,))
        row = c.fetchone()
        cb_type.set([t[1] for t in types if t[0] == row[0]][0])
        ent_name.insert(0, row[1]); ent_price.insert(0, row[2])
        ent_min.insert(0, row[3]); ent_stock.insert(0, row[4]); 
        ent_pack.insert(0, row[5]); cb_unit.set(row[6])
    db.close()

    def save():
        try:
            price, min_q = float(ent_price.get()), float(ent_min.get())
            pack = float(ent_pack.get())
            if price < 0 or min_q < 0: raise ValueError("Цена и мин. количество не могут быть отрицательными!")
            if not ent_name.get(): raise ValueError("Введите наименование!")
            
            type_id = [t[0] for t in types if t[1] == cb_type.get()][0]
            db = sqlite3.connect("aroma_dom.db"); c = db.cursor()
            if material_id:
                c.execute("UPDATE Materials SET Name=?, TypeId=?, Price=?, Min=?, Stock=?, Pack=?, Unit=? WHERE Id=?",
                          (ent_name.get(), type_id, price, min_q, float(ent_stock.get()), pack, cb_unit.get(), material_id))
            else:
                c.execute("INSERT INTO Materials (Name, TypeId, Price, Min, Stock, Pack, Unit) VALUES (?,?,?,?,?,?,?)",
                          (ent_name.get(), type_id, price, min_q, float(ent_stock.get()), pack, cb_unit.get()))
            db.commit(); db.close()
            form.destroy(); load_cards()
        except Exception as e:
            messagebox.showerror("Ошибка ввода", f"Некорректные данные:\n{e}", parent=form)
            
    tk.Button(form, text="Сохранить", bg=ACCENT, fg="white", command=save).pack(pady=15)

init_db()
root = tk.Tk()
root.title("Арома Дом — Материалы")
root.geometry("600x700")
root.configure(bg=BG_MAIN)

try: root.iconbitmap("app.ico")
except Exception: pass

header = tk.Frame(root, bg=ACCENT, pady=10); header.pack(fill="x")

try:
    logo = tk.PhotoImage(file="logo.png")
    tk.Label(header, image=logo, bg=ACCENT).pack(side="left", padx=10)
except Exception: pass

tk.Label(header, text="Арома Дом", font=(FONT, 14, "bold"), bg=ACCENT, fg="white").pack(side="left", padx=5)
tk.Button(header, text="+ Добавить", bg="white", fg=ACCENT, command=lambda: open_form(None)).pack(side="right", padx=15)

canvas = tk.Canvas(root, bg=BG_MAIN, highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scroll_frame = tk.Frame(canvas, bg=BG_MAIN)
scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=580)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True); scrollbar.pack(side="right", fill="y")

load_cards()
root.mainloop()