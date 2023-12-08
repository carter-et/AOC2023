import time as time

RED_MAX = 12
GREEN_MAX = 13
BLUE_MAX = 14

def processFile(file):
    total = 0
    for line in file:
        isPossible = True
        data = line.split(':')
        gameId = data[0]
        gameBag = data[1].split(';')
        for pull in gameBag:
            show = pull.split(',')
            for block in show:
                x = "".join(list(filter(lambda x: x.isdigit(), block)))
                val = int(x)
                if block.find('red') != -1 and val > RED_MAX:
                    isPossible = False
                    break
                elif block.find('green') != -1 and val > GREEN_MAX:
                    isPossible = False
                    break
                elif block.find('blue') != -1 and val > BLUE_MAX:
                    isPossible = False
                    break
            
        if isPossible:
            
            idVal = "".join(list(filter(lambda x: x.isdigit(), gameId)))
            total += int(idVal)
    return total

def processFilePartTwo(file):
    total = 0
    for line in file:
        data = line.split(':')
        gameBag = data[1].split(';')
        power = 0
        maxBlocks = {
                "red": 0,
                "green": 0,
                "blue": 0
            }
        for pull in gameBag:
            show = pull.split(',')
            for block in show:
                x = "".join(list(filter(lambda x: x.isdigit(), block)))
                val = int(x)
                if block.find('red') != -1:
                    if val > maxBlocks["red"]:
                        maxBlocks.update({'red': val})
                elif block.find('green') != -1:
                    if val > maxBlocks["green"]:
                        maxBlocks.update({'green': val})
                elif block.find('blue') != -1:
                    if val > maxBlocks["blue"]:
                        maxBlocks.update({'blue': val})
        total += (maxBlocks['red'] * maxBlocks['green'] * maxBlocks['blue']) 
    return total

def run():
    file = open('./day02/data.txt', 'r')
    answer = processFilePartTwo(file)
    print(answer)

if __name__ == "__main__":
    s_time = time.time()
    run()
    e_time = time.time()
    print('Time: ', e_time - s_time)