from lib.utility.time import hour


def printc(prefix, content, count):
    if count == 0:
        print(prefix + " " + content)
    else:
        line = ""
        for i in range(count):
            line = line + "="
        print(line + "\n" + prefix + " " + str(hour()) + " " + content + "\n" + line)
