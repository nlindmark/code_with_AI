# Code with AI - Tävlingsplattform

En kodningstävling med 5 progressivt svårare nivåer. Varje nivå har en `solution.py` och `verify.py` som mäter exekveringstid och skickar resultat till en Flask leaderboard-server.

## 🚀 Snabbstart

### Setup

Välj en av följande metoder:

#### Metod 1: Conda (rekommenderas)

1. Skapa en conda-miljö:
```bash
conda create -n code-with-ai python=3.9
conda activate code-with-ai
```

2. Installera beroenden:
```bash
pip install -r requirements.txt
```

#### Metod 2: venv (alternativ)

1. Skapa en virtuell miljö och aktivera den:
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

2. Installera beroenden:
```bash
pip install -r requirements.txt
```

3. Konfigurera miljövariabler (kopiera `.env.example` till `.env` och redigera):
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Redigera `.env` och sätt:
- `AI_CODE_USER`: Ditt användarnamn
- `UPDATE_URL`: URL till servern (standard: `http://127.0.0.1:5000/update`)
- `API_KEY`: API-nyckel för säkerhet (samma som server använder)

### Starta servern

```bash
python main.py
```

Servern startar på http://127.0.0.1:5000/

Öppna webbläsaren och gå till http://127.0.0.1:5000/ för att se leaderboard.

## 🌐 Multi-Machine Setup

För att köra tävlingen från flera maskiner (en server + flera klientmaskiner):

### Server-maskin

1. **Starta servern**:
   ```bash
   python main.py
   ```

2. **Servern kommer automatiskt att:**
   - Bindas till `0.0.0.0` (tillgänglig från alla nätverksgränssnitt)
   - Visa både lokal och nätverks-IP-adress vid start
   - Visa URL som deltagare ska använda

3. **Exempel på utskrift vid start:**
   ```
   ============================================================
   🚀 Server startar på port 5000
   ============================================================
   📍 Lokal åtkomst:
      http://127.0.0.1:5000/
      http://localhost:5000/

   🌐 Nätverksåtkomst:
      http://192.168.1.100:5000/

   💡 Dela denna URL med deltagare:
      http://192.168.1.100:5000/

   📊 Leaderboard: http://127.0.0.1:5000/leaderboard
   ============================================================
   ```

4. **Konfigurera brandvägg (om nödvändigt):**
   - Se till att port 5000 (eller den port du använder) är öppen i brandväggen
   - Linux: `sudo ufw allow 5000` eller konfigurera iptables
   - Windows: Öppna port i Windows Firewall-inställningar
   - macOS: Konfigurera i Systeminställningar → Säkerhet

5. **Anpassa host/port (valfritt):**
   - Sätt miljövariabel `FLASK_HOST` för att ändra host (standard: `0.0.0.0`)
   - Sätt miljövariabel `FLASK_PORT` för att ändra port (standard: `5000`)
   ```bash
   export FLASK_HOST=0.0.0.0
   export FLASK_PORT=5000
   ```

### Klientmaskiner

**Ingen konfiguration behövs!** Deltagare behöver bara:

1. **Öppna webbläsare** på klientmaskinen
2. **Gå till serverns URL** (t.ex. `http://192.168.1.100:5000/`)
3. **Logga in** med användarnamn och börja tävla

Serverns URL visas tydligt när servern startar - dela denna URL med alla deltagare.

### Felsökning

- **Klienter kan inte ansluta:**
  - Kontrollera att servern körs och är bunden till `0.0.0.0`
  - Kontrollera att brandväggen tillåter trafik på port 5000
  - Verifiera att båda maskinerna är på samma nätverk
  - Testa att pinga serverns IP från klientmaskinen

- **Servern visar inte nätverks-IP:**
  - Kontrollera nätverksinställningar på servern
  - Du kan manuellt hitta IP-adressen med:
    - Linux/Mac: `hostname -I` eller `ifconfig`
    - Windows: `ipconfig`

- **Port redan i bruk:**
  - Ändra port med miljövariabel: `export FLASK_PORT=5001`
  - Eller stoppa den process som använder porten

### Kör en nivå

För att testa och skicka in resultat för en nivå:

