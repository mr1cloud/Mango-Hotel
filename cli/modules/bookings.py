from pymongo.database import Database
from bson import ObjectId


class Bookings:
    def __init__(self, db: Database):
        self.collection = db['bookings']
        self.rooms = db['rooms']

    @staticmethod
    def _print(b):
        print(f"  [{b['_id']}] Гость ID: {b['guest_id']} | Номер ID: {b['room_id']} | "
              f"{b['check_in']} → {b['check_out']} | Статус: {b['status']} | "
              f"Сумма: {b.get('total_price', '?')} руб")

    def show_all(self):
        bookings = list(self.collection.find())
        print("Бронирования:")
        if not bookings:
            print("  Нет бронирований в базе.")
            return
        for b in bookings:
            self._print(b)

    def add(self, guest_id, room_id, check_in, check_out, total_price):
        try:
            result = self.collection.insert_one({
                "guest_id": ObjectId(guest_id),
                "room_id": ObjectId(room_id),
                "check_in": check_in,
                "check_out": check_out,
                "status": "Подтверждено",
                "total_price": float(total_price),
            })
            self.rooms.update_one({"_id": ObjectId(room_id)}, {"$set": {"is_available": False}})
            print(f"Бронирование добавлено с ID: {result.inserted_id}")
        except Exception as e:
            print(f"Ошибка: {e}")

    def delete(self, booking_id):
        try:
            booking = self.collection.find_one({"_id": ObjectId(booking_id)})
            if not booking:
                print(f"Бронирование с ID {booking_id} не найдено.")
                return
            self.collection.delete_one({"_id": ObjectId(booking_id)})
            self.rooms.update_one({"_id": booking["room_id"]}, {"$set": {"is_available": True}})
            print(f"Бронирование удалено, номер освобождён.")
        except Exception:
            print("Ошибка: некорректный ID.")

    def search(self, guest_id):
        try:
            bookings = list(self.collection.find({"guest_id": ObjectId(guest_id)}))
            print("Результаты поиска:")
            if not bookings:
                print("  Бронирований для этого гостя не найдено.")
                return
            for b in bookings:
                self._print(b)
        except Exception:
            print("Ошибка: некорректный ID.")

    def sort(self):
        print("Сортировать по: 1 - Дате заезда, 2 - Стоимости")
        field = "check_in" if input("Выбор: ").strip() == "1" else "total_price"
        for b in self.collection.find().sort(field, 1):
            self._print(b)

    def menu(self):
        while True:
            print("\n--- Управление бронированиями ---")
            print("1. Показать все бронирования")
            print("2. Добавить бронирование")
            print("3. Удалить бронирование")
            print("4. Поиск по ID гостя")
            print("5. Сортировка")
            print("0. Назад в главное меню")
            choice = input("\nВыберите действие: ").strip()

            if choice == "1":
                self.show_all()
            elif choice == "2":
                self.add(
                    guest_id=input("ID гостя: "),
                    room_id=input("ID номера: "),
                    check_in=input("Дата заезда (ГГГГ-ММ-ДД): "),
                    check_out=input("Дата выезда (ГГГГ-ММ-ДД): "),
                    total_price=input("Итоговая стоимость (руб): "),
                )
            elif choice == "3":
                self.delete(input("Введите ID бронирования для удаления: "))
            elif choice == "4":
                self.search(input("Введите ID гостя: "))
            elif choice == "5":
                self.sort()
            elif choice == "0":
                break
            else:
                print("Неверный выбор. Попробуйте еще раз.")
