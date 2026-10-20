import sqlite3

def calculate_products(prod_type_id, mat_type_id, raw_qty, param1, param2):
    if raw_qty <= 0 or param1 <= 0 or param2 <= 0:
        return -1
    
    try:
        db = sqlite3.connect("aroma_dom.db")
        c = db.cursor()
        c.execute("SELECT Coef FROM ProductTypes WHERE Id=?", (prod_type_id,))
        coef_row = c.fetchone()
        c.execute("SELECT Loss FROM MaterialTypes WHERE Id=?", (mat_type_id,))
        loss_row = c.fetchone()
        
        if not coef_row or not loss_row: 
            return -1
        
        coef = coef_row[0]
        loss = loss_row[0] / 100.0  
        
        mat_per_unit = param1 * param2 * coef
        usable_raw = raw_qty * (1 - loss)
        
        return int(usable_raw / mat_per_unit)
    except Exception:
        return -1
    finally:
        if 'db' in locals(): db.close()

if __name__ == "__main__":
    print("Результат теста (ожидается 99):", calculate_products(1, 1, 1000, 2.0, 5.0))