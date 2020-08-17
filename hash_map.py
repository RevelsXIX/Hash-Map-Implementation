# Joshua Revels
# CS 261
# Portfolio Project
# hash-map.py


class SLNode:
    def __init__(self, key, value):
        self.next = None
        self.key = key
        self.value = value

    def __str__(self):
        return '(' + str(self.key) + ', ' + str(self.value) + ')'


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add_front(self, key, value):
        """Create a new node and inserts it at the front of the linked list
        Args:
            key: the key for the new node
            value: the value for the new node"""
        new_node = SLNode(key, value)
        new_node.next = self.head
        self.head = new_node
        self.size = self.size + 1

    def remove(self, key):
        """Removes node from linked list
        Args:
            key: key of the node to remove """
        if self.head is None:
            return False
        if self.head.key == key:
            self.head = self.head.next
            self.size = self.size - 1
            return True
        cur = self.head.next
        prev = self.head
        while cur is not None:
            if cur.key == key:
                prev.next = cur.next
                self.size = self.size - 1
                return True
            prev = cur
            cur = cur.next
        return False

    def contains(self, key):
        """Searches linked list for a node with a given key
        Args:
        	key: key of node
        Return:
        	node with matching key, otherwise None"""
        if self.head is not None:
            cur = self.head
            while cur is not None:
                if cur.key == key:
                    return cur
                cur = cur.next
        return None

    def __str__(self):
        out = '['
        if self.head != None:
            cur = self.head
            out = out + str(self.head)
            cur = cur.next
            while cur != None:
                out = out + ' -> ' + str(cur)
                cur = cur.next
        out = out + ']'
        return out


def hash_function_1(key):
    hash = 0
    for i in key:
        hash = hash + ord(i)
    return hash


def hash_function_2(key):
    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


