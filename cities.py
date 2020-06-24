import math
import copy
import random
import tkinter


def read_cities(file_name):

    """
    This function reads in the cities from the given `file_name`, and returns them as a list of four-tuples:

      [(state, city, latitude, longitude), ...] 

      @param file_name: name of the file that contains the city data
      @return: road_map: a list of four tuples that includes map data
    """

    road_map = []

    file = open(file_name, "r")
    lines = file.readlines()

    # remove trailing whitespace and split file by using spaces
    # to convert variables into float
    for line in lines:
        road_map.append((line.rstrip().split('\t')[0],
                         line.rstrip().split('\t')[1],
                         float(line.rstrip().split('\t')[2]),
                         float(line.rstrip().split('\t')[3])))
    file.close()

    return road_map


def print_cities(road_map):
    """
    Prints a list of cities, along with their locations.
    Prints two digits after the decimal point.

      @param road_map: a list tuples, output of the read_cities function.
      @return: cities: a list tuples, includes cities and their coordinates
    """

    cities = []

    for i in road_map:
        cities.append([i[1],
                       round(float(i[2]), ndigits=2),
                       round(float(i[3]), ndigits=2)])

    return cities


def compute_total_distance(road_map):
    """
    Returns the sum of the distances of all he connections in the `road_map`
    as a floating point number. For the last city in the list,
    it calculates distance between the first and the last city.

    It calculates Euclidean Distance between two cities for given coordinates (x1,y1), (x2,y2):

        distance between two cities = square root((x1 - x2) ** 2 + (y1 - y2) ** 2)

        @param road_map: a list of tuples, output of the read_cities function.
        @return: sum_distances: total distance  of all cities in the road_map
    """

    sum_distances = 0.0

    for i in range(len(road_map)):
        # condition to calculate distance between cities in the list
        if i != len(road_map) - 1:
            sum_distances += math.sqrt(
                (road_map[i][2] - road_map[i + 1][2]) ** 2 +
                (road_map[i][3] - road_map[i + 1][3]) ** 2)
        # extra condition to calculate the distance between the last city and the first city in the list
        else:
            sum_distances += math.sqrt(
                (road_map[i][2] - road_map[0][2]) ** 2 +
                (road_map[i][3] - road_map[0][3]) ** 2)

    return sum_distances


def swap_cities(road_map, index1, index2):
    """
    This function takes the city at location `index1` in the `road_map`, and the  city at location `index2`,
    swaps their positions in the `road_map`, and then computes the new total distance, and return the tuple:

        (new_road_map, new_total_distance)

        @param road_map: a list of tuples, output from the read_cities function.
        @param index1: index of the city in road_map which need to swap with the city in index2
        @param index2: index of the city in road_map which need to swap with the city in index1
        @return: the tuple (new_road_map, new_total_distance)
    """
    # in order not to change the original road_map variable, copy of the road_map is created
    road_map_copy = copy.deepcopy(road_map)

    # to swap cities with given indexes
    if index1 != index2:
        swap = road_map_copy[index2]
        road_map_copy[index2] = road_map_copy[index1]
        road_map_copy[index1] = swap

    return (road_map_copy, compute_total_distance(road_map_copy))


def shift_cities(road_map):
    """
    For every index i in the `road_map`, the city at the position i moves
    to the position i+1. The city at the last position moves to the position
    0. Return the new road map.
    @param road_map:
    @return: a new road_map: a list of four tuples that includes map data
    """
    # to shift cities, the last city is removed and then it added to the first index

    new_road_map = [road_map[-1]] + road_map[:-1]

    return new_road_map


def find_best_cycle(road_map):
    """
    Using a combination of `swap_cities` and `shift_cities`, 
    try `10000` swaps/shifts, and each time keep the best cycle found so far. 
    After `10000` swaps/shifts, return the best cycle found so far.
    Use randomly generated indices for swapping.
    """

    # created baseline best_cycle and best_total_distance variables by swap_cities function.
    best_cycle, best_total_distance = swap_cities(road_map,
                                                  random.randint(0, len(road_map)-1),
                                                  random.randint(0, len(road_map)-1))

    for i in range(10001):

        # apply shift_cities function to find the best cycle
        shift_best_cycle = shift_cities(best_cycle)
        shift_best_distance = compute_total_distance(best_cycle)

        if best_total_distance > shift_best_distance:
            best_cycle = shift_best_cycle
            best_total_distance = shift_best_distance

        # apply swap_cities function to find the best cycle
        swap_best_cycle, swap_best_distance = swap_cities(best_cycle,
                                                          random.randint(0, len(road_map)-1),
                                                          random.randint(0, len(road_map)-1))
        if best_total_distance > swap_best_distance:
            best_cycle = swap_best_cycle
            best_total_distance = swap_best_distance

    return best_cycle


