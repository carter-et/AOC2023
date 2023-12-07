import time as time
import re as regex

def getFirst(line):
    pos = regex.search(r"\d", line).group()
    return pos

def getLast(line):
    line = line[::-1]
    pos = regex.search(r"\d", line).group()
    return pos

def search(line, pattern):
    return line.find(pattern)

def getFirstString(line):
    matches = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    pos = len(line)
    val = None
    for i in range(0, len(matches)):
        check = search(line, matches[i])
        if (check != -1 and check < pos):
            pos = check
            val = values[i]
    
    return "%d" % val

def getLastString(line):
    matches = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    line = line[::-1]

    pos = len(line)
    val = None
    for i in range(0, len(matches)):
        reverseMatch = matches[i][::-1]
        check = search(line, reverseMatch)
        if (check != -1 and check < pos):
            pos = check
            val = values[i]
    
    return "%d" % val

def processFilePartTwo(file):
    sum = 0
    for line in file:
        digits = "".join([getFirstString(line), getLastString(line)])
        num = int(digits)
        sum += num
        pass

    return sum

def processFile(file):
    sum = 0
    for line in file:
        digits = "".join([getFirst(line), getLast(line)])
        num = int(digits)
        sum += num
        pass

    return sum

def run():
    file = open('./day01/data.txt', 'r')
    # answer = processFile(file)
    answer = processFilePartTwo(file)
    print(answer)

if __name__ == "__main__":
    s_time = time.time()
    run()
    e_time = time.time()
    print('Time: ', e_time - s_time)