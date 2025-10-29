L = list(open("man_frames.txt"))

f = open("man1.txt","a")

while L:
    frame = L[:27]
    L = L[54:]

    f.write('printf(1, "\\x1b[2J\\x1b[H");\n')
    f.write('printf(1, "\\\n')
    for i in frame:
        f.write(i[:-3]+"\\n\\\n")
    f.write('");\n')
    f.write('sleep(4);\n')


f.close()