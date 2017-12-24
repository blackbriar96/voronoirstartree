from sympy import Point, Polygon

class Voronoi(object):
    def __init__(self, name, points):        
        self.name = name
        self.bound = Polygon(*points)
    
class RStartTree(object):
    def __init__(self, max_content_size = 4, content = list(), is_leaf = True):
        self.max_content_size = max_content_size

        self.all_content = list()
        self.childs = list()
        self.is_leaf = is_leaf
        self.parent = None
        self.bound = None

        for voronoi in content:
            # temporary
            self.childs.append(voronoi)
            self.bound = RStartTree.update_bound(self, voronoi)
            # self.insert(voronoi)

    def seq_search(self, query_point, include_on_edge = False):
        for voronoi in self.all_content:
            if voronoi.bound.encloses_point(query_point) or (include_on_edge and len(voronoi.bound.intersection(query_point)) > 0):
                return voronoi.name
        return 'Not Found'

    def search(self, query_point, include_on_edge = False):
        possible_region = list()
        for node in self.childs:
            if node.bound.encloses_point(query_point) or (include_on_edge and len(node.bound.intersection(query_point)) > 0):
                if isinstance(node, RStartTree) :
                    possible_region.append(node.search(query_point))
                else:
                    possible_region.append(node.name)
        return 'Not Found' if len(possible_region) < 1 else ' '.join(possible_region)

    @staticmethod
    def count_overlap_area(first, second):
        first_xmin, first_ymin, first_xmax, first_ymax = first.bound.bounds
        second_xmin, second_ymin, second_xmax, second_ymax = second.bound.bounds
        return (max(0, min(first_xmax, second_xmax)) - max(first_xmin, second_xmin)) * \
                (max(0, min(first_ymax, second_ymax)) - max(first_ymin, second_ymin))

    @staticmethod
    def choose_leaf(node, new_inserted):
        if node.is_leaf:
            return node
        else:
            choosed = None
            choosed_expanded_size = 0
            choosed_total_overlap = 0
            for i, child in enumerate(node.childs):
                expanded_size = RStartTree.update_bound(child, new_inserted).area
                
                total_overlap = 0
                for j, other_child in enumerate(node.childs[:i] + node.childs[i+1:]):
                    overlap = RStartTree.count_overlap_area(child, other_child)                    
                    total_overlap += overlap

                if choosed is None or \
                    choosed_total_overlap > total_overlap or \
                    (choosed_total_overlap == total_overlap and choosed_expanded_size > expanded_size):

                    choosed = child
                    choosed_expanded_size = expanded_size
                    choosed_total_overlap = total_overlap                


            return RStartTree.choose_leaf(choosed, new_inserted)
    
    @staticmethod
    def update_bound(current, other):
        if current.bound is None:
            return other.bound
        else:
            current_xmin, current_ymin, current_xmax, current_ymax = current.bound.bounds
            other_xmin, other_ymin, other_xmax, other_ymax = other.bound.bounds
            
            current_xmin = other_xmin if other_xmin < current_xmin else current_xmin
            current_ymin = other_ymin if other_ymin < current_ymin else current_ymin
            current_xmax = other_xmax if other_xmax > current_xmax else current_xmax
            current_ymax = other_ymax if other_ymax > current_ymax else current_ymax

            return Polygon((current_xmin, current_ymin), (current_xmax, current_ymin), (current_xmax, current_ymax), (current_xmin, current_ymax))


import unittest
class TestRStartTree(unittest.TestCase):
    def test_update_bound(self):
        polygon_a = Voronoi("poly_a", [(2, 5), (2, 2), (9, 2), (9, 5)])
        polygon_b = Voronoi("poly_b", [(6, 7), (6, 3), (12, 3), (12, 7)])
        polygon_c = Voronoi("poly_c", [(2, 7), (2, 2), (12, 2), (12, 7)])

        self.assertEqual(polygon_c.bound, RStartTree.update_bound(polygon_a, polygon_b))        

    def test_overlap(self):
        polygon_a = Voronoi("poly_a", [(2, 5), (2, 2), (9, 2), (9, 5)])
        polygon_b = Voronoi("poly_b", [(6, 7), (6, 3), (12, 3), (12, 7)])
        self.assertEqual(6, RStartTree.count_overlap_area(polygon_a, polygon_b))

    def test_choose_leaf(self):
        polygon_a = Voronoi("poly_a", [(2, 5), (2, 2), (9, 2), (9, 5)])
        tree_a = RStartTree(content = [polygon_a])
        self.assertEqual(tree_a, RStartTree.choose_leaf(tree_a, polygon_a))

        polygon_b = Voronoi("poly_b", [(6, 7), (6, 3), (12, 3), (12, 7)])
        tree_b = RStartTree(content = [polygon_b])

        tree_all = RStartTree(is_leaf = False, content = [tree_a, tree_b])
        # polygon_c = Voronoi("poly_c", [(11, 8), (11, 6), (14, 6), (14, 8)])        
        polygon_c = Voronoi("poly_c", [(1, 6), (1, 4), (2, 4), (2, 6)])        
        self.assertEqual(tree_a, RStartTree.choose_leaf(tree_all, polygon_c))        

    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()