import pytest
from bot import ChatBot, reflect, format_lineup, FESTIVAL_INFO


@pytest.fixture()
def bot_instance():
    return ChatBot()


class TestChatBotCore:

    def test_greeting_variations(self, bot_instance):
        """Test 1: Different greeting variations work correctly"""
        greetings = ["halo", "hi", "hello", "hey", "hai", "hallo", "hei", "hola"]
        for greeting in greetings:
            response = bot_instance.reply(greeting)
            assert "FestPal" in response
            assert any(word in response.lower() for word in ["halo", "mau tanya"])

    def test_identity_questions(self, bot_instance):
        """Test 2: Bot correctly identifies itself - bidirectional support"""
        identity_questions = [
            "siapa namamu?",
            "who are you",
            "siapa kamu",
            "siapa anda", 
            "who r u",
            "who u",
            "nama kamu apa",
            "nama anda siapa"
        ]
        for question in identity_questions:
            response = bot_instance.reply(question)
            assert "FestPal" in response
            assert "Bot" in response or "bot" in response

    def test_user_identity_questions(self, bot_instance):
        """Test 3: Bot handles user identity questions appropriately"""
        user_identity_questions = [
            "who am i",
            "siapa aku",
            "siapa saya"
        ]
        for question in user_identity_questions:
            response = bot_instance.reply(question)
            assert "akses" in response.lower() or "data akunmu" in response.lower()
            assert "profil" in response.lower() or "cs" in response.lower()

    def test_ticket_pricing_comprehensive(self, bot_instance):
        """Test 4: Ticket pricing information is comprehensive"""
        price_questions = [
            "berapa harga tiket",
            "ticket price",
            "harga tiket"
        ]
        for question in price_questions:
            response = bot_instance.reply(question)
            assert "tiket" in response.lower() or "ticket" in response.lower()
            assert "rp" in response.lower()
            assert "350.000" in response  # Festival A price
            assert "250.000" in response  # Festival B price
            assert "500.000" in response  # VIP price

    def test_lineup_and_schedule(self, bot_instance):
        """Test 5: Lineup and schedule information"""
        lineup_questions = [
            "lineup",
            "siapa guest star nya",
            "siapa yang tampil",
            "daftar penampil"
        ]
        for question in lineup_questions:
            response = bot_instance.reply(question)
            assert "Tulus" in response or "Taylor Swift" in response
            assert "Day 1" in response or "Day 2" in response
            assert ":" in response  # Time format

    def test_location_and_parking(self, bot_instance):
        """Test 6: Location and parking information"""
        location_questions = ["lokasi", "venue", "dimana", "where"]
        for question in location_questions:
            response = bot_instance.reply(question)
            assert "GOR UNY" in response or "Yogyakarta" in response

        parking_questions = ["parkir", "parking", "parkir mobil"]
        for question in parking_questions:
            response = bot_instance.reply(question)
            assert "parkir" in response.lower()
            assert any(word in response for word in ["umum", "motor", "VIP"])

    def test_refund_processing(self, bot_instance):
        """Test 7: Refund queries and order code processing"""
        response = bot_instance.reply("refund")
        assert "refund" in response.lower() or "pengembalian" in response.lower()

        response = bot_instance.reply("refund order #ORDER123")
        assert "123" in response  # After reflection transformation
        assert "tercatat" in response or "support" in response

        response = bot_instance.reply("refund order ORDER123")
        assert "123" in response
        assert "tercatat" in response or "support" in response

        response = bot_instance.reply("refund order ABC456")
        assert "456" in response or "ABC456" in response

        refund_questions = ["minta refund", "pengembalian uang"]
        for question in refund_questions:
            response = bot_instance.reply(question)
            assert len(response) > 0
            assert isinstance(response, str)

    def test_payment_methods(self, bot_instance):
        """Test 8: Payment method queries"""
        payment_questions = [
            "bisa gopay ga",
            "payment method",
            "metode pembayaran",
            "terima OVO",
            "credit card"
        ]
        for question in payment_questions:
            response = bot_instance.reply(question)
            assert any(method in response.lower() for method in ["gopay", "ovo", "dana", "kartu"])

    def test_help_functionality(self, bot_instance):
        """Test 9: Help and capabilities"""
        help_questions = ["help", "bantuan", "menu", "apa yang bisa kamu lakukan", "perintah", "info", "panduan"]
        for question in help_questions:
            response = bot_instance.reply(question)
            assert "membantu" in response.lower() or "bisa" in response.lower()
            assert "tiket" in response.lower()
            assert "•" in response  # Bullet points
            assert "refund" in response.lower()
            assert "lineup" in response.lower()

    def test_qr_and_eticket_issues(self, bot_instance):
        """Test 10: QR code and e-ticket support"""
        qr_questions = [
            "QR tidak bisa discan",
            "e-ticket error",
            "barcode blur",
            "qr code fail"
        ]
        for question in qr_questions:
            response = bot_instance.reply(question)
            assert any(word in response.lower() for word in ["qr", "ticket", "loket", "box office"])

    def test_resale_transfer_warnings(self, bot_instance):
        """Test 11: Resale and transfer warnings"""
        resale_questions = [
            "resale",
            "re-sale",
            "jual ulang",
            "transfer tiket",
            "transfer ticket",
            "jual tiket"
        ]
        for question in resale_questions:
            response = bot_instance.reply(question)
            assert "resmi" in response.lower()

    def test_ticket_not_received(self, bot_instance):
        """Test 12: Ticket not received issues"""
        ticket_issues = [
            "tidak terima tiket",
            "belum menerima e-ticket",
            "haven't received ticket",
            "no ticket received",
            "ga dapat eticket"
        ]
        for issue in ticket_issues:
            response = bot_instance.reply(issue)
            assert any(word in response.lower() for word in ["spam", "cs", "bukti", "support", "email", "pembayaran"])

    def test_how_to_buy_tickets(self, bot_instance):
        """Test 13: How to buy ticket information"""
        cara_questions = ["cara beli tiket", "cara membeli tiket"]
        for question in cara_questions:
            response = bot_instance.reply(question)
            assert "website resmi" in response.lower()
            assert "pilih kategori" in response.lower()

        english_questions = ["how to purchase ticket", "how do i buy"]
        for question in english_questions:
            response = bot_instance.reply(question)
            assert len(response) > 0

    def test_promo_voucher(self, bot_instance):
        """Test 14: Promo and voucher information"""
        promo_questions = ["voucher", "promo", "diskon", "kode promo", "coupon"]
        for question in promo_questions:
            response = bot_instance.reply(question)
            assert "promo" in response.lower() or "voucher" in response.lower()
            assert "checkout" in response.lower()

    def test_guest_star_specific(self, bot_instance):
        """Test 15: Guest star specific queries"""
        guest_questions = ["siapa guest star", "siapa guest star nya", "siapa bintang tamu"]
        for question in guest_questions:
            response = bot_instance.reply(question)
            assert "lineup" in response.lower()
            assert "Day 1" in response
            assert "Taylor Swift" in response or "Tulus" in response

    def test_todays_performers(self, bot_instance):
        """Test 16: Today's performers query"""
        response = bot_instance.reply("siapa tampil hari ini")
        assert "Day 1" in response
        assert "Tulus" in response
        assert "•" in response

    def test_ticket_categories(self, bot_instance):
        """Test 17: Ticket categories"""
        category_questions = ["kategori tiket", "jenis tiket"]
        for question in category_questions:
            response = bot_instance.reply(question)
            assert "Festival A" in response
            assert "Festival B" in response
            assert "VIP" in response

    def test_rules_and_policies(self, bot_instance):
        """Test 18: Rules and policies"""
        rule_questions = ["aturan", "peraturan", "rules", "policy", "dilarang"]
        for question in rule_questions:
            response = bot_instance.reply(question)
            assert "identitas" in response.lower() or "dilarang" in response.lower()
            assert "senjata" in response.lower() or "alkohol" in response.lower()

    def test_contact_customer_service(self, bot_instance):
        """Test 19: Customer service contact"""
        contact_questions = ["contact", "kontak", "customer service", "cs", "support", "hotline"]
        for question in contact_questions:
            response = bot_instance.reply(question)
            assert "support@festpal.com" in response
            assert "+62-812-3456-7890" in response

    def test_merchandise(self, bot_instance):
        """Test 20: Merchandise information"""
        merch_questions = ["merch", "merchandise", "kaos", "t-shirt", "booth"]
        for question in merch_questions:
            response = bot_instance.reply(question)
            assert "booth" in response.lower()
            assert "venue" in response.lower()

    def test_emergency_medical(self, bot_instance):
        """Test 21: Emergency and medical"""
        emergency_questions = ["darurat", "medical", "emergency", "dokter", "ambulans"]
        for question in emergency_questions:
            response = bot_instance.reply(question)
            assert "darurat" in response.lower() or "medis" in response.lower()
            assert "petugas" in response.lower() or "venue" in response.lower()

    def test_lost_and_found(self, bot_instance):
        """Test 22: Lost and found"""
        lost_questions = ["hilang", "lost and found", "lost", "barang hilang"]
        for question in lost_questions:
            response = bot_instance.reply(question)
            assert "pos informasi" in response.lower() or "lost" in response.lower()
            assert "bukti" in response.lower()

    def test_thank_you_goodbye(self, bot_instance):
        """Test 23: Thank you and goodbye responses"""
        thank_questions = ["terima kasih", "thanks", "thank you"]
        for question in thank_questions:
            response = bot_instance.reply(question)
            assert "sama-sama" in response.lower()
        
        goodbye_questions = [
            "bye",
            "goodbye",
            "sampai jumpa",
        ]
        for question in goodbye_questions:
            response = bot_instance.reply(question)
            assert "sampai jumpa" in response.lower() or "festival" in response.lower()

    def test_generic_fallback_keywords(self, bot_instance):
        """Test 24: Generic fallback for recognized keywords"""
        fallback_keywords = ["tiket", "harga", "jadwal", "vip"]
        for keyword in fallback_keywords:
            response = bot_instance.reply(keyword)
            assert "kamu bisa tanya" in response.lower()
            assert "contact" in response.lower()

        response = bot_instance.reply("aturan")
        assert "aturan" in response.lower() or "dilarang" in response.lower()
        assert "identitas" in response.lower()

    def test_default_fallback_handling(self, bot_instance):
        """Test 25: Unknown queries fallback appropriately"""
        unknown_queries = ["qwertyuiop", "blablabla", "xyz123", "random nonsense text"]
        for query in unknown_queries:
            response = bot_instance.reply(query)
            assert isinstance(response, str)
            assert len(response) > 0
            assert "maaf" in response.lower() or "tidak mengerti" in response.lower()


