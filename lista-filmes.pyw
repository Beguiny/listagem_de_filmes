import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import json
from datetime import datetime
import os

# Adicione essa variável no início do seu código
PROXIMO_ID = 1

# Lista de serviços de streaming ordenados alfabeticamente
onde_opcoes = ["Apple TV", "Baixar", "Cinema", "Disney+", "GloboPlay", "HBO+", "Netflix", "Prime Video", "Star+"]
onde_opcoes.sort()

class AdicionarFilmePopup:
    def __init__(self, parent, callback, alteracao=False, filme=None):
        self.popup = tk.Toplevel(parent)
        self.popup.title("Adicionar/Alterar Filme")

        self.callback = callback

        # Variáveis de controle para os campos de entrada
        self.var_nome = tk.StringVar()
        self.var_genero = tk.StringVar()
        self.var_onde = tk.StringVar(value=onde_opcoes[0])  # Defina um valor padrão
        self.var_vontade = tk.IntVar()
        self.var_nota = tk.IntVar()
        self.var_visto = tk.BooleanVar()



        # Adicione a variável de controle para o ID
        self.var_id = tk.IntVar()

        # Criar e posicionar os widgets do formulário
        tk.Label(self.popup, text="ID:", width=10).pack()
        tk.Entry(self.popup, textvariable=self.var_id, state='readonly', width=10).pack()

        tk.Label(self.popup, text="Nome:", width=40).pack()
        tk.Entry(self.popup, textvariable=self.var_nome, width=50).pack()

        tk.Label(self.popup, text="Gênero:", width=30).pack()
        tk.Entry(self.popup, textvariable=self.var_genero, width=40).pack()

        tk.Label(self.popup, text="Onde:", width=20).pack()
        self.combobox_onde = ttk.Combobox(self.popup, values=onde_opcoes, textvariable=self.var_onde, width=28)
        self.combobox_onde.pack()

        tk.Label(self.popup, text="Vontade:", width=20).pack()
        tk.Scale(self.popup, from_=0, to=10, orient=tk.HORIZONTAL, variable=self.var_vontade, length=300).pack()

        # Exibir o campo "Nota" apenas durante a alteração
        if alteracao:
            tk.Checkbutton(self.popup, text="Visto", variable=self.var_visto).pack()

            tk.Label(self.popup, text="Nota:", width=20).pack()
            tk.Scale(self.popup, from_=0, to=10, orient=tk.HORIZONTAL, variable=self.var_nota, length=300).pack()

            # Se for uma alteração, preencher os campos com os dados do filme
            if filme:
                self.var_id.set(filme.get("ID", ""))
                self.var_nome.set(filme.get("Nome", ""))
                self.var_genero.set(filme.get("Gênero", ""))
                self.var_onde.set(filme.get("Onde", ""))
                self.var_vontade.set(filme.get("Vontade", 0))
                self.var_nota.set(filme.get("Nota", 0))
                self.var_visto.set(filme.get("Visto", False))
        else:
            # Se não for alteração, oculta o campo "Visto"
            self.var_visto.set(False)

        tk.Button(self.popup, text="Salvar", command=self.salvar_filme).pack()

    def salvar_filme(self):
        roaming_dir = os.path.join(os.getenv('APPDATA'), 'Lista de filmes')
        os.makedirs(roaming_dir, exist_ok=True)
        file_path = os.path.join(roaming_dir, "registros_filmes.json")
        with open(file_path, "w") as file:
            json.dump(self.lista_filmes, file)
        # Adiciona a data/hora de inclusão
        agora = datetime.now()
        data_hora_inclusao = agora.strftime("%H:%M %d/%m/%Y")

        # Chama a função de callback no objeto pai
        self.callback({
            "ID": self.var_id.get() if self.var_id.get() else self.gerar_novo_id(),  # Use a variável de controle do ID
            "Nome": self.var_nome.get(),
            "Gênero": self.var_genero.get(),
            "Onde": self.var_onde.get(),
            "Vontade": self.var_vontade.get(),
            "Nota": self.var_nota.get(),
            "Visto": self.var_visto.get(),
            "DataHoraInclusao": data_hora_inclusao
        })
        self.popup.destroy()

    def gerar_novo_id(self):
        global PROXIMO_ID
        novo_id = PROXIMO_ID
        PROXIMO_ID += 1
        return novo_id

class ListaFilmesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Filmes")

        # Inicializar lista de filmes
        self.lista_filmes = []

        # Carregar registros do arquivo JSON se existir
        self.carregar_registros()

        # Criar e configurar a Treeview para exibir a lista
        self.tree = ttk.Treeview(self.root, columns=("ID", "Número", "Visto", "Nome", "Gênero", "Onde", "Vontade", "Nota", "DataHoraInclusao"))
        self.tree.heading("#0", text="", anchor=tk.CENTER)  # Adiciona uma coluna vazia para ocupar o espaço
        self.tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.tree.heading("Número", text="Nº", anchor=tk.CENTER)
        self.tree.heading("Visto", text="Visto", anchor=tk.CENTER)
        self.tree.heading("Nome", text="Nome", anchor=tk.CENTER)
        self.tree.heading("Gênero", text="Gênero", anchor=tk.CENTER)
        self.tree.heading("Onde", text="Onde", anchor=tk.CENTER)
        self.tree.heading("Vontade", text="Vontade", anchor=tk.CENTER)
        self.tree.heading("Nota", text="Nota", anchor=tk.CENTER)
        self.tree.heading("DataHoraInclusao", text="Data/Hora Inclusão", anchor=tk.CENTER)
        self.tree.pack(padx=10, pady=10)

        # Configurar a opção de redimensionar as colunas
        self.tree.column("#0", stretch=tk.NO, width=0)  # Coluna vazia
        self.tree.column("ID", stretch=tk.NO, width=0)  # Coluna ID (oculta)
        self.tree.column("Número", stretch=tk.NO, width=50)
        self.tree.column("Visto", stretch=tk.NO, width=70)
        self.tree.column("Nome", stretch=tk.YES, width=350)
        self.tree.column("Gênero", stretch=tk.YES, width=150)
        self.tree.column("Onde", stretch=tk.YES, width=100)
        self.tree.column("Vontade", stretch=tk.YES, width=100)
        self.tree.column("Nota", stretch=tk.YES, width=70)
        self.tree.column("DataHoraInclusao", stretch=tk.YES, width=150)

        # Adicionar barras de rolagem à Treeview
        yscrollbar = ttk.Scrollbar(self.root, orient='vertical', command=self.tree.yview)
        yscrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=yscrollbar.set)

        xscrollbar = ttk.Scrollbar(self.root, orient='horizontal', command=self.tree.xview)
        xscrollbar.pack(side='bottom', fill='x')
        self.tree.configure(xscrollcommand=xscrollbar.set)


        # Adicionar botões e entradas
        self.btn_adicionar = tk.Button(self.root, text="Adicionar Filme", command=self.abrir_popup_adicionar_filme)
        self.btn_adicionar.pack(pady=5)
        
        self.btn_alterar = tk.Button(self.root, text="Alterar Filme", command=self.abrir_popup_alterar_filme)
        self.btn_alterar.pack(pady=5)

        self.btn_excluir = tk.Button(self.root, text="Excluir Filme", command=self.excluir_filme)
        self.btn_excluir.pack(pady=5)

        self.btn_sortear = tk.Button(self.root, text="Sortear Filme Não Visto", command=self.sortear_filme_nao_visto)
        self.btn_sortear.pack(pady=5)

        # Adiciona evento de clique na Treeview para permitir a seleção de filmes para alteração
        self.tree.bind("<ButtonRelease-1>", self.selecionar_filme)

        # Atualizar a lista na GUI
        self.atualizar_lista()

    def abrir_popup_adicionar_filme(self):
        # Abre a janela de adicionar/alterar filme
        AdicionarFilmePopup(self.root, self.adicionar_filme)

    def abrir_popup_alterar_filme(self):
        # Abre a janela de adicionar/alterar filme apenas se um filme estiver selecionado
        selecionado = self.tree.selection()
        if selecionado:
            item_id = self.tree.focus()
            item_info = self.tree.item(item_id)
            values = item_info['values']

            if values:
                nome_filme = values[3]  # Obtém o nome do filme (antes era values[1])
                filme_selecionado = next((filme for filme in self.lista_filmes if filme.get("Nome") == nome_filme), None)

                if filme_selecionado:
                    AdicionarFilmePopup(self.root, lambda dados_filme=filme_selecionado: self.alterar_filme(dados_filme),
                                        alteracao=True, filme=filme_selecionado)
                else:
                    messagebox.showwarning("Filme Não Encontrado", f"Não foi possível encontrar o filme '{nome_filme}'.")
            else:
                messagebox.showwarning("Informação Inválida", "Não foi possível obter informações sobre o filme selecionado.")
        else:
            messagebox.showinfo("Nenhum Filme Selecionado", "Por favor, selecione um filme para alterar.")

    def adicionar_filme(self, novo_filme):
        # Adicionar um novo filme à lista
        self.lista_filmes.append(novo_filme)
        self.atualizar_lista()
        self.salvar_registros()

    def alterar_filme(self, dados_filme):
        # Alterar um filme na lista pelo ID
        filme_id = dados_filme.get("ID")
        indice_filme = None

        for i, filme in enumerate(self.lista_filmes):
            if filme.get("ID") == filme_id:
                indice_filme = i
                break

        if indice_filme is not None:
            # Atualiza os dados do filme encontrado
            self.lista_filmes[indice_filme].update(dados_filme)
            self.atualizar_lista()
            self.salvar_registros()
        else:
            messagebox.showwarning("Filme Não Encontrado", f"Não foi possível encontrar o filme com ID '{filme_id}'.")

    def excluir_filme(self):
        # Excluir o filme selecionado da lista
        selecionado = self.tree.selection()
        if selecionado:
            item_id = self.tree.focus()
            item_info = self.tree.item(item_id)
            values = item_info['values']

            if values:
                id_filme = values[0]  # Obtém o ID do filme
                filme_selecionado = next((filme for filme in self.lista_filmes if filme.get("ID") == id_filme), None)

                if filme_selecionado:
                    self.lista_filmes.remove(filme_selecionado)
                    self.atualizar_lista()
                    self.salvar_registros()
                else:
                    messagebox.showwarning("Filme Não Encontrado", f"Não foi possível encontrar o filme com ID {id_filme}.")
            else:
                messagebox.showwarning("Informação Inválida", "Não foi possível obter informações sobre o filme selecionado.")
        else:
            messagebox.showinfo("Nenhum Filme Selecionado", "Por favor, selecione um filme para excluir.")

    def sortear_filme_nao_visto(self):
        # Filtrar filmes não vistos
        filmes_nao_vistos = [filme for filme in self.lista_filmes if not filme.get("Visto", False)]

        # Sortear aleatoriamente um filme não visto
        if filmes_nao_vistos:
            filme_sorteado = random.choice(filmes_nao_vistos)
            messagebox.showinfo("Filme Sorteado", f"Filme Sorteado: {filme_sorteado.get('Nome', '')}")
        else:
            messagebox.showinfo("Sem Filmes Não Vistos", "Todos os filmes foram vistos.")

    def selecionar_filme(self, event):
        # Atualiza os botões de alterar/excluir com base na seleção na Treeview
        selecionado = self.tree.selection()
        if selecionado:
            self.btn_alterar["state"] = "normal"
            self.btn_excluir["state"] = "normal"
        else:
            self.btn_alterar["state"] = "disabled"
            self.btn_excluir["state"] = "disabled"

    def atualizar_lista(self):
        # Limpar a Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Preencher a Treeview com os filmes
        for i, filme in enumerate(self.lista_filmes):
            visto_texto = "✔" if filme.get("Visto", False) else ""
            self.tree.insert("", i, values=(filme.get("ID", ""), i + 1, visto_texto, filme.get("Nome", ""), filme.get("Gênero", ""),
                                            filme.get("Onde", ""), filme.get("Vontade", ""), filme.get("Nota", ""),
                                            filme.get("DataHoraInclusao", ""),))

            # Centralizar o texto da coluna "Nome"
            self.tree.column("Nome", anchor=tk.CENTER)
            self.tree.column("Número", anchor=tk.CENTER)
            self.tree.column("Visto", anchor=tk.CENTER)
            self.tree.column("Nome", anchor=tk.CENTER)
            self.tree.column("Gênero", anchor=tk.CENTER)
            self.tree.column("Onde", anchor=tk.CENTER)
            self.tree.column("Vontade", anchor=tk.CENTER)
            self.tree.column("Nota", anchor=tk.CENTER)
            self.tree.column("DataHoraInclusao", anchor=tk.CENTER)

    def salvar_registros(self):
        # Salvar registros em um arquivo JSON
        with open("registros_filmes.json", "w") as file:
            json.dump(self.lista_filmes, file)

    def carregar_registros(self):
        # Carregar registros de um arquivo JSON, se existir
        try:
            with open("registros_filmes.json", "r") as file:
                self.lista_filmes = json.load(file)
        except FileNotFoundError:
            # Se o arquivo não existir, cria uma lista vazia
            self.lista_filmes = []

# Criar a aplicação
root = tk.Tk()
app = ListaFilmesApp(root)
root.mainloop()