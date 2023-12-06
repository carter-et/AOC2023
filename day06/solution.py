import time as time

def getRunsFromHold(time, hold):
    runs = 0
    if ((time + 1) % 2 == 0):
        runs = (((time + 1) / 2) - hold) * 2
    else:
        runs = ((((time + 1) / 2) - hold) * 2)

    return runs

def multiplicationOfAllPerms(perms):
    result = 1
    for i in range(0, len(perms)):
        result = result * perms[i]
    return result

def getCompetitionPerms(competitions):
    perms = []
    for competition in competitions:
        count = 0
        time = int(competition[0])
        distance = int(competition[1])
        for ms in range(0, time):
            holdtime = ms
            runtime = time - holdtime
            result = runtime * holdtime
            if result > distance:
                count = getRunsFromHold(time, holdtime)
                perms.append(int(count))
                break
    return perms

# return the data as a set of both sets [[time, distance], [time, distance], ...]
def processFile(file):
    line = file.readline()
    times = line[line.find(':') + 1:].split()
    line = file.readline()
    distances = line[line.find(':') + 1:].split()
    competitions = []
    for i in range(0, len(times)):
        competitions.append([times[i], distances[i]])

    print(competitions)
    return competitions

def processFilePartTwo(file):
    line = file.readline()
    times = ''.join(line[line.find(':') + 1:].split())
    line = file.readline()
    distances = ''.join(line[line.find(':') + 1:].split())
    competitions = []
    competitions.append([times, distances])

    print(competitions)
    return competitions

def run():
    file = open('./day06/data.txt', 'r')
    # data = processFile(file)
    data = processFilePartTwo(file)
    perms = getCompetitionPerms(data)
    answer = multiplicationOfAllPerms(perms)
    print(answer)


if __name__ == "__main__":
    s_time = time.time()
    run()
    e_time = time.time()
    print('Time: ', e_time - s_time)