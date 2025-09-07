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

### Install Dependencies

```bash
# Clone repository
git clone <repository-url>
cd bot

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows

# Install packages
pip install -r requirements.txt
```

### Konfigurasi Token/Kredensial (Optional untuk Discord)

```bash
# Copy environment template
cp .env.example .env

# Edit .env untuk Discord integration
DISCORD_TOKEN=your_discord_bot_token_here
```

## Running

### CLI Mode

```bash
# Jalankan di terminal
python main.py --cli

# Quick test
python -c "from bot import ChatBot; bot = ChatBot(); print(bot.reply('halo'))"
```

### Discord Integration

```bash
# Jalankan Discord bot (memerlukan DISCORD_TOKEN di .env)
python main.py

# Bot akan online di Discord server
```

## Demo

### CLI Interface

```bash
$ python main.py --cli
🎵 FestPal Bot CLI - Ketik 'quit' untuk keluar

You: halo
Bot: Halo! Saya FestPal — mau tanya soal tiket, jadwal, lokasi, atau bantuan CS?

You: berapa harga tiket?
Bot: 🎟️ Harga tiket:
• Festival A (Standing): Rp350.000
• Festival B (Standing): Rp250.000
• VIP (Seating): Rp500.000
Beli lewat website resmi atau partner resmi.

You: siapa guest star nya?
Bot: Berikut lineup singkat:
Day 1:
  • Tulus — 18:00
  • Sabrina Carpenter — 20:00
  • Taylor Swift — 22:00
Day 2:
  • Adele — 17:30
  • Justin Bieber — 19:30
  • Ariana Grande — 21:30

Ketik 'lineup' atau 'siapa tampil hari ini' untuk detail hari tertentu.

You: refund order #ORDER123
Bot: Permintaan refund tercatat untuk pesanan 123. Silakan hubungi support resmi dan sertakan bukti pembayaran serta nomor pesanan tersebut.

You: quit
Bot: Sampai jumpa! 
```

### Discord Integration

![Discord Bot Demo](docs/discord-demo.gif)

_Demo: Bot merespons pertanyaan di Discord dengan format yang sama seperti CLI_

**Contoh percakapan Discord:**

```
User: @FestPal halo
Bot: Halo! Saya FestPal — mau tanya soal tiket, jadwal, lokasi, atau bantuan CS?

User: bisa gopay ga?
Bot: Pembayaran via e-wallet (GoPay/OVO/DANA) dapat tersedia di payment gateway website resmi.
Untuk konfirmasi, lanjutkan ke halaman checkout kanal pembelian yang kamu gunakan.

User: refund order #ORDER123
Bot: Permintaan refund tercatat untuk pesanan 123. Silakan hubungi support resmi dan sertakan
bukti pembayaran serta nomor pesanan tersebut.

User: help
Bot: Saya bisa membantu:
• Info tiket & harga (contoh: 'berapa harga tiket')
• Cara beli & metode pembayaran (contoh: 'bisa gopay ga')
• Refund / masalah tiket (contoh: 'i want refund' atau 'refund #ORDER123')
• QR / e-ticket (contoh: 'QR tidak bisa discan')
• Jadwal / lineup / siapa guest star (contoh: 'siapa guest star nya' atau 'lineup')
• Parkir & transport (contoh: 'parkir mobil dimana?')
• Contact CS (ketik 'contact')
```

## Tests

Project memiliki **29 test cases** yang mencakup semua fitur utama:

```bash
# Jalankan tests (dalam virtual environment)
source venv/bin/activate && pytest tests/ -v

# Output:
# ========================================== 29 passed in 0.05s ==========================================
```

### Test Cases:

#### Core Bot Functionality (27 tests):

