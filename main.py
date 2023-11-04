from datetime import date, timedelta

WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")


def close_birthday_users(users, start, end):
    now = date.today()
    result = []
    for user in users:
        # Розраховуємо день народження на цей рік та на наступний рік
        birthday_this_year = user.get('birthday').replace(year=now.year)
        birthday_next_year = user.get('birthday').replace(year=now.year + 1)

        # Розраховуємо різницю в днях між поточною датою та днем народження користувача на цей рік
        days_until_birthday_this_year = (birthday_this_year - now).days

        # Перевіряємо, чи день народження відбувся цього року, але знаходиться в межах тижня
        if 0 <= days_until_birthday_this_year <= 7:
            if birthday_this_year.weekday() >= 5:  # Якщо день народження випадає на суботу чи неділю
                result.append((user, birthday_this_year + timedelta(days=7 - birthday_this_year.weekday())))
            else:
                result.append((user, birthday_this_year))

        # Перевіряємо, чи день народження відбудеться наступного року в межах тижня
        elif (birthday_next_year - now).days <= 7:
            result.append((user, birthday_next_year))

    return result


def get_birthdays_per_week(users):
    # Отримуємо поточну дату (сьогодні)
    now = date.today()

    # Визначаємо день тижня для поточної дати
    current_week_day = now.weekday()

    # Визначаємо початкову дату тижня на основі поточної дати
    # Якщо поточний день тижня >= 5 (субота або неділя), то переноситься на наступний тиждень
    if current_week_day >= 5:
        start_date = now + timedelta(days=(7 - current_week_day))
    else:
        start_date = now - timedelta(days=current_week_day)

    # Визначаємо кінцеву дату тижня, додаючи 4 дні до початкової дати (тиждень складається з 5 робочих днів)
    end_date = start_date + timedelta(days=4)

    # Визначаємо користувачів, чиї дні народження в тижні знаходяться близько до поточної дати
    birthday_users = close_birthday_users(users, start=start_date, end=end_date)

    # Ініціалізуємо пустий словник для зберігання результатів
    result = {}

    # Для кожного користувача та його дня народження, відсортованих за днем народження
    for user, birthday in sorted(birthday_users, key=lambda x: x[1]):

        # Визначаємо день народження користувача
        user_birthday = birthday.weekday()

        # Визначаємо різницю в днях між днем народження та початковою датою тижня
        days_until_birthday = (birthday - start_date).days

        # Якщо різниця в днях більше або дорівнює 5, то користувач святкуватиме наступного тижня
        if days_until_birthday >= 5:
            days_until_birthday -= 7

        # Визначаємо день тижня, в який користувач буде святкувати свій день народження
        user_happy_day = WEEKDAYS[days_until_birthday]

        # Якщо такого дня тижня ще немає в словнику результатів, то створюємо його і додаємо ім'я користувача
        if user_happy_day not in result:
            result[user_happy_day] = []

        # Додаємо ім'я користувача до відповідного дня тижня
        result[user_happy_day].append(user.get('name'))

    # Повертаємо результат у вигляді словника, де ключ - це день тижня, а значення - це список імен користувачів
    return result


if __name__ == "__main__":
    users = [
        {"name": "Jan Koum", "birthday": date(1976, 1, 1)},
        {"name": "John Doe", "birthday": date(1990, 11, 5)},
    ]

    result = get_birthdays_per_week(users)
    print(result)
