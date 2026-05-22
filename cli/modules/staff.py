from pymongo.database import Database
from bson import ObjectId


class Staff:
    def __init__(self, db: Database):
        self.collection = db['staff']

    def show_all(self):
        staff = self.collection.find()
        print("Сотрудники:")
        if not staff:
            print("  Нет сотрудников в базе.")
            return
        for s in staff:
            print(f"  [{s['_id']}] {s['full_name']} | {s['position']} | "
                  f"Тел: {s['phone']} | Зарплата: {s['salary']} руб")

    def add(self, full_name, position, phone, salary):
        staff_member = {
            "full_name": full_name,
            "position": position,
            "phone": phone,
            "salary": salary
        }
        result = self.collection.insert_one(staff_member)
        print(f"Сотрудник добавлен с ID: {result.inserted_id}")

    def delete(self, staff_id):
        result = self.collection.delete_one({"_id": ObjectId(staff_id)})
        if result.deleted_count > 0:
            print(f"Сотрудник с ID {staff_id} удалён.")
        else:
            print(f"Сотрудник с ID {staff_id} не найден.")

    def search(self, query):
        staff = self.collection.find({"full_name": {"$regex": query, "$options": "i"}})
        print("Результаты поиска:")
        if not staff:
            print("  Нет сотрудников, соответствующих запросу.")
            return
        for s in staff:
            print(f"  [{s['_id']}] {s['full_name']} | {s['position']} | "
                  f"Тел: {s['phone']} | Зарплата: {s['salary']} руб")

    def menu(self):
        while True:
            print("\n--- Управление сотрудниками ---")
            print("1. Показать всех сотрудников")
            print("2. Добавить сотрудника")
            print("3. Удалить сотрудника")
            print("4. Поиск сотрудника")
            print("0. Назад в главное меню")
            choice = input("\nВыберите действие: ")

            if choice == "1":
                self.show_all()
            elif choice == "2":
                full_name = input("Введите ФИО: ")
                position = input("Должность: ")
                phone = input("Телефон: ")
                salary = input("Зарплата: ")
                try:
                    salary = float(salary)
                    self.add(full_name, position, phone, salary)
                except ValueError:
                    print("Ошибка: зарплата должна быть числом.")
            elif choice == "3":
                staff_id = input("Введите ID сотрудника для удаления: ")
                self.delete(staff_id)
            elif choice == "4":
                query = input("Введите имя для поиска: ")
                self.search(query)
            elif choice == "0":
                break
            else:
                print("Неверный выбор. Попробуйте еще раз.")
