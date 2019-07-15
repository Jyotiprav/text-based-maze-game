import random


def load_map(filename):
    with open(filename) as f:
        lst = []
        for line in f:
            lst.append(list(line.rstrip().split()))
        return lst


def generate_map(map_data, p_x, p_y, player_id):

    map_visual = [x[:] for x in map_data]
    map_coors = {}

    for i in range(0, len(map_data)):
        for j in range(0, len(map_data[i])):
            map_coors[(i, j)] = int(map_data[i][j])

    for i in range(0, len(map_visual)):
        for j in range(0, len(map_visual[i])):
            if j == p_y and i == p_x:
                map_visual[i][j] = '('+player_id+')'
            elif map_visual[i][j] == '-2':
                map_visual[i][j] = '(X)'
            else:
                map_visual[i][j] = '(_)'

    return (map_visual, map_coors)


def load_items(filename):
    '''
    (str) -> dict

    Read data from the file with the given filename and
    create and return a dictionary with item data, structured
    as described in the assignment handout, Part 1 Section III.

    IMPORTANT: Make sure to use the given variable <filename>
    within this code. DO NOT replace filename with a specific
    .txt string. You MUST use the variable filename, or else
    all our test cases will fail, and you will receive a 0.
    '''

    # YOUR CODE HERE #
    with open(filename) as j:
        dct = {}
        for line in j:
            line = line.strip().split(',')
            dct[line[0]] = line[1:]
        for i in dct:
            #print(dct[i][1])
            dct[i][1]=float(dct[i][1])
            dct[i][2] = float(dct[i][2])
            #ine[2]=int(line[1])
        return dct


def load_locations(filename):
    '''
    (str) -> dict

    Read data from the file with the given filename and create
    and return a dictionary with location data, structured as
    described in the assignment handout, Part 1 Section III.

    IMPORTANT: Make sure to use the given variable <filename>
    within this code. DO NOT replace filename with a specific
    .txt string. You MUST use the variable filename, or else
    all our test cases will fail, and you will receive a 0.
    '''

    # YOUR CODE HERE #
    with open(filename) as j:
        listOfLines = list()
        for line in j:
            listOfLines.append(line.strip())

    dict = {}
    k = 0
    for i in range(0, len(listOfLines) - 1):
        if (listOfLines[i] == '[BEGIN DESCRIPTION]') and (listOfLines[i - 1].isdigit() or listOfLines[i - 1].replace('.', '').isdigit() or listOfLines[i-1].replace('-','').isdigit()):
            dict[float(listOfLines[i - 1])] = [listOfLines[i + 1], []]
            k = float(listOfLines[i - 1])
            # print(k)
        elif listOfLines[i] == '[BEGIN ACTIONS]':
            i = i + 1
            while listOfLines[i] != '[END ACTIONS]':
                dict[k][1].append(listOfLines[i])
                i = i + 1
    for i in dict:
        if len(dict[i][1]) == 0:
            continue
        else:
            for j in range(len(dict[i][1])):
                dict[i][1][j] = (dict[i][1][j].split(','))
                dict[i][1][j][1] = float(dict[i][1][j][1])
                dict[i][1][j] = tuple(dict[i][1][j])
    return dict



def get_indices(lst, elm):
    '''
    (list of lists, object) -> tuple of two ints

    Given a list of lists and an element, find the first
    pair of indices at which that element is found and return
    this as a tuple of two ints. The first int would be the
    index of the sublist where the element occurs, and the
    second int would be the index within this sublist where
    it occurs.

    >>> get_indices([[1, 3, 4], [5, 6, 7]], 1)
    (0, 0)

    >>> get_indices([[1, 3, 4], [5, 6, 7]], 7)
    (1, 2)
    '''

    '''for i, pair_1 in enumerate(lst):
        for j, pair_2 in enumerate(pair_1):
            if pair_2 == elm:
                return (i, j)'''

    for i in range(0,len(lst)):
        for j in range(0,len(lst[i])):
            if lst[i][j]==elm:
                return (i,j)




def update_map(map_visual, map_coors, player_id, px, py, dx, dy):
    '''
    (list of lists, dict, str, int, int, int, int) -> None or tuple of two ints

    This function is very similar to update_grid from
    the lab, but there are few IMPORTANT differences.
    Read the description below carefully!

    Given the player's current position as px and py,
    and the directional changes in dx
    and dy, update map_visual to change the player's
    x-coordinate by dx, and their y-coordinate by dy.
    The player's position should be represented as (*)
    where * is their given player id.

    Notes:
    This time, we don't have a w and h representing the grid,
    as the map's width and height may vary depending on the
    file that we read. So, you should figure out the width
    and height using the len function and the given map_visual.

    If the move is NOT valid (not within the map's area) OR
    it would involve moving to a coordinate in which the
    location ID is -2 (which is the ID representing all
    inaccessible locations), then NO change occurs to the map_visual.
    The map_visual stays the same, and nothing is returned.

    If the move IS possible, the grid is updated just like it was
    for lab 5, and the new x- and y- coordinates of the player
    are returned as a tuple.
    '''

    if dy + px >= len(map_visual) or dx + py >= len(map_visual[0]) or dy+px<0 or dx+py<0:
        return None
    if map_visual[dy + px][dx + py] == '(X)':
        return None
    else:
        map_visual[dy + px][dx + py] = '('+player_id+')'
        map_visual[px][py] = '(_)'
    return (dy+px,dx+py)



