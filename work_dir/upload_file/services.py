import pdfplumber
from django.contrib import messages

from upload_file.models import Client

locus_from_mother_and_child = ['D3S1358', 'vWA', 'D16S539', 'CSF1PO', 'TPOX', 'D8S1179', 'D21S11', 'D18S51', 'Penta E',
                               'D2S441', 'D19S433', 'THO1', 'FGA', 'D22S1O45', 'D5S818', 'D13S317', 'D7S82O', 'D6S1O43',
                               'D1OS1248', 'D1S1656', 'D12S391', 'D2S1338', 'Penta D']


def get_table_from_pdf_file(request, file_pdf):
    """Extract locus from pdf file 'Mother and child' or 'Evrolab' firms"""
    with pdfplumber.open(file_pdf) as pdf:
        try:
            # this is Mother and Child table page
            page = pdf.pages[2]

        except IndexError:
            # this is evrolab table page
            page = pdf.pages[0]

        table = page.extract_table()

        locus_dict = {}
        for row in table:
            key = row[0].replace('0', 'O') if row[0] is not None and '0' in row[0] else row[0]
            if key in locus_from_mother_and_child:
                locus_dict[key] = row[1].replace(' ', '')

        lines_pdf = page.extract_text()

        lines = lines_pdf.split('\n')
        name = ''
        if 'eurolab' in lines_pdf:
            for line in lines:
                if 'Name' in line:
                    name += line.split(':')[-1].strip()
                if name:
                    break
        else:
            for line in lines:
                if 'Locus' in line:
                    name += (line.split()[1] + ' ' + line.split()[2]).strip()
                if name:
                    break

        if locus_dict and name:
            return locus_dict, name

    return None, None


def compare_dnk_child_with_father(child_dnk):
    """Find father by locus child"""
    for father_instance in Client.objects.all():
        father_dnk = father_instance.locus

        child_dnk = [(name, value) for name, value in child_dnk]
        if len(father_dnk) == 15:
            exclude = ['Penta E', 'D2S441', 'D22S1O45', 'D6S1O43', 'D1OS1248', 'D1S1656', 'D12S391', 'Penta D']
            child_dnk = [(name, value) for name, value in child_dnk if name not in exclude]

        list_matching = []
        for key, value in child_dnk:
            if key in father_dnk:
                child_value = value.split(',')
                father_value = father_dnk[key]

                father_locus = [num.strip() for num in father_value.split(',')]
                list_matching.append(any(num.strip() in father_locus for num in child_value))

        if all(list_matching) and len(list_matching) > 1:
            return father_instance
        else:
            list_matching = []

    return None


def verify_form_fields(request, dnk):
    """Validating data from dnk form
        if False delete child and dnk objects
        else return True"""

    items = [(name, value) for name, value in dnk]
    integer_and_dot = '0123456789.'
    for key, value in items:

        while ' ' in value:
            value = value.replace(' ', '')

        if not value:
            messages.error(request, 'Form lines can not be a empty')
            return False

        try:
            share_value = value.split(',')

            if len(share_value[0].strip(integer_and_dot)) != 0 or len(share_value[1].strip(integer_and_dot)) != 0:
                messages.error(request, 'Number should contain only 0123456789.')
                return False
        except IndexError:
            messages.error(request, 'Only two numbers separated by a comma')
            return False

    else:
        return True
