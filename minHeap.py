class MinHeapNode:
    def __init__(self, ride, rbt, min_heap_index):
        self.ride = ride # ride object
        self.rbTree = rbt # rbTree object
        self.min_heap_index = min_heap_index # index of the node in the min heap
        

class MinHeap:
    def __init__(self):
        self.heap_array = [0] # index 0 is not used
        self.heap_size = 0 # number of elements in the heap

    def _swap_elements(self, index1, index2):
        # swap the elements
        self.heap_array[index1], self.heap_array[index2] = self.heap_array[index2], self.heap_array[index1] 
        self.heap_array[index1].min_heap_index, self.heap_array[index2].min_heap_index = index1, index2 

    def _bubble_up(self, pos):
        #heapify up
        while pos // 2 > 0:
            parent_pos = pos // 2
            if self.heap_array[pos].ride.is_less_than(self.heap_array[parent_pos].ride):  # if the element is less than its parent
                self._swap_elements(pos, parent_pos)
            else:
                break
            pos = parent_pos

    def _find_min_child(self, pos):
        left_child_pos = pos * 2
        right_child_pos = left_child_pos + 1

        if right_child_pos > self.heap_size:  # if the element has only one child
            return left_child_pos  # return the index of the left child
        elif self.heap_array[left_child_pos].ride.is_less_than(self.heap_array[right_child_pos].ride):
            return left_child_pos
        else:
            return right_child_pos

    def _bubble_down(self, pos):
        # heapify down
        left_child_pos = 2 * pos
        right_child_pos = 2 * pos + 1
        min_child_pos = pos
        # if the element has a left child and it is less than the element
        if left_child_pos <= self.heap_size and self.heap_array[left_child_pos].ride.is_less_than(self.heap_array[min_child_pos].ride): 
            min_child_pos = left_child_pos
        
        # if the element has a right child and it is less than the element
        if right_child_pos <= self.heap_size and self.heap_array[right_child_pos].ride.is_less_than(self.heap_array[min_child_pos].ride):   
            min_child_pos = right_child_pos
        
        # if the element is not the minimum element
        if min_child_pos != pos:
            self._swap_elements(pos, min_child_pos)
            self._bubble_down(min_child_pos)


    def modify_element(self, pos, updated_key):
        node = self.heap_array[pos]  # get the node
        node.ride.tripDuration = updated_key  # update the key

        parent_pos = pos // 2
        if pos == 1 or self.heap_array[parent_pos].ride.is_less_than(self.heap_array[pos].ride):  # if the element is the root or greater than its parent
            self._bubble_down(pos)
        else:
            self._bubble_up(pos)

    def add(self, element):
        self.heap_array.append(element)  # add the element to the end of the array
        self.heap_size += 1  # increment the heap size
        self._bubble_up(self.heap_size)  # bubble up the element to its correct position

    def extract_min(self):
        if len(self.heap_array) == 1: # if the heap is empty
            return 'No Rides Available'
        min_val = self.heap_array[1] # get the minimum element
        self._swap_elements(1, self.heap_size) 
        self.heap_size -= 1 
        self.heap_array.pop() # remove the last element
        self._bubble_down(1) 
        return min_val # return the minimum element
    
    def remove_element(self, pos):
        self._swap_elements(pos, self.heap_size) 
        self.heap_size -= 1
        self.heap_array.pop() # remove the last element
        self._bubble_down(pos) # bubble down the element to its correct position