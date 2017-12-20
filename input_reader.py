'''
This file define how my TA gain it's input
'''

import pickle
from model import Point, Voronoi

def clean_input(address='voronoi.input'):
    """
    clean input file from empty lines
    """
    file_input = open(address, 'r')
    file_output = open(address+".out", 'w')

    for line in file_input:
        if line not in ('', ' ', '\n'):
            file_output.write(line)


def read_input(address='voronoi.input'):
    """
    read input file in address location and return array points
    param:
    - address

    retun:
    - voronoi list
    """
    file_input = open(address, 'r')

    current_region = ''
    points = list()
    voronoi_list = list()

    for line in file_input:
        data = line.split(',')

        if current_region != data[0]:
            if len(points) > 0:
                voronoi_list.append(Voronoi(current_region, points))
            
            points = list()

        current_region = data[0]
        points.append((float(data[1]), float(data[2])))
    
    if len(points) > 0:
        voronoi_list.append(Voronoi(current_region, points))

    return voronoi_list

def store_processed_input(voronoi_list, file_address='processed.in'):
    """
    store processing input into json
    """
    with open(file_address, 'wb') as output:
        pickle.dump(voronoi_list, output, pickle.HIGHEST_PROTOCOL)


def get_processed_input(address='processed.in'):
    """
    read input from processed file
    """
    with open(address, 'rb') as input_file:
        return pickle.load(input_file)
