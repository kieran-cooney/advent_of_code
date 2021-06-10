"""
Maths time!

So rather than checking through all 176,851 combinations of weights,
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

We repeat this strategy for part 2:
1. Find the optimal solution regardless of calories
2. Optimise the first solution with respect to how far from the calories
target the recipe is. So the new solution will have the target calories.
3. Optimise the second solution with respect to the score again, but this time
only allowing changes in solution which keep the total teaspoons and calories
fixed.

This ended up being a long and complicated solution, so I can't recommend it.
But hey, it's fast!
"""
import re
import sys
import numpy as np
from itertools import permutations
from functools import reduce
from math import gcd

TEASPOON_TOTAL = 100
CALORIE_TOTAL = 500

INPUT_PATTERN = re.compile(
    r"^([A-Z][a-z]*): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)$"
)

def parse_input(filepath):
    """
    Return a list of ingredients, a numpy array of the property
    of each ingredient, and an array of the calories of each ingredient.
    """
    ingredients = list()
    data = list()
    calories = list()

    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        ingredient, *line_data, kcal = INPUT_PATTERN.match(line).groups()
        ingredients.append(ingredient)
        data.append(line_data)
        calories.append(kcal)
    
    # Transpose so rows index properties and columns index ingredients
    array = np.array(data).T.astype('int')
    calories_array = np.array(calories).astype('int')

    return ingredients, array, calories_array


def get_random_amounts(properties, total=TEASPOON_TOTAL):
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


def get_calories(amounts, calories):
    """
    Return the total calories of a recipe given the recipe amounts and the
    calories of each ingredient.
    """
    result = np.sum(amounts*calories)
    return result


def get_initial_amounts(properties, total=TEASPOON_TOTAL, verbose=True):
    """
    Return an initial vector of ingredient amounts to kick off the
    gradient ascent. Also return initial score.
    """
    score = 0
    num_guesses = 0
    
    if verbose:
        print("Finding initial random recipe")
    
    while score <= 0:
        amounts = get_random_amounts(properties)
        score = get_score(amounts, properties)
        
        num_guesses += 1
        
        if verbose:
            print("\tGuess {} -> {}".format(num_guesses, amounts))
    
    print(
        "Random recipe {} found after {} guesses with score {}.\n"
        .format(amounts, num_guesses, score)
    )
    
    return amounts, score


def get_delta_amounts_array(num_ingredients):
    """
    Return an array of 0's, 1's and -1's. Each row corresponds to a direction
    we can perturb our ingredient amounts by.

    In order to ensure that our total amount of ingredients is constant, we
    need to change the amounts of two ingredients, by +1 and -1 respectively.

    This results in N*(N-1) possible ways to increment the ingredient amounts,
    where N = len(properties) is the number of ingredients.
    """
    indices = range(num_ingredients)
    index_pairs = list(permutations(indices, 2))

    delta_array = np.zeros((len(index_pairs), num_ingredients), dtype='int')

    for i, (d1, d2) in enumerate(index_pairs):
        delta_array[i, d1] = 1
        delta_array[i, d2] = -1

    return delta_array


def get_delta_amounts_array_fixed_calories(ingredient_calories):
    """
    Similar to get_delta_amounts_array, but now the perturbations in the
    recipe amounts will change the amounts such that
    * The total amount is fixed
    * The total calories are fixed.
    
    This solution won't generalise to more constraints or more ingredients,
    so that's not great. A general solution might use sympy's nullspace, or
    some other linear diophantine equation solver.
    
    The solution here is based on the following example:
    https://brilliant.org/wiki/system-of-linear-diophantine-equations/
    """
    w1, w2, w3, w4 = ingredient_calories
    
    def multi_gcd(a):
        """Get the gcd of more than 2 numbers"""
        return reduce(gcd, a)

    # A term that came out in my workings.
    g = multi_gcd([w2 - w1, w3 - w1, w4 - w1])
    
    # The two vectors in this array correspond to two perturbations
    # we can make. You can check by hand they work!
    X = np.array([
        [w3 - w2, w1 - w3, w2 - w1, 0],
        [w4 - w2, w1 - w4, 0, w2 -w1]
    ])

    # Scale by g, that's how the maths goes.
    X = np.floor_divide(X, g)
    
    # An array summarising the combinations of the vectors of X we will
    # take.
    Y = np.array([
        [1, 0],
        [-1, 0],
        [0, 1],
        [0, -1],
        [1, -1],
        [-1, 1],
    ])

    # Matrix product to get an array of all possible combinations of the
    # vectors in X
    delta_array = np.dot(X.T, Y.T).T

    # Finally scale by the gcd across each vector. This ensures we're taking
    # the smallest possible perturbation in each case.
    gcd_array = np.array([multi_gcd(a) for a in delta_array])[..., np.newaxis]
    
    delta_array = np.floor_divide(delta_array, gcd_array)

    return delta_array


