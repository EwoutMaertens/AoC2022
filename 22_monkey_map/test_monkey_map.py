from monkey_map import move, Direction

# unit tests for the move function, as it is quite a complex beast -> splitting it up might be a good idea

def test_move_east_obstacle():
    # Arrange
    board_map = [['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']]
    obstacle_index = 6
    board_map[0][obstacle_index] = '#'
    move_amount = 20
    direction = Direction.E
    start_row = 0
    start_column = 0

    # Act
    final_row, final_column = move(board_map, move_amount, direction, start_row, start_column)

    # Assert
    assert final_row == start_row
    assert final_column == obstacle_index - 1
    assert board_map[final_row][final_column] == '.'
    assert board_map[final_row][final_column + 1] == '#'


def test_move_east_incomplete():
    # Arrange
    board_map = [[' ', ' ', '.', '.', '.', '.', '.', '.', '.', '.', ' ', ' ']]
    move_amount = 10
    direction = Direction.E
    start_row = 0
    start_column = 2

    # Act
    final_row, final_column = move(board_map, move_amount, direction, start_row, start_column)

    # Assert
    assert final_row == start_row
    assert final_column == 4 # hardcoded for speed reasons
    assert board_map[final_row][final_column] == '.'


def test_move_east_incomplete_obstacle():
    # Arrange
    board_map = [[' ', ' ', '#', '.', '.', '.', '.', '.', '.', '.', ' ', ' ']]
    move_amount = 10
    direction = Direction.E
    start_row = 0
    start_column = 3

    # Act
    final_row, final_column = move(board_map, move_amount, direction, start_row, start_column)

    # Assert
    assert final_row == start_row
    assert final_column == 9 # hardcoded for speed reasons
    assert board_map[final_row][final_column] == '.'


def test_move_east_free():
    # Arrange
    board_map = [['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']]
    move_amount = 189
    direction = Direction.E
    start_row = 0
    start_column = 0

    # Act
    final_row, final_column = move(board_map, move_amount, direction, start_row, start_column)

    # Assert
    assert final_row == start_row
    assert final_column == move_amount % len(board_map[0])
    assert board_map[final_row][final_column] == '.'


def test_move_west_obstacle():
    # Arrange
    board_map = [['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']]
    obstacle_index = 6
    board_map[0][obstacle_index] = '#'
    move_amount = 20
    direction = Direction.W
    start_row = 0
    start_column = 0

    # Act
    final_row, final_column = move(board_map, move_amount, direction, start_row, start_column)

    # Assert
    assert final_row == start_row
    assert final_column == obstacle_index + 1
    assert board_map[final_row][final_column] == '.'
    assert board_map[final_row][final_column - 1] == '#'


def test_move_west_incomplete():
    # Arrange
    board_map = [[' ', ' ', '.', '.', '.', '.', '.', '.', '.', '.', ' ', ' ']]
    move_amount = 10
    direction = Direction.W
    start_row = 0
    start_column = 2

    # Act
    final_row, final_column = move(board_map, move_amount, direction, start_row, start_column)

    # Assert
    assert final_row == start_row
    assert final_column == 8 # hardcoded for speed reasons
    assert board_map[final_row][final_column] == '.'


def test_move_west_incomplete_obstacle():
    # Arrange
    board_map = [[' ', ' ', '.', '.', '.', '.', '.', '.', '.', '#', ' ', ' ']]
    move_amount = 10
    direction = Direction.W
    start_row = 0
    start_column = 2

    # Act
    final_row, final_column = move(board_map, move_amount, direction, start_row, start_column)

    # Assert
    assert final_row == start_row
    assert final_column == start_column
    assert board_map[final_row][final_column] == '.'


def test_move_west_free():
    # Arrange
    board_map = [['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']]
    move_amount = 189
    direction = Direction.W
    start_row = 0
    start_column = 0

    # Act
    final_row, final_column = move(board_map, move_amount, direction, start_row, start_column)

    # Assert
    assert final_row == start_row
    assert final_column == (-1 * move_amount) % len(board_map[0])
    assert board_map[final_row][final_column] == '.'


