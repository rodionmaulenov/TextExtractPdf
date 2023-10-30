from django import forms

locus = ['D3S1358', 'vWA', 'D16S539', 'CSF1PO', 'TPOX', 'D8S1179', 'D21S11', 'D18S51', 'Penta E',
         'D2S441', 'D19S433', 'THO1', 'FGA', 'D22S1O45', 'D5S818', 'D13S317', 'D7S82O', 'D6S1O43',
         'D1OS1248', 'D1S1656', 'D12S391', 'D2S1338']


class LocusForm(forms.Form):
    for locus_name in locus:
        locals()[locus_name] = forms.CharField(max_length=100, required=False)

    def clean(self):
        cleaned_data = super().clean()

        for locus_name in locus:
            value = cleaned_data.get(locus_name, '')

            if not value:
                return cleaned_data

            integer_and_dot = '0123456789.'
            while ' ' in value:
                value = value.replace(' ', '')

            try:
                _, __ = value.split(',')
                if not _ or not __:
                    self.add_error(locus_name, forms.ValidationError("two numbers"))
            except ValueError:
                self.add_error(locus_name, forms.ValidationError("two numbers"))

            share_value = value.split(',')
            if len(share_value) != 2:
                self.add_error(locus_name, forms.ValidationError("comma separated"))
            try:

                if len(share_value[0].strip(integer_and_dot)) != 0 or len(
                        share_value[1].strip(integer_and_dot)) != 0:
                    self.add_error(locus_name, forms.ValidationError(f"contain {integer_and_dot}"))
            except IndexError:
                pass

        return cleaned_data
