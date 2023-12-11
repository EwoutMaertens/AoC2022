from typing import List, Tuple
import sys
from enum import Enum
import re
import numpy



# HELPER CLASSES AND FUNCTIONS


class Direction(Enum):
    """Helper class to store direction and the value (used for score and direction vector)"""
    E = 0
    S = 1
    W = 2
    N = 3

# Direction vectors used when travelling in a certain direction, to manipulate row or column
DIRECTION_VECTORS = [[0, 1], [1, 0], [0, -1], [-1, 0]]

 # GRID_SIZE is hardcoded for now, can be automatically calculated in the future
GRID_SIZE = 50


class Matrix2D(List[List[str]]):
    """Type hinting class for a 2D matrix"""
    pass


class Coordinates(Tuple[int, int]):
    """Type hinting class for a set of coordinates (row, column)"""
    pass


class Vector(Tuple[int, int]):
    """Type hinting class for a vector"""
    pass


class EdgeSide(Tuple[Coordinates, Coordinates, Direction, Vector]):
    """Type hinting class for an edge side stored in VERTEXS_MAP"""
    pass


def print_2d_matrix(matrix: Matrix2D) -> None:
    """Prints out a 2D matrix cleanly"""
    for row in range(len(matrix)):
        for column in range(len(matrix[row])):
            print(matrix[row][column], end='')
        print()



# MONKEY MAP - GENERAL (for both part 1 and 2)


def get_starting_coordinates(board_map: Matrix2D) -> Coordinates:
    """Finds the starting coordinates on the board and returns them in Tuple form (row, column)"""
    for x in range(len(board_map[0])):
        if board_map[0][x] == '.':
            return (0, x)


def check_action_is_rotate(action: str) -> bool:
    """Checks if the performed action is 'R' or 'L', which stands for rotate"""
    return action == 'R' or action == 'L'


def rotate(action: str, direction: Direction) -> Direction:
    """
    Rotates the current direction once according to action.
    Rotate left is direction - 1, rotate right is direction + 1.

    Returns the new direction.

    Example:
    If current direction is 0 and you rotate left, it would become -1. With a mod 4 (all directions)
    we can make sure direction stays within bounds, as this would result in 3.
    """
    if action == 'R':
        return Direction( (direction.value + 1) % 4 )
    elif action == 'L':
        return Direction( (direction.value - 1) % 4 )
    raise RuntimeError(f"Unknown action {action}, something went wrong.")


def process_input_file(input_file: str) -> Tuple[Matrix2D, str]:
    """
    Processes the input file line by line.
    Each line will be inserted in a board_map array. Since a string is also an array of strings (Python),
    we can see board_map as a 2D matrix. Added extra code to make sure the grid for the board_map is consistent
    for all columns.

    The final line, split from the board with an empty line, are the actions to follow in a string.

    Returns a tuple of the board_map and the actions_to_follow.
    """
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

        actions_to_follow = f.readline().strip()

    if max_line_size is None:
        raise RuntimeError("You provided an empty file...")

    # I realized when running input.txt, I would be getting an index error because not all rows are equal in size.
    # The trailing ' ' characters are omitted and not added to the line it read in.
    # This would make it so that when shifting rows and having to jump from one side of the board to another,
    # we could run into a board_map[new_row][column] where that column value caused an index error.
    # Adding trailing ' ' characters fixes this issue.
    # This was not picked up by my tests, as there I never had any missing trailing ' ' characters.
    for row in range(len(board_map)):
        line = board_map[row]
        while len(line) < max_line_size:
            line += ' '
        board_map[row] = line
        

    print_2d_matrix(board_map)
    print(actions_to_follow)
    return (board_map, actions_to_follow)



# MONKEY MAP - PART ONE


def move_part1(board_map: Matrix2D, move_amount: int, direction: Direction, row: int, column: int) -> Coordinates:
    """
    Movement function for part 1.

    Traverses the board map according to the given move_amount and direction.
    The starting location is (row, column).

    If a '#' symbol is encountered, it will stop at the point right before this obstacle.
    If a ' ' symbol is encountered, it will wrap around the board and continue from there.
    If a '.' symbol is encountered, it will continue as normal from this point.

    Returns the new coordinates of the point after the move (row, column).
    """
    delta_row, delta_column = DIRECTION_VECTORS[direction.value]

    for _ in range(move_amount):
        next_element = board_map[(row + delta_row) % len(board_map)][ (column + delta_column) % len(board_map[row]) ]

        if next_element == '#':
            break

        if next_element == '.':
            row = (row + delta_row) % len(board_map)
            column = (column + delta_column) % len(board_map[row])
            continue

        # We encountered an empty space, will have to continue moving until we find either '#' or '.'
        new_row = row
        new_column = column
        while next_element == ' ':
            new_row = (new_row + delta_row) % len(board_map)
            new_column = (new_column + delta_column) % len(board_map[row])
            next_element = board_map[new_row][new_column]

        if next_element == '#':
            break
        else:
            row = new_row
            column = new_column

    return row, column


