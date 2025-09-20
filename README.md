# PPB GitHub Actions Runner — auto-raport nauki (gotowiec)

Ten pakiet uruchamia **automatyczne raportowanie nauki** w chmurze (GitHub Actions).
Co godzinę powstaje `reports/latest_report.md` z panelem postępu, a (opcjonalnie) leci powiadomienie na Telegram.

## Szybki start (5 kroków)
1. **Utwórz repo** na GitHub (np. `ppb-auto-nauka`) i **wrzuć** całą zawartość tego folderu.
2. W repo przejdź do **Settings → Secrets and variables → Actions → New repository secret** i dodaj (opcjonalnie do powiadomień):
   - `TELEGRAM_TOKEN` — token od @BotFather
   - `TELEGRAM_CHAT_ID` — ID Twojej rozmowy z botem (lub grupy)
3. (Opcjonalnie) skopiuj `config.sample.json` → `config.json` i zmień:
   - `"timezone": "Europe/Warsaw"` (już ustawione),
   - dodaj/usuń moduły w `"modules"`,
   - `"telegram.enabled": true` jeśli chcesz powiadomienia.
4. Przejdź do **Actions** w repo i włącz workflow (jeśli GitHub pyta o zgodę). Możesz też odpalić ręcznie — **Run workflow**.
5. Poczekaj chwilę. W katalogu `reports/` pojawi się `latest_report.md`. Jeśli włączyłeś Telegram — przyjdzie krótkie powiadomienie.

## Gdzie edytuję treść nauki?
- Dodawaj pliki `.md` lub `.txt` do folderu `knowledge/` — pierwszy wiersz będzie nagłówkiem w raporcie.
- Workflow działa **co godzinę** (zmień w `.github/workflows/auto_report.yml` — CRON).

## Jak udostępnić raport do dalszego rozwijania wiedzy?
- Skopiuj zawartość `reports/latest_report.md` i wklej w rozmowie, albo
- Pobierz plik i prześlij w czacie — rozwinę go w **Strumieniu Wiedzy**.

## Dostosowanie CRON
W pliku `.github/workflows/auto_report.yml`:
```
schedule:
  - cron: '0 * * * *'   # co godzinę (UTC)
```
Przykłady:
- co 15 min: `*/15 * * * *`
- codziennie 19:00 UTC: `0 19 * * *` (pamiętaj o różnicy czasu z Europe/Warsaw).

## Bezpieczeństwo
- Tokeny trzymaj tylko w **GitHub Secrets**.
- Nie commituj `config.json` z danymi wrażliwymi.

## Co generuje raport?
- Paski postępu (ASCII), % i ETA (symulowane / do podpięcia pod Twoje metryki).
- Lista ostatnich plików z `knowledge/`.

Masz pytania? Wrzucasz raport — ja rozbudowuję wiedzę i moduły dalej.