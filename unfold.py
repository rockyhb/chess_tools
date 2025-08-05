from chess import pgn, Move
from chess.pgn import Game, GameNode, ChildNode, Headers
from typing import List
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('source', type=argparse.FileType('r'),
                    help="Source PGN file")
parser.add_argument('target', type=argparse.FileType('w'),
                    help="Target PGN file")
args = parser.parse_args()


def recurse_game(node: GameNode) -> List[Game]:

    games = []
    if len(node.variations) > 0:
        for i, v in enumerate(node.variations):
            games.extend(recurse_game(v))
    else:
        g = pgn.Game()
        g.headers = game.headers
        node_stack = []
        temp_node = node
        while temp_node.parent:
            node_stack.append(temp_node)
            temp_node = temp_node.parent
        node_stack.reverse()
        node = g
        for move_node in node_stack:
            node = node.add_variation(
                move_node.move, comment=move_node.comment, nags=move_node.nags, starting_comment=move_node.starting_comment)

        games.append(g)
    return games


# pgn_file = open("testdata/test.pgn")
game = pgn.read_game(args.source)
games = recurse_game(game)

for g in games:
    print(g, file=args.target)
    print("", file=args.target)
