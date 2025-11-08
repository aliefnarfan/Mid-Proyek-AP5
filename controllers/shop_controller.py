# Controller for shop
from utils.database import db, cursor

cursor.execute("SELECT COUNT(*) AS total FROM shop_items;")
count = cursor.fetchone()['total']

if count == 0:
    shop_data = [
        ("Health Potion", "Memulihkan 50 HP", "potion", 30, 1),
        ("Energy Elixir", "Memulihkan 50 Energy", "potion", 40, 1),
        ("Iron Sword", "Senjata dasar meningkatkan damage", "weapon", 100, 2),
        ("Steel Armor", "Meningkatkan pertahanan dasar", "armor", 120, 3),
        ("Magic Staff", "Senjata khusus Archmage", "weapon", 150, 4)
    ]
    cursor.executemany("""
        INSERT INTO shop_items (item_name, description, item_type, price, min_floor)
        VALUES (%s, %s, %s, %s, %s);
    """, shop_data)
    db.commit()
    print("Shop items default berhasil dimasukkan ke database.")


def show_shop(floor_level: int):
    cursor.execute(
        "SELECT * FROM shop_items WHERE min_floor <= %s ORDER BY price ASC;",
        (floor_level,)
    )
    items = cursor.fetchall()

    print("\n=== SHOP GLOBAL ===")
    for item in items:
        print(f"[{item['id']}] {item['item_name']} ({item['item_type']}) - {item['price']} gold | {item['description']}")
    return items


def buy_item(character_id: int, item_id: int):
    try:
        cursor.execute("SELECT gold FROM characters WHERE id = %s;", (character_id,))
        char = cursor.fetchone()
        if not char:
            print("⚠️ Karakter tidak ditemukan.")
            return

        gold = char['gold']

        cursor.execute("SELECT * FROM shop_items WHERE id = %s;", (item_id,))
        item = cursor.fetchone()
        if not item:
            print("⚠️ Item tidak ditemukan.")
            return

        if gold < item['price']:
            print("❌ Gold tidak cukup untuk membeli item ini.")
            return

        cursor.execute("UPDATE characters SET gold = gold - %s WHERE id = %s;", (item['price'], character_id))

        cursor.execute("SELECT * FROM inventory WHERE character_id = %s AND item_id = %s;", (character_id, item_id))
        existing = cursor.fetchone()

        if existing:
            cursor.execute("UPDATE inventory SET quantity = quantity + 1 WHERE id = %s;", (existing['id'],))
        else:
            cursor.execute("INSERT INTO inventory (character_id, item_id, quantity) VALUES (%s,%s,1);", (character_id, item_id))

        db.commit()
        print(f"✅ Berhasil membeli {item['item_name']} seharga {item['price']} gold.")

    except Exception as e:
        db.rollback()
        print(f"⚠️ Terjadi kesalahan saat membeli item: {e}")


def open_shop(character):
    while True:
        items = show_shop(character.floor)
        print(f"\nGold kamu saat ini: {character.gold}")
        print("Ketik ID item untuk membeli, atau 0 untuk keluar.")

        try:
            choice = int(input("Masukkan pilihan: "))
        except ValueError:
            print("Masukkan angka yang valid.")
            continue

        if choice == 0:
            print("Keluar dari shop...\n")
            break

        buy_item(character.character_id, choice)

        cursor.execute("SELECT gold FROM characters WHERE id = %s;", (character.character_id,))
        character.gold = cursor.fetchone()['gold']