import unittest
from statistics_service import StatisticsService
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),
            Player("Lemieux", "PIT", 45, 54),
            Player("Kurri",   "EDM", 37, 53),
            Player("Yzerman", "DET", 42, 56),
            Player("Gretzky", "EDM", 35, 89)
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_vaaralla_nimella_hakeminen_ei_palauta_mitaan(self):
        tulos = self.stats.search("Huippupelaaja")

        self.assertIsNone(tulos)
    
    def test_haku_oikealla_nimella_toimii(self):
        pelaaja = self.stats.search("Kurri")

        self.assertEqual(pelaaja.name, "Kurri")
        self.assertEqual(pelaaja.team, "EDM")

    def test_haku_tiimin_nimella_antaa_oikeat_pelaajat(self):
        pelaajat = self.stats.team("EDM")

        self.assertEqual(len(pelaajat), 3)
        self.assertEqual(pelaajat[2].name, "Gretzky")

    def test_top_lista_oikeassa_jarjestyksessa(self):
        top_lista = self.stats.top(2)

        self.assertEqual(top_lista[0].name, "Gretzky")
        self.assertEqual(top_lista[1].name, "Lemieux")
        self.assertEqual(len(top_lista), 2)

    