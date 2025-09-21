# Instrukcja — instalacja paczki ALL‑IN‑ONE

1. Wyczyść repo (usuń dotychczasowe pliki, o ile chcesz „od zera”).
2. Wgraj zawartość tej paczki (zachowaj ścieżki).
3. Repo → Settings → Actions → General:
   - Allow all actions and reusable workflows
   - Workflow permissions → Read and write permissions
4. Actions → uruchom testowo każdy workflow (Run workflow).
5. (Opcjonalnie) Sekrety SMTP dla tygodniowego maila:
   - SMTP_HOST, SMTP_PORT (587), SMTP_USER, SMTP_PASS (hasło aplikacji), MAIL_FROM, MAIL_TO
6. Wrzuć logotypy do `assets/logos/` i podlinkuj je w PDF-ach i materiałach.

> Całość działa automatycznie: 07:00 wiedza, 20:00 raport dzienny, co godzinę raport godzinowy, w niedzielę e‑mail z tygodniówką.


## Dodatkowo — PDF premium i archiwum
- **Generate Premium PDF** (on demand & on push): uruchomi się po każdej zmianie w `projects/**` lub ręcznie z `Actions`.
- **Weekly Reports Archive**: w niedzielę ~20:10 spina `reports/` w archiwum `archives/YYYY-MM-DD_reports.zip`.

> Aby wymusić użycie fontu **DejaVu Serif**, wrzuć plik `DejaVuSerif.ttf` do `assets/fonts/`. W przeciwnym razie użyjemy Times-Roman.
