import os
from functools import partial

here = os.path.abspath(os.path.dirname(__file__))
get_path = partial(os.path.join, here)


with open(get_path('members.txt'), mode='r', encoding='utf-8') as f:
    members = [line.strip() for line in f.readlines()]
