import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import os
import uuid
from datetime import datetime, timedelta
import jwt


class EmailService:
    """
    Email service for sending verification and password recovery emails
    """

    def __init__(self):
        self.smtp_server = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SMTP_USER", "")
        self.sender_password = os.getenv("SMTP_PASSWORD", "")
        self.secret_key = os.getenv("BETTER_AUTH_SECRET", "fallback-secret-key-for-development")

    def send_verification_email(self, recipient_email: str, user_id: str) -> bool:
        """
        Send email verification email to user

        Args:
            recipient_email: Email address to send verification to
            user_id: User ID to include in verification token

        Returns:
            True if email was sent successfully, False otherwise
        """
        try:
            # Generate verification token
            verification_token = self.generate_verification_token(user_id)

            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = "Verify your email address"
            message["From"] = self.sender_email
            message["To"] = recipient_email

            # Create the plain-text and HTML version of your message
            text = f"""\
            Please verify your email address by clicking the link below:

            Verify: {os.getenv('FRONTEND_URL', 'http://localhost:3000')}/verify-email?token={verification_token}

            If you didn't create an account with us, please ignore this email."""

            html = f"""\
            <html>
            <body>
                <h2>Welcome to TASKAPP!</h2>
                <p>Please verify your email address by clicking the link below:</p>
                <p>
                    <a href="{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/verify-email?token={verification_token}">
                        Verify Email Address
                    </a>
                </p>
                <p>If you didn't create an account with us, please ignore this email.</p>
            </body>
            </html>
            """

            # Turn these into plain/html MIMEText objects
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")

            # Add HTML/plain parts to MIMEMultipart message
            message.attach(part1)
            message.attach(part2)

            # Create secure connection and send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())

            return True

        except Exception as e:
            print(f"Error sending verification email: {e}")
            return False

    def send_password_reset_email(self, recipient_email: str, user_id: str) -> bool:
        """
        Send password reset email to user

        Args:
            recipient_email: Email address to send reset link to
            user_id: User ID to include in reset token

        Returns:
            True if email was sent successfully, False otherwise
        """
        try:
            # Generate reset token
            reset_token = self.generate_reset_token(user_id)

            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = "Password Reset Request"
            message["From"] = self.sender_email
            message["To"] = recipient_email

            # Create the plain-text and HTML version of your message
            text = f"""\
            You requested to reset your password. Click the link below to reset it:

            Reset Password: {os.getenv('FRONTEND_URL', 'http://localhost:3000')}/reset-password?token={reset_token}

            If you didn't request a password reset, please ignore this email."""

            html = f"""\
            <html>
            <body>
                <h2>Password Reset Request</h2>
                <p>You requested to reset your password. Click the link below to reset it:</p>
                <p>
                    <a href="{os.getenv('FRONTEND_URL', 'http://localhost:3000')}/reset-password?token={reset_token}">
                        Reset Password
                    </a>
                </p>
                <p>If you didn't request a password reset, please ignore this email.</p>
            </body>
            </html>
            """

            # Turn these into plain/html MIMEText objects
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")

            # Add HTML/plain parts to MIMEMultipart message
            message.attach(part1)
            message.attach(part2)

            # Create secure connection and send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())

            return True

        except Exception as e:
            print(f"Error sending password reset email: {e}")
            return False

    def generate_verification_token(self, user_id: str) -> str:
        """
        Generate a verification token for email verification

        Args:
            user_id: User ID to include in the token

        Returns:
            JWT token string
        """
        # Token expires in 24 hours
        expiration = datetime.utcnow() + timedelta(hours=24)

        payload = {
            "user_id": user_id,
            "exp": expiration,
            "type": "verification"
        }

        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        return token

    def generate_reset_token(self, user_id: str) -> str:
        """
        Generate a reset token for password reset

        Args:
            user_id: User ID to include in the token

        Returns:
            JWT token string
        """
        # Token expires in 1 hour
        expiration = datetime.utcnow() + timedelta(hours=1)

        payload = {
            "user_id": user_id,
            "exp": expiration,
            "type": "reset"
        }

        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        return token

    def verify_token(self, token: str, expected_type: str) -> Optional[str]:
        """
        Verify a token and return the user ID if valid

        Args:
            token: JWT token to verify
            expected_type: Expected token type ("verification" or "reset")

        Returns:
            User ID if token is valid, None otherwise
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])

            # Check if token type matches expected type
            if payload.get("type") != expected_type:
                return None

            return payload.get("user_id")
        except jwt.ExpiredSignatureError:
            # Token has expired
            return None
        except jwt.JWTError:
            # Invalid token
            return None