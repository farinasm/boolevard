import copy
import mpbn
import pandas as pd
import pyeda
from pyeda.inter import *
from colomoto_jupyter import tabulate
from boolevard.utils import *

def Pert(model, perturbation, additive = True):
    '''
    Perturb the model by creating a perturbation node that
    targets a specific node in the model, simulating a positive (ACT)
    or negative (INH) effect in the target.
    '''
    pert_model = copy.copy(model)
    content = pert_model.bnet
    rules = {}

    for line in content:
        if "#" not in line and "targets" not in line and "target" not in line:
            node, rule = line.split(", ", 1)
            rules[node] = rule
    
    tnode, pertType = perturbation.split("%")
    new_rules = rules.copy()

    if additive:

        if pertType == "INH":
            new_rules[tnode] = "(" + new_rules[tnode] + ")" + " & !" + tnode + "_" + pertType

        elif pertType == "ACT":
            new_rules[tnode] = "(" + new_rules[tnode] + ")" + " | " + tnode + "_" + pertType
    
    else:

        if pertType == "INH":
            new_rules[tnode] = new_rules[tnode] = "!" + tnode + "_" + pertType

        elif pertType == "ACT":
            new_rules[tnode] = new_rules[tnode] = tnode + "_" + pertType

    pnode = tnode + "_" + pertType
    new_rules[pnode] = pnode
    new_content = []

    new_content.append(f"# Perturbation: {perturbation}")
    new_content.append("targets, factors")

    for idx, (target, factor) in enumerate(new_rules.items()):
        new_content.append(f"{target}, {factor}")

    pert_model.bnet = "\n".join(new_content)
    pert_model.Nodes = list(new_rules.keys())
    pert_model.DNFs = dict(zip(pert_model.Nodes, [expr(rule.replace(" ", "").replace("!", "~")).to_dnf() for rule in new_rules.values()]))
    pert_model.NDNFs = dict(zip(pert_model.Nodes, [ExprNot(expr(rule.replace(" ", "").replace("!", "~"))).to_dnf() for rule in new_rules.values()]))
    pert_model._IsPert = any(line.startswith("# Perturbed") for line in pert_model.bnet)
    pert_model._Pert = [line.split(":")[1].strip() for line in pert_model.bnet if line.startswith("# Perturbed")]
    
    mpbn_model = mpbn.MPBooleanNetwork(new_rules)
    pert_model.SS = tabulate(list(mpbn_model.attractors()))
    pert_model.Info = pd.concat([pert_model.SS.transpose(), pd.DataFrame({"DNF": pert_model.DNFs, "NDNF": pert_model.NDNFs}, index = pert_model.Nodes)], axis = 1) 
    pert_model.Info = pert_model.Info.loc[:, ~(pert_model.Info == "*").any()]
    pert_model.Info = pert_model.Info.loc[:, (pert_model.Info.loc[[pnode]] == 1).all(axis = 0) | pert_model.Info.columns.str.contains("DNF")]
    
    return pert_model