from pymongo.database import Database
from bson import ObjectId


class Rooms:
    def __init__(self, db: Database):
        self.collection = db['rooms']

    def show_all(self):
        rooms = self.collection.find()
        print("Номера:")
        if not rooms:
            print("  Нет номеров в базе.")
            return
        for r in rooms:
            status = "Свободен" if r.get("is_available") else "Занят"
            print(f"  [{r['_id']}] №{r['number']} | {r['room_type']} | "
                  f"{r['floor']} этаж | {r['price_per_night']} руб/ночь | {status}")

    def add(self, number, room_type, floor, price_per_night):
        room = {
            "number": number,
            "room_type": room_type,
            "floor": floor,
            "price_per_night": price_per_night,
            "is_available": True,
        }
        result = self.collection.insert_one(room)
        print(f"Номер добавлен с ID: {result.inserted_id}")

    def delete(self, room_id):
        result = self.collection.delete_one({"_id": ObjectId(room_id)})
        if result.deleted_count > 0:
            print(f"Номер с ID {room_id} удалён.")
        else:
            print(f"Номер с ID {room_id} не найден.")

    def search(self, query):
        rooms = self.collection.find({"room_type": {"$regex": query, "$options": "i"}})
        print("Результаты поиска:")
        if not rooms:
            print("  Нет номеров, соответствующих запросу.")
            return
        for r in rooms:
            status = "Свободен" if r.get("is_available") else "Занят"
            print(f"  [{r['_id']}] №{r['number']} | {r['room_type']} | "
                  f"{r['floor']} этаж | {r['price_per_night']} руб/ночь | {status}")

    def menu(self):
        while True:
            print("\n--- Управление номерами ---")
            print("1. Показать все номера")
            print("2. Добавить номер")
            print("3. Удалить номер")
            print("4. Поиск номера по типу")
            print("0. Назад в главное меню")
            choice = input("\nВыберите действие: ")

            if choice == "1":
                self.show_all()
            elif choice == "2":
                number = input("Номер комнаты: ")
                room_type = input("Тип (Одноместный/Двухместный/Люкс): ")
                floor = input("Этаж: ")
                price = input("Цена за ночь (руб): ")
                try:
                    self.add(number, room_type, int(floor), float(price))
                except ValueError:
                    print("Ошибка: этаж и цена должны быть числами.")
            elif choice == "3":
                room_id = input("Введите ID номера для удаления: ")
                self.delete(room_id)
            elif choice == "4":
                query = input("Введите тип номера для поиска: ")
                self.search(query)
            elif choice == "0":
                break
            else:
                print("Неверный выбор. Попробуйте еще раз.")