class HashMap:
    """
    Creates a new hash map with the specified number of buckets.
    Args:
        capacity: the total number of buckets to be created in the hash table
        function: the hash function to use for hashing values
    """

    def __init__(self, capacity, function):
        self._buckets = []
        for i in range(capacity):
            self._buckets.append(LinkedList())
        self.capacity = capacity
        self._hash_function = function
        self.size = 0

    def clear(self):
        """
        Empties out the hash table deleting all links in the hash table.
        """
        capacity = self.capacity
        self._buckets = []
        for i in range(capacity):
            self._buckets.append(LinkedList())
        self.size = 0

    def get(self, key):
        """
        Returns the value with the given key.
        Args:
            key: the value of the key to look for
        Return:
            The value associated to the key. None if the link isn't found.
        """

        # hash the number
        hashKey = self._hash_function(key)
        index = hashKey % len(self._buckets)

        # if bucket at the specified key is empty, return None
        # else, search the bucket at the specified key, if found return value, if not, return None
        if self._buckets[index].size == 0:
            return None
        else:
            hashList = self._buckets[index]
            bucketNode = hashList.head
            while bucketNode is not None:
                if key != bucketNode.key:
                    bucketNode = bucketNode.next
                else:
                    return bucketNode.value
            return None

    def resize_table(self, capacity):
        """
        Resizes the hash table to have a number of buckets equal to the given
        capacity. All links need to be rehashed in this function after resizing
        Args:
            capacity: the new number of buckets.
        """
        newHash = HashMap(capacity, hash_function_1)
        newHash.size = self.size

        # variables to keep track of index and how many nodes have been rehashed
        rehashed = 0
        index = 0

        # loop executes while there are still nodes to be rehashed. terminates when it rehashes them all
        while rehashed < self.size:
            if self._buckets[index].size == 0:
                index = index + 1
            else:
                tempList = self._buckets[index]
                tempLength = tempList.size
                tempNode = tempList.head
                x = 0
                # loop uses length of bucket/linked list to determine how long to execute
                while x < tempLength:
                    tempKey = tempNode.key
                    tempValue = tempNode.value

                    # finds value to be rehashed. rehashes it to new hash table.
                    newHash.put(tempKey, tempValue)
                    newHash.size = newHash.size - 1         # to offset the size adding function of 'put' function

                    tempNode = tempNode.next

                    rehashed = rehashed + 1
                    x = x + 1
                index = index + 1

        # sets all current table parameters to the new hash tables parameters
        self._buckets = newHash._buckets
        self.capacity = newHash.capacity
        self._hash_function = newHash._hash_function
        self.size = newHash.size

    def put(self, key, value):
        """
        Updates the given key-value pair in the hash table. If a link with the given
        key already exists, this will just update the value and skip traversing. Otherwise,
        it will create a new link with the given key and value and add it to the table
        bucket's linked list.

        Args:
            key: they key to use to has the entry
            value: the value associated with the entry
        """
        # finding hash key
        hashKey = self._hash_function(key)
        index = hashKey % len(self._buckets)

        # insert node into first slot if bucket is empty.
        # otherwise, iterate through the linked list to see if that value already exists
        # if it does, update the value
        # if it does not, insert node at head of linked list
        if self._buckets[index].size == 0:
            self._buckets[index].add_front(key, value)
            self.size = self.size + 1
        else:
            hashList = self._buckets[index]
            bucketNode = hashList.head

            while bucketNode is not None:
                if key != bucketNode.key:
                    bucketNode = bucketNode.next
                else:
                    bucketNode.value = value
                    return True

            hashList.add_front(key, value)
            self.size = self.size + 1

    def remove(self, key):
        """
        Removes and frees the link with the given key from the table. If no such link
        exists, this does nothing.

        Args:
            key: they key to search for and remove along with its value
        """
        # finding hash key
        hashKey = self._hash_function(key)
        index = hashKey % len(self._buckets)

        if self._buckets[index].size == 0:
            return False
        else:
            hashList = self._buckets[index]
            bucketNode = hashList.head
            if key == bucketNode.key:
                after = bucketNode.next
                hashList.head = after
                hashList.size = hashList.size - 1
                return True
            else:
                prevNode = bucketNode
                bucketNode = prevNode.next
                found = False
                while found is False:
                    if key != bucketNode.key:
                        if bucketNode.next:
                            bucketNode = bucketNode.next
                            prevNode = prevNode.next
                        else:
                            return False
                    else:
                        after = bucketNode.next
                        prevNode.next = after
                        hashList.size = hashList.size - 1
                        return True

    def contains_key(self, key):
        """
        Searches to see if a key exists within the hash table

        Returns:
            True if the key is found False otherwise

        """

        index = 0
        while index < self.capacity:
            if self._buckets[index].size == 0:
                index = index + 1
            else:
                hashList = self._buckets[index]
                bucketNode = hashList.head
                while bucketNode is not None:
                    if key != bucketNode.key:
                        bucketNode = bucketNode.next
                    else:
                        return True
                index = index + 1
        return False

    def empty_buckets(self):
        """
        Returns:
            The number of empty buckets in the table
        """
        emptyBuckets = self.capacity
        for bucket in self._buckets:
            if bucket.size != 0:
                emptyBuckets = emptyBuckets - 1
        return emptyBuckets

    def table_load(self):
        """
        Returns:
            the ratio of (number of links) / (number of buckets) in the table as a float.

        """
        buckets = self.capacity
        links = 0
        for bucket in self._buckets:
            if bucket.size != 0:
                index = 0
                while index < bucket.size:
                    links = links + 1
                    index = index + 1
        loadFactor = links / buckets
        return float(loadFactor)

    def top_word_helper(self):
        nodeArray = []
        index = 0
        while index < self.capacity:
            if self._buckets[index].size == 0:
                index = index + 1
            else:
                hashList = self._buckets[index]
                bucketNode = hashList.head
                while bucketNode is not None:
                    nodeArray.append(bucketNode)
                    bucketNode = bucketNode.next
                index = index + 1

        return nodeArray

    def __str__(self):
        """
        Prints all the links in each of the buckets in the table.
        """

        out = ""
        index = 0
        for bucket in self._buckets:
            out = out + str(index) + ': ' + str(bucket) + '\n'
            index = index + 1
        return out

