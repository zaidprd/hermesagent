from django import forms

from .models import Project

_TEXT = "w-full border border-slate-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"


class ProjectForm(forms.ModelForm):
    language = forms.CharField(
        required=False,
        initial="Indonesia",
        widget=forms.TextInput(attrs={"class": _TEXT}),
    )

    class Meta:
        model = Project
        fields = ["name", "niche", "language", "tone", "target_audience"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": _TEXT, "placeholder": "mis. SEO Website A", "autofocus": True}
            ),
            "niche": forms.TextInput(
                attrs={"class": _TEXT, "placeholder": "mis. fikih ibadah, parenting Islami"}
            ),
            "tone": forms.TextInput(
                attrs={"class": _TEXT, "placeholder": "mis. santai & mengedukasi"}
            ),
            "target_audience": forms.TextInput(
                attrs={"class": _TEXT, "placeholder": "mis. muslim usia 25–40 tahun"}
            ),
        }
        labels = {
            "name": "Nama project",
            "niche": "Niche / topik",
            "language": "Bahasa",
            "tone": "Gaya bahasa",
            "target_audience": "Target pembaca",
        }

    def clean_language(self):
        return self.cleaned_data.get("language") or "Indonesia"


class ProjectThreadsForm(forms.ModelForm):
    threads_access_token = forms.CharField(
        required=False,
        label="Access Token",
        widget=forms.PasswordInput(
            render_value=True,
            attrs={"class": _TEXT, "placeholder": "EAAxxxxxxx..."},
        ),
    )

    class Meta:
        model = Project
        fields = ["threads_user_id", "threads_access_token"]
        widgets = {
            "threads_user_id": forms.TextInput(
                attrs={"class": _TEXT, "placeholder": "1234567890"}
            ),
        }
        labels = {
            "threads_user_id": "Threads User ID",
            "threads_access_token": "Access Token",
        }
        help_texts = {
            "threads_user_id": "Nomor ID akun Threads kamu (bukan username).",
            "threads_access_token": "Long-lived token dengan scope threads_content_publish.",
        }


class ProjectWPForm(forms.ModelForm):
    wp_app_password = forms.CharField(
        required=False,
        label="Application Password",
        widget=forms.PasswordInput(
            render_value=True,
            attrs={"class": _TEXT, "placeholder": "xxxx xxxx xxxx xxxx xxxx xxxx"},
        ),
    )

    class Meta:
        model = Project
        fields = ["wp_site_url", "wp_username", "wp_app_password"]
        widgets = {
            "wp_site_url": forms.URLInput(
                attrs={"class": _TEXT, "placeholder": "https://myblog.com"}
            ),
            "wp_username": forms.TextInput(
                attrs={"class": _TEXT, "placeholder": "admin"}
            ),
        }
        labels = {
            "wp_site_url": "URL WordPress",
            "wp_username": "Username WordPress",
            "wp_app_password": "Application Password",
        }
