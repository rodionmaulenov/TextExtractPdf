from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator

from input_text.forms import LocusForm
from input_text.services import CompareLocusMixin
from home_api.decorators import optimized_view_decorator


@method_decorator(
    decorator=optimized_view_decorator(['users_input_text', 'users_upload']),
    name='dispatch'
)
class InputTextView(CompareLocusMixin, View):
    template_name = 'input_text/input.html'

    def get(self, request):
        form = LocusForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LocusForm(request.POST)
        if form.is_valid():
            list_father = self.compare_dnk(request, form)
            self.get_message(request, list_father)

        return render(request, self.template_name, {'form': form})
