from copy import deepcopy
from typing import Callable, List, Any, Tuple
from time import perf_counter
import sys
from enum import Enum
import re

# GENERAL

class Direction(Enum):
    E = 0
    S = 1
    W = 2
    N = 3


def print_2d_matrix(matrix: List[List[str]]):
    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            print(matrix[row][column], end='')
        print()


def process_input_file(input_file: str) -> Tuple[List[List[str]], str]:
    board_map = []

    max_line_size = None
    with open(input_file, 'r') as f:
        line = f.readline().strip('\n')
        max_line_size = len(line)
        while line:
            board_map.append(line)
            line = f.readline().strip('\n')
            if len(line) > max_line_size:
                max_line_size = len(line)

        path_to_follow = f.readline().strip()

    if max_line_size is None:
        raise RuntimeError("You provided an empty file...")

    # I realized when running input.txt, I would be getting an index error because not all rows are equal in size
    # The trailing ' ' characters are omitted and not added to the line read in
    # This would make it so that when shifting rows and having to jump from one side of the board to another
    # we could run into a board_map[new_row][column] where that column value caused an index error
    # Adding trailing ' ' characters will fix this issue.
    # This was not picked up by my tests, as there I never had any missing trailing ' ' characters
    for row in range(len(board_map)):
        line = board_map[row]
        while len(line) < max_line_size:
            line += ' '
        board_map[row] = line
        

    print_2d_matrix(board_map)
    print(path_to_follow)
    return (board_map, path_to_follow)


def get_starting_coordinates(board_map: List[List[str]]):
    for x in range(len(board_map[0])):
        if board_map[0][x] == '.':
            return (0, x)

def check_action_is_rotate(action: str) -> bool:
    return action == 'R' or action == 'L'

def rotate(action: str, direction: Direction) -> Direction:
    if action == 'R':
        return Direction( (direction.value + 1) % 4 )
    elif action == 'L':
        return Direction( (direction.value - 1) % 4 )
    raise RuntimeError(f"Unknown action {action}, something went wrong.")

def move(board_map, move_amount: int, direction: Direction, row: int, column: int):
    # TODO: clean this up
    if direction == direction.E:
        for i in range(move_amount):
            next_element = board_map[row][ (column + 1) % len(board_map[row]) ]
            if next_element == '#':
                break
            if next_element == '.':
                column = (column + 1) % len(board_map[row])
                continue
            new_column = column
            while next_element == ' ':
                new_column = (new_column + 1) % len(board_map[row])
                next_element = board_map[row][new_column]
            if next_element == '#':
                break
            else:
                column = new_column
        return row, column

    elif direction == direction.S:
        for i in range(move_amount):
            next_element = board_map[ (row + 1) % len(board_map) ][column]
            if next_element == '#':
                break
            if next_element == '.':
                row = (row + 1) % len(board_map) 
                continue
            new_row = row
            while next_element == ' ':
                new_row = (new_row + 1) % len(board_map)
                next_element = board_map[new_row][column]
            if next_element == '#':
                break
            else:
                row = new_row
        return row, column

    elif direction == direction.W:
        for i in range(move_amount):
            next_element = board_map[row][ (column - 1) % len(board_map[row]) ]
            if next_element == '#':
                break
            if next_element == '.':
                column = (column - 1) % len(board_map[row])
                continue
            new_column = column
            while next_element == ' ':
                new_column = (new_column - 1) % len(board_map[row])
                next_element = board_map[row][new_column]
            if next_element == '#':
                break
            else:
                column = new_column
        return row, column

    elif direction == direction.N:
        for i in range(move_amount):
            next_element = board_map[ (row - 1) % len(board_map) ][column]
            if next_element == '#':
                break
            if next_element == '.':
                row = (row - 1) % len(board_map) 
                continue
            new_row = row
            while next_element == ' ':
                new_row = (new_row - 1) % len(board_map)
                next_element = board_map[new_row][column]
            if next_element == '#':
                break
            else:
                row = new_row
        return row, column


# PART ONE

def traverse_board_map(board_map: List[List[str]], path_to_follow: str) -> Any:
    row, column = get_starting_coordinates(board_map)
    direction = Direction.E
    print(f"({row}, {column} - {direction})")
    action_list = re.findall(r'\d+|\w', path_to_follow)
    # path_map = deepcopy(board_map)
    # for row in range(len(path_map)):
    #     path_map[row] = path_map[row].split()

    for action in action_list:
        print(action)
        if check_action_is_rotate(action):
            direction = rotate(action, direction)
        else:
            row, column = move(board_map, int(action), direction, row, column)
        print(f"({row}, {column} - {direction})")

    return 1000 * (row + 1) + 4 * (column + 1) + direction.value

# PART TWO

def process_input_line_p2(line: str) -> Any:
    pass

def process_result_list_p2(result_list: List[Any]) -> Any:
    pass

# MAIN

def main(input_file: str):
    board_map, path_to_follow = process_input_file(input_file)
    res = traverse_board_map(board_map, path_to_follow)

    print(f"Part 1 - Sample answer: \t{res}")


if __name__ == '__main__':
    main(sys.argv[1])
# time_start = perf_counter()
# result = process_result_list_p1(process_input_file('input.txt'))
# time_stop = perf_counter()
# print(f"Part 1 - Answer:        \t{result}\t - took {time_stop-time_start} seconds")
# print("----------------------------------------------\n")

# print(f"Part 2 - Sample answer: \t{process_result_list_p2(process_input_file('sample.txt', process_input_line_p2))}")

# time_start = perf_counter()
# result = process_result_list_p2(process_input_file('input.txt', process_input_line_p2))
# time_stop = perf_counter()
# print(f"Part 2 - Answer:        \t{result}\t - took {time_stop-time_start} seconds")
# print("----------------------------------------------\n")
