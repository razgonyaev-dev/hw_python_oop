import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        wasted = 0
        for object in self.records:
            if object.date == today:
                wasted += object.amount
        return wasted

    def get_week_stats(self):
        today = dt.date.today()
        week_ago = today - dt.timedelta(days=6)
        wasted = 0
        for object in self.records:
            if object.date >= week_ago and object.date <= today:
                wasted += object.amount
        return wasted


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        remained = self.limit - self.get_today_stats()
        if remained > 0:
            return (
                'Сегодня можно съесть что-нибудь ещё, '
                f'но с общей калорийностью не более {remained} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 74.34
    EURO_RATE = 94.24

    def get_today_cash_remained(self, currency):
        cur = 'руб'
        remained = self.limit - self.get_today_stats()
        if currency == 'eur':
            remained /= self.EURO_RATE
            cur = 'Euro'
        if currency == 'usd':
            remained /= self.USD_RATE
            cur = 'USD'
        if remained < 0:
            remained = abs(remained)
            return f'Денег нет, держись: твой долг - {remained:.2f} {cur}'
        elif remained == 0:
            return 'Денег нет, держись'
        else:
            return f'На сегодня осталось {remained:.2f} {cur}'


cash_calc = CashCalculator(5000)
cash_calc.add_record(Record(3300, 'Поход в кабак', '09.05.2021'))
cash_calc.add_record(Record(400, 'Такси', '09.05.2021'))
cash_calc.add_record(Record(1500, 'Мойка'))
cash_calc.add_record(Record(500, 'Заправка', '03.05.2021'))
calor_calc = CaloriesCalculator(1500)
calor_calc.add_record(Record(300, 'Омлет', '09.05.2021'))
calor_calc.add_record(Record(800, 'Стейк'))
calor_calc.add_record(Record(450, 'Пельмешки', '04.05.2021'))
print(cash_calc.get_today_stats())
print(cash_calc.get_week_stats())
print(cash_calc.get_today_cash_remained('rub'))
print(calor_calc.get_calories_remained())
