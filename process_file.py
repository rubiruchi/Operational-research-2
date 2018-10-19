def parse_line_into_queue(file_lines):
    queue = []
    lines = [line.rstrip('\n') for line in file_lines]
    lines = [line.split(' ') for line in lines]
    print(lines)
    for i in lines:
        for j in i:
            queue.append(j)
    return queue

