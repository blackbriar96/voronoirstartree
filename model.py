from sympy import Point, Polygon

class Voronoi(object):
    def __init__(self, name, points):        
        self.name = name
        self.bound = Polygon(*points)
    
class RStartTree(object):
    def __init__(self, max_content_size = 4, content = list()):
        self.max_content_size = max_content_size

        self.all_content = list()
        self.childs = list()
        self.is_leaf = True
        self.parent = None
        self.bound = None

        for voronoi in content:
            self.insert(voronoi)

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
    def choose_leaf(node, new_inserted):
        if node.is_leaf:
            return node
        else:
            choosed = None
            choosed_expanded_size = None
            for i, child in enumerate(node.childs):
                child_expanded_size = RStartTree.update_bound(child, new_inserted).area
                
                if choosed is None and choosed_expanded_size is None:
                    choosed = child
                    choosed_expanded_size = child_expanded_size

                for j, other_child in enumerate(node.childs[:i]+node.childs[i+1:]):                    
                    if not child.is_leaf and child_expanded_size < other_child.bound.area:
                        choosed = child
                        choosed_expanded_size = child_expanded_size
                    else:
                        pass

    def insert(self, voronoi):
        self.all_content.append(voronoi)

        node = self.choose_leaf(self)

        if not self.is_leaf:
            pass
            # choose leaf            
        elif len(self.childs) < self.max_content_size:
            self.childs.append(voronoi)
            self.bound = RStartTree.update_bound(self, voronoi)
        else:
            # split
            pass
        
        return self.bound
    
    @staticmethod
    def update_bound(current, other):
        if current.bound is None:
            return other.bound
        else:
            other_xmin, other_ymin, other_xmax, other_ymax = other.bound.bounds
            current_xmin, current_ymin, current_xmax, current_ymax = current.bound.bounds
            
            current_xmin = other_xmin if other_xmin < current_xmin else current_xmin
            current_ymin = other_ymin if other_ymin < current_ymin else current_ymin
            current_xmax = other_xmax if other_xmax < current_xmax else current_xmax
            current_ymax = other_ymax if other_ymax < current_ymax else current_ymax
            
            return Polygon((current_xmin, current_ymin), (current_xmax, current_ymin), (current_xmax, current_ymax), (current_xmin, current_ymax))