def increment(amounts, score, properties, deltas, verbose=True):
    """
    From a given vector of ingredient amounts, find the best score we could
    get by repeatedly changing amounts by one of the vectors in deltas.

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
        print('\tAmounts: {}'.format(new_amounts))
        print('\tScore: {}'.format(new_score))

    return new_amounts, new_score


def increment_calories(amounts, ingredient_calories, deltas, verbose=True):
    """
    From a given vector of ingredient amounts, find the best we could do by
    taking one unit from one ingredient and adding one unit to another.

    Return this new vector of ingredient amounts and the new score.
    """
    # Use numpy broadcasting to get array of all possible amount vectors to
    # check
    possible_amounts = amounts + deltas

    # Array of possible scores after all possible updates
    possible_calories =ingredient_calories.dot(possible_amounts.T)

    calories_errors = np.square(possible_calories - CALORIE_TOTAL)
    # Find max score and index, and use to update amounts and score
    best_index = np.argmin(calories_errors)
    new_calories = possible_calories[best_index]
    
    new_amounts = possible_amounts[best_index]

    if verbose:
        print('\tAmounts: {}'.format(new_amounts))
        print('\tCalories: {}'.format(new_calories))

    return new_amounts, new_calories


def find_best_recipe(recipe, properties, calories=None,
                     total=TEASPOON_TOTAL, verbose=True):
    """
    Find the best vector of ingredient amounts, such that the total amount
    of ingredients is total=100. The 'best' is given by the higest score.
    """
    old_amounts = recipe
    old_score = get_score(old_amounts, properties)

    if calories is not None:
        delta_amounts = get_delta_amounts_array_fixed_calories(calories)
    else:
        delta_amounts = get_delta_amounts_array(len(recipe))

    calories_message = 'any' if calories is None else "fixed"

    if verbose:
        print("Finding best recipe for {} calories.".format(calories_message))

    new_amounts, new_score = increment(
        old_amounts, old_score, properties, delta_amounts, verbose
    )

    # Increment until the new_score is not better than the old score.
    # This would usually give us a local optimum, but because the problem
    # is global we know the solution is a global optimum.
    while new_score > old_score:
        old_score = new_score
        old_amounts = new_amounts
        new_amounts, new_score = increment(
            old_amounts, old_score, properties, delta_amounts, verbose
        )
    
    return new_amounts, new_score


def adjust_recipe_for_calories(amounts, ingredient_calories,
                                   target=CALORIE_TOTAL, verbose=True):
    """
    Adjust a recipe so that it has the target amount of calories
    """
    delta_amounts = get_delta_amounts_array(len(amounts))
    
    current_calories = get_calories(amounts, ingredient_calories)

    if verbose:
        print("Adjusting recipe for fixed calories")

    while current_calories != target:
        amounts, current_calories = increment_calories(
            amounts,
            ingredient_calories,
            delta_amounts
        )
    
    if verbose:
        print("\n")

    return amounts


def main(filepath, verbose=True):
    ingredients, ingredient_properties, calories = parse_input(filepath)
    
    guess_recipe, guess_score = get_initial_amounts(
        ingredient_properties, verbose=verbose
    )
    first_recipe, first_score = find_best_recipe(
        guess_recipe, ingredient_properties, verbose=verbose
    )
    
    print('\nBest recipe at any calories:')
    for ingredient, amount in zip(ingredients, first_recipe):
        print("{} -> {} teaspoons".format(ingredient, amount))
    print('Best score: {}\n'.format(first_score))

    second_recipe = adjust_recipe_for_calories(first_recipe, calories, verbose=verbose)
    final_recipe, final_score = find_best_recipe(
        second_recipe, ingredient_properties, calories, verbose=verbose
    )
    
    print('\nBest recipe at 500 calories:')
    for ingredient, amount in zip(ingredients, final_recipe):
        print("{} -> {} teaspoons".format(ingredient, amount))
    print('Best score: {}\n'.format(final_score))


if __name__=='__main__': 
    if len(sys.argv) > 1: 
        filepath = sys.argv[1] 
    else: 
        filepath = "input.txt" 
    main(filepath) 