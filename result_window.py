import wx
import wx.lib.scrolledpanel as scrolled


class ResultFrame(wx.Frame):

    def __init__(self, parent, Graph):
        # Frame
        wx.Panel.__init__(self, parent)
        # Panel
        self.panel = scrolled.ScrolledPanel(self, -1, size=(wx.DisplaySize()))
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # Headers
        self.hbox_headers = wx.BoxSizer(wx.HORIZONTAL)

        #Binding
        #self.Bind(wx.EVT_CLOSE, self.on_exit)

        title = wx.StaticText(self.panel, label="Node name", size=(150, -1))
        font = title.GetFont()
        font.PointSize += 5
        font = font.Bold()
        title.SetFont(font)
        title.SetBackgroundColour(self.panel.GetBackgroundColour())
        self.hbox_headers.Add(title, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)

        t0 = wx.StaticText(self.panel, label="T0", size=(100, -1))
        t0.SetFont(font)
        t0.SetBackgroundColour(self.panel.GetBackgroundColour())
        self.hbox_headers.Add(t0, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 5)

        t1 = wx.StaticText(self.panel, label="T1", size=(20, -1))
        t1.SetFont(font)
        t1.SetBackgroundColour(self.panel.GetBackgroundColour())
        self.hbox_headers.Add(t1, 0, wx.EXPAND | wx.RIGHT | wx.ALL, 5)

        self.vbox.Add(self.hbox_headers)
        self.panel.SetSizer(self.vbox)
        self.show_results(Graph)
        self.Show()

    def show_results(self, Graph):
        nodes_list = list(Graph.nodes.data())
        for node in nodes_list:
            print(node)
            node_name = wx.StaticText(self.panel, -1, "           " + node[0],size=(150,-1))
            font = node_name.GetFont()
            font.PointSize +=2
            t0 = wx.StaticText(self.panel, -1, str(node[1].get('t0')), size=(100,-1))
            t1 = wx.StaticText(self.panel, -1, str(node[1].get('t1')), size=(20,10))
            node_name.SetFont(font)
            t0.SetFont(font)
            t1.SetFont(font)
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            hbox.Add(node_name ,0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
            hbox.Add(t0 ,0, wx.EXPAND | wx.ALIGN_CENTER | wx.ALL, 5)
            hbox.Add(t1 ,0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
            self.vbox.Add(hbox)

        self.panel.SetupScrolling()

    def on_exit(self, event):
        self.Close(True)