def traverse_board_map(board_map: Matrix2D, path_to_follow: str) -> int:
    """
    Main function for part 1.

    Arranges initial values (starting_point, direction and actions)
    Then traverses through the map by either:
    - rotating
    - moving

    Returns the custom scoring value for AoC2022 day 22.
    """
    row, column = get_starting_coordinates(board_map)
    direction = Direction.E
    action_list = re.findall(r'\d+|\w', path_to_follow)

    for action in action_list:
        if check_action_is_rotate(action):
            direction = rotate(action, direction)
        else:
            row, column = move_part1(board_map, int(action), direction, row, column)

    return 1000 * (row + 1) + 4 * (column + 1) + direction.value



# MONKEY MAP - PART TWO


# Had to draw this out, please check 'cube_drawing_with_vertex_map.pdf'
# This is hardcoded for my solution only, automatically generating this would be incredibly complex
# This is a mapping for:
# - on the left side the source edge with its vertices, and the movement vector along this edge
# - on the right the destination edge with vertices, and the movement vector along this edge
VERTEX_MAP = [
    [[(2, 1), (1, 1), Direction.W, (-1, 0)], [(2, 1), (2, 0), Direction.N, (0, -1)]], # edge A
    [[(2, 2), (1, 2), Direction.E, (-1, 0)], [(1, 3), (1, 2), Direction.S, (0, -1)]], # edge B
    [[(2, 0), (3, 0), Direction.W, (1,  0)], [(1, 1), (0, 1), Direction.W, (-1, 0)]], # edge C
    [[(0, 1), (0, 2), Direction.N, (0,  1)], [(3, 0), (4, 0), Direction.W, (1,  0)]], # edge D
    [[(0, 2), (0, 3), Direction.N, (0,  1)], [(4, 0), (4, 1), Direction.S, (0,  1)]], # edge E
    [[(1, 3), (0, 3), Direction.E, (-1, 0)], [(2, 2), (3, 2), Direction.E, (1,  0)]], # edge F
    [[(3, 1), (3, 2), Direction.S, (0,  1)], [(3, 1), (4, 1), Direction.E, (1,  0)]]  # edge G
]

# TODO: do not alter a global constant, instead make this into a function
# Leaving quick and dirty for now
for edge in range(len(VERTEX_MAP)):
    for edge_side in range(2):
        for vertex in range(2):
            VERTEX_MAP[edge][edge_side][vertex] = numpy.multiply(VERTEX_MAP[edge][edge_side][vertex], GRID_SIZE)


def reverse_direction(direction: Direction) -> Direction:
    """Reverses the direction, by turning 180 degrees."""
    return Direction( (direction.value + 2) % 4 )


def calculate_point_on_other_edge_side(edge_side: EdgeSide, point_index: int) -> Coordinates:
    """
    This function already knows the index of the point on the source edge.
    Now we need to calculate the index of the point on the destination edge.

    Returns the coordinates for the newly acquired point on the destination edge.

    Example:
    Previous point was (0, 61) with an index of 11.
    Let's say the destination edge runs from (100, 50) to (150, 50).
    The edge movement vector for this destination edge is (1, 0). (1 = delta_along_row, 0 = delta_along_column)
    This means our new point will be (111, 50), because the movement vector only changes the row.
    """
    vertex_start, vertex_end, edge_direction, edge_movement_vector = edge_side
    delta_along_row, delta_along_column = edge_movement_vector[0], edge_movement_vector[1]

    new_point = numpy.add(vertex_start, numpy.multiply((delta_along_row, delta_along_column), point_index))
    return new_point[0], new_point[1]


def calculate_index_on_edge_for_point(original_point_coordinates: Coordinates, edge_side: EdgeSide, direction: Direction) -> int:
    """
    Function that calculates the index position of our current point on the edge,
    in case we are about to walk off it.

    Returns the index, if a wrap would happen, otherwise returns -1.

    Example:
    Let's say the edge runs from (0, 50) to (0, 100).
    The current direction is North and the edge direction is also North.
    If the point would be (0, 61), this point would lie on this edge with and index of 11 (50 + 11 = 61).

    # TODO: This function feels a bit multi-functional by only calculating index if direction matches
    # We should probably split this up into a more modular function
    """
    vertex_start, vertex_end, edge_direction, edge_movement_vector = edge_side

    # Potential to walk off the map!
    if edge_direction == direction:

        delta_along_row, delta_along_column = edge_movement_vector[0], edge_movement_vector[1]
        vertex_start_row, vertex_start_column = vertex_start[0], vertex_start[1]

        for i in range(GRID_SIZE):
            if (vertex_start_row + ( i * delta_along_row ), vertex_start_column + ( i * delta_along_column)) == original_point_coordinates:
                return i

    return -1


