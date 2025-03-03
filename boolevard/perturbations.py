import copy
import mpbn
from colomoto_jupyter import tabulate

def pert(model, perturbation, additive = True):
    '''
    Perturb the model by creating a perturbation node that
    targets a specific node in the model, simulating a positive (ACT)
    or negative (INH) effect in the target.
    '''
    pert_model = copy.deepcopy(model)
    content = model.content.splitlines()
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
    new_content.append("targets, factors")

    for idx, (target, factor) in enumerate(new_rules.items()):
        new_content.append(f"{target}, {factor}")

    pert_model.content = "\n".join(new_content)
    pert_model.file_path = model.file_path.replace(".bnet", "_pert_{tnode}_{pertType}.bnet")
    pert_model_mpbn = mpbn.MPBooleanNetwork(new_rules)
    pert_model.stable_states = tabulate(list(pert_model_mpbn.attractors()))
    pert_model.info = pert_model.ModelInfo()
    pert_model.info = pert_model.info.loc[:, (pert_model.info.loc[[pnode]] == 1).all(axis = 0) | pert_model.info.columns.str.contains("DNF")]

    return pert_model