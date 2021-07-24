with open('data.csv', 'r') as rfile:
    lines = rfile.readlines()

wfile = open('data-clean.csv', 'w')

wfile.write(lines[0])

for line in lines[1:]:
    try:
        l = line.rstrip('\n').split(',')
        *_, numeric = l
        float(numeric)
        wfile.write(line)
    except Exception as e:
        pass
