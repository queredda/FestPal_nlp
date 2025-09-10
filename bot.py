import re
from typing import Dict, Optional, List, Tuple, Pattern
from dataclasses import dataclass

@dataclass
class FestivalInfo:
    name: str
    location: str
    parking: Dict[str, str]
    lineup: Dict[str, List[Tuple[str, str]]]
    support_contact: str

FESTIVAL_INFO = FestivalInfo(
    name="FestPal",
    location="GOR UNY, Yogyakarta",
    parking={
        "general": "Parkir umum di sisi barat lapangan (terbatas). Tarif sesuai petunjuk di lokasi.",
        "vip": "Area VIP parking (reservasi/booking diperlukan untuk akses VIP).",
        "motor": "Parkir motor tersedia dekat pintu masuk timur.",
        "tips": "Disarankan menggunakan transportasi online atau datang lebih awal untuk menghindari antrian parkir."
        },
    lineup={
    "Day 1": [("Tulus", "18:00"), ("Sabrina Carpenter", "20:00"), ("Taylor Swift", "22:00")],
    "Day 2": [("Adele", "17:30"), ("Justin Bieber", "19:30"), ("Ariana Grande", "21:30")],
    },
    support_contact="support@festpal.com / +62-812-3456-7890"
)

_REFLECTION_MAP = {
    # Indonesian pronouns
    # "saya": "kamu",
    "aku": "kamu",
    "gue": "kamu",
    "gua": "kamu",
    "kamu": "saya",
    "anda": "saya",
    "kami": "kalian",
    "kita": "kalian", 
    "kalian": "kami",
    
    # Indonesian possessives
    "punyaku": "punyamu",
    "punyamu": "punyaku", 
    "milikku": "milikmu",
    "milikmu": "milikku",
    "namaku": "namamu",
    "namamu": "namaku",
    "tiketku": "tiketmu",
    "tiketmu": "tiketku",
    "pesananku": "pesananmu",
    "pesananmu": "pesananku",
    
    # English pronouns and possessives
    "i": "you",
    "me": "you", 
    "you": "me",
    "my": "your",
    "your": "my",
    "mine": "yours",
    "yours": "mine",
    "u": "saya",
    "ur": "mu",
}


def reflect(text: str) -> str:
    if not text:
        return text
    
    text_lower = text.lower().strip()

    # First check for multi-word phrases
    for phrase, replacement in _REFLECTION_MAP.items():
        if " " in phrase and phrase in text_lower:
            text_lower = text_lower.replace(phrase, replacement)

    # Then process individual words while preserving punctuation and spacing
    tokens = re.findall(r"\w+|[^\w\s]", text_lower, flags=re.UNICODE)
    reflected_tokens = []

    for token in tokens:
        reflected_tokens.append(_REFLECTION_MAP.get(token, token))

    return " ".join(reflected_tokens).strip()


def format_lineup(lineup: Dict[str, List[Tuple[str, str]]]) -> str:
    if not lineup:
        return "Lineup belum tersedia."

    lines = []
    for day, acts in lineup.items():
        lines.append(f"{day}:")
        if not acts:
            lines.append("  - Belum ada jadwal")
        else:
            for artist, time in acts:
                lines.append(f"  - {artist} — {time}")
        lines.append("")  # Add spacing between days

    return "\n".join(lines).strip()


