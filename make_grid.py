import math

# Word list from: http://bryanhelmig.com/python-crossword-puzzle-generator/
word_list = ['saffron', 'pumpernickel', 'leaven', 'coda', 'paladin', 'syncopation', 'albatross', 'harp', 'piston', 'caramel', 'coral', 'dawn', 'pitch', 'fjord', 'lip', 'lime', 'mist', 'plague', 'yarn', 'snicker']
grid_height = 15
grid_width = 21

longest_word_len = len(max(word_list, key=len))
assert min(grid_width, grid_height) >= longest_word_len, "both board dimensions should exceed the longest word length"


grid = dict(letters = [[0 for x in range(grid_width)] for y in range(grid_height)],
            filled  = [[False for x in range(grid_width)] for y in range(grid_height)])


word_list.sort(key=len, reverse=True)

def check_word_index_conformability(word_to_place, start_ind, end_ind):
    assert 2 == len(start_ind) and 2 == len(end_ind), "indices should be 2 element lists"

    vert_dim = end_ind[1] - start_ind[1]
    horz_dim = end_ind[0] - start_ind[0]

    assert 0 <= vert_dim and 0 <= horz_dim, "need for end_ind >= start_ind"

    is_horz = 0 == horz_dim
    is_vert = 0 == vert_dim
    assert is_horz or is_vert, "one of the dimensions should match"

    word_size = vert_dim + horz_dim
    assert len(word_to_place) == word_size, "location to place should match dimensions of word to be placed"

def enumerate_indices_between(start_ind, end_ind):
    vert_dim = end_ind[1] - start_ind[1]
    horz_dim = end_ind[0] - start_ind[0]

    word_size = vert_dim + horz_dim

    indices_between = [None] * word_size

    for idx in range(word_size):
        w = idx / word_size
        r = round(start_ind[0] * (1 - w) + end_ind[0] * w) # round may be a bit fragile, better to do this with int sequences
        c = round(start_ind[1] * (1 - w) + end_ind[1] * w)
        indices_between[idx] = [r, c]
    return indices_between

def place_word(word_to_place, start_ind, end_ind, grid):
    check_word_index_conformability(word_to_place, start_ind, end_ind)
    letters = grid["letters"]
    filled = grid["filled"]
    indices_between = enumerate_indices_between(start_ind, end_ind)
    for counter, ind in enumerate(indices_between):
        idx1 = ind[0]
        idx2 = ind[1]
        if not filled[idx1][idx2]:
            letters[idx1][idx2] = word_to_place[counter]
            filled[idx1][idx2] = True
        else:
            assert letters[idx1][idx2] == word_to_place[counter], "should not be overriding an already placed letter"
    out = dict(letters=letters, filled=filled)
    return out

def print_grid(grid):
    letters = grid["letters"]
    filled  = grid["filled"]

    d1 = len(letters)
    d2 = len(letters[0])

    assert len(filled) == d1, "first dimension mismatch"
    assert len(filled[0]) == d2, "second dimension mismatch"

    for dim1 in range(d1):
        for dim2 in range(d2):
            if filled[dim1][dim2]:
                print(letters[dim1][dim2], end="")
            else:
                print('.', end="")
        print('\n')


row = int(grid_height/2)
# roughly in the middle of the grid
left_margin = int((grid_width - longest_word_len)/2)-1


word_to_place = word_list[0]
start_ind = [row, left_margin]
end_ind = [row, left_margin + longest_word_len]

grid = place_word(word_to_place, start_ind, end_ind, grid)
grid = place_word('test', [6, 13], [10, 13], grid)

print_grid(grid)

# 1. Create a grid of whatever size and a list of words.
# 2. Shuffle the word list, and then sort the words by longest to shortest.
# 3. Place the first and longest word at the upper left most position, 1,1 (vertical or horizontal).
# 4. Move onto next word, loop over each letter in the word and each cell in the grid looking for letter to letter matches.
# 5. When a match is found, simply add that position to a suggested coordinate list for that word.
# 6. Loop over the suggested coordinate list and "score" the word placement based on how many other words it crosses.
#    Scores of 0 indicate either bad placement (adjacent to existing words) or that there were no word crosses.
# 7. Back to step #4 until word list is exhausted. Optional second pass.
# 8. We should now have a crossword, but the quality can be hit or miss due to some of the random placements. So, we
#    buffer this crossword and go back to step #2. If the next crossword has more words placed on the board, it replaces
#    the crossword in the buffer. This is time limited (find the best crossword in x seconds).
