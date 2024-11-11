

import tkinter as tk
from tkinter import messagebox
from translator_backend import traduzir_texto  # Corrige o nome do backend

def traduzir():
    texto_original = entrada_texto.get("1.0", tk.END).strip()
    idioma = 'pt' if var_idioma.get() == 'PT' else 'en'
    if texto_original:
        try:
            traducao = traduzir_texto(texto_original, idioma_destino=idioma)
            saida_texto.config(state=tk.NORMAL)
            saida_texto.delete("1.0", tk.END)
            saida_texto.insert(tk.END, traducao)
            saida_texto.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Erro", str(e))
    else:
        messagebox.showwarning("Atenção", "Insira algum texto para traduzir.")

# Interface com Tkinter com tema escuro
root = tk.Tk()
root.title("Tradutor de Inglês-Português")

# Cores do tema
bg_color = "#1e1e1e"        # Fundo da janela e widgets
fg_color = "#f5f5f5"        # Cor do texto principal
highlight_color = "#333333" # Cor de fundo de entrada e saída de texto
button_color = "#444444"    # Cor do botão

# Configuração da janela principal
root.configure(bg=bg_color)
root.geometry("500x400")

# Título e entrada de texto
tk.Label(root, text="Texto para Traduzir:", bg=bg_color, fg=fg_color, font=("Helvetica", 10, "bold")).pack(pady=(10, 5))
entrada_texto = tk.Text(root, height=7, width=50, bg=highlight_color, fg=fg_color, insertbackground=fg_color, font=("Helvetica", 10))
entrada_texto.pack(pady=(0, 10))

# Opções de idioma
var_idioma = tk.StringVar(value='PT')
tk.Radiobutton(root, text="Inglês para Português", variable=var_idioma, value='PT', bg=bg_color, fg=fg_color, selectcolor=button_color, activebackground=bg_color).pack(anchor="w", padx=20)
tk.Radiobutton(root, text="Português para Inglês", variable=var_idioma, value='EN', bg=bg_color, fg=fg_color, selectcolor=button_color, activebackground=bg_color).pack(anchor="w", padx=20)

# Botão Traduzir
tk.Button(root, text="Traduzir", command=traduzir, bg=button_color, fg=fg_color, activebackground=highlight_color, activeforeground=fg_color, font=("Helvetica", 10, "bold"), relief=tk.FLAT).pack(pady=(10, 15))

# Saída de texto traduzido
tk.Label(root, text="Tradução:", bg=bg_color, fg=fg_color, font=("Helvetica", 10, "bold")).pack()
saida_texto = tk.Text(root, height=7, width=50, state=tk.DISABLED, bg=highlight_color, fg=fg_color, font=("Helvetica", 10))
saida_texto.pack(pady=(0, 10))

root.mainloop()