class ChatBot:

    def __init__(self, bot_name: str = "FestPal", chatbot_response: Optional[Dict[str, str]] = None) -> None:
        if chatbot_response is None:
            chatbot_response = self.chatbot_response()

        # Compile patterns for better performance
        self._rules: List[Tuple[Pattern, str]] = [
            (re.compile(pattern, flags=re.IGNORECASE | re.UNICODE), response) 
            for pattern, response in chatbot_response.items()
        ]

        self.bot_name = bot_name
        self.intro = f"Hai, saya {self.bot_name} — bot panduan {FESTIVAL_INFO.name}. Tanya saja: harga, jadwal, lokasi, refund, atau ketik 'help'."
        self.default_response = (
            "Maaf, saya tidak mengerti. Coba tanyakan dengan kata kunci seperti: 'harga tiket', 'jadwal', 'bisa gopay?', 'refund', "
            "atau ketik 'help' untuk daftar bantuan lengkap."
        )

    def chatbot_response(self) -> Dict[str, str]:
        return {
            # GREETINGS & IDENTITY
            r"\b(?:hi|hello|hey|hai|hallo|hei|halo|hola)\b": 
                "Halo! Saya FestPal, asisten festival kamu. Mau tanya soal tiket, jadwal, lokasi, atau bantuan lainnya? Ketik 'help' untuk menu lengkap.",
            r"\b(?:who(?:\s*(?:are|r))?\s*(?:you|u)|siapa\s+(?:kamu|anda|namamu|nama\s+(?:kamu|anda)))\b": 
                f"Saya adalah {FESTIVAL_INFO.name} Bot — asisten resmi festival. Saya membantu informasi tiket, jadwal, dan layanan festival.",
            r"\b(?:siapa\s+(?:aku|saya)|who\s+am\s+i)\b": 
                "Saya tidak memiliki akses ke data pribadi. Untuk info akun, periksa profil aplikasi atau hubungi customer service.",

            # HELP & CAPABILITIES
            r"\b(?:help|bantuan|menu|perintah|info|panduan|apa\s+yang\s+bisa\s+(?:kamu|anda)(?:\s+lakukan)?)\b": 
                "MENU BANTUAN FESTPAL BOT\n"
                "=========================\n\n"
                "TIKET & PEMBELIAN:\n"
                "- Info harga tiket: 'berapa harga tiket', 'ticket price'\n"
                "- Kategori tiket: 'jenis tiket', 'kategori tiket'\n"
                "- Cara beli tiket: 'cara beli tiket', 'how to buy'\n"
                "- Metode pembayaran: 'bisa pakai gopay?', 'payment method'\n"
                "- Promo & voucher: 'ada promo?', 'kode diskon'\n\n"
                "MASALAH TIKET:\n"
                "- Refund tiket: 'refund', 'refund ORDER123'\n"
                "- Tiket belum sampai: 'tiket belum sampai', 'haven't received ticket'\n"
                "- QR code bermasalah: 'QR tidak bisa scan', 'QR error'\n"
                "- Transfer/resale tiket: 'jual tiket', 'transfer tiket'\n\n"
                "JADWAL & ACARA:\n"
                "- Lineup artis: 'lineup', 'siapa yang tampil'\n"
                "- Guest star: 'siapa guest star', 'bintang tamu'\n"
                "- Jadwal hari ini: 'siapa tampil hari ini'\n"
                "- Jadwal waktu tertentu: 'jam 20:00'\n\n"
                "LOKASI & FASILITAS:\n"
                "- Lokasi venue: 'dimana lokasinya', 'alamat'\n"
                "- Info parkir: 'parkir dimana?', 'parkir motor'\n"
                "- Merchandise: 'beli merch', 'booth merchandise'\n\n"
                "BANTUAN & DARURAT:\n"
                "- Customer service: 'contact', 'hubungi CS'\n"
                "- Darurat medis: 'medis', 'emergency'\n"
                "- Barang hilang: 'barang hilang', 'lost and found'\n"
                "- Aturan festival: 'aturan', 'rules'\n\n"
                "Ketik pertanyaan atau kata kunci untuk bantuan spesifik!",

            # TICKET REFUND (Specific patterns first)
            r"(?:refund|pengembalian).*(?:order|nomor|no\.?|kode|pesanan)\s*[:#]?\s*([A-Za-z0-9-]{3,})": 
                "Permintaan refund untuk pesanan {0} telah dicatat. Silakan hubungi CS resmi dengan bukti pembayaran dan nomor pesanan tersebut untuk proses lebih lanjut.",
            r"\b(?:refund|pengembalian\s+uang|minta\s+refund|pengembalian)\b": 
                "Kebijakan refund:\n- Refund penuh jika acara dibatalkan resmi\n- Refund parsial sesuai T&C untuk alasan tertentu\n- Sebutkan nomor pesanan untuk bantuan lebih lanjut",

            # TICKET RESALE & TRANSFER
            r"\b(?:resale|re[- ]?sale|jual\s+ulang|transfer\s+tiket|jual\s+tiket)\b": 
                    "PERINGATAN: Tiket dari penjualan ulang tidak resmi berisiko diblokir. Untuk keamanan, beli hanya dari kanal resmi atau partner terpercaya.",

            # TICKET DELIVERY ISSUES
            r"(?:tiket(?:ku|mu|nya)?|e-?ticket)\s*(?:tidak|gak|ga|belum)\s*(?:sampai|datang|terkirim|dikirim)": 
                "Jika e-ticket belum sampai:\n- Cek folder spam/promosi email\n- Tunggu hingga 2x24 jam setelah pembayaran\n- Hubungi CS dengan bukti pembayaran jika masih belum ada",

            r"(?:tidak|gak|ga|belum)\s*(?:mendapat|menerima|terima|dapat).*(?:tiket|e-?ticket|email|invoice)": 
                "Jika belum menerima e-ticket:\n- Cek folder spam/promosi email\n- Tunggu hingga 2x24 jam setelah pembayaran\n- Hubungi CS dengan bukti pembayaran jika masih belum ada",

            r"(?:haven'?t|did\s*not|not)\s+receive.*ticket|no.*ticket.*received": 
                "If you haven't received your e-ticket, please check spam folder and contact our official support with proof of purchase.",

            # QR CODE & E-TICKET ISSUES
            r"\b(?:qr|qr\s*code|scan)\b.*(?:error|tidak|gak|ga|fail|cannot|can't|rusak|buram|blur)": 
                "Masalah QR code? Solusinya:\n- Pastikan layar terang dan QR jelas\n- Kunjungi box office dengan bukti pembayaran\n- Petugas akan verifikasi manual untuk akses masuk",

            r"\b(?:qr|e-?ticket|eticket|barcode)\b": 
                "E-ticket berisi QR code akan dikirim ke email terdaftar. Pastikan QR code terlihat jelas saat di-scan di pintu masuk.",

            # PAYMENT METHODS
            r"\b(?:bisa|boleh|accept|support|terima|menerima)\b.*\b(gopay|ovo|dana|shopeepay|shopee\s+pay)\b": 
                "E-wallet {0} tersedia di checkout. Lanjutkan ke halaman pembayaran untuk konfirmasi ketersediaan metode pembayaran.",
            r"\b(?:metode|method|payment|pembayaran)\b": 
                "Metode pembayaran yang tersedia:\n- Kartu kredit/debit\n- Transfer bank\n- E-wallet (GoPay, OVO, DANA, ShopeePay)\n- Cek halaman checkout untuk detail lengkap",

            # TICKET PRICES & CATEGORIES
            r"\b(?:berapa\s+harga|harga\s+tiket|ticket\s+price)\b": 
                "Harga tiket:\n"
                "- Festival A (Standing): Rp 350.000\n"
                "- Festival B (Standing): Rp 250.000\n"
                "- VIP (Seating): Rp 500.000\n\n"
                "Beli melalui website resmi atau partner terpercaya!",

            r"\b(?:kategori|jenis|tipe)\s*tiket\b": 
                "Kategori tiket tersedia:\n- Festival A (Standing)\n- Festival B (Standing)\n- VIP (Seating dengan fasilitas eksklusif)",

            # HOW TO BUY
            r"(?:cara|how\s+to|bagaimana).*(?:beli|membeli|purchase).*tiket": 
                "Cara beli tiket:\n"
                "1. Kunjungi website resmi\n"
                "2. Pilih kategori & jumlah tiket\n"
                "3. Isi data pembeli\n"
                "4. Pilih metode pembayaran\n"
                "5. Selesaikan pembayaran\n"
                "6. Cek email untuk e-ticket QR code",

            # LINEUP & GUEST STARS
            r"\b(?:siapa\s+guest\s*star|siapa\s+bintang\s*tamu|guest\s*star)\b": 
                f"Guest stars & lineup:\n{format_lineup(FESTIVAL_INFO.lineup)}\n\nKetik 'lineup' untuk detail lengkap!",

            r"\b(?:line[\s-]?up|lineup|daftar\s+penampil|siapa\s+(?:yang\s+)?tampil)\b": 
                f"Lineup lengkap:\n{format_lineup(FESTIVAL_INFO.lineup)}",

            r"\b(?:siapa\s+tampil\s+hari\s+ini|jadwal\s+hari\s+ini)\b": 
                f"Penampil hari ini (Day 1):\n" + "\n".join([f"  - {artist} — {time}" for artist, time in FESTIVAL_INFO.lineup.get("Day 1", [])]),

            # LOCATION & PARKING
            r"\b(?:parkir|parking)(?:\s+(?:mobil|motor|dimana|di\s+mana))?\b": 
                f"Info parkir:\n"
                f"- Umum: {FESTIVAL_INFO.parking['general']}\n"
                f"- Motor: {FESTIVAL_INFO.parking['motor']}\n"
                f"- VIP: {FESTIVAL_INFO.parking['vip']}\n"
                f"Tips: {FESTIVAL_INFO.parking['tips']}",

            r"\b(?:lokasi|venue|alamat|dimana|di\s+mana|where|tempat)\b": 
                f"Lokasi: {FESTIVAL_INFO.location}\n\nCek peta dan denah lengkap di website resmi.",

            # RULES & POLICIES
            r"\b(?:aturan|peraturan|dilarang|larangan|rules|policy|kebijakan)\b": 
                "Aturan penting:\n"
                "- Wajib bawa: KTP/identitas + e-ticket QR\n"
                "- Dilarang: senjata, narkoba, kembang api, alkohol\n"
                "- Tidak dianjurkan: tripod besar, payung panjang",

            # PROMO & VOUCHER
            r"\b(?:voucher|promo|diskon|kode\s+promo|coupon)\b": 
                "Info promo:\n- Cek syarat & ketentuan di halaman promo\n- Masukkan kode saat checkout\n- Pastikan kode masih berlaku dan sesuai syarat",

            # CONTACT & SUPPORT
            r"\b(?:contact|kontak|customer\s*service|cs|support|hotline|hubungi)\b": 
                f"Customer Service:\n{FESTIVAL_INFO.support_contact}\n\nTersedia 24/7 untuk bantuan tiket dan festival.",

            # MERCHANDISE
            r"\b(?:merch|merchandise|kaos|t-shirt|booth|store|toko)\b": 
                "Merchandise resmi tersedia di booth khusus dalam venue. Pembayaran tunai/non-tunai tersedia sesuai ketentuan booth.",

            # EMERGENCY & MEDICAL
            r"\b(?:darurat|medis|medical|emergency|ambulans|dokter|sakit)\b": 
                "Darurat medis: segera hubungi petugas terdekat atau kunjungi pos medis di venue. Petugas siaga 24 jam selama acara.",

            # LOST & FOUND
            r"\b(?:hilang|lost|barang\s+hilang|lost\s+and\s+found)\b": 
                "Barang hilang? Laporkan ke Pos Informasi/Lost & Found di venue. Bawa bukti kepemilikan jika ada.",

            # TIME BASED QUERIES
            r"(?:jam|pukul|time)\s+([0-2]?[0-9]:[0-5][0-9])": 
                "Jadwal jam {0} - cek lineup untuk mengetahui artis yang tampil pada waktu tersebut.",

            # GREETINGS & FAREWELLS
            r"\b(?:terima\s*kasih|thanks|thank\s+you|thx)\b": 
                "Sama-sama! Ada yang lain bisa saya bantu? Jangan ragu bertanya!",

            r"\b(?:bye|goodbye|selamat\s+tinggal|sampai\s+jumpa|see\s+you)\b": 
                "Sampai jumpa di festival! Jangan lupa bawa e-ticket dan bersiap untuk pengalaman tak terlupakan!",

            # GENERIC KEYWORD FALLBACK
            r"\b(?:tiket|ticket|festival|acara|event)\b": 
                "Tentang tiket festival, apa yang ingin kamu ketahui? Bisa tanya: harga, cara beli, atau ketik 'help' untuk menu lengkap.",
        }

    def reply(self, user_input: str) -> str:
        if not user_input:
            return self.intro

        text = user_input.strip()

        # Try to match against each rule pattern
        for pattern, response in self._rules:
            match = pattern.search(text)
            if not match:
                continue

            # Apply reflection to captured groups
            try:
                groups: List[str] = [reflect(g or "") for g in match.groups()] if match.groups() else []
            except Exception:
                groups = []

            # Format response with reflected groups if placeholders exist
            if "{" in response and groups:
                try:
                    return response.format(*groups)
                except (IndexError, ValueError):
                    # If formatting fails, return response without formatting
                    return response

        return response

        return self.default_response