def parse_line(line):
    line = line.rstrip("\n")
    line = line.split(" ")
    return line


def read_data(file):
    queue = []
    line = file.readline()
    queue.append(parse_line(line))
    while line:
        line = file.readline()
        queue.append(parse_line(line))
    queue.pop(-1)
    print(queue)
    return queue

# def choose_file():
#     Tk().withdraw()
#     filename = askopenfilename()
#     print(filename)
#     read_data(filename)
#
# choose_file()

