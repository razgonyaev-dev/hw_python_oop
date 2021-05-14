import datetime as dt


class Calculator:
    TODAY = dt.date.today()
    WEEK = dt.timedelta(days=6)

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        return sum(
            rec.amount for rec in self.records if
            rec.date == self.TODAY)

    def get_week_stats(self):
        week_ago = self.TODAY - self.WEEK
        return sum(
            rec.amount for rec in self.records if
            week_ago < rec.date <= self.TODAY)


class Record:

    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, self.DATE_FORMAT).date()


class CaloriesCalculator(Calculator):
    STOP_EATING = 'Хватит есть!'
    YOU_CAN_EAT = (
        'Сегодня можно съесть что-нибудь ещё, '
        'но с общей калорийностью не более {remained} кКал')

    def get_calories_remained(self):
        remained = self.limit - self.get_today_stats()
        if remained > 0:
            return self.YOU_CAN_EAT.format(remained=remained)
        return self.STOP_EATING


class CashCalculator(Calculator):
    RUB_RATE = 1
    USD_RATE = 60.0
    EURO_RATE = 70.0

    currency_exchanger = {
        'rub': [RUB_RATE, 'руб'],
        'usd': [USD_RATE, 'USD'],
        'eur': [EURO_RATE, 'Euro']}

    STAY_STRONG_WITH_DEBT = 'Денег нет, держись: твой долг - {cash} {title}'
    STAY_STRONG = 'Денег нет, держись'
    YOU_HAVE_MONEY = 'На сегодня осталось {cash} {title}'
    UNKNOWN_CURRENCY = 'Неизвестная валюта: "{currency}", попробуйте другую'

    def get_today_cash_remained(self, currency='rub'):
        if currency not in self.currency_exchanger:
            raise KeyError(self.UNKNOWN_CURRENCY.format(currency=currency))

        rate, title = self.currency_exchanger[currency]

        cash_remained = self.limit - self.get_today_stats()
        out_cash_remained = round(cash_remained / rate, 2)

        if cash_remained < 0:
            return self.STAY_STRONG_WITH_DEBT.format(
                cash=abs(out_cash_remained), title=title)
        elif cash_remained == 0:
            return self.STAY_STRONG
        return self.YOU_HAVE_MONEY.format(
            cash=out_cash_remained, title=title)


if __name__ == '__main__':
    cash_calc = CashCalculator(5000)
    cash_calc.add_record(Record(3300, 'Поход в кабак', '12.05.2021'))
    cash_calc.add_record(Record(5100, 'Такси', '08.05.2021'))
    cash_calc.add_record(Record(143542, 'Мойка'))
    cash_calc.add_record(Record(500, 'Заправка', '06.05.2021'))
    calor_calc = CaloriesCalculator(1500)
    calor_calc.add_record(Record(300, 'Омлет', '09.05.2021'))
    calor_calc.add_record(Record(0, 'Стейк'))
    calor_calc.add_record(Record(450, 'Пельмешки', '05.05.2021'))
    print(cash_calc.get_today_stats())
    print(cash_calc.get_week_stats())
    print(cash_calc.get_today_cash_remained('eur'))
    print(calor_calc.get_calories_remained())
