
'''
import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse
from .forms import ApicodigoETraduzForm, ImageUploadForm, TraducaoECodigoForm, ApiForm
import requests 
import base64
from io import BytesIO
import os
from PIL import Image
import json
import uuid
from django.conf import settings
from django.core.files.storage import default_storage

# Configuração da API de tradução e geração de código


#view para criação de imagens

api_hugging_face = "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"  

def criarimagem(request):
# Defina o seu endpoint e a chave da API OpenAI
    form = ApicodigoETraduzForm()

    if request.method == 'POST':
        form = ApicodigoETraduzForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data['input']
            endpoint = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"


            # Descrição do que deseja transformar em imagem

            # Configura os parâmetros da requisição
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_hugging_face}",
            }

            payload = {"inputs": prompt}

            # Faz a requisição para a API
            response = requests.post(endpoint, headers=headers, json=payload)

            # Verifica se a requisição foi bem-sucedida
            if response.status_code == 200:
                image_data = response.content
                image = Image.open(BytesIO(image_data))

                image_name = f"{uuid.uuid4()}.png"
                image_path = os.path.join(settings.MEDIA_ROOT, image_name)
                image.save(image_path)
                print("Imagem gerada com sucesso!")
                image_url = f"{settings.MEDIA_URL}{image_name}"
                return render(request, 'minha_app/criacao_imagem.html', {'form': form, 'imagem': request.build_absolute_uri(image_url)})
            else:
                print("Erro:", response.status_code, response.text)
    return render(request, 'minha_app/criacao_imagem.html', {'form': form})





# View para tradução e geração de código
api_key_google = "AIzaSyApiBUucvHYTjPeZnWZnfwj8ZZQ3blxl5A"
genai.configure(api_key=api_key_google)

def traducao_e_codigo_view(request):
    resultado = None
    dados_api = ""
    form = TraducaoECodigoForm()  # Inicializa o formulário

    if request.method == 'POST':
        form = TraducaoECodigoForm(request.POST)
        if form.is_valid():
            texto = form.cleaned_data['texto']
            operacao = form.cleaned_data['operacao']
            idioma = form.cleaned_data.get('idioma', 'en')  # Define inglês como padrão

            try:
                # Inicializa o modelo
                model = genai.GenerativeModel(model_name="gemini-1.5-flash")

                # Realiza a operação baseada no tipo solicitado
                if operacao == 'traduzir':
                    prompt = f"Traduza o seguinte texto para {idioma}: {texto}"
                    response = model.generate_content(prompt)
                elif operacao == 'gerar_codigo':
                    response = model.generate_content(texto)

                # Extrai o texto da resposta
                dados_api = response.text if hasattr(response, 'text') else str(response)

            except Exception as e:
                dados_api = f"Ocorreu um erro ao chamar a API: {str(e)}"

    # Renderiza o template com `dados_api`
    return render(request, 'minha_app/traducao_e_codigo.html', {'form': form, 'dados': dados_api})


api_key = "AIzaSyApiBUucvHYTjPeZnWZnfwj8ZZQ3blxl5A"
genai.configure(api_key=api_key)  # Configura a chave da API

def api_sumario(request):
    form = ApiForm()  # Inicializa o formulário
    resposta = None
    dados_api = ""

    if request.method == 'POST':
        form = ApiForm(request.POST)  # Cria uma instância do formulário com os dados do POST
        if form.is_valid():
            texto = form.cleaned_data['pedido']  # Captura o texto enviado pelo usuário
            
            try:
                # Inicializa o modelo generativo
                model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                
                # Cria o prompt para sumarização
                prompt = f"Sumarize o seguinte texto: {texto}"
                response = model.generate_content(prompt)  # Chamada para a API
                
                # Extrai o resultado da resposta da API
                dados_api = response.text if hasattr(response, 'text') else str(response)
                resposta = dados_api  # Sumarização gerada

            except Exception as e:
                dados_api = f"Ocorreu um erro ao chamar a API: {str(e)}"

    # Renderiza o template com o formulário e os resultados
    return render(request, 'minha_app/base.html', {
        'form': form,
        'resposta': resposta,
        'dados': dados_api
    })
'''