1. **Greeting variations** - respons salam dalam berbagai bahasa (halo, hi, hello, hey, dll)
2. **Identity questions** - bot mengidentifikasi dirinya dengan benar (who are you, siapa kamu)
3. **User identity questions** - penanganan pertanyaan identitas user (who am i, siapa aku)
4. **Ticket pricing** - informasi harga tiket komprehensif (Festival A/B, VIP)
5. **Lineup and schedule** - jadwal artis dan lineup (Day 1/2, guest stars)
6. **Location and parking** - info lokasi venue dan fasilitas parkir (umum/VIP/motor)
7. **Refund processing** - penanganan refund dengan order code reflection
8. **Payment methods** - metode pembayaran (GoPay, OVO, DANA, kartu kredit)
9. **Help functionality** - menu bantuan dan capabilities lengkap
10. **QR and e-ticket issues** - troubleshooting tiket elektronik dan barcode
11. **Resale transfer warnings** - peringatan penjualan ulang tiket tidak resmi
12. **Ticket not received** - penanganan tiket yang belum diterima via email
13. **How to buy tickets** - panduan cara pembelian tiket
14. **Promo voucher** - informasi kode promo dan diskon
15. **Guest star specific** - query spesifik tentang bintang tamu
16. **Today's performers** - artis yang tampil hari ini
17. **Ticket categories** - kategori dan jenis tiket
18. **Rules and policies** - aturan dan larangan di venue
19. **Contact customer service** - informasi kontak CS lengkap
20. **Merchandise** - informasi booth merchandise
21. **Emergency medical** - bantuan darurat dan medis
22. **Lost and found** - penanganan barang hilang
23. **Thank you goodbye** - respons terima kasih dan perpisahan
24. **Generic fallback keywords** - fallback untuk kata kunci yang dikenali
25. **Default fallback handling** - respons untuk input tidak dikenal

#### Utility Functions (4 tests):

28. **Reflection function** - mapping kata ganti (saya ↔ kamu, my ↔ your)
29. **Lineup formatting** - format tampilan jadwal dengan bullet points
30. **Festival info structure** - validasi kelengkapan data festival
31. **ChatBot initialization** - inisialisasi bot dengan parameter custom

## Project Structure

```
bot/
├── main.py              # Entry point (CLI & Discord)
├── bot.py               # Core chatbot logic
├── requirements.txt     # Dependencies
├── .env.example        # Environment template
├── tests/              # Unit tests (31 test cases)
│   ├── __init__.py
│   └── test_bot.py
├── logs/               # Application logs
│   └── bot.log         # Example log entries
└── docs/               # Documentation
    ├── README.md       # Demo creation guide
    └── discord-demo.gif # Discord bot demo
```

## Logs

Bot menggunakan structured logging:

```bash
# View real-time logs
tail -f logs/bot.log

# Sample log entries:
2025-09-07 15:50:08,539 - INFO - FestPal Bot starting - Mode: CLI
2025-09-07 15:50:08,542 - INFO - CLI user query: 'halo'
2025-09-07 15:50:08,542 - INFO - CLI bot response provided
2025-09-07 15:50:08,542 - INFO - CLI user query: 'berapa harga tiket'
2025-09-07 15:50:08,542 - INFO - CLI session ended by user
```



## Capabilities

Bot dapat menjawab pertanyaan tentang:

### Tiket & Pembayaran

- **Harga tiket**: Festival A (Rp350.000), Festival B (Rp250.000), VIP (Rp500.000)
- **Kategori tiket**: Standing vs Seating, regular vs VIP
- **Cara beli**: panduan step-by-step pembelian
- **Metode pembayaran**: GoPay, OVO, DANA, kartu kredit/debit, transfer bank
- **Promo & voucher**: kode diskon dan syarat ketentuan

### Event & Lineup

- **Lineup lengkap**: Day 1 (Tulus, Sabrina Carpenter, Taylor Swift), Day 2 (Adele, Justin Bieber, Ariana Grande)
- **Jadwal tampil**: jam penampilan setiap artis
- **Guest star**: informasi bintang tamu utama
- **Penampil hari ini**: query spesifik untuk hari tertentu

### Lokasi & Fasilitas

- **Venue**: GOR UNY, Yogyakarta dengan peta dan denah
- **Parkir umum**: sisi barat lapangan (terbatas)
- **Parkir VIP**: area khusus dengan reservasi
- **Parkir motor**: dekat pintu masuk timur
- **Tips transport**: rekomendasi transportasi online

### Support & Customer Service

- **Refund**: kebijakan pengembalian dengan order code tracking
- **QR/e-ticket issues**: troubleshooting barcode dan scan problems
- **Tiket tidak diterima**: penanganan email delivery issues
- **Contact CS**: support@festpal.com / +62-812-3456-7890
- **Resale warning**: peringatan tiket tidak resmi

### Informasi Tambahan

- **Aturan venue**: yang diperbolehkan dan dilarang
- **Merchandise**: booth resmi di venue
- **Emergency**: bantuan darurat dan medis
- **Lost & found**: penanganan barang hilang
- **Help menu**: daftar lengkap capabilities

### Advanced Features

- **Natural Language**: bahasa Indonesia dan Inggris
- **Reflection mapping**: otomatis mengubah kata ganti (saya↔kamu)
- **Order code processing**: ekstraksi dan tracking nomor pesanan
- **Context awareness**: respons yang relevan dengan konteks
- **Fallback handling**: respons helpful untuk query tidak dikenal

---
