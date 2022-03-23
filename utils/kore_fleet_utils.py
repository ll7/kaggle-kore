# Copyright 2022 Kaggle Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# copied from https://github.com/Kaggle/kaggle-environments/blob/master/kaggle_environments/envs/kore_fleets/kore_fleets.py
# modified by Lennart Luttkus

import copy
import json
import math
import numpy as np
from os import path
from random import choice, randint, randrange, sample, seed, random
# from .helpers import board_agent, Board, ShipyardAction #https://github.com/Kaggle/kaggle-environments/blob/master/kaggle_environments/envs/kore_fleets/helpers.py
from kaggle_environments import utils
from kaggle_environments.helpers import Point, Direction


def get_col_row(size, pos):
    return pos % size, pos // size


def get_to_pos(size, pos, direction):
    col, row = get_col_row(size, pos)
    if direction == "NORTH":
        return pos - size if pos >= size else size ** 2 - size + col
    elif direction == "SOUTH":
        return col if pos + size >= size ** 2 else pos + size
    elif direction == "EAST":
        return pos + 1 if col < size - 1 else row * size
    elif direction == "WEST":
        return pos - 1 if col > 0 else (row + 1) * size - 1

def check_path(board, start, dirs, dist_a, dist_b, collection_rate):
    kore = 0
    npv = .98
    current = start
    steps = 2 * (dist_a + dist_b + 2)
    for idx, d in enumerate(dirs):
        for _ in range((dist_a if idx % 2 == 0 else dist_b) + 1):
            current = current.translate(d.to_point(), board.configuration.size)
            kore += int((board.cells.get(current).kore or 0) * collection_rate)
    return math.pow(npv, steps) * kore / (2 * (dist_a + dist_b + 2))

def check_location(board, loc, me):
    if board.cells.get(loc).shipyard and board.cells.get(loc).shipyard.player.id == me.id:
        return 0
    kore = 0
    for i in range(-3, 4):
        for j in range(-3, 4):
            pos = loc.translate(Point(i, j), board.configuration.size)
            kore += board.cells.get(pos).kore or 0
    return kore

def get_closest_enemy_shipyard(board, position, me):
    min_dist = 1000000
    enemy_shipyard = None
    for shipyard in board.shipyards.values():
        if shipyard.player_id == me.id:
            continue
        dist = position.distance_to(shipyard.position, board.configuration.size)
        if dist < min_dist:
            min_dist = dist
            enemy_shipyard = shipyard
    return enemy_shipyard
    
def get_shortest_flight_path_between(position_a, position_b, size, trailing_digits=False):
    mag_x = 1 if position_b.x > position_a.x else -1
    abs_x = abs(position_b.x - position_a.x)
    dir_x = mag_x if abs_x < size/2 else -mag_x
    mag_y = 1 if position_b.y > position_a.y else -1
    abs_y = abs(position_b.y - position_a.y)
    dir_y = mag_y if abs_y < size/2 else -mag_y
    flight_path_x = ""
    if abs_x > 0:
        flight_path_x += "E" if dir_x == 1 else "W"
        flight_path_x += str(abs_x - 1) if (abs_x - 1) > 0 else ""
    flight_path_y = ""
    if abs_y > 0:
        flight_path_y += "N" if dir_y == 1 else "S"
        flight_path_y += str(abs_y - 1) if (abs_y - 1) > 0 else ""
    if not len(flight_path_x) == len(flight_path_y):
        if len(flight_path_x) < len(flight_path_y):
            return flight_path_x + (flight_path_y if trailing_digits else flight_path_y[0])
        else:
            return flight_path_y + (flight_path_x if trailing_digits else flight_path_x[0])
    return flight_path_y + (flight_path_x if trailing_digits or not flight_path_x else flight_path_x[0]) if random() < .5 else flight_path_x + (flight_path_y if trailing_digits or not flight_path_y else flight_path_y[0])
