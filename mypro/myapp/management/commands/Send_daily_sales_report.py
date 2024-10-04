# sales_management/management/commands/send_daily_sales_report.py

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from django.db.models import Sum
from myapp.models import Purchase  # Adjust the import path as per your project structure
import json

class Command(BaseCommand):
    help = 'Send daily sales report to manager'

    def handle(self, *args, **options):
        # Calculate start and end dates for the current day
        today = datetime.now().date()
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())

        # Query purchases within the current day
        daily_purchases = Purchase.objects.filter(date_of_purchase__range=[start_of_day, end_of_day])

        # Aggregate total sales for each product
        total_sales = daily_purchases.values('product_name').annotate(total_quantity=Sum('quantity'), total_amount=Sum('amount'))

        # Prepare JSON data
        sales_data = {}
        for item in total_sales:
            product_name = item['product_name']
            qty = item['total_quantity']
            amount = item['total_amount']
            sales_data[product_name] = {'QTY': qty, 'Amount': amount}

        # Convert sales_data to JSON format
        sales_json = json.dumps(sales_data, indent=2)

        # Send email
        subject = 'Daily Sales Report'
        message = f'Attached is the daily sales report.\n\n{sales_json}'
        from_email = settings.EMAIL_HOST_USER
        to_email = ['santhoshpv002@gmail.com']  # Replace with manager's email address

        send_mail(subject, message, from_email, to_email)

        self.stdout.write(self.style.SUCCESS('Daily sales report sent successfully'))
