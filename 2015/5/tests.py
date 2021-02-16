from solution import good_string

test_cases = [
    ('ugknbfddgicrmopn', True),
    ('aaa', True),
    ('jchzalrnumimnmhp', False),
    ('haegwjzuvuyypxyu', False),
    ('dvszwmarrgswjxmb', False)
]

num_correct = 0

for test, answer in test_cases:
    print("Expected answer for {}: {}".format(test, answer))
    result = good_string(test, True)

    if result == answer:
        print("Right answer!")
        num_correct += 1
    else:
        print("Wrong answer!")
    
    print("")

print('Number of cases right: {}/{}'.format(num_correct, len(test_cases)))