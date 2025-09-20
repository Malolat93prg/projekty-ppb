# 📊 PPB Auto-Learning & Hourly Reporting

System automatyzuje **ciągłą naukę** i **raportowanie postępu** dla Stowarzyszenia Polska Potęga Bezpieczeństwa (PPB).  
Co godzinę generuje raport `reports/latest_report.md` oraz wysyła go e-mailem.

---

## 🚀 Co robi ten projekt
- ⏱️ **CRON co godzinę** (GitHub Actions) uruchamia generowanie raportu.
- 🧠 Zbiera skróty z folderu `knowledge/` (pierwsza linia z każdego pliku).
- 📈 Tworzy kompaktowe **paski postępu** z % i **ETA**.
- ✉️ Wysyła raport na e-mail (SMTP).
- 💬 (Opcjonalnie) wysyła powiadomienia na **Telegram**.

---

## 📂 Struktura repo