def check_items(current_location, game_items, inventory):
    '''
    (float, dict, list) -> None

    Given a float location id and a dict of game items, check
    if any of the game items are found in the current
    location provided. If they are, add them to the inventory
    that's provided.

    The game_items dict has item names as keys, and values
    as lists with the following information in this order:
    [description of item, location ID of where the item is found,
    location ID of where item should be dropped off].

    You should be modifying the variable 'inventory',
    within this function, and NOT returning anything.
    '''

    for i in game_items:
        if game_items[i][1] == current_location:
            inventory.append(i)



def check_game_won(game_data, inventory, p_x, p_y):
    '''
    (dict, list, int, int) -> bool

    Return True iff the player is at the goal location, and all
    goal items are in the player's inventory.
    '''

    #for i in game_data['goal_items']:
    if game_data['goal_location'] != (p_x, p_y):
        return False
    else:
        for i in game_data['goal_items']:
            if i in inventory:
                continue
            else:
                return False

    return True



def do_action(decision, game_data, current_location, inventory):
    '''
    (int, dict, float, list) -> str

    Given the game data dict, and the current location ID, get
    all the possible actions at that location.

    show_actions(game_data['location_data'][current_location][1])

    If the decision number given as 'decision' falls outside the number
    of allowed actions at this location, then return the string

    "Invalid decision. Please select choice from the decisions listed."
    Make sure this string is EXACTLY as above.

    Else, if the decision is valid, then figure out the location information
    of the new location ID that the player should end up at after
    doing this decision (use game_data, current_location, and the decision
    chosen to figure this out).

    Check for any items at this new location and add to inventory (remember you
    can call already existing functions to make your code shorter
    and less repetitive).

    Return the text description of the new location ID where you end up
    after doing this action (e.g. the same way that visit_location function
    returns text description of visited location).
    '''

    # YOUR CODE HERE #

    #location_id=current_location
    show_actions(game_data['location_data'][current_location][1])
    if decision>len(game_data['location_data'][current_location][1]):
        return "Invalid decision. Please select choice from the decisions listed."
    else:
        location_id= game_data['location_data'][current_location][1][decision-1][1]
        check_items(location_id,game_data['game_items'],inventory)
        return game_data['location_data'][location_id][0]




# --------------------------------------------------------------------------------------#
# --- EVERYTHING BELOW IS COMPLETED FOR YOU. DO NOT MAKE CHANGES BEYOND THIS LINE. ---- #
# --------------------------------------------------------------------------------------#

def check_inventory(inventory):
    '''
    (list) -> None

    Print out the contents of the inventory.

    NOTE:
    THIS FUNCTION IS ALREADY COMPLETE.
    YOU DO NOT NEED TO CHANGE THIS FUNCTION.
    '''

    if len(inventory) == 0:
        print("You have nothing in" \
              "your inventory.")
    print("Items in your inventory: " + str(inventory))


def visit_location(game_data, current_location):
    '''
    (dict, float) -> str

    Visit the current location data by printing out the map,
    checking if any items are found at that location,
    and then returning the text associated with this current location.

    NOTE:
    THIS FUNCTION IS ALREADY COMPLETE.
    YOU DO NOT NEED TO CHANGE THIS FUNCTION.
    '''

    print_map(game_data["map_visual"])
    check_items(current_location, game_data["game_items"], inventory)
    return game_data["location_data"][current_location][0]


def show_actions(actions):
    '''
    (list) -> None

    Given a list of special actions, print out all these actions (if any),
    and other basic actions that are possible.

    NOTE:
    THIS FUNCTION IS ALREADY COMPLETE.
    YOU DO NOT NEED TO CHANGE THIS FUNCTION.
    '''

    print("-------------------------")
    for i in range(len(actions)):
        print(i + 1, actions[i][0])
    print("Type N, S, E, or W to move, or inventory to check inventory.")
    print("-------------------------")


def print_map(map_data):
    '''
    (list of lists) -> None

    Print out the map represented by the given list of lists map_data.

    NOTE:
    THIS FUNCTION IS ALREADY COMPLETE.
    YOU DO NOT NEED TO CHANGE THIS FUNCTION.
    '''

    s = ''
    for row in range(len(map_data)):
        s += ''.join(location for location in map_data[row]) + "\n"
    print(s)


