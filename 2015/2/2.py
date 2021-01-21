triple = tuple[int, int, int]

def parse_dimensions_string(s: str) -> triple:
    s = s.strip()
    dim_strings = s.split("x")
    dims = tuple(sorted(int(dim_string) for dim_string in dim_strings))
    return dims

def wrapping_paper(dim_triple: triple) -> int:
    x,y,z = dim_triple
    return (3*x*y) + (2*y*z) + (2*z*x)


def ribbon(dim_triple: triple) -> int:
    x,y,z = dim_triple

    wrap_length = 2*(x+y)
    tie_length = x*y*z
    
    return wrap_length + tie_length


def read_input(filepath: str = "input.txt") -> list[triple]:
    with open(filepath) as file:
        dimension_strings = file.readlines()

    dimension_triples = [
        parse_dimensions_string(line) for line in dimension_strings
    ]

    return dimension_triples


def main():
    dim_triples = read_input()

    required_paper = sum(wrapping_paper(i) for i in dim_triples)
    required_ribbon = sum(ribbon(i) for i in dim_triples)

    print(rf"Total area of wrapping paper required: {required_paper}")
    print(rf"Total length of ribbon required: {required_ribbon}")


if __name__=='__main__':
    main()
