import mpbn
import os
import pandas as pd
from pyeda import *
from pyeda.inter import *
from colomoto_jupyter import tabulate


def load(file_path):
    '''
    Loads the model and returns a BooLEV-class object
    '''
    class BooLEV:

        def __init__(self, file_path):
            self.file_path = file_path
            self.content = self._read_file()
            self.stable_states = self._get_SS()
            self.info = self.ModelInfo()
        
        def _read_file(self):
            with open(self.file_path, "r") as f:
                return f.read()
        
        def _get_SS(self):
            model = mpbn.load(self.file_path)
            stable_states = tabulate(list(model.attractors()))
            return stable_states
        
        def ModelInfo(self):
            content = self.content.splitlines()
            nodes = []
            DNFs = []
            NDNFs = []
            for line in content:
                if "#" not in line and "targets" not in line and "target" not in line: 
                    node, rule = line.split(",")
                    nodes.append(node)
                    DNFs.append(expr(rule.replace(" ", "").replace("!", "~")).to_dnf())
                    NDNFs.append(ExprNot(expr(rule.replace(" ", "").replace("!", "~"))).to_dnf())
            
            SS = self.stable_states
            info = pd.concat([SS.transpose(), pd.DataFrame({"DNF": DNFs, "NDNF": NDNFs}, index = nodes)], axis = 1)
            del self.stable_states
            return info
        
    return BooLEV(file_path)