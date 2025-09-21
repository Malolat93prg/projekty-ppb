# 📊 PPB – Repo ALL-IN-ONE (Automatyczne raporty i projekty)

To repozytorium zostało przygotowane do **automatycznego generowania i archiwizowania raportów** związanych z projektami Stowarzyszenia *Polska Potęga Bezpieczeństwa (PPB)*.  
Całość działa w pełni automatycznie w oparciu o **GitHub Actions**.

---

## 🔧 Struktura repozytorium

```
.
├── .github/
│   └── workflows/         # Pliki workflow GitHub Actions
│       ├── hourly_report.yml
│       ├── daily_email.yml
│       ├── weekly_email.yml
│       ├── weekly_archive.yml
│       ├── monthly_report_pdf.yml
│       └── cleanup.yml
│
├── reports/               # Generowane raporty (godzinowe, dzienne, tygodniowe, miesięczne)
│   ├── daily/
│   ├── weekly/
│   └── monthly/
│
├── tools/                 # Skrypty pomocnicze
│   ├── generate_report.py
│   ├── email_sender.py
│   ├── generate_monthly_pdf.py
│   └── ...
│
├── projects/              # Pliki i dokumenty projektów
├── docs/                  # Dokumentacja
├── assets/                # Logo, grafiki, czcionki
│
├── requirements.txt       # Lista wymaganych bibliotek Pythona
└── README.md              # Ten plik
```

---

## ⏱ Automatyczne zadania

Repozytorium zawiera następujące workflow:

### 1. Raport godzinowy
- Generuje raport co godzinę i zapisuje w repozytorium.
- Zawiera aktualne postępy, dane i pliki projektowe.

### 2. Raport dzienny (20:00)
- Generuje **pełny raport dzienny** z wszystkich projektów.
- Wysyła podsumowanie emailem.

### 3. Raport tygodniowy (niedziela 20:00)
- Generuje podsumowanie całego tygodnia.
- Wysyła na e-mail oraz archiwizuje w `reports/weekly`.

### 4. Raport miesięczny (1 dnia miesiąca, 20:05)
- Generuje **raport w formacie PDF**.
- Raport zawiera podsumowanie wszystkich działań i projektów.

### 5. Cleanup (niedziela 23:00)
- Automatyczne czyszczenie starych artefaktów i logów, aby repo było zawsze schludne.

---

## 📬 Konfiguracja e-mail

Do wysyłania raportów używane są **sekrety GitHub**:

- `SMTP_HOST`  
- `SMTP_PORT`  
- `SMTP_USER`  
- `SMTP_PASS`  
- `MAIL_FROM`  
- `MAIL_TO`

⚠️ Wszystkie muszą być poprawnie ustawione w `Settings → Secrets and variables → Actions`.

---

## 📦 Wymagane biblioteki

Wszystkie wymagane biblioteki są w `requirements.txt`. Instalacja odbywa się automatycznie w GitHub Actions:

```
pip install -r requirements.txt
```

Lista głównych bibliotek:
- `reportlab` – generowanie PDF
- `pytz` – obsługa stref czasowych
- `smtplib` (Python built-in) – wysyłka e-mail
- `os`, `datetime`, `zipfile` – systemowe

---

## 🚀 Jak to działa?

1. Workflow’y uruchamiają się automatycznie zgodnie z harmonogramem (`cron`).
2. Raport jest generowany przez skrypty w katalogu `tools/`.
3. Raporty są commitowane do repozytorium i archiwizowane w folderze `reports/`.
4. Dzienny, tygodniowy i miesięczny raport są wysyłane e-mailowo.

---

## 🗂 Projekty w repozytorium

Repo służy również jako **centralne archiwum projektów PPB**:  
- *Bezpieczny Pieszy*  
- *Zwolnij przy przejściu*  
- *Odblask ratuje życie*  
- + wszystkie przyszłe projekty i materiały (PDF, DOCX, PPTX, grafiki)

Każdy projekt ma własny folder w `projects/`.

---

## ✅ Podsumowanie

- Wszystkie raporty działają automatycznie (**godzinowe, dzienne, tygodniowe, miesięczne**).  
- Repo służy też jako **archiwum projektów i dokumentów**.  
- Skrypty i workflow zostały zoptymalizowane, aby działać **bez konieczności dalszej ręcznej ingerencji**.  
- Każdy tydzień i miesiąc zamykany jest raportem PDF/Markdown + wysyłką mailową.  
