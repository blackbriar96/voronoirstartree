"""
Turn .input to .in
"""
import os
import input_reader

def turn_input_to_in(address, out_dir='out/'):
    """
    Main function in utils.py
    """
    file_name = address.split('/')
    name = file_name[-1][:file_name[-1].index('.')]
    # read input from raw data
    voronoi_list = input_reader.read_input(address)

    # store readed voronoi to increase processing speed
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    input_reader.store_processed_input(voronoi_list, out_dir+name+'.in')


def get_all_files_in(directory):
    """
    Main function in utils.py
    """
    for a_file in os.listdir(directory):
        path = os.path.join(directory, a_file)
        yield path

def main(directory):
    """
    Main function in utils.py
    """
    for a_file in get_all_files_in(directory):
        if a_file.endswith(".input"):            
            print('TURN: ', a_file, 'TO: .in')
            turn_input_to_in(a_file)

if __name__ == '__main__':
    main('object/')
