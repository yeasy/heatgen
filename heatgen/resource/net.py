__author__ = 'baohua'

from heatgen.resource.resource import Resource

class Net(Resource):
    """
    The class for a net, which can be the endpoint of a service chain

    >>> print Net("a").get_json()
    {"a": {"Type": "OS::Quantum::Net", "Properties": {"name": "a"}}}
    """

    def __init__(self, id, type="OS::Quantum::Net", name=None):
        super(Net, self).__init__(id,type,name=name or id)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
