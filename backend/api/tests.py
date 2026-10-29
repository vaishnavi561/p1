from django.test import TestCase, override_settings
from django.core import mail
from django.core.management import call_command

@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class TestEmailManagementCommand(TestCase):
    def test_send_test_email_command(self):
        call_command('send_test_email', 'test@example.com')
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('MedLife AI Test Email', mail.outbox[0].subject)