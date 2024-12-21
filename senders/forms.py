from django import forms

from senders.models import Mailing, Message, Recipient


class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_class = "form-control"

        for field in self.fields.values():
            field.widget.attrs["class"] = (
                f"{field.widget.attrs.get('class', '')} {default_class}"
            )


class RecipientForm(BaseForm):
    class Meta:
        model = Recipient
        fields = (
            "email",
            "first_name",
            "last_name",
            "middle_name",
            "comment",
        )
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "middle_name": forms.TextInput(attrs={"class": "form-control"}),
            "comment": forms.Textarea(attrs={"class": "form-control"}),
        }


class MessageForm(BaseForm):
    class Meta:
        model = Message
        fields = ("subject", "body")
        widgets = {
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control"}),
        }


class MailingForm(BaseForm):
    class Meta:
        model = Mailing
        fields = (
            "start_date",
            "end_date",
            "status",
            "message",
            "recipients",
        )
        widgets = {
            "start_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "end_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "status": forms.Select(attrs={"class": "form-control"}),
            "message": forms.Select(attrs={"class": "form-control"}),
            "recipients": forms.CheckboxSelectMultiple(
                attrs={"class": "form-check"}
            ),
        }