import google.generativeai as genai
from django.shortcuts import render
from django.http import JsonResponse
from .forms import ApicodigoETraduzForm, TraducaoECodigoForm, ApiForm, ImageUploadForm
import requests
import base64
from io import BytesIO
import os
from PIL import Image
import uuid
from django.conf import settings
from diffusers import BitsAndBytesConfig, SD3Transformer2DModel
from diffusers import StableDiffusion3Pipeline
import torch

# Configuração das chaves das APIs
api_hugging_face = "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"
api_key_google = "AIzaSyApiBUucvHYTjPeZnWZnfwj8ZZQ3blxl5A"
genai.configure(api_key=api_key_google)

# View unificada para criação de imagem, tradução/geração de código e sumarização
def unified_view(request):
    imagem_url = None
    dados_api = ""
    resposta = None
    extracted_text = ""
    form_imagem = ApicodigoETraduzForm()
    form_traducao_codigo = TraducaoECodigoForm()
    form_sumario = ApiForm()
    form_extracao_texto = ImageUploadForm()

    if request.method == 'POST':
        action = request.POST.get('action')

        # Ação para criar imagem
        if action == 'create_image':
            form_imagem = ApicodigoETraduzForm(request.POST)
            if form_imagem.is_valid():
                prompt = form_imagem.cleaned_data['input']
                endpoint = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_hugging_face}",
                }
                payload = {"inputs": prompt}
                response = requests.post(endpoint, headers=headers, json=payload)

                if response.status_code == 200:
                    image_data = response.content
                    image = Image.open(BytesIO(image_data))
                    image_name = f"{uuid.uuid4()}.png"
                    image_path = os.path.join(settings.MEDIA_ROOT, image_name)
                    image.save(image_path)
                    imagem_url = f"{settings.MEDIA_URL}{image_name}"
                else:
                    dados_api = f"Erro ao gerar imagem: {response.status_code} - {response.text}. Aguarde de 1 à 8 minutos pela resposta da API."

        # Ação para tradução e geração de código
        elif action == 'translate_code':
            form_traducao_codigo = TraducaoECodigoForm(request.POST)
            if form_traducao_codigo.is_valid():
                texto = form_traducao_codigo.cleaned_data['texto']
                operacao = form_traducao_codigo.cleaned_data['operacao']
                idioma = form_traducao_codigo.cleaned_data.get('idioma', 'en')
                try:
                    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                    if operacao == 'traduzir':
                        prompt = f"Traduza o seguinte texto para {idioma}: {texto}"
                        response = model.generate_content(prompt)
                    elif operacao == 'gerar_codigo':
                        response = model.generate_content(texto)
                    dados_api = response.text if hasattr(response, 'text') else str(response)
                except Exception as e:
                    dados_api = f"Ocorreu um erro ao chamar a API: {str(e)}"

        # Ação para sumarização
        elif action == 'generate_summary':
            form_sumario = ApiForm(request.POST)
            if form_sumario.is_valid():
                texto = form_sumario.cleaned_data['pedido']
                try:
                    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
                    prompt = f"Sumarize o seguinte texto: {texto}"
                    response = model.generate_content(prompt)
                    resposta = response.text if hasattr(response, 'text') else str(response)
                except Exception as e:
                    resposta = f"Ocorreu um erro ao chamar a API: {str(e)}"

        # Ação para extrair texto de imagem
        elif action == 'extract_text':
            form_extracao_texto = ImageUploadForm(request.POST, request.FILES)
            if form_extracao_texto.is_valid():
                image_file = request.FILES['image']
                image = Image.open(image_file).convert("RGB")

                buffered = BytesIO()
                image.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

                endpoint = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
                headers = {
                    "Authorization": f"Bearer {api_hugging_face}",
                }
                payload = {"inputs": img_str}

                response = requests.post(endpoint, headers=headers, json=payload)

                if response.status_code == 200:
                    result = response.json()
                    extracted_text = result[0].get("generated_text", "Legenda não encontrada.") if isinstance(result, list) else "Legenda não encontrada."
                else:
                    extracted_text = f"Erro ao processar a imagem: {response.status_code} - {response.text}"

    return render(request, 'minha_app/unified_page.html', {
        'form_imagem': form_imagem,
        'form_traducao_codigo': form_traducao_codigo,
        'form_sumario': form_sumario,
        'form_extracao_texto': form_extracao_texto,
        'imagem_url': imagem_url,
        'dados': dados_api,
        'resposta': resposta,
        'extracted_text': extracted_text,
    })