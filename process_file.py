from collections import Counter


def parse_actions_into_queue(file_lines):
    queue = []
    lines = [line.rstrip('\n') for line in file_lines]
    lines = [line.split(' ') for line in lines]
    print(lines)
    for i in lines:
        for j in i:
            queue.append(j)
    return queue


first_action_counter = 1

def parse_events_into_queue(file_lines):
    queue = []
    lines = [line.rstrip('\n') for line in file_lines] # przewaznie rozbijam plik usuwajac \n
    lines = [line.split(' ') for line in lines] # i splitujac tak zebym mial komorki pojedyncze
    print(lines)
    # TODO: 1. Usuwanie tutaj..
    successor_index = 3
    for data_cell in lines:
        construct_field(data_cell,queue)
        # Poprzednia iteracja calej funkcji
        #
        #
        # for value in data_cell:
        #     #Has no previous actions
        #     if value == '-':
        #         first_action_counter += 1
        #         queue.append("1")
        #         queue.append(str(first_action_counter))
        #     #Check if we are on 3rd data_cell and its not "-"
        #     elif str.isalpha(value) and data_cell.index(value) > 0:
        #         value.replace(",", "") #for more than 1
        #         if len(value) == 1:
        #             index = queue.index(value)
        #             value_of_indexed = queue[index + successor_index]
        #             queue.append(value_of_indexed)
        #             second_action_counter = int(find_highest_event(queue)) + 1
        #             queue.append(str(second_action_counter))
        #         else:
        #             value = list(value)
        #             print(queue)
        #             found_previous_events = []
        #             for previous_event in range(0, len(queue), 4):
        #                 if queue[previous_event] in value:
        #                     index = queue.index(queue[previous_event])
        #                     value_of_indexed = queue[index + successor_index]
        #                     found_previous_events.append(value_of_indexed)
        #                     # index = queue.index(previous_event)
        #                     # value_of_indexed = queue[index + successor_index]
        #                     # queue.append(value_of_indexed)
        #             print("Found previous events")
        #             print(found_previous_events)
        #             found_keys = Counter(found_previous_events).keys()
        #             for key in found_keys:
        #                 queue.append()
        #
        #
        #     #Not on previous event so simply adding value
        #     else:
        #         queue.append(value)
    print(queue)
    return(queue)

# TODO: Ta raczej tez cala mozna wywalic..
def construct_field(data_cell, queue):
    ACTION_INDEX = 0
    TIME_INDEX = 1
    FIRST_EVENT_INDEX = 2           # To zrobilem po to zeby bylo przejrzysciej mi sie dostawac do poszczegolnych pol fielda zamiast robic osobna klase
    SECOND_EVENT_INDEX = 3          # co prawda no.. malo sensu to mialo
    field = [None]*4                # po to zeby nie uzywac append tylko sie odwolywac wlasnie
    global first_action_counter     # to jest zmienna inkrementowana dla poczatkowego zdarzania danej akcji ( czyli to 1->2, to to bedzie 1)

    field[ACTION_INDEX] = data_cell[ACTION_INDEX] # wpisuje pierwsze wartosci fielda
    field[TIME_INDEX] = data_cell[TIME_INDEX]

    data_cell[FIRST_EVENT_INDEX] = data_cell[FIRST_EVENT_INDEX].replace(",","")  # replace w przypadku gdy w pliku mamy wpisane B,C,D dlatego bo inaczej isAlpha dawalo false

    if data_cell[FIRST_EVENT_INDEX] == '-': # gdzie nie ma poprzednich zdarzen
        first_action_counter += 1
        field[FIRST_EVENT_INDEX] = "1"  # na sztywno wpisany
        field[SECOND_EVENT_INDEX] = str(first_action_counter)  # wyliczony z tej globalnej
    # Sprawdzane 3 wydarzenie czy char i czy i czy index wiekszy niz 3, to tak naprawde pozostalosc tej poprzedniej funkcji wiec troche zly jest
    elif str.isalpha(data_cell[FIRST_EVENT_INDEX]) and data_cell.index(data_cell[FIRST_EVENT_INDEX]) > 0:
        # sprawdzanie czy dlugosc jest jeden bo to przypadek gdzie jest 1 wydarzenie wczesniejsze
        if len(data_cell[FIRST_EVENT_INDEX]) == 1:
            index = queue.index(data_cell[FIRST_EVENT_INDEX])      # wylapanie indexu wczesniejszego wydarzenia
            value_of_indexed = queue[index + SECOND_EVENT_INDEX]   # przesuniecie tak zeby wyciagnac nr jego zdarzenia koncowego
            field[FIRST_EVENT_INDEX] = value_of_indexed
            second_action_counter = int(find_highest_event(queue)) + 1 # znalezienie najwiekszego poprzedniego i zwiekszenie o 1
            field[SECOND_EVENT_INDEX] = str(second_action_counter)     # BUG 1: Mozliwosc ze sa rowne i wtedy wywali sie przy rysowaniu
        else:
            # Przypadek gdzie wiecej niz 1 zdarzenie
            list_of_events = list(data_cell[FIRST_EVENT_INDEX])  # Zamiana na liste zeby byly pojedynczo
            found_previous_events = []
            for previous_event in range(0, len(queue), 4):        # Petla skaczaca tylko po nazwach wydarzeniach juz przeparsowanych
                if queue[previous_event] in list_of_events:       # Jesli znajdzie takie wydarzenie to wyciaga jego wartosci
                    index = queue.index(queue[previous_event])    # index
                    value_of_indexed = queue[index + SECOND_EVENT_INDEX]     # zdarzenie koncowe
                    found_previous_events.append(value_of_indexed)   # wrzuca do listy koncowych zdarzen znalezionych
            print(found_previous_events)
            found_keys = Counter(found_previous_events)  # zlicza ich ilosc i daje taka mape gdzie najwyzszy jest 1 elementem
            # BUG 2: lipa jest gdy sa jakies 2 rowne siebie..
            highest_counter = max(found_keys.values()) #wyciaga ten najwyzszy bo z dict nie dalo sie bezposrednio wyciagnac jego wartosci (nie wiem czemu..)
            for value, key in found_keys.items(): # petla po tych znalezionych
                if key == highest_counter: # i tu jest wlasnie bug
                    field[FIRST_EVENT_INDEX] = value
                    field[SECOND_EVENT_INDEX] = str(find_highest_event(queue))  # nie zwiekszam o 1 bo to prawodpodobnie tez prowadzi do wspolnego
                    if field[SECOND_EVENT_INDEX] == field[FIRST_EVENT_INDEX]:   # check czy sa rowne
                        field[SECOND_EVENT_INDEX] = str(int(field[SECOND_EVENT_INDEX])+1)
                else:
                    #mock_field to w zasadzie kazdy dodatkowy zrobiony jesli bedzie wiecej niz 1, w calosci w zasadzi jest to bledne podejscie wiec no
                    # TO BE DELETED
                    mock_field = [None] * 4
                    mock_field[ACTION_INDEX] = ' '
                    mock_field[TIME_INDEX] = 0
                    mock_field[FIRST_EVENT_INDEX] = str(value)
                    mock_field[SECOND_EVENT_INDEX] = field[FIRST_EVENT_INDEX]
                    for i in mock_field: #Wrzucanie do kolejki po kolei zeby zachowac ta sama strukture
                        queue.append(i)
            print(found_keys)
            # for key in found_keys:
            #     queue.append()
    for i in field: #tutaj tez
        queue.append(i)


def find_highest_event(queue):
    events = []
    for i in range(3 , len(queue), 4):
        events.append(queue[i])
    return max(events)