def test_move_north_obstacle():
    # Arrange
    board_map = [['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.']]
    obstacle_index = 6
    board_map[obstacle_index][0] = '#'
    move_amount = 20
    direction = Direction.N
    start_row = 0
    start_column = 0

    # Act
    final_row, final_column = move(board_map, move_amount, direction, start_row, start_column)

    # Assert
    assert final_row == obstacle_index + 1
    assert final_column == start_column
    assert board_map[final_row][final_column] == '.'
    assert board_map[final_row - 1][final_column] == '#'


def test_move_north_incomplete():
    # Arrange
    board_map = [[' '], [' '], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], [' '], [' ']]
    move_amount = 10
    direction = Direction.N
    start_row = 2
    start_column = 0

    # Act
    final_row, final_column = move(board_map, move_amount, direction, start_row, start_column)

    # Assert
    assert final_row == 8 # hardcoded for speed reasons
    assert final_column == start_column
    assert board_map[final_row][final_column] == '.'


def test_move_north_incomplete_obstacle():
    # Arrange
    board_map = [[' '], [' '], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['#'], [' '], [' ']]
    move_amount = 10
    direction = Direction.N
    start_row = 2
    start_column = 0

    # Act
    final_row, final_column = move(board_map, move_amount, direction, start_row, start_column)

    # Assert
    assert final_row == start_row
    assert final_column == start_column
    assert board_map[final_row][final_column] == '.'


def test_move_north_free():
    # Arrange
    board_map = [['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.']]
    move_amount = 20
    direction = Direction.N
    start_row = 0
    start_column = 0

    # Act
    final_row, final_column = move(board_map, move_amount, direction, start_row, start_column)

    # Assert
    assert final_row == (-1 * move_amount) % len(board_map)
    assert final_column == start_column
    assert board_map[final_row][final_column] == '.'


def test_move_south_obstacle():
    # Arrange
    board_map = [['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.']]
    obstacle_index = 6
    board_map[obstacle_index][0] = '#'
    move_amount = 20
    direction = Direction.S
    start_row = 0
    start_column = 0

    # Act
    final_row, final_column = move(board_map, move_amount, direction, start_row, start_column)

    # Assert
    assert final_row == obstacle_index - 1
    assert final_column == start_column
    assert board_map[final_row][final_column] == '.'
    assert board_map[final_row + 1][final_column] == '#'


def test_move_south_incomplete():
    # Arrange
    board_map = [[' '], [' '], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], [' '], [' ']]
    move_amount = 10
    direction = Direction.S
    start_row = 2
    start_column = 0

    # Act
    final_row, final_column = move(board_map, move_amount, direction, start_row, start_column)

    # Assert
    assert final_row == 4 # hardcoded for speed reasons
    assert final_column == start_column
    assert board_map[final_row][final_column] == '.'


def test_move_south_incomplete_obstacle():
    # Arrange
    board_map = [[' '], [' '], ['#'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], [' '], [' ']]
    move_amount = 10
    direction = Direction.S
    start_row = 3
    start_column = 0

    # Act
    final_row, final_column = move(board_map, move_amount, direction, start_row, start_column)

    # Assert
    assert final_row == 9 # hardcoded for speed reasons
    assert final_column == start_column
    assert board_map[final_row][final_column] == '.'


def test_move_south_free():
    # Arrange
    board_map = [['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.'], ['.']]
    move_amount = 20
    direction = Direction.S
    start_row = 0
    start_column = 0

    # Act
    final_row, final_column = move(board_map, move_amount, direction, start_row, start_column)

    # Assert
    assert final_row == move_amount % len(board_map)
    assert final_column == start_column
    assert board_map[final_row][final_column] == '.'
