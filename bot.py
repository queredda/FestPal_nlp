import re
from typing import Dict, Optional, List, Tuple

FESTIVAL_INFO = {
    "name": "FestPal",
    "location": "GOR UNY, Yogyakarta",
    "parking": {
        "general": "Parkir umum di sisi barat lapangan (terbatas). Tarif sesuai petunjuk di lokasi.",
        "vip": "Area VIP parking (reservasi/booking diperlukan untuk akses VIP).",
        "motor": "Parkir motor tersedia dekat pintu masuk timur.",
        "tips": "Disarankan menggunakan transportasi online atau datang lebih awal untuk menghindari antrian parkir."
    },
    "lineup": {
        "Day 1": [("Tulus", "18:00"), ("Sabrina Carpenter", "20:00"), ("Taylor Swift", "22:00")],
        "Day 2": [("Adele", "17:30"), ("Justin Bieber", "19:30"), ("Ariana Grande", "21:30")],
    },
    "support_contact": "support@festpal.com / +62-812-3456-7890",
}

# Reflection map
_REFLECTION_MAP = {
    "saya": "kamu",
    "aku": "kamu",
    "gue": "kamu",
    "gua": "kamu",
    "kamu": "saya",
    "anda": "saya",
    "kami": "kalian",
    "kita": "kalian",
    "kalian": "kami",
    "punyaku": "punyamu",
    "punyamu": "punyaku",
    "my": "your",
    "your": "my",
    "me": "you",
    "you": "me",
    "u": "saya",
    "ur": "mu",
}


def reflect(text: str) -> str:
    if not text:
        return text
    # split into tokens keeping punctuation
    tokens = re.findall(r"\w+|[^\w\s]", text.lower(), flags=re.UNICODE)
    reflected = [_REFLECTION_MAP.get(t, t) for t in tokens]
    return " ".join(reflected)


def format_lineup(lineup: Dict[str, List[Tuple[str, str]]]) -> str:
    """Return pretty lineup string from FESTIVAL_INFO['lineup']"""
    lines = []
    for day, acts in lineup.items():
        lines.append(f"{day}:")
        for artist, time in acts:
            lines.append(f"  • {artist} — {time}")
    return "\n".join(lines)


