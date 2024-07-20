from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Submit


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class PdfForm(forms.Form):
    file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Compress PDFs',
                Field('file',type='file',css_class='form-control form-control-lg',id='PdfForm_file'),
            ),
            Submit('submit', 'Submit', css_class='btn btn-warning'),
        )


class MergeForm(forms.Form):
    title = 'Merge PDFs'
    tag_id = 'MergeForm_file'

    file = MultipleFileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                self.title,
                Field('file',type='file',id=self.tag_id,css_class='form-control form-control-lg'),
            ),
            Submit('submit', 'Submit', css_class='btn btn-warning'),
        )


class RotateForm(MergeForm):
    file = forms.FileField()
    title = 'Rotate PDFs'
    tag_id = 'RotateForm_file'