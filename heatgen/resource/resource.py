__author__ = 'baohua'
import json

class Resource(object):
    """
    The basic class of a resource

    >>> print Resource("001","OS::TEST::TEST",name="example").get_json()
    {"001": {"Type": "OS::TEST::TEST", "Properties": {"name": "example"}}}
    """

    def __init__(self,id,type, **kwargs):
        self.id = id
        self.type = type
        self.properties = kwargs

    def get(self):
        '''
        :return: Get a dict of id:{} format of the resource
        '''
        result = {}
        result[self.id] = {
            "Type": self.type,
            "Properties": self.properties,
        }
        return result

    def get_json(self):
        return json.dumps(self.get())


class Resources(object):
    """
    The basic class of a resource

    >>> print Resource("001","OS::TEST::TEST",name="example").get_json()
    {"001": {"Type": "OS::TEST::TEST", "Properties": {"name": "example"}}}
    """
    def __init__(self, *args): #given several resource units
        self.data = {}
        for arg in args:
            self.data.update(arg)

    def get(self):
        return {"Resources" : self.data}

    def get_json(self):
        return json.dumps(self.get())


if __name__ == "__main__":
    import doctest
    doctest.testmod()