```bash
python levels/level1/verify.py
python levels/level2/verify.py
# ... osv
```

Varje `verify.py` kommer:
1. Köra testfall för att verifiera din lösning
2. Mäta exekveringstiden
3. Skicka resultatet till servern

## 📁 Projektstruktur

```
code-with-ai/
├── main.py                  # Flask-server (leaderboard API)
├── db.py                    # Databaslager (SQLite3)
├── common.py                # Gemensamma verktyg (timing + submission)
├── static/
│   └── index.html          # Leaderboard UI
├── levels/
│   ├── level1/
│   │   ├── solution.py     # Din lösning här
│   │   └── verify.py       # Verifieringsskript
│   ├── level2/
│   │   ├── input.txt
│   │   ├── solution.py
│   │   └── verify.py
│   ├── level3/
│   │   ├── data.csv
│   │   ├── solution.py
│   │   └── verify.py
│   ├── level4/
│   │   ├── secret.txt
│   │   ├── solution.py
│   │   └── verify.py
│   └── level5/
│       ├── api_stub.json
│       ├── template.md
│       ├── solution.py
│       └── verify.py
├── requirements.txt
└── README.md
```

## 🎯 Nivåer

### Nivå 1: Vokaler
Räkna vokaler (svenska + engelska: a, e, i, o, u, y, å, ä, ö) i en text.

### Nivå 2: Nummersummering
Läs en fil med blandad text och summera alla heltal (positiva och negativa).

### Nivå 3: CSV-aggregation
Läs en CSV-fil med kategori och värde, beräkna genomsnitt per kategori.

### Nivå 4: Caesar-chiffer
Dekryptera en text som är krypterad med Caesar-chiffer (shift 7).

### Nivå 5: JSON + Mall
Läs JSON-data, beräkna genomsnitt och hitta topprestation. Ersätt platshållare i en markdown-mall.

## 🔧 API Endpoints

### GET /
Serverar leaderboard-HTML-sidan.

### GET /leaderboard
Returnerar leaderboard som JSON:
```json
[
  {
    "user": "användarnamn",
    "max_level": 5,
    "total_ms": 1500,
    "levels": {
      "1": {"ms": 200, "ts": 1234567890},
      "2": {"ms": 300, "ts": 1234567900},
      ...
    }
  },
  ...
]
```

### POST /update
Skickar in resultat:
```json
{
  "user": "användarnamn",
  "level": 1,
  "ms": 200
}
```

Kräver header: `X-API-Key: <din_api_key>`

### GET /reset
Raderar alla resultat. Kräver `X-API-Key` header.

## 📝 Lägga till nya nivåer

1. Skapa en ny mapp under `levels/` (t.ex. `level6/`)
2. Kopiera strukturen från en befintlig nivå:
   - `solution.py` - implementera lösningsfunktionen
   - `verify.py` - verifiera och skicka resultat
   - Eventuella datafiler (txt, csv, json, etc.)
3. I `verify.py`:
   - Importera `time_exec` och `submit_result` från `common`
   - Läs miljövariabler: `AI_CODE_USER`, `UPDATE_URL`, `API_KEY`
   - Kör testfall och verifiera korrekthet
   - Mät tid med `time_exec()`
   - Skicka resultat med `submit_result(user, level, ms, update_url, api_key)`

## 🔐 Miljövariabler

- `AI_CODE_USER`: Ditt tävlingsanvändarnamn
- `UPDATE_URL`: URL till serverns `/update` endpoint
- `API_KEY`: API-nyckel för säkerhet (måste matcha serverns)

## 💡 Tips

- Servern sparar bästa tid per nivå - du kan köra flera gånger för att förbättra!
- Leaderboard sorteras efter: högsta nivå → lägsta totaltid → tidigaste tidsstämpel
- Om servern inte är tillgänglig kommer `verify.py` att fortsätta utan att krascha (endast varning)

## 🐛 Felsökning

- **Servern startar inte**: Kontrollera att port 5000 är ledig
- **Kan inte skicka resultat**: Kontrollera att servern körs och att `UPDATE_URL` är korrekt
- **Importfel**: Se till att du kör `verify.py` från rätt directory eller att `common.py` finns i root

