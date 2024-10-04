from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from django.db.models import Sum
from myapp.models import Purchase  # Adjust the import path as per your project structure
import json

class Command(BaseCommand):
    help = 'Send weekly sales report to manager'

    def handle(self, *args, **options):
        # Calculate start and end dates for the current week
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())  # Monday of the current week
        end_of_week = start_of_week + timedelta(days=6)  # Sunday of the current week

        # Query purchases within the current week
        weekly_purchases = Purchase.objects.filter(date_of_purchase__range=[start_of_week, end_of_week])

        # Aggregate total sales for each product
        total_sales = weekly_purchases.values('product_name').annotate(total_quantity=Sum('quantity'), total_amount=Sum('amount'))

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
        subject = 'Weekly Sales Report'
        message = f'Attached is the weekly sales report for {start_of_week.strftime("%Y-%m-%d")} to {end_of_week.strftime("%Y-%m-%d")}.\n\n{sales_json}'
        from_email = settings.EMAIL_HOST_USER
        to_email = ['kumarmurugaiya71@gmail.com']  # Replace with manager's email address

        send_mail(subject, message, from_email, to_email)

        self.stdout.write(self.style.SUCCESS('Weekly sales report sent successfully'))
