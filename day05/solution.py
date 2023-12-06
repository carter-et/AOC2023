from enum import Enum
import time as time

class DataTypes(Enum):
    Seeds = 0
    SeedToSoil = 1
    SoilToFertilizer = 2 
    FertilizerToWater = 3
    WaterToLight = 4
    LightToTempurature = 5
    TempuratureToHumidity = 6
    HumdityToLocation = 7

class ConversionMap:
    def __init__(self, sourceStart, destinationStart, range):
        self.sourceStart = int(sourceStart)
        self.sourceEnd = int(sourceStart) + int(range) - 1
        self.destinationStart = int(destinationStart)
        self.range = int(range)
        self.transposition = int(destinationStart) - int(sourceStart)
    
    def isInRange(self, value):
        return (value >= self.sourceStart) and (value <= self.sourceEnd)
    
    def getDestination(self, item):
        diff = item - self.sourceStart
        return self.destinationStart + diff
    
    def transposePair(self, pair):
        return Pair(pair.start + self.transposition, pair.end + self.transposition)
    
    def __repr__(self):
        return "[%d - %d] (%d)" % (self.sourceStart, self.sourceEnd, self.transposition)

class Pair:
    def __init__(self, start, end):
        self.start = int(start)
        self.end = int(end)
    
    def __repr__(self):
        return "[%d - %d]" % (self.start, self.end)

'''
################################################################################
Helper Methods
################################################################################
'''

def getStringConversion(type):
    if type == DataTypes.Seeds: return "seeds:"
    if type == DataTypes.SeedToSoil: return "seed-to-soil map:"
    if type == DataTypes.SoilToFertilizer: return "soil-to-fertilizer map:" 
    if type == DataTypes.FertilizerToWater: return "fertilizer-to-water map:"
    if type == DataTypes.WaterToLight: return "water-to-light map:"
    if type == DataTypes.LightToTempurature: return "light-to-temperature map:"
    if type == DataTypes.TempuratureToHumidity: return "temperature-to-humidity map:"
    if type == DataTypes.HumdityToLocation: return "humidity-to-location map:"

# expects the lines of the file 
def processData(file):
    maps = []

    # process seed values
    line = file.readline()
    str = getStringConversion(DataTypes.Seeds)
    startingSpot = line.find(str) + len(str)
    seeds = line[startingSpot:].split()
    seeds = pairSeeds(seeds)

    # skip to Seed To Soil conversion map
    while(True):
        line = file.readline()
        if(line != '\n'):
            break

    # maps kinda looks like [[type, maps[]], [type, maps[]]]
    maps.append([DataTypes.SeedToSoil, readMapData(file)])
    maps.append([DataTypes.SoilToFertilizer, readMapData(file)])
    maps.append([DataTypes.FertilizerToWater, readMapData(file)])
    maps.append([DataTypes.WaterToLight, readMapData(file)])
    maps.append([DataTypes.LightToTempurature, readMapData(file)])
    maps.append([DataTypes.TempuratureToHumidity, readMapData(file)])
    maps.append([DataTypes.HumdityToLocation, readMapData(file)])

    return (seeds, maps)

# continues reading a file until next segment, adding notable lines to the maps
def readMapData(file):
    maps = []
    while(True):
        line = file.readline()
        if(line != '\n'):
            # check to see if we made it to the next conversion map
            if(":" in line):
                break
            elif(not line):
                break
            tmp = line.split()
            # the problem gives you dest, src, rng, but my obj order has the first 2 flipped
            maps.append(ConversionMap(tmp[1], tmp[0], tmp[2])) 
    
    return maps

# scope the big list of maps, filtering by type
def scopeMaps(maps, type):
    return maps[type]

# convert seeds into pairs
def pairSeeds(seeds):
    list = [] 
    for x in range(len(seeds)):
        if(x % 2 == 0):
            if(x == len(seeds) - 1):
                pass
            else:
                start = seeds[x]
                rng = seeds[x+1]
                end = int(start) + int(rng) - 1
                pair = Pair(int(start), int(end))
                list.append(pair)
    return list

def getLayer(maps, type):    
    def bySource(e):
        return e.sourceStart
    
    layer = []
    for set in maps:
        if set[0] == type:
            layer = set[1]
    
    layer.sort(key=bySource)
    return layer

