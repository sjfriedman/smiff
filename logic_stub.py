with open("logic_input.txt", 'r') as f:
    lines = [entry.strip() for entry in f.readlines()]
    for line in lines:
        print(line)