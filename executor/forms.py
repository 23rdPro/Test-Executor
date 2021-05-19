# import os
from django import forms

from users.models import User
from .models import Executor
from django.utils.translation import gettext_lazy as _


class ExecutorForm(forms.ModelForm):

    def __init__(self, user, *args, **kwargs):  # guarantees each user can only initiate a test under their name
        super(ExecutorForm, self).__init__(*args, **kwargs)
        self.fields['tester'].queryset = User.objects.filter(username=user)

    class Meta:
        model = Executor
        fields = ('environment_id', 'file', 'tester')
        help_texts = {
            'tester': _('Only logged in user per view'),
            'file': _('Select one or more files using command key')

        }

# to upload test files
# class UploadTestFileForm(forms.Form):
#     file = forms.FileField(help_text=_('Upload file containing python test'))
#
#     def clean_file(self):
#         file = self.cleaned_data['file']
#         if not file.name.endswith('.py'):
#             raise forms.ValidationError(_('Upload must be a Python file'), code='invalid')
#
#         if os.path.isfile('executor/tests/' + 'test_' + file.name):
#             raise forms.ValidationError(_('File already exists'))
#
#         return file
