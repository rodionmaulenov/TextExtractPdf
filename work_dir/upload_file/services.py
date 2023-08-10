import csv
import os
import tabula

from django.contrib import messages

locus = ['D3S1358', 'vWa', 'D16S539', 'CSF1P0', 'TPOX', 'D8S1179', 'D21S11', 'D18S51', 'Penta E', 'D2S441',
         'D19S433', 'THO1', 'FGA', 'D22S1045', 'D5S818', 'D13S317', 'D7S820', 'D6S1043', 'D10S1248', 'D1S1656',
         'D12S391', 'D2S1338', 'Penta D']


def pdf_extract_text(pdf_file=None):
    """First get pdf file
     second create new directory
      and return path to writing file"""
    table = tabula.read_pdf(pdf_file, pages='3')
    csv_data = table[0].to_csv(index=False)
    file_name = '_'.join(table[0].columns[1].split())
    print(csv_data)
    csv_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'csv_files')

    if not os.path.exists(csv_directory):
        os.makedirs(csv_directory)

    csv_file_path = os.path.join(csv_directory, f"{file_name}.csv")

    with open(csv_file_path, 'w') as csv_file:
        csv_file.write(csv_data)

    return csv_file_path


def retrieve_values(file_path):
    """Obtain the values from file"""
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
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

    return name, locus_dict


def get_dict_from_instances(objects_list):
    """Derive dict from DNK objects"""
    locus_dict_from_objects = {}
    for obj in objects_list:
        locus_dict_from_objects[obj.locus] = obj.data
    return locus_dict_from_objects


def find_father_by_locus(dictionary, client_list):
    """Find father by locus child"""
    count_matching = []
    client = None
    for obj in client_list:
        locus_property = obj.locus

        for key, value in dictionary.items():
            if key in locus_property:
                values_to_match = value.split(',')
                property_value = locus_property[key]
                numbers_in_property = [num.strip() for num in property_value.split(',')]

                count_matching.append(any(num.strip() in numbers_in_property for num in values_to_match))

        if all(count_matching):
            client = obj

    return client


def verify_data(request, objs, child):
    """validate data from formset"""
    data = None
    for obj in objs:
        data = obj.data
    if data is None:
        messages.error(request, 'Form lines can not be a empty')
        child.delete()
        return False
    while ' ' in data:
        data = data.replace(' ', '')
    res = data.split(',')

    int_and_dot = '0123456789.'
    for i in res:
        if len(i.strip(int_and_dot)) != 0:
            messages.error(request, 'Value must be integer either float. "22,11" or "1.4,6"')
            child.delete()
            return False

    if len(res) != 2:
        messages.error(request, 'Two numbers must be separated by a comma. "22.1,11.1" or "1.4,6"')
        child.delete()
        return False

    for val in res:
        try:
            float(val)
            int(float(val))
        except ValueError:
            messages.error(request, 'Value must be integer either float. "10,13" or "0.6,11"')
            child.delete()
            return False

    return True
