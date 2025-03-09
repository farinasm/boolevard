import time
import re
import itertools
import pandas as pd
from collections import Counter
from pyeda import *
from pyeda.inter import *
from boolevard.utils import *

completePaths = 0
stored_nodes = {}
drivers = {}

def Drivers(model_info, ss):
    '''
    Extracts drivers from (N)DNFs based on the local state of the node within a given stable state.
    
    Arguments
    ---------
    model_info (pd.DataFrame): Info attribute of the BooLEV object.
    ss (int): Stable State to evaluate.
    ---------

    Returns
    ---------
    dict
        Dictionary containing de drivers of each node within the stable state.
    ---------
    '''
    print(f"Evaluating Stable State: {ss}")

    data = pd.concat([model_info[[ss]], model_info[["DNF"]], model_info[["NDNF"]]], axis = 1)
    data_dict = {}

    for node in data.index:
        lsNode = data.loc[node, data.columns[0]]
        stable_state = data.iloc[:, 0]

        if lsNode == 1:
            ruleBlocks = re_notation.sub(lambda x: '~' + x.group(1), model_info.at[node, "DNF"].to_unicode()).replace("·", "&").replace(" ", "").split("+")
        
        else:
            ruleBlocks = re_notation.sub(lambda x: '~' + x.group(1), model_info.at[node, "NDNF"].to_unicode()).replace("·", "&").replace(" ", "").split("+")
        
        blockStates = [expr(re_replace_vars.sub(lambda x: str(stable_state[x.group()]), block)) for block in ruleBlocks]
        driver = "|".join(block for block, state in zip(ruleBlocks, blockStates) if state)
        data_dict[node] = {"state": data.loc[node, ss], "Driver": driver.replace('~','')}
    
    return data_dict
        
