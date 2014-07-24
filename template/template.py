__author__ = 'baohua'

import  json


class Template(object):
    """
    Seed :The basic class for different abstract templates
    """

    def __init__(self, version="0.1",desc="Example",resources={}, export_file="test_export.json"):
        self.version = version
        self.desc = desc
        self.resources = resources #list of the resource objects
        self.export_file = export_file

    def get(self):
        res_dict = {}
        for e in self.resources:
            res_dict.update(e.get())
            print e.get()
        self.data = {
            "HeatTemplateFormatVersion": self.version,
            "Description": self.desc,
            "Resources": res_dict
        }
        return self.data

    def get_json(self):
        return json.dumps(self.get())

    def export(self):
        '''
        Export the template into outside json file.
        :return:
        '''
        with open(self.export_file,'w') as f:
            json.dump(self.get(), f, indent=4)

