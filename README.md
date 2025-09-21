# PPB – Repo ALL‑IN‑ONE (automaty + struktura)

Ten szablon zawiera:
- **raporty co godzinę** (commit do `reports/hourly/`)
- **raport dzienny z e‑mailem o 20:00 Europe/Warsaw**
- **tygodniowe archiwum (niedziela 20:00)** jako ZIP + artefakt Actions
- katalogi na projekty, materiały i dokumentację

## Sekrety wymagane (Settings → Secrets → Actions)
- `SMTP_HOST` (np. `smtp.wp.pl` lub `smtp.gmail.com`)
- `SMTP_PORT` (`465` dla SSL)
- `SMTP_USER` (login do poczty)
- `SMTP_PASS` (hasło aplikacji)
- `MAIL_FROM` (adres nadawcy)
- `MAIL_TO` (adres odbiorcy)

## Struktura
- `.github/workflows/…` — automaty GitHub Actions
- `tools/…` — skrypty pomocnicze
- `projects/…` — pliki projektów
- `reports/` — generowane raporty (hourly/daily/weekly)
- `assets/` — logo, czcionki itp.
- `docs/` — dokumentacja

**Uwaga (Windows/Android):** katalogi zaczynające się od kropki (np. `.github`) są ukryte.
Jeśli nie możesz ich wgrać jako folder, utwórz plik w UI GitHub o nazwie `.github/workflows/hourly.yml`.
