# Mahad Ahmed 20i-0426 Section F

# Genetic Algorithm---
# 1 - Generate Initial Population
# 2 - Fitness Evaluation of the candidates
# 3 - Selection of Best Candidates
# 4 - Reproduction from those new Candidates (Crossover / Mutation)
# 5 - Replacement of the least fit members in the population
# 6 - Termination based on some criteria


# N number of courses e.g. C1,C2,C3...CN
# K number of exam halls e.g. H1,H2,...HN used for max 6 hours
# 3 Time slots available - T1 , T2, T3 - x hours

# each solution in the format [(c1,t1,h1),(c2,t2,h2),(c3,t3,h2)]
# in code the tuple will be like [(1,1,1),(2,2,2),(3,3,2)]

import random
import copy

MAX_GENERATIONS = 100
POPULATION_SIZE = 20
MAX_HOURS = 6
population = []
cnum = 0
hnum = 0
tnum = 0


def initialise_population(n, k):
    global cnum, hnum, tnum
    cnum = n
    hnum = k
    tnum = random.randint(1, 3)
    print(f"The hours for 1 time slot is {tnum}")
    # Generate n random initial populations
    for i in range(POPULATION_SIZE):
        entity = []
        for j in range(1, cnum + 1):
            randomHall = random.randint(1, k)
            randomSlot = random.randint(1, 3)
            exam = tuple((j, randomSlot, randomHall))
            entity.append(exam)
        population.append(entity)


def display_population():
    for entity in population:
        new_entity = [(f"C{t[0]}", f"T{t[1]}", f"H{t[2]}") for t in entity]
        print(new_entity)


def get_common_students(x, y):
    condition_map = {(1, 2): 10, (1, 4): 5, (2, 5): 7, (3, 4): 12, (4, 5): 8}
    output = condition_map.get((x, y))
    if output is None:
        return 0
    return output


def perform_crossover(x, y):
    schedule1 = copy.deepcopy(x)
    schedule2 = copy.deepcopy(y)
    course1, course2 = random.sample(range(1, cnum), 2)
    print(f"Crossover on Courses {course1} , {course2}")
    schedule1[course1 - 1] = (course1, y[course2 - 1][1], y[course2 - 1][2])
    schedule2[course2 - 1] = (course2, x[course1 - 1][1], x[course1 - 1][2])
    schedule1[course2 - 1] = (course2, y[course1 - 1][1], y[course1 - 1][2])
    schedule2[course1 - 1] = (course1, x[course2 - 1][1], x[course2 - 1][2])
    return schedule1, schedule2


def perform_mutation(x):
    new_schedule = copy.deepcopy(x)
    course1, course2 = random.sample(range(1, cnum), 2)
    print(f"mutation on Courses {course1} , {course2} of {x}")
    slot1 = random.randint(1, 3)
    slot2 = random.randint(1, 3)
    hall1 = random.randint(1, hnum)
    hall2 = random.randint(1, hnum)
    new_schedule[course1 - 1] = (course1, slot1, hall1)
    new_schedule[course2 - 1] = (course2, slot2, hall2)
    return new_schedule


def calculate_fitness(solution):
    score = 0
    # Calculate penalty for clash in timings
    for index, exam in enumerate(solution):
        (course, slot, hall) = exam
        # print(f"Comparing {course} with: ")
        for j, exam2 in enumerate(solution[index + 1:], index + 1):
            # print(exam2)
            (course2, slot2, hall2) = exam2
            # if there is a clash in time between two exams
            if slot == slot2:
                # if there is a clash in time and the hall
                if hall == hall2:
                    score = score + 5000
                # print(f"Clash between {course} and {course2}")
                score = score + (100 * get_common_students(course, course2))
        # print()
        # Calculate Penalty for exceeding hours
    hours_exceeded = [0 for m in range(hnum)]
    for index, exam in enumerate(solution):
        (course, slot, hall) = exam
        hours_exceeded[hall - 1] = hours_exceeded[hall - 1] + tnum
        if hours_exceeded[hall - 1] > MAX_HOURS:
            # print(f"Hall {hall}: hours used: {hours_exceeded[hall - 1]}")
            score = score + (10 * (hours_exceeded[hall - 1] - MAX_HOURS))
            hours_exceeded[hall - 1] = 6

    # print(f"Score is: {score}")
    return score


def scheduling_algorithm():
    global population
    for generation in range(MAX_GENERATIONS):
        # Evaluate the fitness scores of each individual
        fitness_scores = []
        for solution in population:
            fitness_scores.append(calculate_fitness(solution))
        print(f"Generation {generation} : {fitness_scores}")
        # Select the Parents for the next generation
        parents = []
        for i in range(5):
            index = fitness_scores.index(min(fitness_scores))
            parents.append(population[index])
            del population[index]
            del fitness_scores[index]
        # perform crossover and mutation to obtain new children
        children = []
        for i in range(POPULATION_SIZE - 5):
            parent1, parent2 = random.sample(parents, 2)
            if random.random() < 0.8:
                child1, child2 = perform_crossover(parent1, parent2)
                children.append(child1)
                children.append(child2)
            elif random.random() < 0.1:
                parent3 = random.choice(parents)
                child3 = perform_mutation(parent3)
                children.append(child3)
        population = parents + children
    # Find the best Solution
    final_fitness = []
    for solution in population:
        final_fitness.append(calculate_fitness(solution))
    index = final_fitness.index(min(final_fitness))
    best_fitness = final_fitness[index]
    best_solution = population[index]
    print(f"The Best Solution Found with fitness score {best_fitness} is: ")
    print(best_solution)


initialise_population(5, 2)
display_population()
print('\n')
scheduling_algorithm()
