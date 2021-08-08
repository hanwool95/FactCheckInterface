


with open('wiki.csv', 'r') as f:
    a = []
    for line in f:
        a.append(line[4])
    a.sort(reverse=True)
    print(a)
    print(a[len(a)//5])