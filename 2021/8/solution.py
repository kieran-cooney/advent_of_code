def parse_input(filepath):
    with open(filepath, 'r') as f:
        splits = (l.strip().split(' | ') for l in f)
        out = [
            (a.split(' '), b.split(' '))
            for a, b in splits
        ]

    return out


def get_ans1(inputs):
    valid_nums = [2, 3, 4, 7]
    return sum(len(s) in valid_nums for _, l in inputs for s in l)


def sort_string(s):
    return ''.join(sorted(s))


def decode_inputs(inputs):
    decoder = ['']*10

    def update_decoder(index, string_list):
        assert len(string_list) == 1
        decoder[index] = string_list[0]

    count_map = {2: 1, 3: 7, 4: 4, 7: 8}
    for k, v in count_map.items():
        valid_strings = [s for s in inputs if len(s) == k]
        update_decoder(v, valid_strings)

    zero_six_or_nine = [s for s in inputs if len(s) == 6]
    assert len(zero_six_or_nine) == 3
    
    nines = [s for s in zero_six_or_nine if all(c in s for c in decoder[4])]
    update_decoder(9, nines)

    zeros = [
        s for s in zero_six_or_nine
        if (s!= decoder[9]) and all(c in s for c in decoder[7])
    ]
    update_decoder(0, zeros)

    six = [
        s for s in zero_six_or_nine
        if (s != decoder[0]) and (s != decoder[9])
    ]
    update_decoder(6, six)

    rest = [s for s in inputs if s not in decoder]
    assert len(rest) == 3

    three = [s for s in rest if all(c in s for c in decoder[1])]
    update_decoder(3, three)

    five = [s for s in rest if all(c in decoder[6] for c in s)]
    update_decoder(5, five)

    two = [s for s in rest if (s!= decoder[3]) and (s!= decoder[5])]
    update_decoder(2, two)
    
    assert '' not in decoder
    
    decoder = [sort_string(s) for s in decoder]
    return decoder


def apply_digit_decoder(decoder, input_string):
    input_string = sort_string(input_string)
    for i, s in enumerate(decoder):
        if s == input_string:
            return i
    return None


def apply_decoder(decoder, input_strings):
    out = sum(
        apply_digit_decoder(decoder, s)*(10**i)
        for i, s in enumerate(reversed(input_strings))
    )
    return out

def decode_and_sum(input_pairs):
    out = 0
    for signal, output in input_pairs:
        decoder = decode_inputs(signal)
        num = apply_decoder(decoder, output)
        out += num

    return out


def main(filepath):
    inputs = parse_input(filepath)
    ans1 = get_ans1(inputs)
    print('Answer for part 1: {}'.format(ans1))
    
    ans2 = decode_and_sum(inputs)
    print('Answer for part 2: {}'.format(ans2))

if __name__=='__main__':
    main('input.txt')