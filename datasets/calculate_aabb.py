import sys,os
import numpy as np
import json
from typing import Union
"""this module is used for calculating aabb from nerfstudio dataset"""

def cal_aabb_from_transform(jsonpath:str):
    if not jsonpath.endswith('.json'):
        jsonpath = os.path.join(jsonpath,'transforms.json')
    with open(jsonpath,'r') as f:
        tf = json.load(f)
        assert 'frames' in tf
        frames = tf['frames']
        allc2w = []
        for frame in frames:
            allc2w.append(np.array(frame['transform_matrix']))
        
        allc2w = np.array(allc2w)
        trans = allc2w[:,0:3,3]
        aabb = AABB()
        for vec in trans:
            #print(vec)
            aabb.grow_AABB(vec)
        re = aabb.to_list()
    
    return aabb
        

class AABB:
    def __init__(self) -> None:
        self.min = np.array([0,0,0],dtype=float)
        self.max = np.array([0,0,0],dtype=float)

    def grow_AABB(self,vec:Union[np.array, list]):
        if isinstance(vec,list):
            vec = np.array(vec,dtype=float)
        self.min = np.minimum(self.min,vec)
        self.max = np.maximum(self.max,vec)
    def to_list(self):
        return [self.min.tolist(),self.max.tolist()]



if __name__ == "__main__":
    cal_aabb_from_transform('/home/dzt/code/NeRF-SLAM/Datasets/replica_sample/office0')