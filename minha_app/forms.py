
from django import forms


class ApiForm(forms.Form):
    pedido = forms.CharField(
    )


class ApicodigoETraduzForm(forms.Form):
    input=forms.CharField(
        widget=forms.TextInput()
    )


class ImageUploadForm(forms.Form):
    image = forms.ImageField(label='Selecione uma imagem')
    names = forms.CharField(
        label='Insira os nomes (separados por vírgulas)',
        widget=forms.Textarea(attrs={'placeholder': 'Nome1, Nome2, Nome3'}),
        required=False  # Torne o campo opcional se desejar
    )



class TraducaoECodigoForm(forms.Form):
    OPERACOES = [
        ('traduzir', 'Traduzir'),
        ('gerar_codigo', 'Gerar Código'),
    ]
    IDIOMAS = [
        ('en', 'Inglês'),
        ('es', 'Espanhol'),
        ('fr', 'Francês'),
        ('de', 'Alemão'),
        ('pt', 'Português'),
        ('it', 'Italiano'),
        ('ru', 'Russo'),
        ('ja', 'Japonês'),
        ('zh', 'Chinês'),
        ('ko', 'Coreano'),
        ('ar', 'Árabe'),
        ('hi', 'Hindi'),
        ('bn', 'Bengali'),
        ('pa', 'Panjabi'),
        ('mr', 'Marathi'),
        ('te', 'Telugu'),
        ('vi', 'Vietnamita'),
        ('ta', 'Tâmil'),
        ('ur', 'Urdu'),
        ('fa', 'Persa'),
        ('gu', 'Guzerate'),
        ('tr', 'Turco'),
        ('pl', 'Polonês'),
        ('uk', 'Ucraniano'),
        ('nl', 'Holandês'),
        ('el', 'Grego'),
        ('sv', 'Sueco'),
        ('da', 'Dinamarquês'),
        ('fi', 'Finlandês'),
        ('no', 'Norueguês'),
        ('hu', 'Húngaro'),
        ('cs', 'Tcheco'),
        ('ro', 'Romeno'),
        ('bg', 'Búlgaro'),
        ('sr', 'Sérvio'),
        ('hr', 'Croata'),
        ('sk', 'Eslovaco'),
        ('sl', 'Esloveno'),
        ('he', 'Hebraico'),
        ('ms', 'Malaio'),
        ('th', 'Tailandês'),
        ('id', 'Indonésio'),
        ('am', 'Amárico'),
        ('sw', 'Suaíli'),
        ('zu', 'Zulu'),
        ('xh', 'Xhosa'),
        ('st', 'Soto do Sul'),
        ('lt', 'Lituano'),
        ('lv', 'Letão'),
        ('et', 'Estoniano'),
        ('is', 'Islandês'),
        ('ga', 'Irlandês'),
        ('cy', 'Galês'),
        ('mt', 'Maltês'),
        ('gl', 'Galego'),
        ('eu', 'Basco')

        # Adicione mais idiomas conforme necessário
    ]

    texto = forms.CharField(label='Texto', widget=forms.Textarea(attrs={'rows': 4}))
    operacao = forms.ChoiceField(label='Operação', choices=OPERACOES)
    idioma = forms.ChoiceField(label='Idioma de Destino', choices=IDIOMAS, required=False)


    
class ImageUploadForm(forms.Form):
    image = forms.ImageField(label="Selecione uma imagem")