class ChatBot:
    """
    FestPal chatbot core — ordered regex rules.
    - First matching rule wins.
    - If response contains {0}, {1}, they are filled with reflected capture groups.
    """

    def __init__(self, bot_name: str = "FestPal", chatbot_response: Optional[Dict[str, str]] = None) -> None:
        if chatbot_response is None:
            # Ordered rules: most specific first to avoid accidental matches
            chatbot_response = {
                r"\b(?:who(?:\s*(?:are|r))?\s*(?:you|u|ur)|siapa\s+(?:kamu|namamu))\b": (
                    f"Saya adalah {FESTIVAL_INFO['name']} Bot — FestPal. Saya bantu informasi acara dan masalah tiket."
                ),
                r"\bwho\s+am\s+i\b|\bsiapa\s+(?:aku|saya)\b": (
                    "Saya tidak punya akses ke data akunmu di sini. Untuk info akun, periksa profil aplikasi atau hubungi CS."
                ),
                r"\b(?:hi|hello|hey|hai|hallo|hei|halo|hola)\b": "Halo! Saya FestPal — mau tanya soal tiket, jadwal, lokasi, atau bantuan CS?",

                # ===== HELP / capabilities (cover variations) =====
                r"\b(?:help|bantuan|menu|perintah|info|panduan|apa\s+yang\s+bisa\s+kamu(?:\s+lakuin|lakukan)?)\b": (
                    "Saya bisa membantu:\n"
                    "• Info tiket & harga (contoh: 'berapa harga tiket')\n"
                    "• Cara beli & metode pembayaran (contoh: 'bisa gopay ga')\n"
                    "• Refund / masalah tiket (contoh: 'i want refund' atau 'refund #ORDER123')\n"
                    "• QR / e-ticket (contoh: 'QR tidak bisa discan')\n"
                    "• Jadwal / lineup / siapa guest star (contoh: 'siapa guest star nya' atau 'lineup')\n"
                    "• Parkir & transport (contoh: 'parkir mobil dimana?')\n"
                    "• Contact CS (ketik 'contact')"
                ),

                # ===== Refund specific with order code capture =====
                r"(?:refund|pengembalian).*(?:order|nomor|no\.?|kode|pesanan)\s*[:#]?\s*([A-Za-z0-9-]{3,})": (
                    "Permintaan refund tercatat untuk pesanan {0}. Silakan hubungi support resmi dan sertakan bukti pembayaran serta nomor pesanan tersebut."
                ),
                r"\b(?:refund|pengembalian uang|minta refund|pengembalian)\b": (
                    "Kebijakan refund tergantung jenis tiket. Biasanya refund hanya untuk pembatalan resmi oleh panitia. "
                    "Sebutkan nomor pesananmu supaya saya bantu cek atau hubungi CS."
                ),

                # ===== Resale / transfer =====
                r"\b(?:resale|re[- ]?sale|jual\s+ulang|transfer\s+tiket|transfer\s+ticket|jual\s+tiket)\b": (
                    "⚠️ Penjualan ulang / transfer tiket dari sumber tidak resmi berisiko. Tiket yang dibeli dari sumber tidak resmi dapat diblokir. "
                    "Beli lewat kanal resmi untuk keamanan."
                ),

                # ===== Ticket not received / delivery issues =====
                r"(?:tidak|gak|ga|belum)\s*(?:mendapat|menerima|terima|terkirim).*(?:tiket|e-?ticket|eticket|email|invoice)": (
                    "Jika belum menerima e-ticket, periksa folder spam/promo di email. Jika tetap tidak ada, hubungi CS dengan bukti pembayaran (tanggal & nominal)."
                ),
                r"(?:haven'?t|did not|not)\s+receive.*ticket|no.*ticket.*received": (
                    "If you haven't received your e-ticket, check spam and contact official support with proof of purchase."
                ),

                # ===== QR / e-ticket issues =====
                r"\b(?:qr|qr\s*code|scan|scan\s*qr|e-?ticket|eticket|barcode)\b.*(?:error|tidak|gak|ga|fail|cannot|can't|not\s+read|buram|blur)": (
                    "Jika QR e-ticket tidak terbaca, kunjungi loket box office atau Pos Informasi dengan bukti pembayaran untuk verifikasi manual."
                ),
                r"\b(?:qr|e-?ticket|eticket|barcode)\b": (
                    "E-ticket dikirim ke email yang terdaftar berupa QR code. Pastikan QR jelas & siap saat antrean."
                ),

                # ===== Payment method specific (GoPay, OVO, DANA, credit card) =====
                r"\b(?:bisa|boleh|accept|support|terima|menerima|can i|do you)\b.*\b(gopay|ovo|dana|shopeepay|shopee pay)\b": (
                    "Pembayaran via e-wallet (GoPay/OVO/DANA) dapat tersedia di payment gateway website resmi. "
                    "Untuk konfirmasi, lanjutkan ke halaman checkout kanal pembelian yang kamu gunakan."
                ),
                r"\b(gopay|ovo|dana|shopeepay|bank transfer|bank|kartu kredit|credit card|debit)\b": (
                    "Metode pembayaran umum: kartu kredit/debit, transfer bank, dan e-wallet (gopay/ovo/dana/shopeepay). Periksa halaman checkout untuk daftar metode."
                ),
                r"\b(metode|method|payment|method|metode|pembayaran)\b":(
                    "Metode pembayaran umum: kartu kredit/debit, transfer bank, dan e-wallet (gopay/ovo/dana/shopeepay). Periksa halaman checkout untuk daftar metode."),

                # ===== Price & ticket categories =====
                r"\b(?:berapa\s+harga\s+tiket|harga\s+tiket|ticket\s+price|berapa\s+harga)\b": (
                    "Harga tiket:\n"
                    "• Festival A (Standing): Rp350.000\n"
                    "• Festival B (Standing): Rp250.000\n"
                    "• VIP (Seating): Rp500.000\nBeli lewat website resmi atau partner resmi."
                ),
                r"\b(kategori|jenis)\s*tiket\b": "Kategori tiket: Festival A (Standing), Festival B (Standing), VIP (Seating).",

                # ===== How to buy =====
                r"(?:cara|how to|how do i).*beli.*tiket|cara membeli tiket|how to purchase ticket": (
                    "Cara beli tiket:\n1) Kunjungi website resmi\n2) Pilih kategori & jumlah\n3) Isi data & pilih metode pembayaran\n4) Setelah bayar, cek email untuk e-ticket (QR)."
                ),

                # ===== Promo / voucher =====
                r"\b(voucher|promo|diskon|kode promo|kode diskon|coupon)\b": (
                    "Info promo/voucher:\n• Cek syarat & ketentuan di halaman promo resmi.\n• Masukkan kode promo pada halaman checkout.\n• Jika kode tidak berlaku, pastikan masih masa berlaku & cocok syarat."
                ),

                # ===== Lineup / guest star (specific) =====
                r"\b(?:siapa\s+guest\s*star(?:\s*nya)?|siapa\s+bintang\s*tamu(?:\s*nya)?)\b": (
                    "Berikut lineup singkat:\n" + format_lineup(FESTIVAL_INFO["lineup"])
                    + "\n\nKetik 'lineup' atau 'siapa tampil hari ini' untuk detail hari tertentu."
                ),
                r"\b(line[\s-]?up|lineup|daftar penampil|siapa yang tampil)\b": (
                    "Lineup acara:\n" + format_lineup(FESTIVAL_INFO["lineup"])
                ),
                r"\bsiapa\s+tampil\s+hari\s+ini\b": (
                    # assume Day 1 if user asks without date 
                    "Penampil hari ini (Day 1):\n" + "\n".join([f"• {a} — {t}" for a, t in FESTIVAL_INFO["lineup"].get("Day 1", [])])
                ),

                # ===== Stage / set times capture =====
                r"(?:jam|pukul)\s+([0-2]?[0-9]:[0-5][0-9])\b": "Jadwal jam {0}. Pastikan cek lineup untuk jam tampil artis terkait.",

                # ===== Location & parking (parking rules before general location) =====
                r"\b(parkir|parking|parkir\s+mobil|parkir\s+motor|parkir\s+dimana|parkir\s+di\s+mana)\b": (
                    f"Info parkir:\n• Umum: {FESTIVAL_INFO['parking']['general']}\n"
                    f"• Motor: {FESTIVAL_INFO['parking']['motor']}\n"
                    f"• VIP: {FESTIVAL_INFO['parking']['vip']}\n• Tips: {FESTIVAL_INFO['parking']['tips']}"
                ),
                r"\b(lokasi|venue|alamat|dimana|di\s+mana|where)\b": f"📍 Lokasi: {FESTIVAL_INFO['location']}. Cek peta & denah di website resmi.",

                # ===== Rules & prohibited items =====
                r"\b(aturan|peraturan|dilarang|larangan|rules|policy)\b": (
                    "Aturan singkat:\n• Bawa identitas & e-ticket (QR)\n• Dilarang membawa senjata, obat terlarang, kembang api, alkohol\n• Tidak dianjurkan membawa tripod/payung panjang"
                ),

                # ===== Contact / CS =====
                r"\b(contact|kontak|customer\s*service|cs|support|hotline|hubungi)\b": (
                    f"Hubungi Customer Service: {FESTIVAL_INFO['support_contact']}\n"
                ),

                # ===== Merchandise / merch =====
                r"\b(merch|merchandise|kaos|t-shirt|booth|store)\b": "Merch resmi tersedia di booth merchandise di venue; pembayaran bisa tunai/non-tunai sesuai ketentuan booth.",

                # ===== Emergency / medical =====
                r"\b(darurat|medis|medical|paramedis|ambulans|dokter|emergency)\b": "Jika darurat medis, segera hubungi petugas terdekat atau pos medis di venue.",

                # ===== Lost & found =====
                r"\b(hilang|lost and found|lost|barang hilang)\b": "Laporkan barang hilang ke Pos Informasi / Lost & Found di venue; bawa bukti kepemilikan bila memungkinkan. Hubungi CS dengan bukti kehilangan.",

                # ===== Thank you / goodbye =====
                r"\b(terima\s?kasi?h?|thanks|thank you)\b": "Sama-sama! Ada lagi yang bisa saya bantu?",
                r"\b(bye|goodbye|selamat\s+tinggal|sampai\s+jumpa|oke|baiklah)\b": "Sampai jumpa di festival! 🎶",

                # ===== Generic fallback (last) =====
                r"\b(tiket|harga|jadwal|lokasi|aturan|parkir|qr|refund|resale|merch|vip|lineup|help)\b": (
                    "Kamu bisa tanya: harga tiket, cara beli, refund, QR/e-ticket, jadwal/lineup, lokasi/parkir, atau ketik 'contact' untuk CS."
                ),
            }

        # compile patterns (preserve insertion order)
        self._rules = [(re.compile(pat, flags=re.IGNORECASE), resp) for pat, resp in chatbot_response.items()]
        self.bot_name = bot_name
        self.intro = f"Hai, saya {self.bot_name} — bot panduan {FESTIVAL_INFO['name']}. Tanya saja: harga, jadwal, lokasi, refund, atau ketik 'help'."
        self.default_response = (
            "Maaf, saya tidak mengerti. Coba tanyakan dengan kata kunci (contoh: 'harga tiket', 'jadwal', 'bisa gopay ga', 'refund'), "
            "atau ketik 'help/bantuan' untuk daftar bantuan."
        )

    def reply(self, user_input: str) -> str:
        if not user_input:
            return self.intro

        text = user_input.strip()
        for pattern, response in self._rules:
            m = pattern.search(text)
            if not m:
                continue

            # collect groups safely and reflect them
            try:
                groups: List[str] = [reflect(g or "") for g in m.groups()] if m.groups() else []
            except Exception:
                groups = []

            # format only when placeholders present and groups available
            if ("{" in response) and groups:
                try:
                    return response.format(*groups)
                except Exception:
                    return response

            return response

        return self.default_response
