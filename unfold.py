"""Unfold a PGN file"""

import argparse
from typing import List
from chess import pgn
from chess.pgn import Game, GameNode

parser = argparse.ArgumentParser()
parser.add_argument('source', type=argparse.FileType('r'),
                    help="Source PGN file")
parser.add_argument('target', type=argparse.FileType('w'),
                    help="Target PGN file")
args = parser.parse_args()


def recurse_game(node: GameNode) -> List[Game]:
    """Recurse over game"""
    games = []
    if len(node.variations) > 0:
        for _, v in enumerate(node.variations):
            games.extend(recurse_game(v))
    else:
        temp_game = pgn.Game()
        temp_game.headers = game.headers
        node_stack = []
        temp_node = node
        while temp_node.parent:
            node_stack.append(temp_node)
            temp_node = temp_node.parent
        node_stack.reverse()
        node = temp_game
        for move_node in node_stack:
            node = node.add_variation(
                move_node.move, comment=move_node.comment, nags=move_node.nags,
                starting_comment=move_node.starting_comment)

        games.append(temp_game)
    return games


# pgn_file = open("testdata/test.pgn")
game = pgn.read_game(args.source)
game_list = recurse_game(game)

for g in game_list:
    print(g, file=args.target)
    print("", file=args.target)