def calculate_index_for_wrap(row: int, column: int, direction: Direction) -> Tuple[int, EdgeSide]:
    """
    This functions determines if a wrap around an edge is needed.
    All edges with both their sides are checked, as it is possible that the point resides on any of them.

    If the point_index returned from calculate_index_on_edge_for_point is different than -1,
    we know 100% sure that we are about to move off the current edge.

    Returns -1 if no wrap is needed, otherwise returns the index position of the current point.
    Also returns the destination edge side, as it is possible we are moving from edge side 2 to side 1.

    # TODO: This function feels a bit multi-functional by calculating index or returning -1 if there is no wrap needed
    # We should probably split this up into calculate_index and check_wrap_needed or something along these lines
    """
    point_index = -1

    for edge_side_1, edge_side_2 in VERTEX_MAP:
        point_index = calculate_index_on_edge_for_point((row, column), edge_side_1, direction)
        if point_index != -1:
            break

        point_index = calculate_index_on_edge_for_point((row, column), edge_side_2, direction)
        if point_index != -1:
            # edge_side_2 is the source, edge_side_1 is the destination. Reverse them.
            edge_side_1, edge_side_2 = edge_side_2, edge_side_1
            break

    destination_edge_side = edge_side_2
    return point_index, destination_edge_side
    

def move_part2(board_map: Matrix2D, move_amount: int, direction: Direction, row: int, column: int) -> Coordinates:
    """
    Movement function for part 2.

    Traverses the board map according to the given move_amount and direction.
    The starting location is (row, column).

    It will first calculate if a wrap to a different edge is needed:
    - if no, simply continue with the next point on the same edge with the same direction
    - if yes, calculate the new point on the different edge and use that point with the updated direction

    If a '#' symbol is encountered, it will stop at the point right before this obstacle.
    If a ' ' symbol is encountered, it will wrap around the board and continue from there.
    If a '.' symbol is encountered, it will continue as normal from this point.

    Returns the new coordinates and new direction of the point after the move (row, column, direction).
    """
    delta_row, delta_column = DIRECTION_VECTORS[direction.value]
    
    print(f"{row}, {column}")
    for _ in range(move_amount):
        current_point_index, dest_edge_side = calculate_index_for_wrap(row + delta_row, column + delta_column, direction)

        # No wrap around needed, simple movement
        if current_point_index == -1:
            new_row, new_column = row + delta_row, column + delta_column
            new_direction = direction
            next_element = board_map[new_row][new_column]

        # Wrap is needed, with an index based off the vertex start to the point
        else:
            new_row, new_column = calculate_point_on_other_edge_side(dest_edge_side, current_point_index)
            next_element = board_map[new_row + delta_row][new_column + delta_column]
            # Direction of the destination edge side is pointing OUT, we need it to point IN
            new_direction = reverse_direction(dest_edge_side[2])

        if next_element == '#':
            break
        if next_element == '.':
            row = new_row
            column = new_column
            direction = new_direction
            continue

    return row, column, direction


def print_cube_schedule_from_board_map(board_map: Matrix2D) -> None:
    """
    Prints out a simple overview for the cube, useful for calculating the vertex map.
    Using this simple matrix to draw out the cube edges + vertices

    Example output:
    011
    010
    110
    100
    """
    simple_grid = []
    for row in range(0, len(board_map), GRID_SIZE):
        simple_grid_line = []
        for column in range(0, len(board_map[row]), GRID_SIZE):
            if board_map[row][column] != ' ':
                simple_grid_line.append(1)
            else:
                simple_grid_line.append(0)
        simple_grid.append(simple_grid_line)

    print_2d_matrix(simple_grid)


def traverse_cube(board_map: Matrix2D, path_to_follow: str) -> int:
    """
    Main function for part 2.

    Prints out a sample of the cube edges.

    Arranges initial values (starting_point, direction and actions)
    Then traverses through the cube by either:
    - rotating
    - moving

    Returns the custom scoring value for AoC2022 day 22.
    """
    print_cube_schedule_from_board_map(board_map)

    row, column = get_starting_coordinates(board_map)
    direction = Direction.E
    action_list = re.findall(r'\d+|\w', path_to_follow)

    for action in action_list:
        if check_action_is_rotate(action):
            direction = rotate(action, direction)
        else:
            row, column, direction = move_part2(board_map, int(action), direction, row, column)

    return 1000 * (row + 1) + 4 * (column + 1) + direction.value



# MAIN

def main(input_file: str) -> None:
    board_map, path_to_follow = process_input_file(input_file)

    score = traverse_board_map(board_map, path_to_follow)
    print(f"Part 1 - Answer: \t{score}")

    score = traverse_cube(board_map, path_to_follow)
    print(f"Part 2 - Answer: \t{score}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Please provide the input file as the only argument.")
        sys.exit(1)

    main(sys.argv[1])
