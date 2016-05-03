#!/usr/bin/env python

"""This script uses the Trello configuration in trello.json and uses that to
put cards that are due today as todoist tasks.
"""

import os
import json
import argparse
import datetime

from trello import TrelloClient


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    'trello_board_name',
    help='name of the Trello Board that we are parsing'
)
parser.add_argument(
    'trello_username',
    help='username of the person whose cards we want to populate'
)
args = parser.parse_args()

# get credentials and instantiate the client
this_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(this_dir, 'trello.json')
with open(filename, 'r') as stream:
    credentials = json.load(stream)
client = TrelloClient(**credentials)

# find the appropriate board
board = None
for _board in client.list_boards():
    if _board.name == args.trello_board_name:
        board = _board
        break
if board is None:
    raise ValueError('board "%(trello_board_name)s" not found' % vars(args))

# find the appropriate member
member = None
for _member in board.get_members():
    if _member.username == args.trello_username:
        member = _member
        break
if member is None:
    raise ValueError('member "%(trello_username)s" not found' % vars(args))


def is_due_today(card, today=None):
    today = today or datetime.date.today()
    return card.due_date and card.due_date.date() == today

# find all of the cards on this board that are owned by this user and are due
# today
cards_due_today = []
for card in board.all_cards():
    if member.id in card.member_ids and is_due_today(card):
        cards_due_today.append(card)

# post these cards to the todoist api


import ipdb; ipdb.set_trace()