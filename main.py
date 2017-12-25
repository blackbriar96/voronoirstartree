import input_reader
import utils
from model import Point, RStartTree

def build(file_dir):
    voronoi_list = input_reader.read_input(file_dir)
    return voronoi_list

if __name__ == '__main__':
    # for a_file in utils.get_all_files_in('object/'):
    #     print a_file,
    #     tree = RStartTree(build(a_file))
    #     print tree

    file_input = raw_input('Input File (file.input): ')
    
    voronoi_list = input_reader.read_input(file_input)
    tree = RStartTree(max_content_size = 4, content = voronoi_list)
    query_point = Point([float(data) for data in raw_input('Query Point (x,y): ').split(',')])

    # print tree.seq_search(query_point, include_on_edge = True)
    region = tree.search(query_point, include_on_edge = True)

    if region is not '':
        print 'Region Found:', region
    else:
        print 'Not Found'