# PPB — Repo ALL‑IN‑ONE (automaty + struktura projektów)

Ten repozytorium jest gotowe do zbierania **wszystkich projektów**, plików PDF, grafik, logotypów, raportów oraz automatycznej „auto‑nauki”.

## Automaty (GitHub Actions)
- **07:00** — moduł wiedzy → `reports/knowledge/`
- **20:00** — raport dzienny z podglądem wiedzy → `reports/daily/`
- **Co godzinę** — raport godzinowy → `reports/hourly/`
- **Niedziela ~20:05** — mail tygodniowy (wymaga sekretów SMTP) → `reports/weekly/` + e‑mail

## Struktura katalogów
```
assets/
  logos/        # logotypy (tu wrzuć logo stowarzyszenia, wersje PDF/PNG/SVG)
  photos/       # zdjęcia kampanii, eventów (z opisami/licencjami)
  fonts/        # pliki fontów (np. DejaVu Serif)
docs/           # dokumentacja, PDF-y, regulaminy
knowledge/      # kolejka tematów auto-nauki (topics.yaml)
projects/
  Bezpieczny_Pieszy/
  Zwolnij_przy_przejsciu/
  Odblask_ratuje_zycie/
  _wspolne_szablony/
reports/
  daily/
  hourly/
  knowledge/
  weekly/
tools/          # skrypty generatorów
```

## Instalacja
1. **Usuń** wszystko z repo (jeśli chcesz mieć czysto).
2. **Wgraj** zawartość tej paczki (z zachowaniem ścieżek).
3. Repo → **Settings → Actions → General**:
   - *Allow all actions and reusable workflows*
   - *Workflow permissions* → **Read and write permissions**
4. **Actions** → uruchom ręcznie:
   - *Knowledge (daily, unlimited)* → **Run workflow**
   - *Daily Report (20:00 Warsaw)* → **Run workflow**
   - *Hourly Report (repo-only)* → **Run workflow**
   - *Weekly Email Summary (Sunday 20:05 Warsaw)* → **Run workflow**

### E‑mail tygodniowy (sekrety SMTP)
Settings → Secrets → Actions → dodaj:
- `SMTP_HOST` (np. `smtp.wp.pl`)
- `SMTP_PORT` (`587`)
- `SMTP_USER` (login e‑mail)
- `SMTP_PASS` (hasło aplikacji)
- `MAIL_FROM` (adres nadawcy)
- `MAIL_TO` (adres odbiorcy)

## Szablony projektowe
W katalogu `projects/_wspolne_szablony/` znajdziesz gotowce:
- **proposal_template.md** — pełny szablon projektu (executive summary, KPI, budżety, pakiety sponsorskie, ewaluacja)
- **sponsor_pack_template.md** — pakiet sponsorski (Mecenas/Partner/WSparcie; korzyści medialne, ROI)
- **press_release_template.md** — komunikat prasowy
- **social_calendar_template.md** — siatka publikacji FB/IG/TikTok
- **event_checklist.md** — lista kontrolna wydarzeń
- **rodo_consent_template.md** — zgody i RODO
- **budget_template.xlsx (opis)** — arkusz budżetowy (opis kolumn)

> Pamiętaj: **logo i dane stowarzyszenia na każdej stronie PDF**. Font: **DejaVu Serif** (PL znaki).


## Nowe funkcje
- Generator **PDF premium** (reportlab) — workflow `Generate Premium PDF`.
- **Tygodniowe archiwum ZIP** katalogu `reports/` — workflow `Weekly Reports Archive`.
