import networkx as nx
import pylab
import wx
import wx.lib.scrolledpanel as scrolled

from process_file import choose_file


class DataElement:
    def __init__(self):
        self.activity = None
        self.time = 0
        self.first_event = None
        self.second_event = None


class MainFrame(wx.Frame):

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(MainFrame, self).__init__(*args, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        # create a panel in the frame
        self.panel = scrolled.ScrolledPanel(self, -1, size=(wx.DisplaySize()))

        # Button plot
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # Mode selection
        # self.tbtn = wx.ToggleButton(panel, -1, "Change to event mode")
        # vbox.Add(self.tbtn, 0, wx.EXPAND | wx.ALIGN_CENTER)
        # self.tbtn.Bind(wx.EVT_TOGGLEBUTTON, self.OnToggle)

        # Title
        self.st = wx.StaticText(self.panel, label="Enter data")
        font = self.st.GetFont()
        font.PointSize += 2
        font = font.Bold()
        self.st.SetFont(font)
        self.vbox.Add(self.st, 0, wx.ALIGN_CENTER)

        # Labels
        hbox_labels = wx.BoxSizer(wx.HORIZONTAL)
        activity_label = wx.StaticText(self.panel, -1, label="Activity", size=(80, -1))
        time_label = wx.StaticText(self.panel, -1, label="Time", size=(80, -1))
        succession_label = wx.StaticText(self.panel, -1, "Succession of events", size=(135, -1))
        add_label = wx.StaticText(self.panel, -1, "Add", size=(30, -1))
        hbox_labels.Add(activity_label, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox_labels.Add(time_label, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox_labels.Add(succession_label, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox_labels.Add(add_label, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        self.vbox.Add(hbox_labels)

        # Input
        hbox_input = wx.BoxSizer(wx.HORIZONTAL)
        self.activity_input = wx.TextCtrl(self.panel, -1, size=(80, -1))
        self.time_input = wx.TextCtrl(self.panel, -1, size=(80, -1))
        self.A_input = wx.TextCtrl(self.panel, -1, size=(50, -1))
        self.B_input = wx.TextCtrl(self.panel, -1, size=(50, -1))
        hbox_input.Add(self.activity_input, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox_input.Add(self.time_input, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox_input.Add(self.A_input, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox_input.Add(wx.StaticText(self.panel, -1, "->"), 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox_input.Add(self.B_input, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)

        # Buttons
        self.btn_add = wx.Button(self.panel, -1, "+", size=(30, -1))
        hbox_input.Add(self.btn_add, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.btn_add.Bind(wx.EVT_BUTTON, self.on_add_clicked)
        self.vbox.Add(hbox_input)

        self.data = []

        self.make_menu_bar()
        self.panel.SetSizer(self.vbox)
        self.CreateStatusBar()
        self.SetStatusText("Welcome to operational research application!")

        self.Centre()
        self.Show()
        self.Fit()

    def make_menu_bar(self):
        menu = wx.Menu()
        plot_item = menu.Append(-1, "&Plot\tCtrl-P", "Plot graph with current data")
        menu.AppendSeparator()
        clear_item = menu.Append(-1, "&Clean\tCtrl-C", "Clean the data")

        menu_file = wx.Menu()
        load_events_item = menu_file.Append(-1, "&Load (events succession)\tCtrl-E",
                                            "Load data as succession of events")
        menu_file.AppendSeparator()
        load_activities_item = menu_file.Append(-1, "&Load (preceding activities)\tCtrl-A",
                                                "Load data as preceding activities")

        menu_bar = wx.MenuBar()
        menu_bar.Append(menu, "&Menu")
        menu_bar.Append(menu_file, "&File")

        self.SetMenuBar(menu_bar)

        self.Bind(wx.EVT_MENU, self.on_plot_clicked, plot_item)
        self.Bind(wx.EVT_MENU, self.on_load_events_clicked, load_events_item)
        # self.Bind(wx.EVT_MENU, self.OnClearClicked, clear_item)

    def on_load_events_clicked(self, event):
        choose_file()
        return

    def on_add_clicked(self, event):
        newDataElement = DataElement()
        if not self.activity_input.GetValue() \
                or not self.time_input.GetValue() \
                or not self.A_input.GetValue() \
                or not self.B_input.GetValue():
            wx.MessageBox("Enter all data!")
            return
        try:
            newDataElement.time = float(self.time_input.GetValue())
            newDataElement.activity = self.activity_input.GetValue()
            newDataElement.first_event = self.A_input.GetValue()
            newDataElement.second_event = self.B_input.GetValue()
            self.data.append(newDataElement)
        except ValueError:
            wx.MessageBox("Wrong time! Enter number")
            return

        # Data element added
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        activity = wx.StaticText(self.panel, -1, self.activity_input.GetValue())
        time = wx.StaticText(self.panel, -1, self.time_input.GetValue())
        A = wx.StaticText(self.panel, -1, self.A_input.GetValue())
        B = wx.StaticText(self.panel, -1, self.B_input.GetValue())
        hbox.Add(activity, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox.Add(time, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox.Add(A, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox.Add(wx.StaticText(self.panel, -1, "->"), 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox.Add(B, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.vbox.Add(hbox)

        self.activity_input.Clear()
        self.time_input.Clear()
        self.A_input.Clear()
        self.B_input.Clear()

        self.panel.SetupScrolling()
        self.SetStatusText("Item added")
        self.panel.SetSizer(self.vbox)
        self.panel.Layout()

    def add_nodes_value(self, G, node, critical_path, is_on_critical=True):
        critical = []
        node_queue = []

        for edge in G.out_edges(node):
            value = G.nodes[edge[0]]['t0'] + G[edge[0]][edge[1]]['time']
            if "t0" not in G.nodes[edge[1]] or value >= G.nodes[edge[1]]['t0']:
                G.nodes[edge[1]]['t0'] = value
                if is_on_critical:
                    if not critical:
                        critical.append((edge[0], edge[1], value))
                    elif value == critical[0][2]:
                        critical.append((edge[0], edge[1], value))
                    elif value > critical[0][2]:
                        critical.clear()
                        critical.append((edge[0], edge[1], value))
            node_queue.append(edge[1])

        for red in critical:
            critical_path.append((red[0], red[1]))
        for node in node_queue:
            added = False
            for red in critical:
                if red[1] == node:
                    self.add_nodes_value(G, node, critical_path)
                    added = True
                    break
            if not added:
                self.add_nodes_value(G, node, critical_path, False)

    def on_plot_clicked(self, event):
        G = nx.DiGraph()
        for dataElement in self.data:
            G.add_edges_from([(dataElement.first_event, dataElement.second_event)], time=dataElement.time)

        node = "1"
        G.nodes[node]['t0'] = 0
        critical_path = []

        self.add_nodes_value(G, node, critical_path)

        normal_path = [edge for edge in G.edges() if edge not in critical_path]

        pos = nx.spring_layout(G)
        pylab.figure()

        nx.draw(G, pos)
        nx.draw_networkx_edge_labels(G, pos, dict([((u, v,), d['time']) for u, v, d in G.edges(data=True)]))
        nx.draw_networkx_edges(G, pos, edgelist=critical_path, edge_color='r', arrows=True)
        nx.draw_networkx_edges(G, pos, edgelist=normal_path, arrows=True)
        nx.draw_networkx_labels(G, pos)
        pylab.axis('off')
        pylab.show()

    def on_toggle(self, event):
        state = event.GetEventObject().GetValue()

        if state:
            event.GetEventObject().SetLabel("Change to event mode")
        else:
            event.GetEventObject().SetLabel("Change to action mode")

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = MainFrame(None, title='Operational research application')
    frm.Show()
    app.MainLoop()