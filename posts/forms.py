from typing import Any
from django import forms
from posts.models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["header", "description", "rate", "is_published", "image"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(attrs={"rows": 3, "placeholder": "Your comment..."})
        }



# class CommonPostForm(forms.Form):
#     header = forms.CharField(max_length=255, min_length=5, required=True)
#     description = forms.CharField()
#     rate = forms.IntegerField(max_value=5, min_value=1, required=True)
#     is_published = forms.BooleanField(disabled=False)

#     def clean_header(self):
#         header = self.cleaned_data.get("header")
#         if header == "запрещенное слово":
#             raise forms.ValidationError(message="Вы ввели запрещенное слово!")

#         return header

#     def clean(self) -> dict[str, Any]:
#         cleaned_data = super().clean()

#         rate = cleaned_data.get("rate")

#         if rate < 5:
#             raise forms.ValidationError("Рейтинг меньше 5 не подходит!")

#         return cleaned_data
