from django.test import TestCase
from input_text.forms import LocusForm


class LocusFormTest(TestCase):

    def test_valid_form(self):
        form_data = {"FGA": "1,1", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
                     "CSF1PO": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
                     "D2S441": "11,14", "D5S818": "13,13", "D7S82O": "12,12",
                     "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
                     "D19S433": "13,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
                     "D3S1358": "15,16", "D6S1O43": "11,12", "D8S1179": "14,14",
                     "Penta D": "11,12", "Penta E": "12,13", "D1OS1248": "15,15",
                     "D22S1O45": "15,15"}

        form = LocusForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {"FGA": "1.1", "vWA": "1619", "THO1": "8,9a", "TPOX": "8,8",
                     "CSF1PO": "", "D18S51": "13,16", "D21S11": "29,30.2",
                     "D2S441": "11,14", "D5S818": "13,13", "D7S82O": "12,12",
                     "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
                     "D19S433": "13,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
                     "D3S1358": "15,16", "D6S1O43": "11,12", "D8S1179": "14,14",
                     "Penta D": "11,12", "Penta E": "12,13", "D1OS1248": "15,15",
                     "D22S1O45": "15,15"}

        form = LocusForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_blank_form(self):

        form = LocusForm(data={})

        self.assertTrue(form.is_valid())
