import networkx as nx
import pylab
import wx
import wx.lib.scrolledpanel as scrolled
from process_file import parse_actions_into_queue, DataElementEvents
from process_file import parse_events_into_queue
from result_window import ResultFrame


class MainFrame(wx.Frame):

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(MainFrame, self).__init__(*args, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        # create a panel in the frame
        self.panel = scrolled.ScrolledPanel(self, -1, size=(wx.DisplaySize()))

        # Button plot
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        # Mode selection
        self.tbtn = wx.ToggleButton(self.panel, -1, "Event mode")
        self.vbox.Add(self.tbtn, 0, wx.EXPAND | wx.ALIGN_CENTER)
        self.tbtn.Bind(wx.EVT_TOGGLEBUTTON, self.on_toggle)

        # Title
        self.st = wx.StaticText(self.panel, label="Enter data")
        font = self.st.GetFont()
        font.PointSize += 2
        font = font.Bold()
        self.st.SetFont(font)
        self.vbox.Add(self.st, 0, wx.ALIGN_CENTER)

        # Labels events
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

        # Input events
        hbox_input = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_add_e = wx.Button(self.panel, -1, "+", size=(30, -1))
        self.activity_input_e = wx.TextCtrl(self.panel, -1, size=(80, -1))
        self.time_input_e = wx.TextCtrl(self.panel, -1, size=(80, -1))
        self.A_input_e = wx.TextCtrl(self.panel, -1, size=(50, -1))
        self.B_input_e = wx.TextCtrl(self.panel, -1, size=(50, -1))
        hbox_input.Add(self.activity_input_e, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox_input.Add(self.time_input_e, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox_input.Add(self.A_input_e, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox_input.Add(wx.StaticText(self.panel, -1, "->"), 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox_input.Add(self.B_input_e, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox_input.Add(self.btn_add_e, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.vbox.Add(hbox_input)

        self.input_event = []
        self.input_event.append(self.activity_input_e)
        self.input_event.append(self.time_input_e)
        self.input_event.append(self.A_input_e)
        self.input_event.append(self.B_input_e)

        # Labels actions
        hbox_labels = wx.BoxSizer(wx.HORIZONTAL)
        activity_label = wx.StaticText(self.panel, -1, label="Activity", size=(80, -1))
        time_label = wx.StaticText(self.panel, -1, label="Time", size=(80, -1))
        succession_label = wx.StaticText(self.panel, -1, "Previous activity", size=(135, -1))
        add_label = wx.StaticText(self.panel, -1, "Add", size=(30, -1))
        hbox_labels.Add(activity_label, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox_labels.Add(time_label, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox_labels.Add(succession_label, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox_labels.Add(add_label, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        self.vbox.Add(hbox_labels)

        # Input actions
        hbox_input = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_add_a = wx.Button(self.panel, -1, "+", size=(30, -1))
        self.activity_input_a = wx.TextCtrl(self.panel, -1, size=(80, -1))
        self.time_input_a = wx.TextCtrl(self.panel, -1, size=(80, -1))
        self.input_a = wx.TextCtrl(self.panel, -1, size=(133, -1))
        hbox_input.Add(self.activity_input_a, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox_input.Add(self.time_input_a, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox_input.Add(self.input_a, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        hbox_input.Add(self.btn_add_a, 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.vbox.Add(hbox_input)
        self.input_action = []
        self.input_action.append(self.activity_input_a)
        self.input_action.append(self.time_input_a)
        self.input_action.append(self.input_a)

        for inp in self.input_action:
            inp.SetEditable(False)
            inp.SetBackgroundColour((50, 50, 50))

        # Buttons
        self.btn_add_e.Bind(wx.EVT_BUTTON, self.on_add_by_events_clicked)
        self.btn_add_a.Bind(wx.EVT_BUTTON, self.on_add_by_actions_clicked)

        self.data = []
        self.is_loaded_as_events = True

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
        load_events_item = menu_file.Append(-1, "&Load from file\tCtrl-EL",
                                            "Load data from file")

        menu_bar = wx.MenuBar()
        menu_bar.Append(menu, "&Menu")
        menu_bar.Append(menu_file, "&File")

        self.SetMenuBar(menu_bar)

        self.Bind(wx.EVT_MENU, self.on_plot_clicked, plot_item)
        self.Bind(wx.EVT_MENU, self.on_load_clicked, load_events_item)
        self.Bind(wx.EVT_MENU, self.on_clear_clicked, clear_item)

    def on_clear_clicked(self, event):
        self.data = []
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.StaticText(self.panel, -1, "Cleaned"), 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.vbox.Add(hbox)

        for inp in self.input_action:
            inp.Clear()
        for inp in self.input_event:
            inp.Clear()

        self.panel.SetupScrolling()
        self.SetStatusText("Data cleaned")
        self.panel.SetSizer(self.vbox)
        self.panel.Layout()

    def on_load_clicked(self, event):

        with wx.FileDialog(self, "Choose your data file..", wildcard="Text file(*.txt)|*.txt",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # User clean

            # User upload
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r') as file:
                    if self.is_loaded_as_events:
                        imported_graph = parse_actions_into_queue(file.readlines())
                    else:
                        imported_graph = parse_events_into_queue(file.readlines())
                    for i in range(0, len(imported_graph), 4):  # data sets are in 4s
                        new_data_element = DataElementEvents()
                        new_data_element.activity = imported_graph[i]
                        new_data_element.time = imported_graph[i + 1]
                        new_data_element.first_event = imported_graph[i + 2]
                        new_data_element.second_event = imported_graph[i + 3]
                        self.data.append(new_data_element)
                        self.set_data_element(new_data_element)
            except IOError:
                wx.LogError("Cannot open file '%s'.")

    def on_add_by_actions_clicked(self, event):
        new_data_element = DataElementEvents()
        for inp in self.input_action:
            if not inp.GetValue():
                wx.MessageBox("Enter all data!")
                return
        try:
            new_data_element.time = float(self.time_input_e.GetValue())
            new_data_element.activity = self.activity_input_e.GetValue()
            new_data_element.first_event = self.A_input_e.GetValue()
            new_data_element.second_event = self.B_input_e.GetValue()
            self.data.append(new_data_element)
        except ValueError:
            wx.MessageBox("Wrong time! Enter number")
            return
        self.set_data_element(new_data_element)

    def on_add_by_events_clicked(self, event):
        new_data_element = DataElementEvents()
        for inp in self.input_event:
            if not inp.GetValue():
                wx.MessageBox("Enter all data!")
                return
        try:
            new_data_element.time = float(self.time_input_e.GetValue())
            new_data_element.activity = self.activity_input_e.GetValue()
            new_data_element.first_event = self.A_input_e.GetValue()
            new_data_element.second_event = self.B_input_e.GetValue()
            self.data.append(new_data_element)
        except ValueError:
            wx.MessageBox("Wrong time! Enter number")
            return
        self.set_data_element(new_data_element)

    def set_data_element(self, data_element):
        # Data element added
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.StaticText(self.panel, -1,
                               str(data_element.activity) + " " + str(data_element.time) + " "
                               + str(data_element.first_event) + "->" + str(data_element.second_event)),
                 0, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.vbox.Add(hbox)

        for inp in self.input_action:
            inp.Clear()
        for inp in self.input_event:
            inp.Clear()

        self.panel.SetupScrolling()
        self.SetStatusText("Item added")
        self.panel.SetSizer(self.vbox)
        self.panel.Layout()

    def add_nodes_t0(self, G, node):
        node_queue = []

        for edge in G.out_edges(node):
            value = G.nodes[edge[0]]['t0'] + G[edge[0]][edge[1]]['time']
            if "t0" not in G.nodes[edge[1]] or value >= G.nodes[edge[1]]['t0']:
                G.nodes[edge[1]]['t0'] = value
            node_queue.append(edge[1])

        for node in node_queue:
            self.add_nodes_t0(G, node)

    def add_nodes_t1(self, G, node, critical_path):
        node_queue = []

        for edge in G.in_edges(node):
            value = G.nodes[edge[1]]['t1'] - G[edge[0]][edge[1]]['time']
            if "t1" not in G.nodes[edge[0]] or value <= G.nodes[edge[0]]['t1']:
                G.nodes[edge[0]]['t1'] = value
                print("%s (%s) %s %s" % (value, G[edge[0]][edge[1]], G.node[edge[0]], G.node[edge[1]]))
                if G.nodes[edge[0]]['t1'] - G.nodes[edge[0]]['t0'] == 0:
                    critical_path.append((edge[0], edge[1]))
            node_queue.append(edge[0])

        for node in node_queue:
            self.add_nodes_t1(G, node, critical_path)

    def on_plot_clicked(self, event):
        if len(self.data) == 0:
            return

        G = nx.DiGraph()
        for dataElement in self.data:
            G.add_edges_from([(dataElement.first_event, dataElement.second_event)], time=int(dataElement.time))

        node = "1"
        G.nodes[node]['t0'] = 0
        self.add_nodes_t0(G, node)

        node = self.data[-1].second_event
        G.nodes[node]['t1'] = G.nodes[node]['t0']
        critical_path = []
        self.add_nodes_t1(G, node, critical_path)

        non_zero_paths = [(u, v) for (u, v, d) in G.edges(data=True) if not d['time'] == 0]
        normal_path = list(set(non_zero_paths) - set(critical_path))
        dashed_path = [(u, v) for (u, v, d) in G.edges(data=True) if d['time'] == 0]
        pos = nx.spring_layout(G)
        pylab.figure()

        nx.draw_networkx_nodes(G, pos)
        nx.draw_networkx_edges(G, pos, edgelist=critical_path, edge_color='r')
        nx.draw_networkx_edges(G, pos, edgelist=normal_path)
        nx.draw_networkx_edges(G, pos, edgelist=dashed_path, width=0)
        nx.draw_networkx_edges(G, pos, edgelist=dashed_path, arrows=False, style='dashed')
        nx.draw_networkx_edge_labels(G, pos, dict([((u, v,), d['time']) for u, v, d in G.edges(data=True)]))
        nx.draw_networkx_labels(G, pos)
        self.second_window = ResultFrame(parent=wx.GetTopLevelParent(self), Graph=G)
        pylab.axis('off')
        pylab.show()

    def on_toggle(self, event):
        state = event.GetEventObject().GetValue()
        self.on_clear_clicked(None)
        if state:
            event.GetEventObject().SetLabel("Action mode")
            self.is_loaded_as_events = False
            for inp in self.input_action:
                inp.SetEditable(False)
                inp.SetBackgroundColour((255, 255, 255))
            for inp in self.input_event:
                inp.SetEditable(False)
                inp.SetBackgroundColour((50, 50, 50))
        else:
            event.GetEventObject().SetLabel("Event mode")
            self.is_loaded_as_events = True
            for inp in self.input_event:
                inp.SetEditable(False)
                inp.SetBackgroundColour((255, 255, 255))
            for inp in self.input_action:
                inp.SetEditable(False)
                inp.SetBackgroundColour((50, 50, 50))

    def on_exit(self, event):
        """Close the frame, terminating the application."""
        #self.second_window.Close(True)
        self.Close(True)


if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = MainFrame(None, title='Operational research application')
    frm.Show()
    app.MainLoop()
