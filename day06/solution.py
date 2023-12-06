import time as time

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
            hold = ms
            run = time - hold
            result = run * hold
            if result > distance:
                print("%d meets targed distance of: %d on run: %d" % (result, distance, hold))
                if ((time + 1) % 2 == 0):
                    print("%d + 1 is even" % (time))
                    halfway = (time + 1) / 2
                    print("%d is halfway" % (halfway))
                    halfOfRun = halfway - hold
                    print("%d is half of run" % (halfOfRun))
                    runs = halfOfRun * 2
                    count = runs
                else:
                    print("%d + 1 is odd" % (time))
                    halfway = (time + 1) / 2
                    print("%d is halfway" % (halfway))
                    halfOfRun = halfway - hold
                    print("%d is half of run" % (halfOfRun))
                    runs = (halfOfRun * 2)
                    count = runs
                perms.append(int(count))
                break
                
        print("amount of successful runs this competition: %d" % int(count))
    print(perms)
    return perms

# return the data as a set of both sets [[time, distance], [time, distance], ...]
def processFile(file):
    line = file.readline()
    times = line[line.find(':') + 1:].split()
    print(times)
    line = file.readline()
    distances = line[line.find(':') + 1:].split()
    print(distances)

    competitions = []
    for i in range(0, len(times)):
        competitions.append([times[i], distances[i]])

    print(competitions)
    return competitions

def processFilePartTwo(file):
    line = file.readline()
    times = ''.join(line[line.find(':') + 1:].split())
    print(times)

    line = file.readline()
    distances = ''.join(line[line.find(':') + 1:].split())
    print(distances)

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