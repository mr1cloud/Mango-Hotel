from pymongo.database import Database
from bson import ObjectId


class Services:
    def __init__(self, db: Database):
        self.collection = db['services']
        self.bookings = db['bookings']

    @staticmethod
    def _print(s):
        print(f"  [{s['_id']}] Бронирование ID: {s['booking_id']} | "
              f"Услуга: {s['service_name']} | Цена: {s['price']} руб | Дата: {s['date']}")

    def show_all(self):
        services = list(self.collection.find())
        print("Услуги:")
        if not services:
            print("  Нет услуг в базе.")
            return
        for s in services:
            self._print(s)

    def add(self, booking_id, service_name, price, date):
        try:
            if not self.bookings.find_one({"_id": ObjectId(booking_id)}):
                print(f"Бронирование с ID {booking_id} не найдено.")
                return
            result = self.collection.insert_one({
                "booking_id": ObjectId(booking_id),
                "service_name": service_name,
                "price": float(price),
                "date": date,
            })
            print(f"Услуга добавлена с ID: {result.inserted_id}")
        except Exception as e:
            print(f"Ошибка: {e}")

    def delete(self, service_id):
        try:
            result = self.collection.delete_one({"_id": ObjectId(service_id)})
            if result.deleted_count > 0:
                print(f"Услуга с ID {service_id} удалена.")
            else:
                print(f"Услуга с ID {service_id} не найдена.")
        except Exception:
            print("Ошибка: некорректный ID.")

    def search(self, query):
        services = list(self.collection.find({"service_name": {"$regex": query, "$options": "i"}}))
        print("Результаты поиска:")
        if not services:
            print("  Нет услуг, соответствующих запросу.")
            return
        for s in services:
            self._print(s)

    def sort(self):
        print("Сортировать по: 1 - Цене, 2 - Дате, 3 - Названию")
        field = {"1": "price", "2": "date", "3": "service_name"}.get(input("Выбор: ").strip(), "date")
        for s in self.collection.find().sort(field, 1):
            self._print(s)

    def menu(self):
        while True:
            print("\n--- Управление услугами ---")
            print("1. Показать все услуги")
            print("2. Добавить услугу")
            print("3. Удалить услугу")
            print("4. Поиск по названию")
            print("5. Сортировка")
            print("0. Назад в главное меню")
            choice = input("\nВыберите действие: ").strip()

            if choice == "1":
                self.show_all()
            elif choice == "2":
                self.add(
                    booking_id=input("ID бронирования: "),
                    service_name=input("Название услуги (Завтрак/Трансфер/Спа/...): "),
                    price=input("Цена услуги (руб): "),
                    date=input("Дата оказания (ГГГГ-ММ-ДД): "),
                )
            elif choice == "3":
                self.delete(input("Введите ID услуги для удаления: "))
            elif choice == "4":
                self.search(input("Введите название услуги для поиска: "))
            elif choice == "5":
                self.sort()
            elif choice == "0":
                break
            else:
                print("Неверный выбор. Попробуйте еще раз.")
