import os
from unittest import TestCase

from django.conf import settings

from upload_file.forms import DnkForm
from upload_file.models import Client, Child
from upload_file.services import compare_dnk_child_with_clients, get_dict_from_instances, pdf_extract_text, \
    retrieve_values


class MyAdminViewPostRequestDnkFormTestCase(TestCase):
    def setUp(self) -> None:
        self.tatu_vasile = Client.objects.create(name='Tasu Vasile',
                                                 locus={"FGA": "21,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
                                                        "CSF1P0": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
                                                        "D2S441": "11,14", "D5S818": "13,13", "D7S820": "12,12",
                                                        "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
                                                        "D19S433": "13,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
                                                        "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
                                                        "Penta D": "11,12", "Penta E": "12,13", "D10S1248": "15,15",
                                                        "D22S1045": "15,15"})
        self.tatu_vasile2 = Client.objects.create(name='Tasu Vasile',
                                                  locus={"FGA": "15,15", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
                                                         "CSF1P0": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
                                                         "D2S441": "11,14", "D5S818": "13,13", "D7S820": "12,12",
                                                         "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
                                                         "D19S433": "13,13", "D1S1656": "121,561", "D2S1338": "00.1,20",
                                                         "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
                                                         "Penta D": "11,12", "Penta E": "12,13", "D10S1248": "15,15",
                                                         "D22S1045": "15,15"})

        self.tatu_vasile3 = Client.objects.create(name='Tasu Vasile',
                                                  locus={"FGA": "15,15", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
                                                         "CSF1P0": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
                                                         "D2S441": "11,14", "D5S818": "13,13", "D7S820": "12,12",
                                                         "D12S391": "19,600", "D13S317": "8,11", "D16S539": "10,11",
                                                         "D19S433": "13,1100", "D1S1656": "121,561",
                                                         "D2S1338": "00.1,20",
                                                         "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
                                                         "Penta D": "11,12", "Penta E": "12,13", "D10S1248": "15,15",
                                                         "D22S1045": "15,15"})
        self.child = Child.objects.create()

    def test_compare_dnk_child_with_clients_is_None(self):
        dictionary_dnk = {
            "FGA": "10,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
            "CSF1P0": "1,14", "D18S51": "13,16", "D21S11": "29,30.2",
            "D2S441": "10,13", "D5S818": "13,13", "D7S820": "12,12",
            "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
            "D19S433": "16,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
            "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
            "Penta_D": "11,12", "Penta_E": "12,13", "D10S1248": "15,15",
            "D22S1045": "15,15"
        }
        clients = Client.objects.all()

        self.assertIsNone(compare_dnk_child_with_clients(dictionary_dnk, clients))

    def test_compare_dnk_child_with_clients_get_client_from_clients(self):
        dictionary_dnk = {
            "FGA": "21,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
            "CSF1P0": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
            "D2S441": "11,14", "D5S818": "13,13", "D7S820": "12,12",
            "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
            "D19S433": "13,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
            "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
            "Penta D": "11,12", "Penta E": "12,13", "D10S1248": "15,15",
            "D22S1045": "15,15"
        }
        clients = Client.objects.all()

        get_client = compare_dnk_child_with_clients(dictionary_dnk, clients)
        self.assertEqual(get_client.name, self.tatu_vasile.name)

    def test_get_dict_from_instances(self):
        valid_dnk_data = {"FGA": "21,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
                          "CSF1P0": "21,22", "D18S51": "13,16", "D21S11": "29,30.2",
                          "D2S441": "14,14", "D5S818": "&&,13", "D7S820": "12,12",
                          "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
                          "D19S433": "13,13", "D1S1656": "21,22", "D2S1338": "19,20",
                          "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
                          "Penta_D": "11,12", "Penta_E": "12,13", "D10S1248": "15,15",
                          "D22S1045": "15,15"}
        dnk_instance = DnkForm(valid_dnk_data).save(commit=False)
        dnk_instance.child = self.child
        dnk_instance.save()

        locus_dict = get_dict_from_instances(dnk_instance)
        self.assertIn("Penta D", locus_dict)
        self.assertEqual(locus_dict, {"FGA": "21,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
                                      "CSF1P0": "21,22", "D18S51": "13,16", "D21S11": "29,30.2",
                                      "D2S441": "14,14", "D5S818": "&&,13", "D7S820": "12,12",
                                      "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
                                      "D19S433": "13,13", "D1S1656": "21,22", "D2S1338": "19,20",
                                      "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
                                      "Penta D": "11,12", "Penta E": "12,13", "D10S1248": "15,15",
                                      "D22S1045": "15,15"})

    def test_pdf_extract_text(self):
        pdf_path = 'test_pdf/TasuVasile.pdf'
        csv_file_path = pdf_extract_text(pdf_path)
        if 'test' in os.environ.get('DJANGO_SETTINGS_MODULE'):
            self.assertEqual(csv_file_path,
                             '/home/runner/work/TextExtractPdf/TextExtractPdf/work_dir/upload_file/csv_files/Tasu_Vasile.csv')
        else:
            self.assertEqual(csv_file_path,
                             '/home/rodion/Desktop/ExtractTextPdf/work_dir/upload_file/csv_files/Tasu_Vasile.csv')

    def test_pdf_not_extract_text(self):
        pdf_path = 'test_pdf/RRodion.pdf'
        csv_file_path = pdf_extract_text(pdf_path)
        self.assertEqual(csv_file_path, None)

    def test_retrieve_values(self):
        if 'test' in os.environ.get('DJANGO_SETTINGS_MODULE'):
            csv_path = '/home/runner/work/TextExtractPdf/TextExtractPdf/work_dir/upload_file/csv_files/Tasu_Vasile.csv'
        else:
            csv_path = '/home/rodion/Desktop/ExtractTextPdf/work_dir/upload_file/csv_files/Tasu_Vasile.csv'
        name, locus_dict = retrieve_values(csv_path)

        expected_name = 'Tasu Vasile'
        expected_locus_dict = {"FGA": "21,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
                               "CSF1P0": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
                               "D2S441": "11,14", "D5S818": "13,13", "D7S820": "12,12",
                               "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
                               "D19S433": "13,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
                               "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
                               "Penta D": "11,12", "Penta E": "12,13", "D10S1248": "15,15",
                               "D22S1045": "15,15"}

        self.assertEqual(name, expected_name)
        self.assertEqual(locus_dict, expected_locus_dict)

        if os.path.exists(csv_path):
            os.remove(csv_path)
