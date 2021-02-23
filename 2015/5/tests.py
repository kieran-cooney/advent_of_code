import re
from solution import good_string, REGEX_PATTERNS

compiled_regexes = [[re.compile(s) for s in l ] for l in REGEX_PATTERNS]

test_cases = [
    [
        ('ugknbfddgicrmopn', True),
        ('aaa', True),
        ('jchzalrnumimnmhp', False),
        ('haegwjzuvuyypxyu', False),
        ('dvszwmarrgswjxmb', False)
    ],
    [
        ('qjhvhtzxzqqjkmpb', True),
        ('xxyxx', True),
        ('uurcxstgmygtbstg', False),
        ('ieodomkazucvgmuy', False),
    ]
]

def test(cases, regexes, part):
    num_correct = 0

    for test, answer in cases:
        print("Expected answer for {}: {}".format(test, answer))
        result = good_string(test, regexes, True)

        if result == answer:
            print("Right answer!")
            num_correct += 1
        else:
            print("Wrong answer!")
        
        print("")

    print(
        'Number of cases right for part {}: {}/{}'
        .format(part, num_correct, len(cases))
    )

for i, (c, r) in enumerate(zip(test_cases, compiled_regexes), start=1):
    test(c, r, i)