import os
import sys
import time
import random


def read_file_into_string(input_file, from_ord, to_ord):
    # take a file "input_file", read it character by character, strip away all unwanted
    # characters with ord < "from_ord" and ord > "to_ord" and return the concatenation
    # of the file as the string "output_string"
    the_file = open(input_file, 'r')
    current_char = the_file.read(1)
    output_string = ""
    while current_char != "":
        if ord(current_char) >= from_ord and ord(current_char) <= to_ord:
            output_string = output_string + current_char
        current_char = the_file.read(1)
    the_file.close()
    return output_string


def stripped_string_to_int(a_string):
    # take a string "a_string" and strip away all non-numeric characters to obtain the string
    # "stripped_string" which is then converted to an integer with this integer returned
    a_string_length = len(a_string)
    stripped_string = "0"
    if a_string_length != 0:
        for i in range(0, a_string_length):
            if ord(a_string[i]) >= 48 and ord(a_string[i]) <= 57:
                stripped_string = stripped_string + a_string[i]
    resulting_int = int(stripped_string)
    return resulting_int


def get_string_between(from_string, to_string, a_string, from_index):
    # look for the first occurrence of "from_string" in "a_string" starting at the index
    # "from_index", and from the end of this occurrence of "from_string", look for the first
    # occurrence of the string "to_string"; set "middle_string" to be the sub-string of "a_string"
    # lying between these two occurrences and "to_index" to be the index immediately after the last
    # character of the occurrence of "to_string" and return both "middle_string" and "to_index"
    middle_string = ""  # "middle_string" and "to_index" play no role in the case of error
    to_index = -1  # but need to initialized to something as they are returned
    start = a_string.find(from_string, from_index)
    if start == -1:
        flag = "*** error: " + from_string + " doesn't appear"
        # trace_file.write(flag + "\n")
    else:
        start = start + len(from_string)
        end = a_string.find(to_string, start)
        if end == -1:
            flag = "*** error: " + to_string + " doesn't appear"
            # trace_file.write(flag + "\n")
        else:
            middle_string = a_string[start:end]
            to_index = end + len(to_string)
            flag = "good"
    return middle_string, to_index, flag


def string_to_array(a_string, from_index, num_cities):
    # convert the numbers separated by commas in the file-as-a-string "a_string", starting from index "from_index",
    # which should point to the first comma before the first digit, into a two-dimensional array "distances[][]"
    # and return it; note that we have added a comma to "a_string" so as to find the final distance
    # distance_matrix = []
    if from_index >= len(a_string):
        flag = "*** error: the input file doesn't have any city distances"
        # trace_file.write(flag + "\n")
    else:
        row = 0
        column = 1
        row_of_distances = [0]
        flag = "good"
        while flag == "good":
            middle_string, from_index, flag = get_string_between(",", ",", a_string, from_index)
            from_index = from_index - 1  # need to look again for the comma just found
            if flag != "good":
                flag = "*** error: there aren't enough cities"
                # trace_file.write(flag + "\n")
            else:
                distance = stripped_string_to_int(middle_string)
                row_of_distances.append(distance)
                column = column + 1
                if column == num_cities:
                    distance_matrix.append(row_of_distances)
                    row = row + 1
                    if row == num_cities - 1:
                        flag = "finished"
                        row_of_distances = [0]
                        for i in range(0, num_cities - 1):
                            row_of_distances.append(0)
                        distance_matrix.append(row_of_distances)
                    else:
                        row_of_distances = [0]
                        for i in range(0, row):
                            row_of_distances.append(0)
                        column = row + 1
        if flag == "finished":
            flag = "good"
    return flag


def make_distance_matrix_symmetric(num_cities):
    # make the upper triangular matrix "distance_matrix" symmetric;
    # note that there is nothing returned
    for i in range(1, num_cities):
        for j in range(0, i):
            distance_matrix[i][j] = distance_matrix[j][i]


# read input file into string