# sort pairs after they get filtered by a layer
def sortPairs(pairs):
    def byStart(e):
        return e.start
    
    pairs.sort(key=byStart)
    return pairs

# squish pairs so that if two ranges overlap, they are combined
def squishPairs(pairs):
    pass

# create additional pairs by splitting them off of current pairs, if they would collide with a layer
def fracturePairs(pairs, layer):
    pass

# convert any pairs that now cleanly collide with the layer
def filterPairs(pairs, layer):
    newPairs = []
    for pair in pairs:
        # print(pair)
        interaction = False
        for map in layer:
            # print(map)
            # check if the left boundary on the map segment intersects this pair
            if (map.sourceStart >= pair.start and map.sourceStart <= pair.end):
                interaction = True
                print(1)
                # check if the right boundary on the map segement intersects this pair
                if (map.sourceEnd <= pair.end):
                    print(2)
                    newPairs.append(Pair(pair.start, map.sourceStart - 1))
                    shiftedPair = map.transposePair(Pair(map.sourceStart, map.sourceEnd))
                    newPairs.append(shiftedPair)
                    # this adds additional work that should be checked, just in case there are more than 2 intersections
                    pairs.append(Pair(map.sourceEnd + 1, pair.end))
                else:
                    print(3)
                    newPairs.append(Pair(pair.start, map.sourceStart - 1))
                    shiftedPair = map.transposePair(Pair(map.sourceStart, pair.end))
                    newPairs.append(shiftedPair)
                break
            # if the left boundary didnt cross, then there's only one option left
            elif (map.sourceEnd >= pair.start and map.sourceEnd <= pair.end):
                interaction = True
                print(4)
                shiftedPair = map.transposePair(Pair(pair.start, map.sourceEnd))
                newPairs.append(shiftedPair)
                # this adds additional work that should be checked, just in case there are more than 2 intersections
                pairs.append(Pair(map.sourceEnd + 1, pair.end))
                break
            # if the boundaries on the map cover the pair
            elif (map.sourceStart <= pair.start and map.sourceEnd >= pair.end):
                interaction = True
                print(5)
                shiftedPair = map.transposePair(pair)
                newPairs.append(shiftedPair)
                break
            # if the pair is "left", then we assume we've already checked any relevant layer filters
            elif (map.sourceStart > pair.end and not interaction):
                interaction = True
                print(6)
                newPairs.append(pair)
                break
        if not interaction:
            print(7)
            newPairs.append(pair)
        
    return newPairs

# fucking magic, part one. prob has breaking changes from part two.
def getSmallestLocation(seedPairs, maps):
    # oh no
    smallestLocation = 999999999

    order = [DataTypes.SeedToSoil, DataTypes.SoilToFertilizer, DataTypes.FertilizerToWater, DataTypes.WaterToLight, DataTypes.LightToTempurature, DataTypes.TempuratureToHumidity, DataTypes.HumdityToLocation]
    value = None
    
    for pair in seedPairs:
        for seed in range(pair[0], pair[0] + pair[1]):
            print(seed)
            value = int(seed)
            for step in order:
                scopedMaps = scopeMaps(maps, step)
                for map in scopedMaps:
                    if map.isInRange(value):
                        value = map.getDestination(value)
                        # because value is updated, it might match another map, so break out of this
                        break
                    
            if value < smallestLocation:
                smallestLocation = value
    
    return smallestLocation

# fucking magic, part two
def getSmallestLocationPartTwo(pairs, maps):
    order = [DataTypes.SeedToSoil, DataTypes.SoilToFertilizer, DataTypes.FertilizerToWater, DataTypes.WaterToLight, DataTypes.LightToTempurature, DataTypes.TempuratureToHumidity, DataTypes.HumdityToLocation]

    print(pairs)
    # print(maps)

    for step in order:
        print(step)
        layer = getLayer(maps, step)
        print('layer')
        print(layer)
        pairs = filterPairs(pairs, layer)
        print('filtered pairs')
        print(pairs)
        pairs = sortPairs(pairs)
        print('sorted pairs')
        print(pairs)

    print(pairs[0].start)
    return 0

def run():
    file = open('./day05/data.txt', 'r')
    (seedPairs, maps) = processData(file)
    
    answer = getSmallestLocationPartTwo(seedPairs, maps)
    print(answer)

if __name__ == "__main__":
    s_time = time.time()
    run()
    e_time = time.time()
    print('Time: ', e_time - s_time)
    pass