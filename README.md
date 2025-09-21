# Projekty PPB – automatyczne raporty (kompletna paczka)

## 1) Wymagane sekrety (Repo → Settings → Secrets and variables → Actions)
- `GH_TOKEN` – Personal Access Token (classic) z zakresami: `repo`, `workflow`
- (opcjonalnie do e‑maili) `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `MAIL_FROM`, `MAIL_TO`

## 2) Co robi paczka
- Godzinowo zapisuje raport: `reports/hourly/PPB_hourly_YYYY-MM-DD_HH.md`
- Codziennie 20:00 (Europe/Warsaw) – tworzy `reports/daily/...md` i wyśle e‑mail (jeśli sekrety SMTP są ustawione)
- W niedzielę 20:00 – tworzy `reports/weekly/...md` i wyśle e‑mail

## 3) Instalacja (krok po kroku)
1. W repo **usuń stare pliki** (żeby uniknąć konfliktów).
2. **Wgraj zawartość** tego ZIP‑a do głównego katalogu repo (nie wrzucaj samego zipa).
3. Dodaj sekret **GH_TOKEN** (token klasyczny z `repo`, `workflow`).
4. (opcjonalnie) Dodaj sekrety SMTP dla wysyłki maili.
5. Wejdź w **Actions** → uruchom ręcznie *Hourly Reports* (Run workflow) – sprawdzisz działanie od ręki.

## 4) Harmonogram (CRON runnera działa w UTC)
- Hourly: `0 * * * *` (co godzinę)
- Daily email: `0 18 * * *` (czyli 20:00 Europe/Warsaw)
- Weekly email: `0 18 * * 0` (niedziela 20:00 Europe/Warsaw)