#######################################################################################################
############ now we read an input file to obtain the number of cities, "num_cities", and a ############
############ symmetric two-dimensional list, "distance_matrix", of city-to-city distances. ############
############ the default input file is given here if none is supplied via a command line   ############
############ execution; it should reside in a folder called "city-files" whether it is     ############
############ supplied internally as the default file or via a command line execution.      ############
############ if your input file does not exist then the program will crash.                ############

input_file = "AISearchfile180.txt"

#######################################################################################################

# you need to worry about the code below until I tell you; that is, do not touch it!

if len(sys.argv) == 1:
    file_string = read_file_into_string("./city-files/" + input_file, 44, 122)
else:
    input_file = sys.argv[1]
    file_string = read_file_into_string("./city-files/" + input_file, 44, 122)
file_string = file_string + ","  # we need to add a final comma to find the city distances
# as we look for numbers between commas
print("I'm working with the file " + input_file + ".")

# get the name of the file

name_of_file, to_index, flag = get_string_between("NAME=", ",", file_string, 0)

if flag == "good":
    print("I have successfully read " + input_file + ".")
    # get the number of cities
    num_cities_string, to_index, flag = get_string_between("SIZE=", ",", file_string, to_index)
    num_cities = stripped_string_to_int(num_cities_string)
else:
    print("***** ERROR: something went wrong when reading " + input_file + ".")
if flag == "good":
    print("There are " + str(num_cities) + " cities.")
    # convert the list of distances into a 2-D array
    distance_matrix = []
    to_index = to_index - 1  # ensure "to_index" points to the comma before the first digit
    flag = string_to_array(file_string, to_index, num_cities)
if flag == "good":
    # if the conversion went well then make the distance matrix symmetric
    make_distance_matrix_symmetric(num_cities)
    print("I have successfully built a symmetric two-dimensional array of city distances.")
else:
    print("***** ERROR: something went wrong when building the two-dimensional array of city distances.")

#######################################################################################################
############ end of code to build the distance matrix from the input file: so now you have ############
############ the two-dimensional "num_cities" x "num_cities" symmetric distance matrix     ############
############ "distance_matrix[][]" where "num_cities" is the number of cities              ############
#######################################################################################################

# now you need to supply some parameters ...

#######################################################################################################
############ YOU NEED TO INCLUDE THE FOLLOWING PARAMETERS:                                 ############
############ "my_user_name" = your user-name, e.g., mine is dcs0ias                        ############

my_user_name = "jgwp24"

############ "my_first_name" = your first name, e.g., mine is Iain                         ############

my_first_name = "Ben"

############ "my_last_name" = your last name, e.g., mine is Stewart                        ############

my_last_name = "Harries"

############ "alg_code" = the two-digit code that tells me which algorithm you have        ############
############ implemented (see the assignment pdf), where the codes are:                    ############
############    BF = brute-force search                                                    ############
############    BG = basic greedy search                                                   ############
############    BS = best_first search without heuristic data                              ############
############    ID = iterative deepening search                                            ############
############    BH = best_first search with heuristic data                                 ############
############    AS = A* search                                                             ############
############    HC = hilling climbing search                                               ############
############    SA = simulated annealing search                                            ############
############    GA = genetic algorithm                                                     ############

alg_code = "GA"

############ you can also add a note that will be added to the end of the output file if   ############
############ you like, e.g., "in my basic greedy search, I broke ties by always visiting   ############
############ the first nearest city found" or leave it empty if you wish                   ############

added_note = ""

############ the line below sets up a dictionary of codes and search names (you need do    ############
############ nothing unless you implement an alternative algorithm and I give you a code   ############
############ for it when you can add the code and the algorithm to the dictionary)         ############

codes_and_names = {'BF': 'brute-force search',
                   'BG': 'basic greedy search',
                   'BS': 'best_first search without heuristic data',
                   'ID': 'iterative deepening search',
                   'BH': 'best_first search with heuristic data',
                   'AS': 'A* search',
                   'HC': 'hilling climbing search',
                   'SA': 'simulated annealing search',
                   'GA': 'genetic algorithm'}

