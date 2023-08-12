import csv
import os
import tabula
from django.forms import model_to_dict

locus = ['D3S1358', 'vWA', 'D16S539', 'CSF1P0', 'TPOX', 'D8S1179', 'D21S11', 'D18S51', 'Penta E', 'D2S441',
         'D19S433', 'THO1', 'FGA', 'D22S1045', 'D5S818', 'D13S317', 'D7S820', 'D6S1043', 'D10S1248', 'D1S1656',
         'D12S391', 'D2S1338', 'Penta D']


def pdf_extract_text(pdf_file=None):
    """First get pdf file
     second create new directory
      and return path to writing file"""
    table = tabula.read_pdf(pdf_file, pages='3')  # get 3 page from pdf
    csv_data = table[0].to_csv(index=False)  # get table without indexing rows
    file_name = '_'.join(table[0].columns[1].split())  # forms name file by name client

    csv_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'csv_files')  # mount storage directory

    if not os.path.exists(csv_directory):
        os.makedirs(csv_directory)

    csv_file_path = os.path.join(csv_directory,
                                 f"{file_name}.csv")  # create path to storage directory with specific file

    with open(csv_file_path, 'w') as csv_file:
        csv_file.write(csv_data)  # writes csv file from path to previously prepared csv directory

    return csv_file_path  # path to file


def retrieve_values(file_path):
    """Obtain the values from file"""
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)  # read csv file with method "reader" from csv package
        locus_dict = {}
        name = ''
        for ind, line in enumerate(csv_reader):
            key, value = line
            if len(line) != 2:
                break
            if ind == 0:
                name += value
            if key in locus:
                locus_dict[key] = value

    os.remove(file_path)

    return name, locus_dict


def get_dict_from_instances(obj_dnk):
    """Derive dict from DNK objects"""
    locus_dict_from_object = {}
    for key, value in model_to_dict(obj_dnk, exclude=('id', 'child'), fields=('D3S1358', 'vWa', 'D16S539')).items():
        if key == 'Penta_D' or key == 'Penta_E':
            key = 'Penta D' if key == 'Penta_D' else 'Penta E'
            locus_dict_from_object[key] = value
        locus_dict_from_object[key] = value
    return locus_dict_from_object


def comapre_dnk_child_with_clients(dictionary_dnk, client_list):
    """Find father by locus child"""
    count_matching = []
    client = None
    for obj in client_list:
        client_locus = obj.locus

        for key, value in dictionary_dnk.items():
            if not key:
                return client
            if key in client_locus:
                dnk_child_to_match = value.split(',')
                client_property_value = client_locus[key]
                numbers_in_property = [num.strip() for num in client_property_value.split(',')]

                count_matching.append(any(num.strip() in numbers_in_property for num in dnk_child_to_match))

        if all(count_matching):
            client = obj

    return client
