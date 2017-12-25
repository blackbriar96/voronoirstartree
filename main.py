import input_reader
import utils
from model import Point, RStartTree
import cPickle as pickle

def build_tree(file_dir):    
    # voronoi_list = input_reader.read_input(file_dir)
    # tree = RStartTree(max_content_size = 4)

    # for voronoi in voronoi_list:
    #     print 'input tree:', voronoi.name
    #     tree.insert(voronoi)

    # with open('save/pypy_tree.pkl', 'wb') as file_output:
    #     pickle.dump(tree, file_output, pickle.HIGHEST_PROTOCOL)

    with open('save/pypy_tree.pkl', 'rb') as file_input:
        tree = pickle.load(file_input)

    return tree

if __name__ == '__main__':
    # file_input = raw_input('Input File (file.input): ')
    # file_input = 'test/test-irfan.input'
    file_input = 'object/region-05-titik.input'
        
    tree = build_tree(file_input)

    query_point = Point([float(data) for data in raw_input('Query Point (x,y): ').split(',')])

    # print tree.seq_search(query_point, include_on_edge = True)
    region = tree.search(query_point, include_on_edge = True)

    if region is not '':
        print 'Region Found:', region
    else:
        print 'Not Found'