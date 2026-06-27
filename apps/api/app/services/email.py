# ruff: noqa: E501
from __future__ import annotations

from structlog import get_logger

from app.config import settings

logger = get_logger()


def _make_verification_email(name: str, url: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background-color:#000;color:#fff;font-family:system-ui,-apple-system,sans-serif">
<table width="100%" cellpadding="0" cellspacing="0" style="background-color:#000;padding:40px 20px">
<tr><td align="center">
<table width="480" cellpadding="0" cellspacing="0" style="background-color:#0a0a0a;border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:48px 40px">
<tr><td style="text-align:center;padding-bottom:24px">
<div style="width:48px;height:48px;margin:0 auto 16px;border-radius:50%;background:radial-gradient(circle,#f59e0b 0%,transparent 70%)"></div>
<h1 style="margin:0 0 8px;font-size:20px;font-weight:600;letter-spacing:-0.02em;color:#fff">Verify your email</h1>
<p style="margin:0 0 32px;font-size:14px;line-height:1.5;color:rgba(255,255,255,0.4)">Hello {name}, welcome to MEMEX. Click below to verify your email address.</p>
</td></tr>
<tr><td style="text-align:center;padding-bottom:32px">
<a href="{url}" style="display:inline-block;padding:14px 32px;border-radius:8px;background:linear-gradient(135deg,#f59e0b,#d97706);color:#000;font-size:14px;font-weight:600;text-decoration:none;letter-spacing:0.01em">Verify Email →</a>
</td></tr>
<tr><td style="text-align:center">
<p style="margin:0;font-size:12px;color:rgba(255,255,255,0.2)">This link expires in 24 hours. If you didn't create an account, ignore this email.</p>
</td></tr>
</table>
</td></tr></table></body></html>"""


def _make_password_reset_email(name: str, url: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background-color:#000;color:#fff;font-family:system-ui,-apple-system,sans-serif">
<table width="100%" cellpadding="0" cellspacing="0" style="background-color:#000;padding:40px 20px">
<tr><td align="center">
<table width="480" cellpadding="0" cellspacing="0" style="background-color:#0a0a0a;border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:48px 40px">
<tr><td style="text-align:center;padding-bottom:24px">
<div style="width:48px;height:48px;margin:0 auto 16px;border-radius:50%;background:radial-gradient(circle,#22d3ee 0%,transparent 70%)"></div>
<h1 style="margin:0 0 8px;font-size:20px;font-weight:600;letter-spacing:-0.02em;color:#fff">Reset your password</h1>
<p style="margin:0 0 32px;font-size:14px;line-height:1.5;color:rgba(255,255,255,0.4)">Hello {name}, click below to reset your password. This link is valid for 1 hour.</p>
</td></tr>
<tr><td style="text-align:center;padding-bottom:32px">
<a href="{url}" style="display:inline-block;padding:14px 32px;border-radius:8px;background:linear-gradient(135deg,#22d3ee,#0891b2);color:#000;font-size:14px;font-weight:600;text-decoration:none;letter-spacing:0.01em">Reset Password →</a>
</td></tr>
<tr><td style="text-align:center">
<p style="margin:0;font-size:12px;color:rgba(255,255,255,0.2)">If you didn't request a password reset, ignore this email.</p>
</td></tr>
</table>
</td></tr></table></body></html>"""


def _make_welcome_email(name: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background-color:#000;color:#fff;font-family:system-ui,-apple-system,sans-serif">
<table width="100%" cellpadding="0" cellspacing="0" style="background-color:#000;padding:40px 20px">
<tr><td align="center">
<table width="480" cellpadding="0" cellspacing="0" style="background-color:#0a0a0a;border:1px solid rgba(255,255,255,0.06);border-radius:16px;padding:48px 40px">
<tr><td style="text-align:center;padding-bottom:24px">
<div style="width:48px;height:48px;margin:0 auto 16px;border-radius:50%;background:radial-gradient(circle,#f59e0b 0%,transparent 70%)"></div>
<h1 style="margin:0 0 8px;font-size:20px;font-weight:600;letter-spacing:-0.02em;color:#fff">Welcome to MEMEX</h1>
<p style="margin:0 0 32px;font-size:14px;line-height:1.5;color:rgba(255,255,255,0.4)">Your artificial memory is ready, {name}. Start preserving, connecting, and discovering like never before.</p>
</td></tr>
<tr><td style="text-align:center;padding-bottom:32px">
<a href="https://memex.sh/login" style="display:inline-block;padding:14px 32px;border-radius:8px;background:linear-gradient(135deg,#f59e0b,#d97706);color:#000;font-size:14px;font-weight:600;text-decoration:none;letter-spacing:0.01em">Enter MEMEX →</a>
</td></tr>
</table>
</td></tr></table></body></html>"""


class EmailService:
    async def send_verification_email(
        self, email: str, name: str, token: str
    ) -> bool:
        url = f"{settings.app_url}/verify-email?token={token}"
        html = _make_verification_email(name, url)
        return await self._send(email, "Verify your email — MEMEX", html)

    async def send_password_reset_email(
        self, email: str, name: str, token: str
    ) -> bool:
        url = f"{settings.app_url}/reset-password?token={token}"
        html = _make_password_reset_email(name, url)
        return await self._send(email, "Reset your password — MEMEX", html)

    async def send_welcome_email(self, email: str, name: str) -> bool:
        html = _make_welcome_email(name)
        return await self._send(email, "Welcome to MEMEX", html)

    async def _send(
        self, to: str, subject: str, html: str
    ) -> bool:
        if not settings.resend_api_key:
            logger.warning("Resend API key not configured; skipping email", to=to, subject=subject)
            return False
        try:
            import resend

            resend.api_key = settings.resend_api_key
            params = {
                "from": "MEMEX <noreply@memex.sh>",
                "to": [to],
                "subject": subject,
                "html": html,
            }
            import asyncio

            await asyncio.to_thread(resend.Emails.send, params)
            logger.info("Email sent", to=to, subject=subject)
            return True
        except Exception as e:
            logger.error("Failed to send email", to=to, subject=subject, error=str(e))
            return False


email_service = EmailService()
