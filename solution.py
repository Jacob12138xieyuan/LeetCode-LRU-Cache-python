# use a dictionary to store all keys and corresponding node (contains value)
# the most recent used key is on the most right of double linked list
# {1: node(key=1, val=1, prev=None, next=2), 2: node(key=2, val=2, prev=1, next=None)}, key in node is the key of dictionary 
class LRUCache(object):
    class Node: # double linked list
        def __init__(self, key, val):
            self.key = key
            self.val = val
            self.prev = None
            self.next = None

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.head = self.Node(-1, -1) # head of the double linked list
        self.tail = self.head # copy head as tail
        self.hashmap = {}
        self.available = capacity

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        if key not in self.hashmap:
            return -1
        curr_node = self.hashmap[key] # found this key, return the value and move it to most right of linked list
        if curr_node.next:
            curr_node.prev.next = curr_node.next
            curr_node.next.prev = curr_node.prev
            self.tail.next = curr_node
            curr_node.prev = self.tail # move it after tail
            curr_node.next = None
            self.tail = curr_node # make it as new tail
        
        return curr_node.val

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: None
        """
        # if key exists
        if key in self.hashmap:
            curr_node = self.hashmap[key] # found this key, update the value and move it to most right of linked list
            curr_node.val = value
            
            if curr_node.next:
                curr_node.prev.next = curr_node.next
                curr_node.next.prev = curr_node.prev
                self.tail.next = curr_node
                curr_node.prev = self.tail # move it after tail
                curr_node.next = None
                self.tail = curr_node # make it as new tail
        
        # key does't exist
        else:
            new_node = self.Node(key, value) # create new node, and move it to most right of linked list
            self.hashmap[key] = new_node # add key to hashmap
            # capacity is full
            if self.available <= 0:
                # delete most left node (least recently used)
                remove_node = self.head.next
                if self.head.next.next:
                    self.head.next = self.head.next.next
                    self.head.next.prev = self.head
                    # remove deleted node key in hashmap
                del self.hashmap[remove_node.key]
           
            # add new_node after tail
            self.tail.next = new_node
            new_node.prev = self.tail
            new_node.next = None
            self.tail = new_node
            self.available-=1
