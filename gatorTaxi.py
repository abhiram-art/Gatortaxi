import sys
from minHeap import MinHeap
from minHeap import MinHeapNode
from rbTree import RBTree 
from rbTree import RBTreeNode

class Ride:
    def __init__(self, ride_number, rideCost, tripDuration):
        #  ride_number: unique number for each ride
        self.ride_number = ride_number
        self.rideCost = rideCost
        self.tripDuration = tripDuration

    def is_less_than(self, other_ride):
        # compare two rides
        if self.rideCost < other_ride.rideCost:
            return True
        elif self.rideCost == other_ride.rideCost:
            if self.tripDuration > other_ride.tripDuration:
                return False
            else:
                return True
        elif self.rideCost > other_ride.rideCost:
            return False

def cancel(ride_number, heap, rbtree):
    # remove ride from heap and rbtree
    heap_node = rbtree.remove(ride_number)
    if heap_node is not None:
        heap.remove_element(heap_node.min_heap_index)

def insert(ride, heap, rbtree):
    # insert ride into heapa and rbtree
    if rbtree.search_key(ride.ride_number) is not None:
        add_out(None, "Duplicate RideNumber", False)
        sys.exit(0)
    rbtree_node = RBTreeNode(None, None)
    min_heap_node = MinHeapNode(ride, rbtree_node, heap.heap_size + 1)
    heap.add(min_heap_node)
    rbtree.add(ride, min_heap_node)

def update(ride_number, new_duration, heap, rbtree):
    # update ride in heap and rbtree
    rbtree_node = rbtree.search_key(ride_number)
    if rbtree_node is None:
        print("")
    elif new_duration <= rbtree_node.ride.tripDuration:
        heap.modify_element(rbtree_node.min_heap_node.min_heap_index, new_duration)
    elif rbtree_node.ride.tripDuration < new_duration <= (2 * rbtree_node.ride.tripDuration):
        cancel(rbtree_node.ride.ride_number, heap, rbtree)
        insert(Ride(rbtree_node.ride.ride_number, rbtree_node.ride.rideCost + 10, new_duration), heap, rbtree)
    else:
        cancel(rbtree_node.ride.ride_number, heap, rbtree)

def add_out(ride, msg, list):
    # write output to file
    with open("output_file.txt", "a") as f:
        if ride is None:
            f.write(f"{msg}\n")
        else:
            if not list:
                f.write(f"({ride.ride_number},{ride.rideCost},{ride.tripDuration})\n")
            else:
                if not ride:
                    f.write("(0,0,0)\n")
                else:
                    ride_str = ','.join(f"({r.ride_number},{r.rideCost},{r.tripDuration})"
                                        for r in ride)
                    f.write(f"{ride_str}\n")

def nxt_ride(heap, rbtree):
    # get next ride from heap and rbtree
    if heap.heap_size != 0:
        popped_node = heap.extract_min()
        rbtree.remove(popped_node.ride.ride_number)
        add_out(popped_node.ride, "", False)
    else:
        add_out(None, "No active ride requests", False)

def ride_out(ride_number, rbtree):
    # get ride from rbtree
    res = rbtree.search_key(ride_number)
    add_out(res.ride if res else Ride(0, 0, 0), "", False)


def rides_out(l, h, rbtree):
    # get rides from rbtree
    rides_list = rbtree.rides_in_range(l, h)
    add_out(rides_list, "", True)

def parse_numbers(s):
    return [int(num) for num in s[s.index("(") + 1:s.index(")")].split(",") if num != '']

heap = MinHeap()
rbtree = RBTree()

with open("output_file.txt", "w"):
    pass

if len(sys.argv) < 2:
    print("Usage: python3 gatorTaxi.py abhiram_input.txt")
    sys.exit(1)

fname = sys.argv[1]

# read input file and call appropriate function
with open(fname, "r") as f:
    for s in f.readlines():
        n = parse_numbers(s)
        if "Insert" in s:
            insert(Ride(n[0], n[1], n[2]), heap, rbtree)
        elif "Print" in s:
            ride_out(n[0], rbtree) if len(n) == 1 else rides_out(n[0], n[1], rbtree)
        elif "UpdateTrip" in s:
            update(n[0], n[1], heap, rbtree)
        elif "GetNextRide" in s:
            nxt_ride(heap, rbtree)
        elif "CancelRide" in s:
            cancel(n[0], heap, rbtree)