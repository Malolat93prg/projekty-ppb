# PPB Auto-Learning Suite (co godzinę, e-mail WP)
Masz dwa tryby: `github_actions_runner/` (chmura) i `local_runner/` (lokalnie). Oba generują raport **co godzinę** i wysyłają e‑mail na `github93@wp.pl` (po ustawieniu SMTP).

## Krok 1 — chmura (zalecane)
- Wgraj zawartość `github_actions_runner/` do pustego repo na GitHub.
- Dodaj sekrety: SMTP_HOST=smtp.wp.pl, SMTP_PORT=587, SMTP_USER=github93@wp.pl, SMTP_PASS, SMTP_FROM=github93@wp.pl, EMAIL_TO=github93@wp.pl.
- Actions → włącz workflow → Run workflow.

## Krok 2 — lokalnie (opcjonalnie)
- Zainstaluj zależności i ustaw `.env` wg `.env.example`.
- Uruchom test → zaplanuj cron/Harmonogram.

Raport znajdziesz w `reports/latest_report.md` (+ e-mail). Treść raportu wklej tu, a ja rozwinę „Strumień wiedzy”.