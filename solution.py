# use a dictionary to store all keys and corresponding node (contains value)
# the most recent used key is on the most right of double linked list
# {1: node(key=1, val=1, prev=None, next=2), 2: node(key=2, val=2, prev=1, next=None)}, key in node is the key of dictionary 
# head -> 1 -> 2 -> tail
class LRUCache(object):
    class Node: # double linked list node
        def __init__(self, key, val):
            self.key = key
            self.val = val
            self.prev = None
            self.next = None

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.head = self.Node(0, 0) # head of the double linked list, dummy head
        self.tail = self.Node(0, 0) # tail of the double linked list, dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head
        self.capacity = capacity
        self.hashmap = {}  
    
    def add_head_next(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next = node
        node.next.prev = node
        
    def delete_tail_prev(self):
        remove_node = self.tail.prev
        self.tail.prev = self.tail.prev.prev
        self.tail.prev.next = self.tail
        remove_node.next = None
        remove_node.prev = None
        # remove deleted node key in hashmap
        del self.hashmap[remove_node.key]
        del remove_node
        
    def move_to_dummy_head_next(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node 
        self.head.next = node
        
    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        if key not in self.hashmap:
            return -1
        node = self.hashmap[key] # found this key
        if node != self.head.next: # not dummy head next
            self.move_to_dummy_head_next(node)
        return node.val

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: None
        """
        # if key exists
        if key in self.hashmap:
            curr_node = self.hashmap[key]
            curr_node.val = value # update value
            if curr_node.prev: # not head
                self.move_to_dummy_head_next(curr_node)
        else:
            new_node = self.Node(key, value) # create new node, and move it to head of linked list
            self.hashmap[key] = new_node # add key to hashmap
            # if capacity is full
            if len(self.hashmap) > self.capacity:
                # delete tail node (least recently used)
                self.delete_tail_prev()  
            self.add_head_next(new_node)