#######################################################################################################
############    now the code for your algorithm should begin                               ############
#######################################################################################################

import timeit, numpy as np


def chooseParents(fitnessArr):
    # prob = random.random()
    # i = 0
    # while prob > fitnessArr[i]:
    #     if i < len(fitnessArr)-1:
    #         i = i + 1
    #     else:
    #         print("yep")
    #         break
    return random.randrange(len(fitnessArr))


def distBetweenCities(fromTown, toTown):
    distance = distance_matrix[fromTown][toTown]
    return distance


class RouteFitness:
    def __init__(self, route):
        self.route = route
        self.distance = 0
        self.fitness = 0.0

    def tourDistance(self):
        if self.distance == 0:
            pathDistance = 0
            for i in range(0, len(self.route)):
                fromTown = self.route[i]
                toTown = None
                if i + 1 < len(self.route):
                    toTown = self.route[i + 1]
                else:
                    toTown = self.route[0]
                pathDistance += distBetweenCities(fromTown, toTown)
            self.distance = pathDistance
        return self.distance


def fitness(population):
    fitnessResults = {}
    normalisedFitness = {}
    totalFitness = 0
    for i in range(0, len(population)):
        fitnessResults[i] = RouteFitness(population[i]).tourDistance()

        totalFitness += fitnessResults[i]
    for i in range(0, len(fitnessResults)):
        tourProb = (fitnessResults[i] / totalFitness)
        if (i == 0):
            normalisedFitness[i] = tourProb
        else:
            normalisedFitness[i] = normalisedFitness[i - 1] + tourProb
    return normalisedFitness


def startPopulation(cityList, popSize):
    popl = []
    for i in range(0, popSize):
        popl.append(random.sample(cityList, len(cityList)))  # appends a random route
    return popl


def reproduce(parent1, parent2, mutationRate):
    offspring1 = []
    offspring2 = []
    rndmPoint = random.randint(1, len(parent1))  # This is the partial mapping approach

    cycles = [-1] * len(parent1)
    cycle_no = 1
    cyclestart = (i for i, v in enumerate(cycles) if v < 0)
    # Cycle cross over operator: https://www.hindawi.com/journals/cin/2017/7430125/
    for pos in cyclestart:

        while cycles[pos] < 0:
            cycles[pos] = cycle_no
            pos = parent1.index(parent2[pos])

        cycle_no += 1

    offspring1 = [parent1[i] if n % 2 else parent2[i] for i, n in enumerate(cycles)]
    offspring2 = [parent2[i] if n % 2 else parent1[i] for i, n in enumerate(cycles)]

    seen = {}
    duplicate = []  # holds indices of values repeated in offspring1
    ind = 0
    for city in offspring1:
        if city not in seen:
            seen[city] = 1
            ind += 1
        else:
            duplicate.append(ind)
            ind += 1
    seen = {}
    ind = 0
    duplicateInd = 0
    for city in offspring2:
        if city not in seen:
            seen[city] = 1
            ind += 1
        else:
            toSwap = offspring2[ind]
            offspring2[ind] = offspring1[duplicate[duplicateInd]]
            offspring1[duplicate[duplicateInd]] = toSwap
            ind += 1
            duplicateInd += 1

    length1 = RouteFitness(offspring1).tourDistance()
    length2 = RouteFitness(offspring2).tourDistance()
    if length1 > length2:
        newChild = offspring2
    else:
        newChild = offspring1
    aRand = random.random()
    if aRand <= mutationRate:
        randInd1 = random.randrange(len(newChild))
        randInd2 = random.randrange(len(newChild))
        while (randInd2 == randInd1):
            randInd2 = random.randrange(len(newChild))
        swapVal = newChild[randInd1]
        newChild[randInd1] = newChild[randInd2]
        newChild[randInd2] = swapVal
    return newChild