def print_map(road_map):
    """
    Prints, in an easily understandable format, the cities and  their connections,
    along with the cost for each connection and the total cost.

    Here an example of the printed output:

        Connection 1 :  Lincoln ========> Pierre     (COST: 5.1052153729977965 )
        Connection 2 :  Pierre ========> Bismarck     (COST: 4.467358777622971 )
        Connection 3 :  Bismarck ========> Helana     (COST: 11.46453602088514 )
        .....
        Connection 50 :  Des Moines =======> Lincoln     (COST: 3.152762894427983 )

        TOTAL COST FOR THE BEST CYCLE IS 343.4879426527414

    """
    total_cost = 0.0

    for i in range(len(road_map)):

        if i != len(road_map) - 1:
            cost = math.sqrt(
                (road_map[i][2] - road_map[i + 1][2]) ** 2 +
                (road_map[i][3] - road_map[i + 1][3]) ** 2)

            print("Connection", i+1, ": ",
                  road_map[i][1], "========>", road_map[i + 1][1],
                  "    (COST:", cost, ")")

            total_cost += cost

        else:
            cost = math.sqrt(
                (road_map[i][2] - road_map[0][2]) ** 2 +
                (road_map[i][3] - road_map[0][3]) ** 2)

            print("Connection", i+1, ": ",
                  road_map[i][1], "=======>", road_map[0][1],
                  "    (COST:", cost, ")", end="\n\n")

            total_cost += cost

    print("TOTAL COST FOR THE BEST CYCLE IS", total_cost)


"""
Functions starts with "visualise" names are created to apply to extend the implementation with functionality to
visualize road maps. To visualize the road map, it follows the way "A" in the coursework. After importing the best map
from cities.py, it uses "TEXTUAL PRINTING" method to visualise the map.

Here is an example of the output:

     -159 -158 -157 -156 -155 -154 -153 -152 -151
       |    |    |    |    |    |    |    |    |
59   - 1  - 3  -    -    -    -   -    -    -
       |    |    |    |    |    |    |    |    |
58   -    - 2  -    -    - 6  -   -  8 -    -
       |    |    |    |    |    |    |    |    |
57   -    -     -    -    - 5  - 7  -    -   -
       |    |    |    |    |    |    |    |    |
56   -    -    -    - 4  -    -    -   -    -

Coordinates are ranging between 90 and -90 for latitude and -180 and 180 for logitudes.
Printed map will only show the specific range of latitudes and longitudes to cover all the cities.

It returns a GUI window using Tkinder module, thus user can scroll up and down in the map to see all the cities.
"""


def visualise_find_latitude_longitude_range(road_map):
    """This function finds the best range of latitudes and longitudes to cover all cities in the road_map"""

    max_lat = -90
    min_lat = 90

    max_long = -180
    min_long = 180

    # to find maximum and minimum values for latitudes and longitudes
    for i in road_map:
        if i[2] < min_lat:
            min_lat = i[2]
        if i[2] > max_lat:
            max_lat = i[2]
        if i[3] < min_long:
            min_long = i[3]
        if i[3] > max_long:
            max_long = i[3]

    # add 1 to minimum values, subtract 1 from maximum values to cover all occurances in the map
    return round(max_lat + 1), round(min_lat - 1), round(max_long + 1), round(min_long - 1)


def visualise_longitudes(max_long, min_long):
    """
    This function returns the longitude values in a specific range as columns.
    The function checks the length of the longitudes and then formats white space before and after of the number.

    Here is the example of the output:
         -159 -158 -157 -156 -155 -154 -153 -152 -151 ....0    1    2    3.... 178  179  180

    @param max_long: maximum longitude in the road_map
    @param min_long: minimum longitude in the road_map
    """

    # to create a list to append strings
    line = []
    # to add additional blank for the beginning of the column
    line.append("     ")
    for i in range(min_long, max_long+1):
        # to check the number of digits and add white spaces around them
        if len(str(i)) == 4:
            line.append(str(i)+" ")
        elif len(str(i)) == 3:
            line.append(" " + str(i) + " ")
        elif len(str(i)) == 2:
            line.append(" " + str(i) + "  ")
        elif len(str(i)) == 1:
            line.append("  " + str(i) + "  ")
    # to concatenate strings in the list
    return "".join(line)


def visualise_longitude_characters(max_long, min_long):
    """
    This function to returns "|" characters that belongs to longitude columns.

    Here is the example of the output of this function:
               |    |    |    |    |    |    |    |    |

    @param max_long: maximum longitude in the road_map
    @param min_long: minimum longitude in the road_map
    """

    line = []
    # add new line before and the spaces in the beginning of the line
    line.append("\n     ")
    for i in range(min_long, max_long+1):
        line.append("  |  ")
    line.append("\n")

    # to concatenate strings in the list
    return "".join(line)


def visualise_latitude_characters_and_mark_locations1(road_map, latitude, longitude):
    """
    This function is to arrange index of the cities between latitude "-" characters.
    It looks for the coordinates of the cities, and finds the correct coordinates in the map, and returns the index
    of the city along with "-" character. If it can not match with the coordinates in the map,
    it just returns "-" character.

    Here is the example of the output:
        - 1  - 3  -    -    - 12 -    -    -    -

    @param road_map: best cycle that we created as road_map
    @param latitude: latitude values of the row
    @param longitude: longitude value of the column

    """

    for city_index in range(0, len(road_map)):
        if latitude == round(road_map[city_index][3]) and longitude == round(road_map[city_index][2]):
            # used string formatting to arrange the white spaces around city index by using their length
            format_num = 3 - len(str(city_index + 1))
            char_number_format = "- " + str(city_index + 1) + "{:>{format_num}}".format("", format_num=format_num)
            break
        else:
            char_number_format = "-    "

    return char_number_format


