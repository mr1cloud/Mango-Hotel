from pymongo.database import Database
from bson import ObjectId


class Guests:
    def __init__(self, db: Database):
        self.collection = db['guests']

    def show_all(self):
        guests = list(self.collection.find())
        print("Гости:")
        if not guests:
            print("  Нет гостей в базе.")
            return
        for g in guests:
            print(f"  [{g['_id']}] {g['full_name']} | Паспорт: {g['passport']} | "
                  f"Тел: {g['phone']} | Email: {g['email']}")

    def add(self, full_name, passport, phone, email):
        result = self.collection.insert_one({
            "full_name": full_name,
            "passport": passport,
            "phone": phone,
            "email": email,
        })
        print(f"Гость добавлен с ID: {result.inserted_id}")

    def delete(self, guest_id):
        result = self.collection.delete_one({"_id": ObjectId(guest_id)})
        if result.deleted_count > 0:
            print(f"Гость с ID {guest_id} удалён.")
        else:
            print(f"Гость с ID {guest_id} не найден.")

    def search(self, query):
        guests = list(self.collection.find({"full_name": {"$regex": query, "$options": "i"}}))
        print("Результаты поиска:")
        if not guests:
            print("  Нет гостей, соответствующих запросу.")
            return
        for g in guests:
            print(f"  [{g['_id']}] {g['full_name']} | Паспорт: {g['passport']} | Тел: {g['phone']}")

    def sort(self):
        print("Сортировать по: 1 - Имени, 2 - Email")
        field = "full_name" if input("Выбор: ").strip() == "1" else "email"
        guests = list(self.collection.find().sort(field, 1))
        for g in guests:
            print(f"  [{g['_id']}] {g['full_name']} | Email: {g['email']}")

    def menu(self):
        while True:
            print("\n--- Управление гостями ---")
            print("1. Показать всех гостей")
            print("2. Добавить гостя")
            print("3. Удалить гостя")
            print("4. Поиск по имени")
            print("5. Сортировка")
            print("0. Назад в главное меню")
            choice = input("\nВыберите действие: ").strip()

            if choice == "1":
                self.show_all()
            elif choice == "2":
                self.add(
                    full_name=input("Полное имя: "),
                    passport=input("Серия и номер паспорта: "),
                    phone=input("Телефон: "),
                    email=input("Email: "),
                )
            elif choice == "3":
                self.delete(input("Введите ID гостя для удаления: "))
            elif choice == "4":
                self.search(input("Введите имя для поиска: "))
            elif choice == "5":
                self.sort()
            elif choice == "0":
                break
            else:
                print("Неверный выбор. Попробуйте еще раз.")
