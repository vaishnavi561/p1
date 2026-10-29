from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Sends a test email using configured SMTP settings (P13).'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Recipient email address for the test.')

    def handle(self, *args, **options):
        recipient = options['email']
        self.stdout.write(f"Sending test email to {recipient} using host {getattr(settings, 'EMAIL_HOST', 'localhost')}...")
        try:
            send_mail(
                subject="MedLife AI Test Email",
                message="Hello from MedLife AI! Your SMTP email configuration is working successfully.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f"Successfully sent test email to {recipient}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to send email: {str(e)}"))