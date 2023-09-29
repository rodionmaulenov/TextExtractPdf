# import os
# from unittest import TestCase
#
# from upload_file.forms import DnkForm
# from upload_file.models import Client, Child
# from upload_file.services import compare_dnk_child_with_clients
#
#
# class MyAdminViewPostRequestDnkFormTestCase(TestCase):
#     def setUp(self) -> None:
#         self.tatu_vasile = Client.objects.create(name='Tasu Vasile',
#                                                  locus={"FGA": "21,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
#                                                         "CSF1P0": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
#                                                         "D2S441": "11,14", "D5S818": "13,13", "D7S820": "12,12",
#                                                         "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
#                                                         "D19S433": "13,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
#                                                         "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
#                                                         "Penta D": "11,12", "Penta E": "12,13", "D10S1248": "15,15",
#                                                         "D22S1045": "15,15"})
#         self.tatu_vasile2 = Client.objects.create(name='Tasu Vasile',
#                                                   locus={"FGA": "15,15", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
#                                                          "CSF1P0": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
#                                                          "D2S441": "11,14", "D5S818": "13,13", "D7S820": "12,12",
#                                                          "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
#                                                          "D19S433": "13,13", "D1S1656": "121,561", "D2S1338": "00.1,20",
#                                                          "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
#                                                          "Penta D": "11,12", "Penta E": "12,13", "D10S1248": "15,15",
#                                                          "D22S1045": "15,15"})
#
#         self.tatu_vasile3 = Client.objects.create(name='Tasu Vasile',
#                                                   locus={"FGA": "15,15", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
#                                                          "CSF1P0": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
#                                                          "D2S441": "11,14", "D5S818": "13,13", "D7S820": "12,12",
#                                                          "D12S391": "19,600", "D13S317": "8,11", "D16S539": "10,11",
#                                                          "D19S433": "13,1100", "D1S1656": "121,561",
#                                                          "D2S1338": "00.1,20",
#                                                          "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
#                                                          "Penta D": "11,12", "Penta E": "12,13", "D10S1248": "15,15",
#                                                          "D22S1045": "15,15"})
#         self.Veiko_Talirano = Client.objects.create(name='Veiko Talirano',
#                                                     locus={"FGA": "20,24", "vWA": "15,16", "THO1": "6,7", "TPOX": "8,8",
#                                                            "CSF1P0": "12,12", "D18S51": "15,17", "D21S11": "29,30.2",
#                                                            "D2S441": "10,14", "D5S818": "11,12", "D7S820": "10,12",
#                                                            "D12S391": "17,20", "D13S317": "11,12", "D16S539": "9,13",
#                                                            "D19S433": "14,15.2", "D1S1656": "12,12", "D2S1338": "17,20",
#                                                            "D3S1358": "15,15", "D6S1043": "13,14", "D8S1179": "12,14",
#                                                            "Penta D": "11,12", "Penta E": "5,14", "D10S1248": "14,15",
#                                                            "D22S1045": "16,16"})
#         self.child = Child.objects.create()
#
#     def test_compare_dnk_child_with_clients_is_None(self):
#         dictionary_dnk = {
#             "FGA": "10,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
#             "CSF1P0": "1,14", "D18S51": "13,16", "D21S11": "29,30.2",
#             "D2S441": "10,13", "D5S818": "13,13", "D7S820": "12,12",
#             "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
#             "D19S433": "16,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
#             "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
#             "Penta_D": "11,12", "Penta_E": "12,13", "D10S1248": "15,15",
#             "D22S1045": "15,15"
#         }
#         clients = Client.objects.all()
#
#         self.assertIsNone(compare_dnk_child_with_clients(dictionary_dnk, clients))
#
#     def test_compare_dnk_child_with_clients_get_client_from_clients(self):
#         dictionary_dnk = {
#             "FGA": "21,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
#             "CSF1P0": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
#             "D2S441": "11,14", "D5S818": "13,13", "D7S820": "12,12",
#             "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
#             "D19S433": "13,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
#             "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
#             "Penta D": "11,12", "Penta E": "12,13", "D10S1248": "15,15",
#             "D22S1045": "15,15"
#         }
#         clients = Client.objects.all()
#
#         get_client = compare_dnk_child_with_clients(dictionary_dnk, clients)
#         self.assertEqual(get_client.name, self.tatu_vasile.name)
#
#     def test_compare_dnk_child_with_clients_get_client_from_clients_Veiko_Talirano(self):
#         dictionary_dnk = {
#             "FGA": "20,24", "vWA": "16,18", "THO1": "7,9.3", "TPOX": "8,8",
#             "CSF1P0": "12,12", "D18S51": "12,17", "D21S11": "29,29",
#             "D2S441": "10,14", "D5S818": "9,11", "D7S820": "10,11",
#             "D12S391": "20,24", "D13S317": "9,12", "D16S539": "12,13",
#             "D19S433": "13,14", "D1S1656": "12,12", "D2S1338": "20,24",
#             "D3S1358": "14,15", "D6S1043": "14,14", "D8S1179": "12,13",
#             "Penta D": "9,11", "Penta E": "5,13", "D10S1248": "14,15",
#             "D22S1045": "16,16"
#         }
#         clients = Client.objects.all()
#
#         get_client = compare_dnk_child_with_clients(dictionary_dnk, clients)
#         self.assertEqual(get_client.name, self.Veiko_Talirano.name)
#
#     def test_get_dict_from_instances(self):
#         valid_dnk_data = {"FGA": "21,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
#                           "CSF1P0": "21,22", "D18S51": "13,16", "D21S11": "29,30.2",
#                           "D2S441": "14,14", "D5S818": "&&,13", "D7S820": "12,12",
#                           "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
#                           "D19S433": "13,13", "D1S1656": "21,22", "D2S1338": "19,20",
#                           "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
#                           "Penta_D": "11,12", "Penta_E": "12,13", "D10S1248": "15,15",
#                           "D22S1045": "15,15"}
#         dnk_instance = DnkForm(valid_dnk_data).save(commit=False)
#         dnk_instance.child = self.child
#         dnk_instance.save()
#
#         locus_dict = get_dict_from_instance(dnk_instance)
#         self.assertIn("Penta D", locus_dict)
#         self.assertEqual(locus_dict, {"FGA": "21,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
#                                       "CSF1P0": "21,22", "D18S51": "13,16", "D21S11": "29,30.2",
#                                       "D2S441": "14,14", "D5S818": "&&,13", "D7S820": "12,12",
#                                       "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
#                                       "D19S433": "13,13", "D1S1656": "21,22", "D2S1338": "19,20",
#                                       "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
#                                       "Penta D": "11,12", "Penta E": "12,13", "D10S1248": "15,15",
#                                       "D22S1045": "15,15"})
#
#     def test_pdf_extract_text(self):
#         pdf_path = 'pdf_for_test/mother_and_child.pdf'
#         csv_file_path = pdf_extract_text(pdf_path)
#         if 'test' in os.environ.get('DJANGO_SETTINGS_MODULE'):
#             self.assertEqual(csv_file_path,
#                              '/home/runner/work/TextExtractPdf/TextExtractPdf/work_dir/upload_file/csv_files/Tasu_Vasile.csv')
#         else:
#             self.assertEqual(csv_file_path,
#                              '/home/rodion/Desktop/ExtractTextPdf/work_dir/upload_file/csv_files/Tasu_Vasile.csv')
#
#     def test_pdf_not_extract_text(self):
#         pdf_path = 'pdf_for_test/RRodion.pdf'
#         csv_file_path = pdf_extract_text(pdf_path)
#         self.assertEqual(csv_file_path, None)
#
#     def test_retrieve_values(self):
#         if 'test' in os.environ.get('DJANGO_SETTINGS_MODULE'):
#             csv_path = '/home/runner/work/TextExtractPdf/TextExtractPdf/work_dir/upload_file/csv_files/Tasu_Vasile.csv'
#         else:
#             csv_path = '/home/rodion/Desktop/ExtractTextPdf/work_dir/upload_file/csv_files/Tasu_Vasile.csv'
#         name, locus_dict = retrieve_values(csv_path)
#
#         expected_name = 'Tasu Vasile'
#         expected_locus_dict = {"FGA": "21,22", "vWA": "16,19", "THO1": "8,9", "TPOX": "8,8",
#                                "CSF1P0": "11,14", "D18S51": "13,16", "D21S11": "29,30.2",
#                                "D2S441": "11,14", "D5S818": "13,13", "D7S820": "12,12",
#                                "D12S391": "19,20", "D13S317": "8,11", "D16S539": "10,11",
#                                "D19S433": "13,13", "D1S1656": "14,16.3", "D2S1338": "19,20",
#                                "D3S1358": "15,16", "D6S1043": "11,12", "D8S1179": "14,14",
#                                "Penta D": "11,12", "Penta E": "12,13", "D10S1248": "15,15",
#                                "D22S1045": "15,15"}
#
#         self.assertEqual(name, expected_name)
#         self.assertEqual(locus_dict, expected_locus_dict)
#
#         if os.path.exists(csv_path):
#             os.remove(csv_path)