def get_moves(d):
    '''
    (str) -> tuple of two ints

    Given a direction that is either 'N', 'S', 'E' or 'W'
    (standing for North, South, East or West), return
    a tuple representing the changes that would occur
    to the x- and y- coordinates if a move is made in that
    direction.

    e.g. If d is 'W', that means the player should move
    to the left. In order to do so, their x-coordinate should
    decrease by 1. Their y-coordinate should stay the same.
    These changes can be represented as the tuple (-1, 0),
    because the x-coordinate would have -1 added to it,
    and the y-coordinate would have 0 added to it.

    >>> get_moves('W')
    (-1, 0)
    >>> get_moves('E')
    (1, 0)

    NOTE:
    THIS FUNCTION IS ALREADY COMPLETE.
    YOU DO NOT NEED TO CHANGE THIS FUNCTION.
    '''

    if (d == "N"):
        return (0, -1)
    elif (d == "S"):
        return (0, 1)
    elif (d == "E"):
        return (1, 0)
    else:
        return (-1, 0)


def print_help():
    '''
    () -> None

    Print out possible decisions that can be made.
    This function is called if the user provides an invalid decision.

    NOTE:
    THIS FUNCTION IS ALREADY COMPLETE.
    YOU DO NOT NEED TO CHANGE THIS FUNCTION.
    '''

    print("Type N, S, E or W to move North, South, East or West. \n" \
          "Type inventory to check inventory. \n" \
          "Type quit to quit the game.")
    print("If special actions are listed, you may type the number beside that action to choose that action.")


def set_game_data(map_file, item_file, location_file):
    '''
    (str, str, str) -> dict

    Read data from the given files and return a dictionary
    of all game data.

    NOTE:
    THIS FUNCTION IS ALREADY COMPLETE.
    YOU DO NOT NEED TO CHANGE THIS FUNCTION.
    '''

    map_data = load_map(map_file)
    map_visual, map_coors = generate_map(map_data, p_x, p_y, player_id)
    game_items = load_items(item_file)
    location_data = load_locations(location_file)

    # The lines below use list comprehensions again!
    # As stated in the lab 5 code, this is not covered in 108
    #   but I'm showing this to you anyway because it can come in handy for shortening code.
    # You can achieve the same thing without using this technique though, so no worries
    #   if you're not fully comfortable with it.
    # More info here about what this means: http://blog.teamtreehouse.com/python-single-line-loops
    game_overs = [k for k, v in location_data.items() if v[0].lower().startswith("game over")]
    goal_items = [k for k, v in game_items.items() if v[2] == -1]

    goal_location = get_indices(map_data, "-1")

    return {"map_data": map_data, "map_visual": map_visual, "map_coors": map_coors,
            "game_items": game_items, "location_data": location_data,
            "goal_items": goal_items, "goal_location": goal_location,
            "game_overs": game_overs, "won": False, "lost": False}


# ==== Finish the functions above according to their docstrings ==== #
# ==== The program starts here. ==== #
# ==== Do NOT change anything below this line. ==== #
if __name__ == "__main__":

    player_id = input("Choose any letter other than 'x' to represent you: ")
    while len(player_id) != 1 or not player_id.isalpha() or player_id.lower() == 'x':
        print("Invalid input.")
        player_id = input("Choose any letter other than 'x' to represent you: ")

    # initialize current player info
    p_x, p_y = 0, 0  # player's starting location is (0, 0) on the map
    inventory = []

    game_data = set_game_data("map.txt", "items.txt", "locations.txt")

    # show map and location data
    current_location = game_data["map_coors"][(p_x, p_y)]
    result = visit_location(game_data, current_location)

    while not game_data["won"] and not game_data["lost"]:

        show_actions(game_data["location_data"][current_location][1])
        decision = input("What do you want to do? > ")

        if decision.upper() in 'NSEW':
            dx, dy = get_moves(decision.upper())
            new_xy = update_map(game_data["map_visual"], game_data["map_coors"], player_id, p_x, p_y, dx, dy)
            if not new_xy:
                print("You can't go there.")
            else:
                p_x, p_y = new_xy
                current_location = game_data["map_coors"][(p_x, p_y)]
                result = visit_location(game_data, current_location)
                print(result)

        elif decision.isdigit():
            result = do_action(int(decision), game_data, current_location, inventory)
            print(result)

        elif "inventory" in decision:
            check_inventory(inventory)

        else:
            print_help()

        game_data["lost"] = result.lower().startswith("game over")
        game_data["won"] = check_game_won(game_data, inventory, p_x, p_y)

    if game_data["won"]:
        print("Congratulations! You found your way back home!")