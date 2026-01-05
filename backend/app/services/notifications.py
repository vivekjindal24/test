import smtplib
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from icalendar import Calendar, Event
from twilio.rest import Client
from app.core.config import get_settings

settings = get_settings()

class NotificationService:
    def send_email(self, to: str, subject: str, body: str) -> None:
        msg = EmailMessage()
        msg["From"] = settings.email_from
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as smtp:
            smtp.send_message(msg)

    def send_sms(self, to: str, body: str) -> None:
        if not (settings.twilio_account_sid and settings.twilio_auth_token and settings.twilio_from_number):
            return
        client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
        client.messages.create(from_=settings.twilio_from_number, to=to, body=body)

    def send_calendar_invite(self, to: str, subject: str, body: str, start: datetime | None = None, duration_minutes: int = 30) -> None:
        start = start or datetime.now(timezone.utc) + timedelta(days=1)
        cal = Calendar()
        cal.add("prodid", "-//research-platform//")
        cal.add("version", "2.0")
        event = Event()
        event.add("summary", subject)
        event.add("dtstart", start)
        event.add("dtend", start + timedelta(minutes=duration_minutes))
        event.add("description", body)
        if settings.calendar_organizer_email:
            event.add("organizer", settings.calendar_organizer_email)
        cal.add_component(event)

        msg = EmailMessage()
        msg["From"] = settings.email_from
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)
        msg.add_attachment(cal.to_ical(), maintype="text", subtype="calendar", filename="invite.ics")
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as smtp:
            smtp.send_message(msg)
