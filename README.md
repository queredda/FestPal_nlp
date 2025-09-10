# FestPal Bot 🎵

Chatbot cerdas untuk festival musik dengan dukungan CLI dan Discord. Bot ini menyediakan informasi tiket, jadwal artis, lokasi venue, dan customer service untuk FestPal Festival.

## Features

- **Informasi Tiket**: Harga, kategori, dan cara pembelian
- **Jadwal & Lineup**: Daftar artis dan jam penampilan
- **Lokasi & Parkir**: Info venue dan fasilitas parkir
- **Customer Service**: Bantuan refund, QR code, dan masalah tiket
- **Multi-platform**: CLI dan Discord bot
- **Natural Language**: Bahasa Indonesia dan Inggris

## Setup & Installation

```bash
# Clone repository
git clone <repository-url>
cd bot

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

## Konfigurasi Token/Kredensial (Optional untuk Discord)

```bash
# Copy environment template
cp env.example .env

# Edit .env file - tambahkan Discord bot token
DISCORD_TOKEN=token_di_sini
```

> **Note**: Dapatkan Discord token dari [Discord Developer Portal](https://discord.com/developers/applications)

## Running

### CLI Mode

```bash
python main.py --cli
```

### Discord Bot

```bash
python main.py
```

### Quick Test

```bash
python -c "from bot import ChatBot; bot = ChatBot(); print(bot.reply('halo'))"
```

## Demo

### CLI Demo

```bash
$ python main.py --cli
🎵 FestPal Bot CLI - Ketik 'quit' untuk keluar

You: halo
Bot: Halo! Saya FestPal — mau tanya soal tiket, jadwal, lokasi, atau bantuan CS?

You: berapa harga tiket?
Bot: Harga tiket:
• Festival A (Standing): Rp350.000
• Festival B (Standing): Rp250.000
• VIP (Seating): Rp500.000
Beli lewat website resmi atau partner resmi.

You: siapa guest star nya?
Bot: Berikut lineup singkat:
Day 1: Tulus (18:00) • Sabrina Carpenter (20:00) • Taylor Swift (22:00)
Day 2: Adele (17:30) • Justin Bieber (19:30) • Ariana Grande (21:30)

You: refund order #ORDER123
Bot: Permintaan refund tercatat untuk pesanan 123. Silakan hubungi support resmi dan sertakan bukti pembayaran serta nomor pesanan tersebut.

You: quit
Bot: Sampai jumpa!
```

### Discord Demo

![Discord Bot Demo](docs/discord-demo.gif)

Bot merespons dengan format yang sama di Discord server.

## Tests

Project memiliki **29 test cases** yang mencakup semua fitur utama:

```bash
# Jalankan tests
pytest tests/ -v
# Output: ========================================== 29 passed in 0.05s ==========================================
```

## Project Structure

```
bot/
├── main.py              # Entry point (CLI & Discord)
├── bot.py               # Core chatbot logic
├── requirements.txt     # Dependencies
├── env.example         # Environment template
├── tests/              # Unit tests (29 test cases)
│   └── test_bot.py
└── logs/               # Application logs
    └── bot.log
```

## Bot Capabilities

- **Tiket & Pembayaran**: Harga, kategori, cara beli, metode pembayaran, promo
- **Event & Lineup**: Jadwal lengkap Day 1-2, guest stars, penampil hari ini
- **Lokasi & Fasilitas**: Venue GOR UNY, parkir umum/VIP/motor, transport
- **Customer Service**: Refund, QR/e-ticket issues, contact CS, resale warning
- **Advanced**: Natural language ID/EN, reflection mapping, order tracking

---
