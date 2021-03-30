import datetime as dt
from typing import Dict, Union, Optional


class Record:
    def __init__(self, amount, comment, date: Optional[str] = None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:

    def __init__(self, limit: Union[str, float]):
        self.limit = limit
        self.records = []
        self.today = dt.date.today()
        self.week_ago = self.today - dt.timedelta(days=7)

# Метод add_record() в качестве аргумента принимает объект
# класса Record и сохраняет его в списке records
    def add_record(self, record: Record) -> None:
        self.records.append(record)

    def get_today_stats(self):
        return sum([record.amount for record in self.records
                    if record.date == self.today])

        # Метод расчета оставшегося лимита за день
    def get_today_limit_balance(self) -> float:
        return self.limit - self.get_today_stats()

        # Считать, сколько денег потрачено за последние 7 дней
        # Считать, сколько калорий получено за последние 7 дней
    def get_week_stats(self):
        return sum([record.amount for record in self.records
                    if self.week_ago <= record.date <= self.today])


class CashCalculator(Calculator):
    RUB_RATE: float = 1
    USD_RATE: float = 75.69
    EURO_RATE: float = 89.19

    # Определять, сколько ещё денег можно потратить сегодня
    # рублях, долларах или евро — метод get_today_cash_remained(currency)
    def get_today_cash_remained(self, currency):
        self.currency = currency
        currencies: Dict[str, tuple[str, float]] = {
            'rub': ('руб', CashCalculator.RUB_RATE),
            'usd': ('USD', CashCalculator.USD_RATE),
            'eur': ('Euro', CashCalculator.EURO_RATE)}
        cash_remained: Union[str, float] = self.get_today_limit_balance()
        name, cash = currencies[currency]
        cash_stats = abs(round(cash_remained / cash, 2))
        if currency not in currencies:
            raise ValueError('Программа не работает с таким видом валюты')
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained > 0:
            return (f'На сегодня осталось '
                    f'{cash_stats} {name}')
        else:
            return (f'Денег нет, держись: твой долг - '
                    f'{cash_stats} {name}')


class CaloriesCalculator(Calculator):
    # Определять, сколько ещё калорий можно/нужно получить сегодня
    # — метод get_calories_remained()
    def get_calories_remained(self):
        calories_remained = self.get_today_limit_balance()
        if calories_remained > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {calories_remained} кКал')
        else:
            return 'Хватит есть!'


class Record:

    def __init__(self, amount, comment, date: Optional[str] = None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
