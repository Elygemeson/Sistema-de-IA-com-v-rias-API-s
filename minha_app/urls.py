'''from django.urls import path
from .views import criarimagem
from .views import recebeimagem
from .views import traducao_e_codigo_view
from .views import api_sumario

urlpatterns = [
    path('criacao_imagem/', criarimagem, name='criacao_imagem'),
    path('receber_a_imagem', recebeimagem, name='recebe_a_imagem'),
    path('traduzecoda', traducao_e_codigo_view, name ='traduzecoda'),
    path('sumario', api_sumario, name ='sumario' ),
]'''


from django.urls import path
from .views import unified_view

urlpatterns = [
    path('', unified_view, name='unified_view'),
]