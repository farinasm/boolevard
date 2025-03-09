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

    def __init__(self, file_path:str):
        '''
        Initialites the BooLEV object by loading the model from a .bnet file.
        @param file_path: path to the .bnet file.
        '''
        self.bnet = open(file_path, "r").read().splitlines()   
        self.Info = self._ModelInfo(file_path)
        self.Nodes = list(self.Info.index)
        self.DNFs = dict(zip(self.Nodes, self.Info["DNF"]))
        self.NDNFs = dict(zip(self.Nodes, self.Info["NDNF"]))
        self.SS = self.Info.drop(["DNF", "NDNF"], axis = 1)
        self._IsPert = any(line.startswith("# Perturbed") for line in self.bnet)
        self._Pert = [line.split(":")[1].strip() for line in self.bnet if line.startswith("# Perturbed")]

    def __repr__(self):
        '''
        Returns the representation of the BooLEV object
        '''
        return f"<BooLEV object at {hex(id(self))}>"
    
    # Internal functions
    def _ModelInfo(self, file_path:str):
        '''
        Retrieves the information of the model, including nodes, cDNFs and cNDNFs, and stable states.
        @param file_path: path to the .bnet file.
        '''
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
    def Export(self, file_path:str):
        '''
        Exports the model in .bnet format.
        @param file_path: path to export the model in .bnet format.
        '''

        with open(file_path, "w") as f:
            
            if self._IsPert == True:
                f.write(f"# Perturbed model with {self._Pert} perturbation(s)\n")
            
            f.write("targets, factors\n")

            for line, (target, factor) in enumerate(zip(self.Nodes, self.Info["DNF"])):
                factor = factor.to_unicode()
                factor = re_notation.sub(lambda x: "!" + x.group(1), factor).replace("+", "|").replace("·", "&").replace("¬", "!")
                if line < len(self.Nodes) - 1:
                    f.write(f"{target}, {factor}\n")

                else:
                    f.write(f"{target}, {factor}")
        return self
    
    def Drivers(self, ss: int):
        '''
        Extracts drivers from (N)DNFs based on the local state of the node within a given stable state.
        @param ss: Stable State to evaluate.
        '''
        return Drivers(self.Info, ss)

    def CountPaths(self, tNodes:list, ss_wise = False):
        '''
        Calculates the signed path count leading to the local state of a node contained in a list. Positive if the local state is 1 and negative if 0.
        @param: tNodes: list of target nodes to evaluate.
        @param: ss_wise: if True, returns a list with the corresponding path counts leading to a target's local state for each stable state. Otherwise, it computes the average path count across all stable states contained in the Info attribute of the BooLEV object. By default: False.
        '''
        return CountPaths(self.Info, tNodes, ss_wise)
    
    def Pert(self, perturbation:str, additive = True):
        '''
        Perturb the model by creating a perturbation node that targets a specific node in the model, simulating a positive (ACT) or negative (INH) effect in the target.
        @param model: BooLEV object.
        @param perturbation: string containing the target node and the perturbation type separated by a percentage symbol. E.g. "Node%ACT", "Node%INH".
        @param additive: if True, the perturbation is additive (i.e. the regulation is incorporated to the target node's rule). Otherwise, the perturbation is substitutive (i.e. the regulation replaces the target node's rule). By default: True
        '''
        return Pert(self, perturbation, additive)
    

def Load(file_path:str):
    '''
    Loads the model and returns a BooLEV-class object
    '''
    return BooLEV(file_path)