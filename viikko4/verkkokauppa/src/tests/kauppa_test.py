import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.varasto_mock = Mock()

        self.varasto_mock.saldo.side_effect = self.varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = self.varasto_hae_tuote

        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

    # tehdään toteutus saldo-metodille
    def varasto_saldo(self, tuote_id):
        if tuote_id == 1:
            return 10
        if tuote_id == 2:
            return 6
        if tuote_id == 3:
            return 0

    # tehdään toteutus hae_tuote-metodille
    def varasto_hae_tuote(self, tuote_id):
        if tuote_id == 1:
            return Tuote(1, "maito", 5)
        if tuote_id == 2:
            return Tuote(2, "patonki", 3)
        if tuote_id == 3:
            return Tuote(3, "juusto", 4)

    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan(self):
        # palautetaan aina arvo 42
        self.viitegeneraattori_mock.uusi.return_value = 42

        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_ostoksen_paaytyttya_pankin_metodia_tilisiirto_kutsutaan_oikeilla_arvoilla(self):
        self.viitegeneraattori_mock.uusi.return_value = 42

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu oikeilla arvoilla
        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 5
        )

    def test_korissa_kaksi_eri_tuotetta_kutsutaan_tilisiirto_metodia_oikeilla_arvoilla(self):
        self.viitegeneraattori_mock.uusi.return_value = 35

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("jukka", "65432")

        # varmistetaan, että metodia tilisiirto on kutsuttu oikeilla arvoilla
        self.pankki_mock.tilisiirto.assert_called_with(
            "jukka", 35, "65432", "33333-44455", 8
        )
    
    def test_korissa_kaksi_samaa_tuotetta_kutsutaan_tilisiirto_metodia_oikeilla_arvoilla(self):
        self.viitegeneraattori_mock.uusi.return_value = 35

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("jukka", "65432")

        # varmistetaan, että metodia tilisiirto on kutsuttu oikeilla arvoilla
        self.pankki_mock.tilisiirto.assert_called_with(
            "jukka", 35, "65432", "33333-44455", 6
        )

    def test_korissa_tuote_joka_on_loppu_kutsutaan_tilisiirtoa_oikeilla_arvoilla(self):
        self.viitegeneraattori_mock.uusi.return_value = 15

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.lisaa_koriin(3)
        self.kauppa.tilimaksu("hilma", "11211")

        # varmistetaan, että metodia tilisiirto on kutsuttu oikeilla arvoilla
        self.pankki_mock.tilisiirto.assert_called_with(
            "hilma", 15, "11211", "33333-44455", 3
        )

    def test_metodi_aloita_asiointi_nollaa_edellisen_ostoksen_tiedot(self):
        self.viitegeneraattori_mock.uusi.return_value = 34

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("hilma", "11211")

        # varmistetaan, että metodia tilisiirto on kutsuttu oikeilla arvoilla
        # ja että ensimmäisen asioinnin tietoja ei näy
        self.pankki_mock.tilisiirto.assert_called_with(
            "hilma", 34, "11211", "33333-44455", 3
        )

    def test_pyydetaan_uusi_viitenumero_jokaiseen_maksuun(self):
        viitegeneraattori_mock2 = Mock(wraps=Viitegeneraattori())

        oikea_kauppa = Kauppa(self.varasto_mock, self.pankki_mock, viitegeneraattori_mock2)

        oikea_kauppa.aloita_asiointi()
        oikea_kauppa.lisaa_koriin(1)
        oikea_kauppa.tilimaksu("hilma", "11211")

        self.assertEqual(viitegeneraattori_mock2.uusi.call_count, 1)

        oikea_kauppa.aloita_asiointi()
        oikea_kauppa.lisaa_koriin(2)
        oikea_kauppa.lisaa_koriin(2)
        oikea_kauppa.tilimaksu("jaakko", "11231")

        self.assertEqual(viitegeneraattori_mock2.uusi.call_count, 2)

    def test_tuotteen_poistaminen_korista_onnistuu(self):
        self.viitegeneraattori_mock.uusi.return_value = 34

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.poista_korista(1)
        self.kauppa.tilimaksu("hilma", "11211")

        # varmistetaan, että metodia tilisiirto on kutsuttu oikeilla arvoilla
        # ja että ensimmäinen tuote poistettiin korista
        self.pankki_mock.tilisiirto.assert_called_with(
            "hilma", 34, "11211", "33333-44455", 3
        )
