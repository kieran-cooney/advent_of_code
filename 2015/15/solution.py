"""
Maths time!

So rather than checking through all 4.6 million combinations of weights,
we can instead recognise that this problem is a convex optimisation problem.
This guarantees that gradient ascent will find the optimal solution.

To see that the problem is convex:
1. The set of all ingredient weights resulting in a positive score is a
convex set, as it set of solutions to all of a collection of linear
inequalities. (Draw a bunch of straight lines, and staying inside of all
of them gives a convex set).
2. For the non-zero values, the score is a product of positive linear
functions, and hence is convex.

To find the solution via gradient ascent, we start with a random guess, and 
then pick the nearest neighbour solution with the highest score, and repeat
until we cannot improve on the solution anymore.
"""

import re
import sys
import numpy as np
from itertools import permutations

INPUT_PATTERN = re.compile(
    r"^([A-Z][a-z]*): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)$"
)

def parse_input(filepath):
    """
    Return a list of ingredients and a numpy array of the property
    of each ingredient.
    """
    ingredients = list()
    data = list()

    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        ingredient, *line_data, _ = INPUT_PATTERN.match(line).groups()
        ingredients.append(ingredient)
        data.append(line_data)
    
    # Transpose so rows index properties and columns index ingredients
    array = np.array(data).T.astype('int')

    return ingredients, array


def get_random_amounts(properties, total=100):
    """
    Get a random amount of ingredients, being careful to try and sample
    uniformly and ensure that the sum equates to 100
    """
    a = np.random.rand(properties.shape[1])

    a = (total/a.sum())*a
    a = a.astype('int')

    surplus = a.sum() - total
    a[0] = a[0] - surplus

    return a


def get_score(amounts, properties):
    """
    Return a scalar score given the array of ingredient properties and
    a vector of ingredient amounts
    """
    score = np.product(properties.dot(amounts).clip(min=0))
    return score


def get_initial_amounts(properties, total=100):
    """
    Return an initial vector of ingredient amounts to kick off the
    gradient ascent. Also return initial score.
    """
    score = 0

    while score <= 0:
        amounts = get_random_amounts(properties)
        score = get_score(amounts, properties)
    
    return amounts, score


def get_delta_amounts_array(properties):
    """
    Return an array of 0's, 1's and -1's. Each row corresponds to a direction
    we can perturb our ingredient amounts by.

    In order to ensure that our total amount of ingredients is constant, we
    need to change the amounts of two ingredients, by +1 and -1 respectively.

    This results in N*(N-1) possible ways to increment the ingredient amounts,
    where N = len(properties) is the number of ingredients.
    """
    indices = range(len(properties))
    index_pairs = list(permutations(indices, 2))

    delta_array = np.zeros((len(index_pairs), len(properties)), dtype='int')

    for i, (d1, d2) in enumerate(index_pairs):
        delta_array[i, d1] = 1
        delta_array[i, d2] = -1

    return delta_array


def increment(amounts, score, properties, deltas, verbose=False):
    """
    From a given vector of ingredient amounts, find the best we could do by
    taking one unit from one ingredient and adding one unit to another.

    Return this new vector of ingredient amounts and the new score.
    """
    # Use numpy broadcasting to get array of all possible amount vectors to
    # check
    possible_amounts = amounts + deltas

    # Array of possible scores after all possible updates
    possible_scores = np.product(
        properties.dot(possible_amounts.T).clip(min=0),
        axis=0
    )

    # Find max score and index, and use to update amounts and score
    max_score_index = np.argmax(possible_scores)
    max_score = np.max(possible_scores)

    if max_score > score:
        new_amounts = possible_amounts[max_score_index]
        new_score = max_score
    else:
        new_amounts = amounts
        new_score = score
    
    if verbose:
        print('Amounts: {}'.format(new_amounts))
        print('Score: {}'.format(new_score))

    return new_amounts, new_score


def find_best_recipe(properties, total=100):
    """
    Find the best vector of ingredient amounts, such that the total amount
    of ingredients is total=100. The 'best' is given by the higest score.
    """
    old_amounts, old_score = get_initial_amounts(properties, total=100)

    delta_amounts = get_delta_amounts_array(properties)

    new_amounts, new_score = increment(
        old_amounts, old_score, properties, delta_amounts
    )

    # Increment until the new_score is not better than the old score.
    # This would usually give us a local optimum, but because the problem
    # is global we know the solution is a global optimum.
    while new_score > old_score:
        old_score = new_score
        old_amounts = new_amounts
        new_amounts, new_score = increment(
            old_amounts, old_score, properties, delta_amounts
        )
    
    return new_amounts, new_score


def main(filepath):
    ingredients, properties = parse_input(filepath)
    recipe, score = find_best_recipe(properties)

    print('Best recipe:')
    for ingredient, amount in zip(ingredients, recipe):
        print("{} -> {} teaspoons".format(ingredient, amount))
    print('Best score: {}'.format(score))


if __name__=='__main__': 
    if len(sys.argv) > 1: 
        filepath = sys.argv[1] 
    else: 
        filepath = "input.txt" 
    main(filepath) 