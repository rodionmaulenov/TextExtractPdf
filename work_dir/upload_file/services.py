import pdfplumber

from upload_file.models import Client

locus_from_mother_and_child = ['D3S1358', 'vWA', 'D16S539', 'CSF1PO', 'TPOX', 'D8S1179', 'D21S11', 'D18S51', 'Penta E',
                               'D2S441', 'D19S433', 'THO1', 'FGA', 'D22S1O45', 'D5S818', 'D13S317', 'D7S82O', 'D6S1O43',
                               'D1OS1248', 'D1S1656', 'D12S391', 'D2S1338']


class ProcessUploadedFileMixin:
    def process_uploaded_file(self, uploaded_file):
        """
        Main logic how to upload, validating logic, getting table page, and save
        pdf file
        """

        page = self.get_table_page(uploaded_file)
        father_dict = self.get_father_locus_and_name(page)

        if 'father_name' in father_dict and 'father_locus' in father_dict:
            father_name = father_dict['father_name']
            father_locus = father_dict['father_locus']

            father, created = Client.objects.get_or_create(
                name=father_name,
                locus=father_locus
            )

            if created:
                father.name = father_name
                father.locus = father_locus
                father.file_upload = uploaded_file
                father.save()
                return {'message': f'Father {father_name} saved successfully', 'log': 'success'}
            else:
                return {'message': f'Father {father_name} already exists', 'log': 'caution'}
        else:
            return father_dict

    def get_table_page(self, file_pdf):
        """Get specified page from PDF file"""

        with pdfplumber.open(file_pdf) as pdf:
            try:
                # this is Mother and Child table page
                page = pdf.pages[2]
                return page

            except IndexError:
                # this is evrolab table page
                page = pdf.pages[0]
        return page

    def get_father_locus_and_name(self, page):
        """
        Getting father locus and his name from table
        in other case return message error to server
        """

        father_dict = {
            'message': f'Error processing',
            'log': 'error'
        }
        try:
            table = page.extract_table()

            father_locus = {}
            for row in table:
                key = row[0].replace('0', 'O') if row[0] is not None and '0' in row[0] else row[0]
                if key in locus_from_mother_and_child:
                    father_locus[key] = row[1].replace(' ', '')

            lines_pdf = page.extract_text()

            lines = lines_pdf.split('\n')
            father_name = ''
            if 'eurolab' in lines_pdf:
                for line in lines:
                    if 'Name' in line:
                        father_name += line.split(':')[-1].strip()
                    if father_name:
                        break
            else:
                for line in lines:
                    if 'Locus' in line:
                        father_name += (line.split()[1] + ' ' + line.split()[2]).strip()
                    if father_name:
                        break

            if father_locus and father_name:
                father_dict['father_locus'] = father_locus
                father_dict['father_name'] = father_name
                return father_dict

        except Exception:
            return father_dict

        return father_dict
