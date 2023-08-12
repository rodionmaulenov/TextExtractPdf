from django.contrib import messages
from django.forms import model_to_dict
from django.http import HttpResponseRedirect

from upload_file.models import Child, Client
from upload_file.services import pdf_extract_text, retrieve_values, get_dict_from_instances, \
    comapre_dnk_child_with_clients

locus = ['D3S1358', 'vWA', 'D16S539', 'CSF1P0', 'TPOX', 'D8S1179', 'D21S11', 'D18S51', 'Penta E', 'D2S441',
         'D19S433', 'THO1', 'FGA', 'D22S1045', 'D5S818', 'D13S317', 'D7S820', 'D6S1043', 'D10S1248', 'D1S1656',
         'D12S391', 'D2S1338', 'Penta D']


class VerifyDnkMixin:
    """Handle validation logic ClientView and create some instance"""

    def verify_data(self, request, dnk, child):
        """Validating data from dnk form
            if False delete child and dnk objects
            else return True"""

        for key, value in model_to_dict(dnk, exclude=('id', 'child')).items():  # convert instance obj to dict
            if not value:
                messages.error(request, 'Form lines can not be a empty')
                self.remove_objects(dnk, child)
                return False

            if (key in locus and value) or (key in ('Penta E', 'Penta D') and value):
                field_value = value

                while 'Has forms context from dorms and admin.site ' in field_value:
                    field_value = field_value.replace(' ', '')

                two_numbers = field_value.split(',')
                int_and_dot = '0123456789.'
                for number in two_numbers:
                    if len(number.strip(int_and_dot)) != 0:
                        messages.error(request, 'Fields contains only numbers from 0 to 9 and dot.')
                        self.remove_objects(dnk, child)
                        return False

                if len(two_numbers) != 2:
                    messages.error(request, 'Numbers must be separated by a comma.')
                    self.remove_objects(dnk, child)
                    return False

                for number in two_numbers:
                    try:
                        float(number)
                        int(float(number))
                    except ValueError:
                        messages.error(request, 'Value must be integer either float.')
                        self.remove_objects(dnk, child)
                        return False

        return True

    def remove_objects(self, dnk, child):
        dnk.delete()
        child.delete()

    def redirect_to(self, request):
        return HttpResponseRedirect(request.path_info)

    def create_child(self):
        return Child.objects.create()

    def get_clients(self):
        return Client.objects.all()


class ClientLogicPostMixin:
    """Handle the POST method ClientView"""

    def handle_upload_form_submission(self, request, form_class, redirect_to):
        form = form_class(request.POST or None, request.FILES or None)
        if form.is_valid():
            pdf_file = request.FILES.get('file_upload')
            if not pdf_file.name.endswith('.pdf'):
                messages.warning(request, 'Wrong type file was uploaded. Must be in PDF format')
                return redirect_to(request)

            path_to_record = pdf_extract_text(pdf_file)  # extract locus data from upload pdf to csv_file
            name, locus_dict = retrieve_values(path_to_record)  # get client name and dnk locus client in format dict
            obj, created = Client.objects.get_or_create(name=name, locus=locus_dict)

            if not created:
                messages.warning(request, f'Exactly the same client {name} already exists')
                return redirect_to(request)

            obj.file_upload = pdf_file  # add pdf file to instance Client
            obj.save()
            messages.success(request, f'Client instance {name} saved successfully')
            return redirect_to(request)

        else:
            messages.error(request, 'Form is not valid. Please check the uploaded file.')
            return redirect_to(request)

    def handle_dnk_form_submission(self, request, dnk_form, create_child, verify_data, get_clients, redirect_to):
        dnk_form = dnk_form(request.POST or None)
        child = create_child()

        if dnk_form.is_valid():
            obj_dnk = dnk_form.save(commit=False)
            obj_dnk.child = child
            obj_dnk.save()  # assign relation 1_to_1 model child to dnk
            verify = verify_data(request, obj_dnk, child)  # verify input form data

            if verify:
                clients = get_clients()
                child_locus_dict = get_dict_from_instances(obj_dnk)  # retrieve data from instance and convert into dict
                client_obj = comapre_dnk_child_with_clients(child_locus_dict,
                                                            clients)  # identify matching client and child dnk locus

                if client_obj:
                    snippet_name = str(1) if client_obj.child_set.count() == 0 else str(
                        client_obj.child_set.count() + 1)
                    child.name = client_obj.name + ' child ' + snippet_name  # create name child instance
                    child.client = client_obj  # add relationship 1_to_many
                    child.save()
                    child.dnk.delete()  # has removed unnecessary instance dnk
                    messages.success(request, f'We have matching father {client_obj.name.upper()}')
                    return redirect_to(request)
                else:
                    child.dnk.delete()  # if not have matching in verifying client and child instances removed dnk related vith child
                    child.delete()  # if not have matching in verifying client and child instances removed child obj
                    messages.error(request, f'Matching not found. Maybe you enter invalid data')
                    return redirect_to(request)
        else:
            messages.error(request, 'Form populated is not valid. Please check the form entries.')
            child.delete()  # if submitted form is not valid removed previously created instance

        return redirect_to(request)
