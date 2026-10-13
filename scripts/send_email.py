#!/usr/bin/env python3
"""
Skrypt wysyłający powiadomienie e-mail o statusie wdrożenia Ansible.
Odczytuje konfigurację z zmiennych środowiskowych i wysyła e-mail,
jeśli skonfigurowane są wymagane zmienne SMTP.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def main() -> None:
    smtp_server = os.environ.get("SMTP_SERVER", "").strip()
    smtp_password = os.environ.get("SMTP_PASSWORD", "").strip()
    smtp_username = os.environ.get("SMTP_USERNAME", "").strip()
    recipient = os.environ.get("NOTIFICATION_EMAIL", "").strip()
    port_str = os.environ.get("SMTP_PORT", "587").strip()
    port = int(port_str) if port_str.isdigit() else 587

    # Jeśli zmienne nie są zdefiniowane, bezpiecznie pomijamy wysyłanie
    if not smtp_server or not smtp_password or not recipient:
        print("Powiadomienie e-mail pominięte: brak wymaganych zmiennych (SMTP_SERVER, SMTP_PASSWORD, NOTIFICATION_EMAIL).")
        return

    status = os.environ.get("WORKFLOW_STATUS", "UNKNOWN")
    repo = os.environ.get("REPO_NAME", "")
    commit = os.environ.get("COMMIT_SHA", "")[:7]
    branch = os.environ.get("COMMIT_REF", "")
    host = os.environ.get("APP_HOST", "nieznany")
    actor = os.environ.get("ACTOR", "")
    run_id = os.environ.get("RUN_ID", "")
    run_url = f"https://github.com/{repo}/actions/runs/{run_id}"

    status_pl = "SUKCES" if status.lower() == "success" else "BŁĄD"
    status_emoji = "✅" if status.lower() == "success" else "❌"
    subject = f"[{status_emoji} {status_pl}] Wdrożenie Ansible: {repo} ({branch})"

    body = f"""Cześć,

Status wdrożenia aplikacji: {status_emoji} {status_pl} ({status})
Repozytorium: {repo}
Gałąź: {branch}
Commit: {commit}
Autor: {actor}
Serwer docelowy: {host}

Szczegóły przebiegu w GitHub Actions:
{run_url}

Wiadomość wygenerowana automatycznie przez pipeline CI/CD.
"""

    msg = MIMEMultipart()
    from_addr = smtp_username if "@" in smtp_username else (f"{smtp_username}@{smtp_server}" if smtp_username else f"no-reply@{smtp_server}")
    msg["From"] = from_addr
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        print(f"Wysyłanie powiadomienia e-mail do: {recipient} przez {smtp_server}:{port}...")
        if port == 465:
            with smtplib.SMTP_SSL(smtp_server, port, timeout=15) as server:
                if smtp_username and smtp_password:
                    server.login(smtp_username, smtp_password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(smtp_server, port, timeout=15) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                if smtp_username and smtp_password:
                    server.login(smtp_username, smtp_password)
                server.send_message(msg)
        print("Powiadomienie e-mail zostało wysłane pomyślnie.")
    except Exception as exc:
        print(f"Ostrzeżenie: Nie udało się wysłać powiadomienia e-mail: {exc}")
        # Błąd powiadomienia nie powinien zatrzymywać pipeline'u


if __name__ == "__main__":
    main()
