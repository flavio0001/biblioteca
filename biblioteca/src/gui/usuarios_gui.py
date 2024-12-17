import wx
from src.database.db_operations import inserir_cliente, listar_clientes, remover_cliente
from src.utils.sounds import play_created, play_error, play_delete, play_list
from src.utils.utils import gerar_Id_cliente


class GerenciarUsuarios(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(GerenciarUsuarios, self).__init__(*args, **kwargs)

        self.SetTitle("Gerenciamento de Usuários")
        self.SetSize((600, 500))
        self.Centre()

        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        lbl_titulo = wx.StaticText(panel, label="Gerenciar Usuários", style=wx.ALIGN_CENTER)
        font = lbl_titulo.GetFont()
        font.PointSize += 4
        lbl_titulo.SetFont(font)
        vbox.Add(lbl_titulo, flag=wx.ALIGN_CENTER | wx.TOP, border=20)

        btn_adicionar = wx.Button(panel, label="Adicionar Usuário")
        btn_adicionar.Bind(wx.EVT_BUTTON, self.adicionar_usuario)
        vbox.Add(btn_adicionar, flag=wx.EXPAND | wx.ALL, border=10)

        btn_listar = wx.Button(panel, label="Listar Usuários")
        btn_listar.Bind(wx.EVT_BUTTON, self.listar_usuarios)
        vbox.Add(btn_listar, flag=wx.EXPAND | wx.ALL, border=10)

        btn_procurar = wx.Button(panel, label="Procurar Usuário")
        btn_procurar.Bind(wx.EVT_BUTTON, self.procurar_usuario)
        vbox.Add(btn_procurar, flag=wx.EXPAND | wx.ALL, border=10)

        btn_remover = wx.Button(panel, label="Remover Usuário")
        btn_remover.Bind(wx.EVT_BUTTON, self.remover_usuario)
        vbox.Add(btn_remover, flag=wx.EXPAND | wx.ALL, border=10)

        btn_voltar = wx.Button(panel, label="Voltar")
        btn_voltar.Bind(wx.EVT_BUTTON, self.voltar)
        vbox.Add(btn_voltar, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(vbox)

    def adicionar_usuario(self, event):
        dlg = wx.TextEntryDialog(self, "Digite o nome do novo usuário:", "Adicionar Usuário")
        if dlg.ShowModal() == wx.ID_OK:
            nome = dlg.GetValue()
            dlg.Destroy()

            if not nome.strip():
                play_error()
                wx.MessageBox("Erro: O campo 'Nome' não pode estar vazio.", "Erro", wx.OK | wx.ICON_ERROR)
                return

            id_cliente = gerar_Id_cliente()
            inserir_cliente(nome, id_cliente)
            play_created()
            wx.MessageBox(f"Usuário '{nome}' adicionado com sucesso!\nID: {id_cliente}", "Sucesso", wx.OK | wx.ICON_INFORMATION)

    def listar_usuarios(self, event):
        usuarios = listar_clientes()
        if usuarios:
            play_list()
            msg = "\n".join([f"Nome: {u['nome']}, ID: {u['id_cliente']}" for u in usuarios])
            wx.MessageBox(f"Lista de Usuários:\n{msg}", "Usuários Cadastrados", wx.OK | wx.ICON_INFORMATION)
        else:
            play_error()
            wx.MessageBox("Nenhum usuário encontrado.", "Usuários Cadastrados", wx.OK | wx.ICON_ERROR)

    def procurar_usuario(self, event):
        dlg = wx.TextEntryDialog(self, "Digite o nome ou ID do usuário que deseja procurar:", "Procurar Usuário")
        if dlg.ShowModal() == wx.ID_OK:
            termo = dlg.GetValue()
            usuarios = listar_clientes()
            dlg.Destroy()

            resultado = [u for u in usuarios if termo.lower() in u['nome'].lower() or termo == str(u['id_cliente'])]
            if resultado:
                play_list()
                msg = "\n".join([f"Nome: {u['nome']}, ID: {u['id_cliente']}" for u in resultado])
                wx.MessageBox(f"Usuários encontrados:\n{msg}", "Resultado", wx.OK | wx.ICON_INFORMATION)
            else:
                play_error()
                wx.MessageBox("Nenhum usuário encontrado com o termo especificado.", "Erro", wx.OK | wx.ICON_ERROR)

    def remover_usuario(self, event):
        dlg = wx.TextEntryDialog(self, "Digite o nome do usuário que deseja remover:", "Remover Usuário")
        if dlg.ShowModal() == wx.ID_OK:
            nome = dlg.GetValue()
            dlg.Destroy()

            id_cliente = wx.GetTextFromUser("Digite o ID do usuário para confirmar a exclusão:", "Remover Usuário")
            usuarios = listar_clientes()

            for usuario in usuarios:
                if usuario['nome'].lower() == nome.lower() and str(usuario['id_cliente']) == id_cliente:
                    excluir_cliente(usuario['id'])
                    play_delete()
                    wx.MessageBox(f"Usuário '{nome}' removido com sucesso.", "Sucesso", wx.OK | wx.ICON_INFORMATION)
                    return

            play_error()
            wx.MessageBox("Erro: Usuário não encontrado ou ID incorreto.", "Erro", wx.OK | wx.ICON_ERROR)

    def voltar(self, event):
        self.Close()
