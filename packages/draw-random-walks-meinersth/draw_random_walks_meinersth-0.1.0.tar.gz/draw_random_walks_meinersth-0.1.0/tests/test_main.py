from draw_random_walks_meinersth.main import parse_args, RANDOM_WALKERS


def test_parser():
    parser = parse_args(['--walkers', '3'])
    assert parser.walkers == 3


def test_draw():
    assert RANDOM_WALKERS == 2
