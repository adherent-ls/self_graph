def func(*a):
    print(a)
    return a


def main():
    from src.base_graph.graph.name_graph import SeriesWithNameGraph
    modules = SeriesWithNameGraph(
        funcs=[
            (func, ['a', ['b', 'c']], ['d', ['e', 'f']]),
        ],
        ini=['a', 'b', 'c'],
        oui=['d', ['e', 'f']]
    )
    d, ef = modules(1, 2, 3)
    e, f = ef
    print(d, e, f)


if __name__ == '__main__':
    main()