class TestUtilityFunctions:
    """Test utility functions"""

    def test_reflect_function(self):
        """Test bidirectional reflection mapping works correctly"""
        test_cases = [
            ("saya senang", "kamu senang"),
            ("aku sedih", "kamu sedih"), 
            ("kamu baik", "saya baik"),
            ("anda ramah", "saya ramah"),
            ("my name", "your name"),
            ("your ticket", "my ticket"),
            ("you are good", "me are good"),
            ("me too", "you too"),
            ("gue baik", "kamu baik"),
            ("punyaku hilang", "punyamu hilang"),
            ("punyamu bagus", "punyaku bagus"),
            ("namaku John", "namamu john"),
            ("namamu apa", "namaku apa"),
            ("milikku rusak", "milikmu rusak"), 
            ("milikmu bagus", "milikku bagus"),
            ("mine is broken", "yours is broken"),
            ("yours works", "mine works"),
            ("u good", "saya good"),
            ("ur name", "mu name"),
        ]
        for input_text, expected in test_cases:
            result = reflect(input_text)
            assert result == expected

    def test_format_lineup_function(self):
        """Test lineup formatting function"""
        test_lineup = {
            "Day 1": [("Artist A", "18:00"), ("Artist B", "20:00")],
            "Day 2": [("Artist C", "19:00")]
        }
        result = format_lineup(test_lineup)
        assert "Day 1:" in result
        assert "Artist A" in result
        assert "18:00" in result
        assert "•" in result  # Bullet points

    def test_festival_info_structure(self):
        """Test festival info data structure"""
        assert "name" in FESTIVAL_INFO
        assert "location" in FESTIVAL_INFO
        assert "parking" in FESTIVAL_INFO
        assert "lineup" in FESTIVAL_INFO
        assert "support_contact" in FESTIVAL_INFO

        parking = FESTIVAL_INFO["parking"]
        assert "general" in parking
        assert "vip" in parking
        assert "motor" in parking
        assert "tips" in parking

        lineup = FESTIVAL_INFO["lineup"]
        assert "Day 1" in lineup
        assert "Day 2" in lineup
        for day_lineup in lineup.values():
            assert isinstance(day_lineup, list)
            for artist_info in day_lineup:
                assert len(artist_info) == 2

        assert FESTIVAL_INFO["name"] == "FestPal"
        assert "GOR UNY" in FESTIVAL_INFO["location"]
        assert "support@festpal.com" in FESTIVAL_INFO["support_contact"]

    def test_chatbot_initialization(self):
        """Test ChatBot initialization"""
        bot = ChatBot()
        assert bot.bot_name == "FestPal"
        assert "FestPal" in bot.intro
        assert "tidak mengerti" in bot.default_response

        custom_bot = ChatBot(bot_name="TestBot")
        assert custom_bot.bot_name == "TestBot"
        assert "TestBot" in custom_bot.intro
