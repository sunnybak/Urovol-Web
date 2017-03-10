from datetime import datetime, timedelta
from .models import  Pi, Data


class ChartData(object):

    @classmethod
    def get_avg_by_day(cls, user, days):

        now = datetime.now().date()

        readings = Data.objects.all()

        data = {'dates': [], 'values': []}

        data['dates'].append("date format")
        data['values'].append(23)

        for avg in glucose_averages:
            data['dates'].append(avg['record_date'].strftime('%m/%d'))
            data['values'].append(core.utils.round_value(avg['avg_value']))

        return data