def visualise_latitude_characters_and_mark_locations2(max_long, min_long, longitude, road_map):
    """
    This function loops through latitudes, calls visualise_latitude_characters_and_mark_location1 function
    to return arranged index of the cities between latitude "-" characters.

    @param max_long: maximum longitude in the road_map
    @param min_long: minimum longitude in the road_map
    @param longitude: specific longitude in all longitudes
    @param road_map: the best cycle that we created as road_map
    """

    line = []
    for latitude in range(min_long, max_long + 1):
        # to loop through our cities
        for city_position in range(0, len(road_map)):
            char_number_formatted = visualise_latitude_characters_and_mark_locations1(road_map, latitude, longitude)

        line.append(char_number_formatted)
    # to concatenate strings in the list
    return "".join(line)


def visualise_latitudes(max_lat, min_lat, max_long, min_long, road_map):
    """
    This function is to print latitudes for every row, it also calls other visualise functions inside
    to reach the final output showed below.

    Here is the example of the output:

         -159 -158 -157 -156 -155 -154 -153 -152 -151
           |    |    |    |    |    |    |    |    |
    59   - 1  - 3  -    -    -    -   -    -    -
           |    |    |    |    |    |    |    |    |
    58   -    - 2  -    -    - 6  -   -  8 -    -
           |    |    |    |    |    |    |    |    |
    57   -    -    -    -    - 5  - 7  -   -    -
           |    |    |    |    |    |    |    |    |
    56   -    -    -    - 4  -    -    -   -    -


    @param max_lat: maximum latitude in the road_map
    @param min_lat: minimum latitude in the road_map
    @param max_long: maximum longitude in the road_map
    @param min_long: minimum longitude in the road_map
    @param road_map: the best cycle that we found

    """

    line = []
    # to call function to print longitude numbers
    long = visualise_longitudes(max_long, min_long)
    line.append(long)
    # to call function to print "|" characters below longitudes
    long_char = visualise_longitude_characters(max_long, min_long)
    line.append(long_char)

    # loop through latitudes
    for latitude in range(max_lat, min_lat - 1, -1):
        # condition just for the last row to format characters
        if latitude == min_lat:
            line.append(str(latitude) + "  ")
            lat_and_loc = visualise_latitude_characters_and_mark_locations2(max_long, min_long, latitude, road_map)
            line.append(lat_and_loc)
        # condition for all rows (latitudes)
        # it formats white spaces around latitudes in the beginning of the every row, it uses the length to format it.
        else:
            format_num = 5 - len(str(latitude))
            line.append(str(latitude) + "{:>{format_num}}".format("", format_num=format_num))
            lat_and_loc = visualise_latitude_characters_and_mark_locations2(max_long, min_long, latitude, road_map)
            line.append(lat_and_loc)
            line.append(long_char)
    return "".join(line)


def visualise(road_map):
    """
    This function takes the best cycle as an input and returns the output of the visualise_latitudes function in
     a GUI window using Tkinder module. The GUI window allows the user to scroll up and down in the map
     to see all of the cities in the road_map interactively.
    """

    max_lat, min_lat, max_long, min_long = visualise_find_latitude_longitude_range(road_map)
    printed_map = visualise_latitudes(max_lat, min_lat, max_long, min_long, road_map)

    # to create close min max buttons
    window = tkinter.Tk()

    # optional to rename the new windon
    window.title("ROAD MAP GUI")

    textContainer = tkinter.Frame(window)
    text = tkinter.Text(textContainer, wrap="none")

    textVsb = tkinter.Scrollbar(textContainer, orient="vertical", command=text.yview)
    textHsb = tkinter.Scrollbar(textContainer, orient="horizontal", command=text.xview)

    text.configure(yscrollcommand=textVsb.set, xscrollcommand=textHsb.set)

    text.grid(row=0, column=0, sticky="nsew")
    textVsb.grid(row=0, column=1, sticky="ns")
    textHsb.grid(row=1, column=0, sticky="ew")

    textContainer.grid_rowconfigure(0, weight=1)
    textContainer.grid_columnconfigure(0, weight=1)

    text.insert(1.0, printed_map)

    text.configure(state='disabled')
    textContainer.pack(side="top", fill="both", expand=True)

    return window.mainloop()


def main():
    """
    Reads in and prints out the city data, then creates the "best"
    cycle and prints it out.
    """
    road_map = read_cities(input("Please write the file name here to load :"))
    best_cycle = find_best_cycle(road_map)

    # to print the original data
    print("\nHere is the original City Data:\n", road_map, "\n")

    # to print the best cycle
    print("\nHere is found the best cycle with its costs:\n")
    print_map(best_cycle)

    # to print the graphically printed map at the new GUI window for the best cycle
    print(visualise(best_cycle))


if __name__ == "__main__":
    main()

