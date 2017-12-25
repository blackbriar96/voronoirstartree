from sympy import Point, Polygon

def comb_and_comp(lst, size):
    """
    get combination and its complementer
    function from https://stackoverflow.com/questions/28992042/algorithm-to-return-all-combinations-of-k-out-of-n-as-well-as-corresponding-comp
    """
    # no combinations
    if len(lst) < size:
        return
    # trivial 'empty' combination
    if size == 0 or lst == []:
        yield [], lst
    else:
        first, rest = lst[0], lst[1:]
        # combinations that contain the first element
        for in_, out in comb_and_comp(rest, size - 1):
            yield [first] + in_, out
        
        # combinations that do not contain the first element
        for in_, out in comb_and_comp(rest, size):
            yield in_, [first] + out

class Voronoi(object):
    def __init__(self, name, points):        
        self.name = name
        self.bound = Polygon(*points)
    
    def __str__(self):
        return str(self.bound)
    
class RStartTree(object):
    def __init__(self, max_content_size = 4, content = list(), is_leaf = True):
        self.max_content_size = max_content_size

        self.all_content = list()
        self.childs = list()
        self.is_leaf = is_leaf
        self.parent = None
        self.bound = None

        for voronoi in content:
            self.all_content.append(voronoi)                        
            self.insert(voronoi)

        for voronoi in content:
            if isinstance(voronoi, RStartTree):
                self.is_leaf = False
                break

    def seq_search(self, query_point, include_on_edge = False):
        for voronoi in self.all_content:
            if voronoi.bound.encloses_point(query_point) or (include_on_edge and voronoi.bound.intersection(query_point)):
                return voronoi.name
        return 'Not Found'

    def search(self, query_point, include_on_edge = False):
        possible_region = list()
        for node in self.childs:
            if node.bound.encloses_point(query_point) or (include_on_edge and node.bound.intersection(query_point)):
                if isinstance(node, RStartTree) :
                    possible_region.append(node.search(query_point, include_on_edge))
                else:
                    possible_region.append(node.name)
        return '' if len(possible_region) < 1 else ''.join(possible_region).strip()

    def insert(self, new_inserted):
        # find node
        node = RStartTree.choose_leaf(self, new_inserted)
        
        if len(node.childs) + 1 > node.max_content_size:            
            #try reinsert
            selected_to_remove = None
            selected_area_reduced = 0
            for child in node.childs:
                area_reduced = node.bound.area - child.bound.area
                if selected_to_remove is None or selected_area_reduced > area_reduced:
                    selected_to_remove = child
                    selected_area_reduced = area_reduced
            
            node.childs.remove(selected_to_remove)
            node.rebound_border()

            root_node = node
            while root_node.parent is not None:
                root_node = root_node.parent
            
            selected_reinsert_node = RStartTree.choose_leaf(root_node, selected_to_remove)
            if (selected_reinsert_node is not node):
                # insert to other node
                selected_reinsert_node.insert(selected_to_remove)
            else:
                # reinsert to current node
                node.childs.append(selected_to_remove)
                node.bound = RStartTree.update_bound(self, selected_to_remove)
        
        # insert new node to current
        node.childs.append(new_inserted)
        node.bound = RStartTree.update_bound(self, new_inserted)
        
        if len(node.childs) > node.max_content_size:  # reinsert to other node failed
            node.childs = list(node.split())
            node.rebound_upward()
    
    def rebound_upward(self):
        if self.parent is not None:
            # print 'rebound_upward', self.parent, self.parent.childs
            self.parent.childs.remove(self)
            for child in self.childs:
                self.parent.childs.append(child)            
            if len(self.parent.childs) > self.parent.max_content_size:
                self.parent.childs = list(self.parent.split())
                self.parent.rebound_upward()
    
    def split(self):        
        # ready the new container
        first_node = None
        second_node = None

        # put indexes in new list
        content_indexes = list(range(len(self.childs)))  
        for max_member_count in range(self.max_content_size):
            for first_indexes, second_indexes in comb_and_comp(content_indexes, max_member_count + 1):                
                new_first = RStartTree(max_content_size = self.max_content_size, content = [self.childs[i] for i in first_indexes])
                new_second = RStartTree(max_content_size = self.max_content_size, content = [self.childs[i] for i in second_indexes])

                if (first_node is None and second_node is None):
                    first_node = new_first
                    second_node = new_second
                else:
                    current_best = first_node.bound.area + second_node.bound.area
                    new_best = new_first.bound.area + new_second.bound.area
                    if new_best <= current_best:  # ' <= ' take last configuration, cause it divide the node with more member
                        first_node = new_first
                        second_node = new_second

        first_node.parent = self
        second_node.parent = self

        self.is_leaf = False
        return first_node, second_node

    def rebound_border(self):
        self.bound = None
        for content in self.childs:
            self.bound = RStartTree.update_bound(self, content)

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
