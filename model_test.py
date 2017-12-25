from model import Voronoi, RStartTree, comb_and_comp, Point
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

        tree_all = RStartTree(content = [tree_a, tree_b])
        polygon_c = Voronoi("poly_c", [(1, 6), (1, 4), (2, 4), (2, 6)])
        self.assertEqual(tree_a, RStartTree.choose_leaf(tree_all, polygon_c))
    
    def test_split(self):
        polygon_a = Voronoi("poly_a", [(2, 5), (2, 2), (9, 2), (9, 5)])
        polygon_b = Voronoi("poly_b", [(2, 2), (2, 1), (8, 1), (9, 2)])
        polygon_c = Voronoi("poly_c", [(0, 5), (0, 2), (1, 2), (1, 5)])
        polygon_d = Voronoi("poly_d", [(18, 5), (18, 2), (21, 2), (21, 5)])
        polygon_e = Voronoi("poly_e", [(18, 8), (18, 6), (23, 6), (23, 8)])

        tree = RStartTree()
        tree.childs = [polygon_a, polygon_b, polygon_c, polygon_d, polygon_e]
        first, second = tree.split()

        self.assertEqual(3, len(first.childs))
        self.assertEqual(2, len(second.childs))
    
    def test_rebound_border(self):
        polygon_a = Voronoi("poly_a", [(2, 5), (2, 2), (9, 2), (9, 5)])
        polygon_b = Voronoi("poly_b", [(2, 2), (2, 1), (8, 1), (9, 2)])
        polygon_c = Voronoi("poly_c", [(0, 5), (0, 2), (1, 2), (1, 5)])

        tree_a = RStartTree(content = [polygon_a, polygon_b])
        tree_b = RStartTree(content = [tree_a, polygon_c])

        tree_a.parent = tree_b
        tree_a.rebound_upward()

        self.assertEqual(3, len(tree_b.childs))
    
    def test_insert(self):    
        polygon_a = Voronoi("poly_a", [(2, 5), (2, 2), (9, 2), (9, 5)])
        polygon_b = Voronoi("poly_b", [(2, 2), (2, 1), (8, 1), (9, 2)])
        polygon_c = Voronoi("poly_c", [(0, 5), (0, 2), (1, 2), (1, 5)])
        polygon_d = Voronoi("poly_d", [(18, 5), (18, 2), (21, 2), (21, 5)])
        polygon_e = Voronoi("poly_e", [(18, 8), (18, 6), (23, 6), (23, 8)])

        tree = RStartTree()
        tree.insert(polygon_a)
        self.assertEqual(1, len(tree.childs))        
        tree.insert(polygon_b)
        self.assertEqual(2, len(tree.childs))
        tree.insert(polygon_c)
        self.assertEqual(3, len(tree.childs))        
        tree.insert(polygon_d)
        self.assertEqual(4, len(tree.childs))        
        tree.insert(polygon_e)
        self.assertEqual(2, len(tree.childs))
    
    def test_search(self):
        polygon_a = Voronoi("poly_a", [(2, 5), (2, 2), (9, 2), (9, 5)])
        polygon_b = Voronoi("poly_b", [(2, 2), (2, 1), (8, 1), (9, 2)])
        polygon_c = Voronoi("poly_c", [(0, 5), (0, 2), (1, 2), (1, 5)])
        polygon_d = Voronoi("poly_d", [(18, 5), (18, 2), (21, 2), (21, 5)])
        polygon_e = Voronoi("poly_e", [(18, 8), (18, 6), (23, 6), (23, 8)])

        tree_a = RStartTree(content = [polygon_a, polygon_b, polygon_c])
        tree_b = RStartTree(content = [polygon_d, polygon_e])

        tree = RStartTree(content = [tree_a, tree_b])
        res = tree.search(Point(19, 2), include_on_edge = True)
        self.assertEqual('poly_d', res)


if __name__ == '__main__':
    unittest.main()