from django.core.management.base import BaseCommand
from institutions.models import OutputReportingPeriod
from datetime import date

class Command(BaseCommand):
    help = 'Update the active quarter based on the current date'

    def handle(self, *args, **kwargs):
        today = date.today()
        OutputReportingPeriod.objects.update(is_active=False)
        
        active_period = OutputReportingPeriod.objects.filter(start_date__lte=today, end_date__gte=today).first()
        if active_period:
            active_period.is_active = True
            active_period.save()

        self.stdout.write(self.style.SUCCESS('Successfully updated the active quarter'))

