import mpbn
import os
import pandas as pd
from pyeda import *
from pyeda.inter import *
from colomoto_jupyter import tabulate
from boolevard.utils import *
from boolevard.transduction import *
from boolevard.perturbations import *

class BooLEV:

    def __init__(self, file_path):
        self.bnet = open(file_path, "r").read().splitlines()   
        self.Info = self._ModelInfo(file_path)
        self.Nodes = list(self.Info.index)
        self.DNFs = dict(zip(self.Nodes, self.Info["DNF"]))
        self.NDNFs = dict(zip(self.Nodes, self.Info["NDNF"]))
        self.SS = self.Info.drop(["DNF", "NDNF"], axis = 1)
        self.IsPert = False

    def __repr__(self):
        return f"<BooLEV object at {hex(id(self))}>"
    
    # Internal functions
    def _ModelInfo(self, file_path):
        content = self.bnet
        nodes = []
        DNFs = []
        NDNFs = []

        for line in content:
            if "#" not in line and "targets" not in line and "target" not in line: 
                node, rule = line.split(",")
                nodes.append(node)
                DNFs.append(expr(rule.replace(" ", "").replace("!", "~")).to_dnf())
                NDNFs.append(ExprNot(expr(rule.replace(" ", "").replace("!", "~"))).to_dnf())
        
        model = mpbn.load(file_path)
        SS = tabulate(list(model.attractors()))
        info = pd.concat([SS.transpose(), pd.DataFrame({"DNF": DNFs, "NDNF": NDNFs}, index = nodes)], axis = 1)
        info = info.loc[:, ~(info == "*").any()]
        return info
    
    # Methods
    def Export(self, file_path):
        '''
        Exports the model in .bnet format
        '''

        with open(file_path, "w") as f:
            f.write("targets, factors\n")

            for line, (target, factor) in enumerate(zip(self.Nodes, self.Info["DNF"])):
                factor = factor.to_unicode()
                factor = re_notation.sub(lambda x: "!" + x.group(1), factor).replace("+", "|").replace("·", "&").replace("¬", "!")
                if line < len(self.Nodes) - 1:
                    f.write(f"{target}, {factor}\n")

                else:
                    f.write(f"{target}, {factor}")
    
    def Drivers(self, ss):
        return Drivers(self.Info, ss)

    def CountPaths(self, tNodes, ss_wise = False):
        return CountPaths(self.Info, tNodes, ss_wise)
    
    def Pert(self, perturbation, additive = True):
        return Pert(self, perturbation, additive)
    

def load(file_path):
    '''
    Loads the model and returns a BooLEV-class object
    '''
    return BooLEV(file_path)