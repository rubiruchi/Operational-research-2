from collections import defaultdict


def parse_actions_into_queue(file_lines):
    queue = []
    lines = [line.rstrip('\n') for line in file_lines]
    lines = [line.split(' ') for line in lines]
    print(lines)
    for i in lines:
        for j in i:
            queue.append(j)
    return queue


# first_action_counter = 1

class DataElementActions:
    def __init__(self, a=None, t=0, p=None):
        if p is None:
            p = []
        self.activity = a
        self.time = t
        self.previous_activities = p

    def __str__(self):
        return str(self.activity) + " " + str(self.previous_activities)

    def __repr__(self):
        return str(self.activity) + " " + str(self.previous_activities)


class DataElementEvents:
    def __init__(self, a=None, t=0, f=None, s=None):
        self.activity = a
        self.time = t
        self.first_event = f
        self.second_event = s

    def __str__(self):
        return str(self.activity) + " " + str(self.first_event) + "->" + str(self.second_event)

    def __repr__(self):
        return str(self.activity) + " " + str(self.first_event) + "->" + str(self.second_event)


class Edge:
    def __init__(self, n=None, t=0, f=None, s=None):
        self.name = n
        self.time = t
        self.first = f
        self.second = s


class Graph:
    def __init__(self):
        self.max_node = 1
        self.edges = []
        self.ends = [1]
        self.connected_nodes = set()
        self.in_edges = defaultdict(list)
        self.z_counter = 1

    def to_queue(self):
        queue = []
        for edge in self.edges:
            queue.append(edge.name)
            queue.append(edge.time)
            queue.append(str(edge.first))
            queue.append(str(edge.second))
        return queue

    def add_activity(self, element):
        print("------------%s------------" % element.activity)
        if element.previous_activities[0] == '-':
            next_node = self.next_node(1)
            self.add_edge(element.activity, element.time, 1, next_node)
        else:
            matching_edges = []
            current_second = 0
            edge = None
            for activity in element.previous_activities:
                for e in self.edges:
                    if e.name == activity:
                        matching_edges.append(e)
                        if edge is None or (e.second in self.ends and e.second > current_second):
                            current_second = e.second
                            edge = e
            print([e.name for e in matching_edges])

            dif = [a for a in set(edge.name for edge in self.in_edges[edge.second])
                .difference(set(element.previous_activities))]
            print("Difference (remove): %s " % dif)
            for e_name in set(dif):
                # remove
                for e in self.edges:
                    if e_name == e.name:
                        # add edge to another node
                        next_node = self.next_node(e.first, e.second)
                        self.add_edge(e.name, e.time, e.first, next_node)
                        # remove
                        print("Removed edge: %s (%s -> %s)" % (e.name, e.first, e.second))
                        self.in_edges[edge.second].remove(e)
                        self.edges.remove(e)
                        break
            self.check_ends()

            # need to add some zero edges
            dif = [a for a in set(element.previous_activities)
                .difference(set(edge.name for edge in self.in_edges[edge.second]))]
            print("Difference (add zero): %s " % dif)
            for e_name in dif:
                # add zero edge
                f = None
                for e in self.edges:
                    if e_name == e.name:
                        f = e.second
                self.add_edge(e_name, 0, f, edge.second)
            self.check_ends()

            next_node = self.next_node(edge.second)
            self.add_edge(element.activity, element.time, edge.second, next_node)

        self.check_ends()
        print("Ends: %s" % self.ends)
        print("Connected: %s" % self.connected_nodes)

    def add_edge(self, a, t, f, s):
        print("Added edge: %s (%s -> %s)" % (a, f, s))
        edge = Edge(a, t, f, s)
        self.edges.append(edge)
        self.in_edges[s].append(edge)
        fs = str(f) + " " + str(s)
        sf = str(s) + " " + str(f)
        self.connected_nodes.add(fs)
        self.connected_nodes.add(sf)

    def next_node(self, previous, removed=0):
        for end in reversed(self.ends):
            pe = str(previous) + " " + str(end)
            if pe not in self.connected_nodes:
                print(self.connected_nodes)
                print(pe)
                if end != previous and end > removed:
                    return end
        self.max_node += 1
        # self.connected_nodes[previous].append(self.max_node)
        return self.max_node

    def check_ends(self):
        self.ends.clear()
        not_ends = set()
        all_nodes = set()

        for i in range(1, self.max_node + 1):
            all_nodes.add(i)
            for edge in self.edges:
                if edge.first == i:
                    not_ends.add(i)

        self.ends = list(all_nodes.difference(not_ends))

    def reduce(self):
        # reduce endings
        if len(self.ends) > 1:
            min_edge = min(e for e in self.ends)
            print("Reduce ends into %s" % min_edge)
            for edge in self.edges:
                if edge.second in self.ends and edge != min_edge:
                    # we want to remove node
                    edge.second = min_edge
            self.ends = [min_edge]


def parse_events_into_queue(file_lines):
    lines = [line.rstrip('\n') for line in file_lines]
    lines = [line.split(' ') for line in lines]
    print(lines)

    data_actions = []
    graph = Graph()

    for i in lines:
        data_action = DataElementActions(i[0], i[1], [i[j] for j in range(2, len(i))])
        data_actions.append(data_action)

    for data_action in data_actions:
        graph.add_activity(data_action)

    return graph.to_queue()
