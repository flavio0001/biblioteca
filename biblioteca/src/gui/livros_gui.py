import wx
from src.database.db_operations import inserir_livro, listar_livros, excluir_livro, listar_emprestimos
from src.utils.sounds import play_created, play_error, play_delete, play_list
from src.utils.utils import gerar_isbn


class GerenciarLivros(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(GerenciarLivros, self).__init__(*args, **kwargs)

        self.SetTitle("Gerenciamento de Livros")
        self.SetSize((600, 500))
        self.Centre()

        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        lbl_titulo = wx.StaticText(panel, label="Gerenciar Livros", style=wx.ALIGN_CENTER)
        font = lbl_titulo.GetFont()
        font.PointSize += 4
        lbl_titulo.SetFont(font)
        vbox.Add(lbl_titulo, flag=wx.ALIGN_CENTER | wx.TOP, border=20)

        btn_adicionar = wx.Button(panel, label="Adicionar Livro")
        btn_adicionar.Bind(wx.EVT_BUTTON, self.adicionar_livro)
        vbox.Add(btn_adicionar, flag=wx.EXPAND | wx.ALL, border=10)

        btn_procurar = wx.Button(panel, label="Procurar Livro")
        btn_procurar.Bind(wx.EVT_BUTTON, self.procurar_livro)
        vbox.Add(btn_procurar, flag=wx.EXPAND | wx.ALL, border=10)

        btn_remover = wx.Button(panel, label="Remover Livro")
        btn_remover.Bind(wx.EVT_BUTTON, self.remover_livro)
        vbox.Add(btn_remover, flag=wx.EXPAND | wx.ALL, border=10)

        btn_lista_emprestados = wx.Button(panel, label="Verificar Livros Emprestados")
        btn_lista_emprestados.Bind(wx.EVT_BUTTON, self.listar_livros_emprestados)
        vbox.Add(btn_lista_emprestados, flag=wx.EXPAND | wx.ALL, border=10)

        btn_voltar = wx.Button(panel, label="Voltar")
        btn_voltar.Bind(wx.EVT_BUTTON, self.voltar)
        vbox.Add(btn_voltar, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(vbox)

    def adicionar_livro(self, event):
        dlg = wx.TextEntryDialog(self, "Adicionar um novo livro. Preencha as informações:\nTítulo", "Adicionar Livro")
        if dlg.ShowModal() == wx.ID_OK:
            titulo = dlg.GetValue()
            dlg.Destroy()

            # Janela para outras informações
            autor = wx.GetTextFromUser("Autor:", "Adicionar Livro")
            editora = wx.GetTextFromUser("Editora:", "Adicionar Livro")
            genero = wx.GetTextFromUser("Gênero:", "Adicionar Livro")
            ano = wx.GetTextFromUser("Ano de Publicação:", "Adicionar Livro")

            try:
                ano = int(ano)
                isbn = gerar_isbn()
                inserir_livro(titulo, autor, editora, genero, ano, isbn)
                play_created()
                wx.MessageBox(f"Livro '{titulo}' adicionado com sucesso!\nISBN: {isbn}", "Sucesso", wx.OK | wx.ICON_INFORMATION)
            except ValueError:
                play_error()
                wx.MessageBox("Erro: O ano deve ser um número.", "Erro", wx.OK | wx.ICON_ERROR)

    def procurar_livro(self, event):
        dlg = wx.TextEntryDialog(self, "Digite o título ou ISBN do livro que deseja procurar:", "Procurar Livro")
        if dlg.ShowModal() == wx.ID_OK:
            termo = dlg.GetValue()
            livros = listar_livros()
            dlg.Destroy()

            resultado = [livro for livro in livros if termo.lower() in livro['titulo'].lower() or termo == str(livro['isbn'])]
            if resultado:
                play_list()
                msg = "\n".join([f"Título: {livro['titulo']}, ISBN: {livro['isbn']}" for livro in resultado])
                wx.MessageBox(f"Livros encontrados:\n{msg}", "Resultado", wx.OK | wx.ICON_INFORMATION)
            else:
                play_error()
                wx.MessageBox("Nenhum livro encontrado com o termo especificado.", "Erro", wx.OK | wx.ICON_ERROR)

    def remover_livro(self, event):
        dlg = wx.TextEntryDialog(self, "Digite o título do livro que deseja remover:", "Remover Livro")
        if dlg.ShowModal() == wx.ID_OK:
            titulo = dlg.GetValue()
            dlg.Destroy()

            isbn = wx.GetTextFromUser("Digite o ISBN do livro para confirmar a exclusão:", "Remover Livro")
            livros = listar_livros()

            for livro in livros:
                if livro['titulo'].lower() == titulo.lower() and str(livro['isbn']) == isbn:
                    excluir_livro(livro['id'])
                    play_delete()
                    wx.MessageBox(f"Livro '{titulo}' removido com sucesso.", "Sucesso", wx.OK | wx.ICON_INFORMATION)
                    return

            play_error()
            wx.MessageBox("Erro: Livro não encontrado ou ISBN incorreto.", "Erro", wx.OK | wx.ICON_ERROR)

    def listar_livros_emprestados(self, event):
        emprestimos = listar_emprestimos(apenas_ativos=True)
        if emprestimos:
            play_list()
            msg = "\n".join([f"Livro: {e['livro_titulo']}, Cliente: {e['cliente_nome']}" for e in emprestimos])
            wx.MessageBox(f"Livros emprestados:\n{msg}", "Livros Emprestados", wx.OK | wx.ICON_INFORMATION)
        else:
            play_error()
            wx.MessageBox("Nenhum livro emprestado no momento.", "Livros Emprestados", wx.OK | wx.ICON_ERROR)

    def voltar(self, event):
        self.Close()
