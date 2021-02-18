from django import forms
from qna.models import Board

class WriteForm(forms.ModelForm):
    class Meta:
        model = Board

        fields = ['title', 'author', 'content', 'image']#, 'password']
        labels = {
            'title': "",
            'author': '',
            'content': '',
            'image': '',
            #'password': '',
        }

        widgets = {
            'title': forms.TextInput(attrs={'placeholder':'제목'}),
            'author': forms.TextInput(attrs={'placeholder':'이름'}),
            'content': forms.TextInput(attrs={'placeholder':'내용 최대xx자'}),
            'image': forms.TextInput(attrs={'placeholder':'이미지 등록'}),
            #'password': forms.PasswordInput(attrs={'placeholder':'글수정,삭제시 필요한 비밀번호'}),
        }           