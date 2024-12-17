import wx
from src.gui.livros_gui import GerenciarLivros
from src.gui.usuarios_gui import GerenciarUsuarios

class MenuPrincipal(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(MenuPrincipal, self).__init__(*args, **kwargs)
        self.SetTitle("Gerenciador de Biblioteca")
        self.SetSize((500, 400))
        self.Centre()

        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        lbl_titulo = wx.StaticText(panel, label="Seja bem vindo(a)", style=wx.ALIGN_CENTER)
        fonte = lbl_titulo.GetFont()
        fonte.PointSize += 4
        lbl_titulo.SetFont(fonte)
        vbox.Add(lbl_titulo, flag=wx.ALIGN_CENTER | wx.TOP, border=20)

        btn_livros = wx.Button(panel, label="Gerenciar Livros")
        btn_livros.Bind(wx.EVT_BUTTON, self.abrir_livros)
        vbox.Add(btn_livros, flag=wx.EXPAND | wx.ALL, border=10)

        btn_usuarios = wx.Button(panel, label="Gerenciar Usuários")
        btn_usuarios.Bind(wx.EVT_BUTTON, self.abrir_usuarios)
        vbox.Add(btn_usuarios, flag=wx.EXPAND | wx.ALL, border=10)

        btn_sair = wx.Button(panel, label="Sair")
        btn_sair.Bind(wx.EVT_BUTTON, self.sair)
        vbox.Add(btn_sair, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(vbox)

    def abrir_livros(self, event):
        janela_livros = GerenciarLivros(parent=None)
        janela_livros.Show()

    def abrir_usuarios(self, event):
        janela_usuarios = GerenciarUsuarios(parent=None)
        janela_usuarios.Show()

    def sair(self, event):
        self.Close()


if __name__ == "__main__":
    app = wx.App()
    frame = MenuPrincipal(None)
    frame.Show()
    app.MainLoop()
