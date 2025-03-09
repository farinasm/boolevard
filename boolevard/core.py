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
        '''
        self._bnet = open(file_path, "r").read().splitlines()   
        self.Info = self._ModelInfo(file_path)
        self.Nodes = list(self.Info.index)
        self.DNFs = dict(zip(self.Nodes, self.Info["DNF"]))
        self.NDNFs = dict(zip(self.Nodes, self.Info["NDNF"]))
        self.SS = self.Info.drop(["DNF", "NDNF"], axis = 1)
        self._IsPert = any(line.startswith("# Perturbed") for line in self._bnet)
        self._Pert = [line.split(":")[1].strip() for line in self._bnet if line.startswith("# Perturbed")]

    def __repr__(self):
        '''
        Returns the representation of the BooLEV object
        '''
        return f"<BooLEV object at {hex(id(self))}>"
    
    # Internal functions
    def _ModelInfo(self, file_path:str):
        '''
        Retrieves the information of the model, including nodes, cDNFs and cNDNFs, and stable states.
        '''
        content = self._bnet
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
        """
        Exports the model in .bnet format.

        Parameters
        **********
        file_path: str
            Path to export the model.

        Returns:
        ********
        BooLEV: object
            The BooLEV object.
        
        Example:
        ********
        >>> model = blv.Load("model.bnet")
        >>> model.Export("model.bnet")
        """

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
        """
        Extracts drivers from (N)DNFs based on the local state of the node within a given stable state.
        
        Parameters:
        ********
        ss: int 
            Stable State to evaluate.

        Returns:
        ********
        dict
            Dictionary containing de drivers of each node within the stable state.

        Example:
        ********
        >>> model = blv.Load("model.bnet")
        >>> model.Drivers(1) # Compute the drivers for each node within the stable state number 1
        """
        return Drivers(self.Info, ss)

    def CountPaths(self, tNodes:list, ss_wise = False):
        """
        Calculates the signed path count leading to the local state of a node contained in a list. Positive if the local state is 1 and negative if 0.
        
        Parameters:
        **********
        tNodes: list
            List of target nodes to evaluate.
        ss_wise: bool
            If True, returns a list with the corresponding path counts leading to a target's local state for each stable state. Otherwise, it computes the average path count across all stable states contained in the Info attribute of the BooLEV object. By default: False.

        Returns:
        **********
        list
            Signed number of paths leading to the local states of the target nodes. Negative if the local state is 0, positive if 1.
        
        Example:
        **********
        >>> model = blv.Load("model.bnet")
        >>> model.CountPaths(["Node1", "Node2"], ss_wise = False)
        """
        return CountPaths(self.Info, tNodes, ss_wise)
    
    def Pert(self, perturbation:str, additive = True):
        """
        Perturbs the model by creating a perturbation node that targets a specific node in the model, simulating a positive (ACT) or negative (INH) effect in the target.
        
        Parameters:
        ********
        tNodes: list
            List of target nodes to evaluate.
        perturbation: str
            String containing the target node and the perturbation type separated by a percentage symbol. E.g. `"Node%ACT"`, `"Node%INH"`.
        additive: bool
            If True, the perturbation is additive (i.e. the regulation is incorporated to the target node's rule). Otherwise, the perturbation is substitutive (i.e. the regulation replaces the target node's rule). By default: True.

        Returns:
        ********
        BooLEV object
            Model (BooLEV object) updated with the perturbation.
        
        Example:
        ********
        >>> model = blv.Load("model.bnet")
        >>> model.Pert("Node%ACT", additive = True)
        >>> model.Pert("Node%INH", additive = False)
        """
        return Pert(self, perturbation, additive)
    

def Load(file_path:str):
    """
    Loads a model in ``b.net`` format and returns a BooLEV-class object.

    This function loads a Boolean model from a `.bnet` file and returns a 
    `BooLEV` object containing the model's structure and associated data.

    Parameters:
    **********
    file_path : str
        Path to the ``.bnet`` file.

    Returns:
    **********
    BooLEV: object
        A `BooLEV` object containing the model with the following attributes:
        
        - `Nodes` (list): List containing the nodes of the model.
        - `DNFs` (dict): Dictionary with the canonical Disjunctive Normal Form (cDNF) of each node.
        - `NDNFs` (dict): Dictionary with the cDNF of the negated rule of each node.
        - `SS` (pd.DataFrame): DataFrame containing the stable states.
        - `Info` (pd.DataFrame): DataFrame containing the stable states, cDNFs, and cNDNFs.

    Example:
    **********
    >>> model = blv.Load("model.bnet")
    """
    return BooLEV(file_path)