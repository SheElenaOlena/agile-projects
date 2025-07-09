from datetime import datetime
import calendar
from django.utils import timezone


def calculate_end_of_month():
    current_date = timezone.now()
    """Получает текущую дату и время с учётом часового пояса Django"""
    amount_of_days = calendar.monthrange(
        current_date.year,
        current_date.month)[1]
    """ Возвращает кол-во дней в текущем месяце (amount_of_days)"""
    date = datetime(
        year=current_date.year,
        month=current_date.month,
        day=amount_of_days,
    )
    """Создаёт объект datetime , указывает последний день месяца"""
    return date.astimezone()
    # """Возвращает дату с часовыми поясами"""

