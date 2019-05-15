import random
from math import radians, cos, sin, sqrt

from numpy import size
from numpy.core._multiarray_umath import sign

random.seed(5)


def fitness_function(x, y):
    result = (4 - 2.1 * x ** 2 + (x ** 4) / 3) * x ** 2 + x * y
    result += (-4 + 4 * y ** 2) * y ** 2
    return result


# the number of iterations
t = 100

# the maximum size of the population
n = 10
bears = []


for i in range(n):
    pos = [random.uniform(-3, 3), random.uniform(-2, 2)]
    bears.append(pos)
i = 0
while i <= t:
    for cur in range(n):
        # Find all the angle values φ at random
        fi0 = radians(random.uniform(0, 90))
        fi1 = radians(random.uniform(0, 360))

        # Calculate the radius r using (3) and the new position (xt)new by (4) using the sign
        # of plus
        alpha = random.uniform(0, 0.3)
        r = 4 * alpha * cos(fi0) * sin(fi0)
        new = [bears[cur][0] + r * cos(fi1), bears[cur][1] + r * cos(fi1)]

        if fitness_function(new[0], new[1]) < fitness_function(bears[cur][0], bears[cur][1]):
            bears[cur] = new
        else:
            # Calculate new position of the bear (xt)new by using the sign of minus in Equation (4)
            fi2 = radians(random.uniform(0, 360))
            new = [new[0] - (r * cos(fi1) + r * cos(fi2)), new[1] - (r * cos(fi1) + r * cos(fi2))]

            if fitness_function(new[0], new[1]) < fitness_function(bears[cur][0], bears[cur][1]):
                bears[cur] = new

    # Randomly select one of the top 10% of bears
    fitness = []
    for bear in bears:
        fitness.append(fitness_function(bear[0], bear[1]))
    sort = sorted(fitness)
    xi, xj = bears[fitness.index(sort[1])], bears[fitness.index(sort[0])]

    # Calculate the new􏰂position in􏰃 accordance with (1)
    dist = sqrt(((xi[0] - xj[0]) ** 2) + ((xi[1] - xj[1]) ** 2))
    alpha = random.uniform(0, 1)
    gama = random.uniform(0, dist)
    x_new = [xj[0] + sign(dist) * alpha + gama, xj[1] + sign(dist) * alpha + gama]

    if fitness_function(x_new[0], x_new[1]) < fitness_function(xj[0], xj[1]):
        bears[fitness.index(sort[0])] = x_new

    # Sort population according to the fitness function
    bears_temp = []
    counter = 0
    while counter < size(fitness):
        bears_temp.append(bears[fitness.index(sort[counter])])
        counter += 1
    bears = bears_temp

    # Choose value κ ∈ ⟨0, 1⟩
    k = random.uniform(0, 1)
    if i < t - 1 and k > 0.75:
        # Choose two of the top 10% of polar bears in the population and add a
        # reproduced one using (6)
        reproduced = [(bears[0][0] + bears[1][0]) / 2, (bears[0][1] + bears[1][1]) / 2]
        bears.append(reproduced)
        n += 1
    elif size(bears) > 0.5 * n and k < 0.25:
        # Remove the worst individual in the population
        bears.pop()
        n -= 1

    i += 1

    print(fitness_function(bears[0][0], bears[0][1]))

