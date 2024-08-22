
from django.core.management.base import BaseCommand
from datetime import date

from institutions.models import OutputReportingPeriod

class Command(BaseCommand):
    help = 'Update start_date and end_date for quarters on April 15th'

    def handle(self, *args, **kwargs):
        today = date.today()
        current_year = today.year

        q1_start = date(current_year, 4, 15)
        q1_end = date(current_year, 7, 14)
        q2_start = date(current_year, 7, 15)
        q2_end = date(current_year, 10, 14)
        q3_start = date(current_year, 10, 15)
        q3_end = date(current_year + 1, 1, 14)
        q4_start = date(current_year + 1, 1, 15)
        q4_end = date(current_year + 1, 4, 14)

        OutputReportingPeriod.objects.update_or_create(
            output_label='Q1',
            defaults={'start_date': q1_start, 'end_date': q1_end}
        )
        OutputReportingPeriod.objects.update_or_create(
            output_label='Q2',
            defaults={'start_date': q2_start, 'end_date': q2_end}
        )
        OutputReportingPeriod.objects.update_or_create(
            output_label='Q3',
            defaults={'start_date': q3_start, 'end_date': q3_end}
        )
        OutputReportingPeriod.objects.update_or_create(
            output_label='Q4',
            defaults={'start_date': q4_start, 'end_date': q4_end}
        )

        self.stdout.write(self.style.SUCCESS('Quarter dates updated successfully'))
