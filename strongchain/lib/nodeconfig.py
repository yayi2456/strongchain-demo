import json

'''
Define NodeConf class, which store the address:port and vk of a running node.
'''
class NodeConf:
    def __init__(self, port, address, vk):
        '''
        initialize a NodeConf object
        '''
        # port: in which port the node is runing
        # address: in which address the node is runing (localhost)
        # vk: verify key that is used to verify a ecdsa signature.
        self.port = port
        self.address = address
        self.vk = vk


    def __eq__(self, other):
        '''
        Return True if all 3 fields equal
        '''
        return self.port == other.port \
            and self.address == other.address \
            and self.vk == other.vk


    @classmethod
    def from_json_str(cls, json_string):
        '''
        Return a NodeConf object composed by values proveided by json_string
        '''
        j = json.loads(json_string)
        return cls(j.get("port"), j.get("address"), j.get("vk"))


    def to_json(self):
        '''
        Return a dict composed by 3 fields of a NodeConf object
        '''
        return {
            "port" : self.port,
            "address" : self.address,
            "vk" : self.vk
        }


    def to_json_str(self, indent = 4):
        '''
        Return a json_string with 4 idents(行缩进) composed by 3 fields of a NodeConf object
        '''
        return json.dumps(self.to_json(), indent = indent)


    def __str__(self):
        '''
        Return a json_string with no idents composed by 3 fields of a NodeConf object
        '''
        return self.to_json_str(indent = None)
