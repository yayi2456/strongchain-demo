import hashlib


class MerkleTree:
    def __init__(self, leaves_list):
        '''
        Construct a new Merkle tree using leaves_list, which is a list of transactions.
        '''
        self.nodes = []# leaves node of the tree,hash
        self.tree = []# list of list of hash
        self.proof_path = []
        for leave in leaves_list:
            self.nodes.append(single_hash(leave))
        # get the level 0 hash nodes
        self.tree.append(self.nodes)
        # build the merkle tree
        self.build(self.nodes)
        # get root
        self.root = self.get_root()

    @classmethod
    def compute_root(cls, leaves):
        '''
        Return merklr Tree root of leaves.
        '''
        tree = cls(leaves)
        return tree.root

    def add(self, new_leave):
        '''
        Add a new leaf to self
        '''
        # Add entries to tree
        self.nodes.append(single_hash(new_leave))
        self.tree = []
        # store the lowest level of hash
        self.tree.append(self.nodes)
        # rebuild and reget root
        self.build(self.nodes)
        self.root = self.get_root()

    def build(self, start_list):
        '''
        Recrusivly build a merkle tree.
        Return root.
        '''
        # Build tree computing new root

        # no node: empty tree. Return 64*'0'
        if 0 == len(start_list):
            return '0' * 64

        end_list = []
        # if there are more than 1 node in this level
        if len(start_list) > 1:
            # if node numbers are even
            if len(start_list) % 2 == 0:
                # double hash
                for i in range(0, len(start_list), 2):
                    end_list.append(double_hash(start_list[i], start_list[i + 1]))
            else:
                for i in range(0, len(start_list) - 1, 2):
                    end_list.append(double_hash(start_list[i], start_list[i + 1]))
                # append the last hash indepently, without hashing again.
                end_list.append(start_list[-1])
            # get the upper level nodes.
            self.tree.append(end_list)
            # build the upper level nodes: recrusivly.
            return self.build(end_list)
        # the root got
        else:
            if len(self.tree) == 0:
                end_list.append(start_list[0])
                self.tree.append(end_list)
                return start_list[0]

    def get_proof(self, entry):
        '''
        Return the proof of entry, which is a int and starts at 0.
        '''
        self.proof_path = []
        if int(entry) > len(self.nodes) - 1:
            return []

        else:
            next_entry = entry
            for i in range(0, len(self.tree) - 1):
                # more than 1 node in level i
                if len(self.tree[i]) != 1:
                    # next_entry is even: next_enrty is at the left side of every 2 nodes.
                    if int(next_entry) % 2 == 0:
                        # next_entry is not the last one: even numbers of nodes in this level.
                        if int(next_entry) != len(self.tree[i]) - 1:
                            # get the right-side node of next_entry, labelled as 'r'
                            # if next_entry is the single one, no proof is added in this level.
                            self.proof_path.append([self.tree[i][int(next_entry) + 1], 'r'])
                    # next_entry is odd: next_enrty is at the right side of every 2 nodes.
                    else:
                        # get the leftside node of next_entry
                        self.proof_path.append([self.tree[i][int(next_entry) - 1], 'l'])
                # set next_entry to its parent node
                next_entry = get_next_entry(next_entry)
            return self.proof_path

    def get_root(self):
        '''
        Return merkle root of self.
        '''

        # Return the current root
        if 0 == len(self.tree[-1]):
            return '0' * 64

        return str(self.tree[-1][0])


def single_hash(value):
    '''
    Return hash of one value
    '''

    if not isinstance(value, str):
        value = str(value)

    return hashlib.sha256(value.encode()).hexdigest()


def double_hash(node1, node2):
    '''
    Return hash of node1||node2
    '''
    return hashlib.sha256((node1 + node2).encode()).hexdigest()


def get_next_entry(value):
    '''
    Return parent node index of node whose index=value
    '''
    if value <= 1:
        return 0
    else:
        if value % 2 == 0:
            return int(value / 2)
        else:
            return int((value - 1) / 2)


def verify_proof(entry, proof, root):
    '''
    Verify proof and Return verify results.
    '''
    test_val = single_hash(entry)
    for i in range(0, len(proof)):
        if proof[i][1] == 'l':
            test_val = double_hash(proof[i][0], test_val)
        else:
            test_val = double_hash(test_val, proof[i][0])
    return test_val == root
