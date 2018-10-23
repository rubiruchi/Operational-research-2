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

    def to_queue(self):
        queue = []
        for edge in self.edges:
            queue.append(edge.name)
            queue.append(edge.time)
            queue.append(str(edge.first))
            queue.append(str(edge.second))
        return queue

    def add_activity(self, element):
        next_node = self.next_node()
        if element.previous_activities[0] == '-':
            print("Added edge: %s (%s -> %s)" % (element.activity, 1, next_node))
            self.edges.append(Edge(element.activity, element.time, 1, next_node))
        else:
            for activity in element.previous_activities:
                for edge in self.edges:
                    if edge.name == activity:
                        print("Added edge: %s (%s -> %s)" % (element.activity, edge.second, next_node))
                        self.edges.append(Edge(element.activity, element.time, edge.second, next_node))
                        break
        self.check_ends()
        print("Ends: %s" % self.ends)

    def next_node(self):
        self.max_node += 1
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
    graph.reduce()
    return graph.to_queue()

    # data_actions = []
    # ends = set()
    # current_event = 1
    # z_counter = 1
    # data_events = {}
    # connected_nodes = defaultdict(list)
    # nodes = set()
    #
    # for i in lines:
    #     data_action = DataElementActions(i[0], i[1], [i[j] for j in range(2, len(i))])
    #     data_actions.append(data_action)
    #
    # for data_action in data_actions:
    #     if data_action.previous_activities == ['-']:
    #         data_event = DataElementEvents(data_action.activity, data_action.time, 1, None)
    #         if current_event in connected_nodes[data_event.first_event] or current_event == data_event.first_event:
    #             current_event += 1
    #             ends.add(current_event)
    #         ends.discard(data_event.first_event)
    #         data_event.second_event = current_event
    #         data_events[data_action.activity] = data_event
    #         connected_nodes[data_event.first_event].append(data_event.second_event)
    #         nodes.add(data_event.first_event)
    #         nodes.add(data_event.second_event)
    #     else:
    #         shared_event = min(data_events[action].second_event for action in data_action.previous_activities)
    #         for action in data_action.previous_activities:
    #             if data_events[action].second_event != shared_event:
    #                 data_event = DataElementEvents("Z" + str(z_counter), 0, data_events[action].second_event,
    #                                                shared_event)
    #                 data_events[data_event.activity] = data_event
    #                 z_counter += 1
    #
    #         data_event = DataElementEvents(data_action.activity, data_action.time, shared_event, None)
    #         if current_event in connected_nodes[data_event.first_event] \
    #                 or current_event == data_event.first_event:
    #             if len(ends) > 1:
    #                 for end in ends:
    #                     if end not in connected_nodes[data_event.first_event]:
    #                         current_event = end
    #                         data_event.second_event = end
    #                         break
    #             else:
    #                 current_event += 1
    #                 while current_event in nodes:
    #                     current_event += 1
    #                 ends.add(current_event)
    #                 data_event.second_event = current_event
    #         ends.discard(data_event.first_event)
    #         data_events[data_action.activity] = data_event
    #         connected_nodes[data_event.first_event].append(data_event.second_event)
    #         nodes.add(data_event.first_event)
    #         nodes.add(data_event.second_event)
    #
    #     print(data_action.activity)
    #     print(data_events)
    #     print(connected_nodes)
    #     print("Ends %s" % ends)
    #
    # for key, data_event in data_events.items():
    #     queue.append(data_event.activity)
    #     queue.append(data_event.time)
    #     queue.append(str(data_event.first_event))
    #     queue.append(str(data_event.second_event))
    #
    # print(queue)
    # return queue
