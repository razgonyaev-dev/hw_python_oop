import datetime as dt


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.today = dt.date.today()
        self.week = dt.timedelta(days=7)
        self.remained = self.limit - self.get_today_stats()

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        return sum(
            rec.amount for rec in self.records if
            rec.date == self.today)

    def get_week_stats(self):
        week_ago = self.today - self.week
        return sum(
            rec.amount for rec in self.records if
            week_ago < rec.date <= self.today)


class Record:
    date_order_ru = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, self.date_order_ru).date()


class CaloriesCalculator(Calculator):
    stop_phrase = 'Хватит есть!'
    cont_phrase = (
        'Сегодня можно съесть что-нибудь ещё, '
        'но с общей калорийностью не более {rem} кКал')

    def get_calories_remained(self):
        remained = self.limit - self.get_today_stats()
        if remained > 0:
            return self.cont_phrase.format(rem=remained)
        else:
            return self.stop_phrase


class CashCalculator(Calculator):
    RUB_RATE = 1
    USD_RATE = 60.0
    EURO_RATE = 70.0

    curr_info = {
        'rub': [RUB_RATE, 'руб'],
        'usd': [USD_RATE, 'USD'],
        'eur': [EURO_RATE, 'Euro']}

    stay_strong_phrase_debt = 'Денег нет, держись: твой долг - {cash} {title}'
    stay_strong_phrase = 'Денег нет, держись'
    you_have_money_phrase = 'На сегодня осталось {cash} {title}'
    unknown_curr_phrase = 'Неизвестная валюта: "{curr}", попробуйте другую'

    def get_today_cash_remained(self, currency='rub'):
        if currency not in CashCalculator.curr_info.keys():
            return self.unknown_curr_phrase.format(curr=currency)

        rate, title = CashCalculator.curr_info[currency]

        cash_remained = self.limit - self.get_today_stats()
        no_cash_remained = abs(round(cash_remained / rate, 2))

        if cash_remained < 0:
            return self.stay_strong_phrase_debt.format(
                cash=no_cash_remained, title=title)
        if cash_remained == 0:
            return self.stay_strong_phrase
        else:
            return self.you_have_money_phrase.format(
                cash=no_cash_remained, title=title)


if __name__ == '__main__':
    cash_calc = CashCalculator(5000)
    cash_calc.add_record(Record(3300, 'Поход в кабак', '12.05.2021'))
    cash_calc.add_record(Record(5100, 'Такси', '07.05.2021'))
    cash_calc.add_record(Record(1000, 'Мойка'))
    cash_calc.add_record(Record(500, 'Заправка', '06.05.2021'))
    calor_calc = CaloriesCalculator(1500)
    calor_calc.add_record(Record(300, 'Омлет', '09.05.2021'))
    calor_calc.add_record(Record(0, 'Стейк'))
    calor_calc.add_record(Record(450, 'Пельмешки', '05.05.2021'))
    print(cash_calc.get_today_stats())
    print(cash_calc.get_week_stats())
    print(cash_calc.get_today_cash_remained('rub'))
    print(calor_calc.get_calories_remained())