def geneticAlgorithm(cityList, popSize, mutationRate, generations):
    pop = startPopulation(cityList, popSize)  # Makes initial array of orders

    bestLength = float("inf")
    for i in range(0, generations):

        if i % 2 == 0:
            fitnessArr = fitness(pop)  # Finds fitness of all the orders and returns dictionary
            newPop = []
            for i in range(0, popSize):
                parent1 = pop[chooseParents(fitnessArr)]  # Chooses fit parents
                parent2 = pop[chooseParents(fitnessArr)]  # Chooses fit parents
                child = reproduce(parent1, parent2, mutationRate)  # Mates them
                childLength = RouteFitness(child).tourDistance()
                if childLength < bestLength:
                    bestLength = childLength
                    bestTour = child
                newPop.append(child)
        if i % 2 == 1:
            fitnessArr = fitness(newPop)
            pop = []
            for i in range(0, popSize):
                parent1 = newPop[chooseParents(fitnessArr)]
                parent2 = newPop[chooseParents(fitnessArr)]
                child = reproduce(parent1, parent2, mutationRate)
                childLength = RouteFitness(child).tourDistance()
                if childLength < bestLength:
                    bestLength = childLength
                    bestTour = child
                pop.append(child)
    return bestTour, bestLength


cityList = list(range(len(distance_matrix[0])))
start = timeit.default_timer()
tour, tour_length = geneticAlgorithm(cityList, 10, 0.01, 600000);
stop = timeit.default_timer()
print('Time: ', stop - start)
print(tour_length)

#######################################################################################################
############ the code for your algorithm should now be complete and you should have        ############
############ computed a tour held in the list "tour" of length "tour_length"               ############
#######################################################################################################

# you do not need to worry about the code below that is, do not touch it

#######################################################################################################
############ start of code to verify that the constructed tour and its length are valid    ############
#######################################################################################################

check_tour_length = 0
for i in range(0, num_cities - 1):
    check_tour_length = check_tour_length + distance_matrix[tour[i]][tour[i + 1]]
check_tour_length = check_tour_length + distance_matrix[tour[num_cities - 1]][tour[0]]
flag = "good"
if tour_length != check_tour_length:
    flag = "bad"
if flag == "good":
    print("Great! Your tour-length of " + str(tour_length) + " from your " + codes_and_names[alg_code] + " is valid!")
else:
    print("***** ERROR: Your claimed tour-length of " + str(
        tour_length) + "is different from the true tour length of " + str(check_tour_length) + ".")

#######################################################################################################
############ start of code to write a valid tour to a text (.txt) file of the correct      ############
############ format if your tour is not valid then you get an error message on the        ############
############ standard output and the tour is not written to a file                         ############
############                                                                               ############
############ the name of file is "my_user_name" + mon-dat-hr-min-sec (11 characters)      ############
############ for example, dcs0iasSep22105857.txt if dcs0iasSep22105857.txt already exists ############
############ then it is overwritten                                                        ############
#######################################################################################################

if flag == "good":
    local_time = time.asctime(
        time.localtime(time.time()))  # return 24-character string in form "Tue Jan 13 10:17:09 2009"
    output_file_time = local_time[4:7] + local_time[8:10] + local_time[11:13] + local_time[14:16] + local_time[17:19]
    # output_file_time = mon + day + hour + min + sec (11 characters)
    output_file_name = my_user_name + output_file_time + ".txt"
    f = open(output_file_name, 'w')
    f.write("USER = " + my_user_name + " (" + my_first_name + " " + my_last_name + ")\n")
    f.write("ALGORITHM = " + alg_code + ", FILENAME = " + name_of_file + "\n")
    f.write("NUMBER OF CITIES = " + str(num_cities) + ", TOUR LENGTH = " + str(tour_length) + "\n")
    f.write(str(tour[0]))
    for i in range(1, num_cities):
        f.write("," + str(tour[i]))
    if added_note != "":
        f.write("\nNOTE = " + added_note)
    f.close()
    print("I have successfully written the tour to the output file " + output_file_name + ".")

