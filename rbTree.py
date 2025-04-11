L = [0, 1]
# L[1] = red , L[0] = black

class RBTreeNode:
    def __init__(self, ride, min_heap_node):
        self.ride = ride # ride object
        self.parent = n  # parent node
        self.left = n  # left node
        self.right = n  # right node
        self.size = 0
        self.color = L[1]  
        self.min_heap_node = min_heap_node # min heap node

n = None
class RBTree:
    def __init__(self):
        # initialize the tree
        self.nil = RBTreeNode(None, None) # nil node
        self.size = 0
        self.nil.left = n 
        self.nil.right = n
        self.tree = n
        self.nil.color = L[0]
        self.root = self.nil

    def _find_min(self, n):
        # find the minimum node
        if n.left == self.nil:
            return n
        else:
            return self._find_min(n.left)

    def _left_rotate(self, x):
        #left rotation
        y = x.right 
        x.right = y.left 

        if y.left != self.nil:
            y.left.parent = x

        self._update_parent(x, y)

        y.left = x
        x.parent = y

    def _update_parent(self, x, y):
        # update parent
        y.parent = x.parent
        if x.parent is n:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

    def _right_rotate(self, x):
        #right rotation
        y = x.left
        x.left = y.right

        if y.right != self.nil:
            y.right.parent = x

        self._update_parent(x, y)

        y.right = x
        x.parent = y

    def remove_node(self, item, key):
        r = 0
        # remove node from tree
        removed = self.nil # removed node
        while item != self.nil: # while item is not nil
            if item.ride.ride_number == key: 
                removed = item
                r += 1
            if item.ride.ride_number >= key:
                item = item.left
            else:
                item = item.right
                r = 0
        if removed == self.nil:
            return
        min_heap_node = removed.min_heap_node  # save min heap node
        y = removed
        r -= 1
        y_original_color = y.color  # save original color
        if removed.left == self.nil:  # if removed node has no left child
            x = removed.right
            self._rb_replace(removed, removed.right) 
            r += 1

        elif removed.right == self.nil:  # if removed node has no right child
            x = removed.left
            self._rb_replace(removed, removed.left)
            r -= 1
    
        else:
            y = self._find_min(removed.right)
            y_original_color = y.color
            x = y.right
            if y.parent == removed: # if y is right child of removed node
                x.parent = y
                r += 1
            else:
                self._rb_replace(y, y.right)
                r = 0
                y.right = removed.right
                y.right.parent = y

            self._rb_replace(removed, y)
            r -= 1
            y.left = removed.left
            y.left.parent = y
            y.color = removed.color
        if y_original_color == L[0]: # if original color is black
            self.rebalance_after_remove(x)
            r = 0
        return min_heap_node
            
    def search_key(self, key):
        # search key in tree
        current = self.root 
        while current != self.nil: 
            if current.ride.ride_number == key: 
                return current 
            if current.ride.ride_number < key: # if current key is less than key
                current = current.right
            else:
                current = current.left
        return n
    
    def _rb_replace(self, item, child_item): 
        elder = item.parent
        # replace item with child item
        if elder is n: # if item is root
            self.root = child_item
        elif item == elder.right: # if item is right child
            elder.right = child_item
        else:
            elder.left = child_item
        child_item.parent = elder # update child item parent

    def remove(self, ride_number):
        # remove ride number from tree
        return self.remove_node(self.root, ride_number)
    
    def rebalance_after_remove(self, item):
        # balance tree after remove
        while item != self.root and item.color == L[0]: 
            if item == item.parent.right: # if item is right child
                sibling = item.parent.left
                if sibling.color != L[0]: # if sibling color is not black
                    item.parent.color = L[1] # set parent color to red
                    sibling.color = L[0] # set sibling color to black
                    self._right_rotate(item.parent)
                    sibling = item.parent.left

                if sibling.right.color == L[0] and sibling.left.color == L[0]: # if sibling right and left color is black
                    sibling.color = L[1] # set sibling color to red
                    item = item.parent
                else:
                    if sibling.left.color != L[1]: # if sibling left color is not black
                        sibling.right.color = L[0] # set sibling right color to black
                        sibling.color = L[1] # set sibling color to red
                        self._left_rotate(sibling)
                        sibling = item.parent.left

                    sibling.color = item.parent.color
                    item.parent.color = L[0]  # set parent color to black
                    sibling.left.color = L[0] # set sibling left color to black
                    self._right_rotate(item.parent)
                    item = self.root
            else:
                sibling = item.parent.right
                if sibling.color != L[0]: # if sibling color is not black
                    item.parent.color = L[1] # set parent color to red
                    sibling.color = L[0] # set sibling color to black
                    self._left_rotate(item.parent)
                    sibling = item.parent.right

                if sibling.right.color == L[0] and sibling.left.color == L[0]: # if sibling right and left color is black
                    sibling.color = L[1] # set sibling color to red
                    item = item.parent
                else:
                    if sibling.right.color != L[1]: # if sibling right color is not black
                        sibling.left.color = L[0]
                        sibling.color = L[1] # set sibling color to red
                        self._right_rotate(sibling)
                        sibling = item.parent.right

                    sibling.color = item.parent.color
                    item.parent.color = L[0] # set parent color to black
                    sibling.right.color = L[0] # set sibling right color to black
                    self._left_rotate(item.parent)
                    item = self.root
        item.color = L[0] # set item color to black

    def _locate_rides_in_range(self, n, low, high, result):
        m = (low + high) // 2
        # locate rides in range 
        if n == self.nil:
            return
        if low < n.ride.ride_number:
            self._locate_rides_in_range(n.left, low, high, result)
            m += 1
        if low <= n.ride.ride_number <= high:
            result.append(n.ride)
            m -= 1
        self._locate_rides_in_range(n.right, low, high, result)
    
    def _rebalance_post_insert(self, node):
        while node.parent.color == L[1]:
            if node.parent == node.parent.parent.left: # if node parent is left child
                sibling = node.parent.parent.right
                if sibling.color == L[0]: # if sibling color is red
                    if node == node.parent.right: # if node is right child
                        node = node.parent
                        self._left_rotate(node)
                    node.parent.color = L[0] # set parent color to black
                    node.parent.parent.color = L[1] # set parent parent color to red
                    self._right_rotate(node.parent.parent)
                else:
                    sibling.color = L[0] # set sibling color to black
                    node.parent.color = L[0] # set parent color to black
                    node.parent.parent.color = L[1] # set parent parent color to red
                    node = node.parent.parent
            else:
                sibling = node.parent.parent.left
                if sibling.color == L[0]: # if sibling color is red
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    node.parent.color = L[0] # set parent color to black
                    node.parent.parent.color = L[1] # set parent parent color to red
                    self._left_rotate(node.parent.parent)
                else:
                    sibling.color = L[0] # set sibling color to black
                    node.parent.color = L[0] # set parent color to black
                    node.parent.parent.color = L[1] # set parent parent color to red
                    node = node.parent.parent
            if node == self.root:
                break
        self.root.color = L[0] # set root color to black

    def add(self, ride, min_heap):
        # add ride to tree
        new_node = RBTreeNode(ride, min_heap)
        new_node.parent = n
        new_node.left = self.nil 
        new_node.right = self.nil
        new_node.color = L[1] # red
        insert_point = n
        temp = self.root
        while temp != self.nil:
            insert_point = temp 
            if new_node.ride.ride_number < temp.ride.ride_number:
                temp = temp.left
            else:
                temp = temp.right
        new_node.parent = insert_point
        if insert_point is n: # tree is empty
            self.root = new_node
        elif new_node.ride.ride_number > insert_point.ride.ride_number:
            insert_point.right = new_node
        else:
            insert_point.left = new_node
        if new_node.parent is n: # new node is root
            new_node.color = L[0]
            return
        if new_node.parent.parent is n: # new node's parent is root
            return
        self._rebalance_post_insert(new_node) # balanced tree

    def rides_in_range(self, low, high):
        # return rides in range
        result_list = []
        self._locate_rides_in_range(self.root, low, high, result_list)
        return result_list