def CountPaths(model_info, tNodes, ss_wise = False):
    '''
    Calculates the signed path count leading to the local state of a node contained in a list. Positive if the local state is 1 and negative if 0.
    
    Arguments
    ---------
    model_info (pd.DataFrame): Info attribute of the BooLEV object.
    tNodes (list): list of target nodes to evaluate.
    ss_wise (bool): if True, returns a list with the corresponding path counts leading to a target's local state for each stable state. Otherwise, it computes the average path count across all stable states contained in the Info attribute of the BooLEV object. By default: False.
    ---------

    Returns
    ---------
    list
        Signed number of paths leading to the local states of the target nodes. Negative if the local state is 0, positive if 1.
    ---------
    '''

    # Functions:
    def _LinearPaths(tNode):
        '''
        Calls resolvePaths and asigns a positive sign if the local state of the target node is 1, negative if 0.
        '''
        _ResolvePaths([tNode], True)

        return completePaths if drivers[tNode]["state"] == 1 else -completePaths
    

    def _ResolvePaths(path:list, save):
        '''
        Construct paths leading to the target's node local state and add them to a counter.
        '''
        global completePaths

        path_found_or = False
        blocks = _ExtractNodes(path[-1])
        store_local = {}

        for block in blocks:
            go, path_found_and = _FilterLoops(path, block)
            
            if go:
                path_found_and = True
                
                for elem in block:

                    if elem in store_local:

                        if store_local[elem][1] > 0 and not store_local[elem][0]:
                            path.append(elem)
                            path_found_and_rec = _ResolvePaths(path, save and len(block) == 1)
                            path.pop()

                        else:
                            path_found_and_rec = store_local[elem][0]

                    else:
                        old_len_completePaths = completePaths
                        path.append(elem)
                        path_found_and_rec = _ResolvePaths(path, save and len(block) == 1)
                        path.pop()
                        store_local[elem] = (path_found_and_rec, completePaths - old_len_completePaths)
                    
                    path_found_and = path_found_and and path_found_and_rec
                    
                    if not path_found_and:
                        break

                if path_found_and and save:
                    completePaths += 1
                    path_found_and = False

            path_found_or = path_found_or or path_found_and

        return path_found_or
    
    def _FilterLoops(path, block):
        '''
        Check for loops at current elongation step. Loops will be discarded.
        '''
        if block[0]== path[-1]:
            return False, True
        
        for elem in block:
            if elem in elem in path:
                return False, False
            
        return True, True
    
    def _ExtractNodes(last):
        '''
        Extracts the nodes from a path and replaces them by their drivers.
        '''
        global stored_nodes, drivers
        
        try:
            newBlocks = stored_nodes[last]
        
        except KeyError:
            newBlocks = re_replace_vars.sub(lambda match: f"({drivers[match.group(0)]['Driver']})", last)
            newBlocks = re.sub(r'\(([^)]+)\)', r'(\1)', newBlocks)
        
            if "&" in newBlocks:
                newBlocks = [block.strip('()') for block in re.split(r'\s*&\s*(?=(?:[^()]*\([^()]*\))*[^()]*$)', newBlocks)]
                newBlocks = [block.split("|") for block in newBlocks] 
                newBlocks = ["&".join(pair) for pair in itertools.product(*newBlocks)] 
            
            else:
                newBlocks = newBlocks.replace("(", "").replace(")", "").split("|")
            
            block_lists = [list(set(block.split("&"))) for block in newBlocks]
            total_counter = Counter()
            
            for block in block_lists:
                total_counter.update(block)

            for i in range(len(block_lists)):
                block_lists[i] = sorted(block_lists[i], key=lambda x: total_counter[x], reverse=True)
            
            newBlocks = sorted(block_lists, key=lambda block: max(block, key=lambda x: total_counter[x]), reverse=True)
            stored_nodes[last] = newBlocks

        return newBlocks

    def _ExtractNodesOptimizeDrivers(last): 
        '''
        Retrieves the nodes and processes the node list when drivers are being optimized.
        '''
        global drivers

        newBlocks = re_replace_vars.sub(lambda match: f"({drivers[match.group(0)]['Driver']})", last) 
        newBlocks = re.sub(r'\(([^)]+)\)', r'(\1)', newBlocks) 
        
        if "&" in newBlocks:
            newBlocks = [block.strip('()') for block in re.split(r'\s*&\s*(?=(?:[^()]*\([^()]*\))*[^()]*$)', newBlocks)] 
            newBlocks = [block.split("|") for block in newBlocks] 
            newBlocks = ["&".join(pair) for pair in itertools.product(*newBlocks)] 

        else:
            newBlocks = newBlocks.replace("(", "").replace(")", "").split("|") 
        
        newBlocks = [elem for block in newBlocks for elem in list(set(block.split("&")))]
        
        return newBlocks
    
    def _OptimizeDrivers(drivers):
        '''
        Simplifies the drivers dictionary.
        '''
        for _ in range(6):
            for node in drivers:
                driverNode = _ExtractNodesOptimizeDrivers(node)
                if len(driverNode) == 1:
                    for nodeSearch in drivers:
                        if node in _ExtractNodesOptimizeDrivers(nodeSearch) and nodeSearch != driverNode[0]:
                            drivers[nodeSearch]["Driver"] = re.sub(r'\b'+node+r'\b', driverNode[0], drivers[nodeSearch]["Driver"])
        
        for data_element in drivers:
            drivers[data_element]['Driver'] = drivers[data_element]['Driver'].replace("&", "|")
    
    global completePaths, stored_nodes, drivers
    model_paths = []

    if len(model_info.columns) > 2:
        for state in [state for state in model_info.columns if state not in ["DNF", "NDNF"]]:
            stored_nodes = {}
            drivers = Drivers(model_info, state)
            _OptimizeDrivers(drivers)
            state_paths = []

            for tNode in tNodes:
                completePaths = 0
                start_time = time.time()
                lpaths = _LinearPaths(tNode)
                simulation_time = (time.time() - start_time)/60
                print(f"{tNode}: {lpaths}, {simulation_time} minutes.")
                state_paths.append(lpaths)
            
            model_paths.append(state_paths)

        if ss_wise:
            return model_paths
        
        else:
            model_score = [sum(x)/len(x) for x in zip(*model_paths)]
            model_score = [str(score) for score in model_score]
            return model_score