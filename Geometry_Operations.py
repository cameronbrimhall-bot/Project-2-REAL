#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 11:25:01 2021

@author: kendrick shepherd
"""

import math
import numpy as np
import sys

# length of the beam
def Length(bar):
    #find a node of the bar
    bar_node = bar.init_node
    #convert the node and bar to a vector
    bar_vec = BarNodeToVector(bar_node, bar)
    #find the length of the vector
    bar_len = VectorTwoNorm(bar_vec)
    #output the vector length
    return bar_len
    

# Find two norm (magnitude) of a vector
def VectorTwoNorm(vector):
    norm = 0
    for i in range(0,len(vector)):
        norm += vector[i]**2
    return np.sqrt(norm)

# Find a shared node between two bars
def FindSharedNode(bar_1,bar_2):
    # Check all combinations of start/end nodes
    if bar_1.init_node == bar_2.init_node or bar_1.init_node == bar_2.end_node:
        return bar_1.init_node
    if bar_1.end_node == bar_2.init_node or bar_1.end_node == bar_2.end_node:
        return bar_1.end_node
    sys.exit("The bars do not share a node.")
    return

# Given a bar and a node on that bar, find the other node
def FindOtherNode(node,bar):
    if(bar.init_node == node):
        return bar.end_node
    elif(bar.end_node == node):
        return bar.init_node
    else: 
        sys.exit("The input node is not on the bar")

# Find a vector from input node (of the input bar) in the direction of the bar
def BarNodeToVector(origin_node,bar):
    other_node = FindOtherNode(origin_node, bar)
    origin_loc = origin_node.location
    other_loc = other_node.location
    vec = [other_loc[0] - origin_loc[0], other_loc[1] - origin_loc[1]]
    return vec

# Convert to bars that meet at a node into vectors pointing away from that node
def BarsToVectors(bar_1,bar_2):
    shared_node = FindSharedNode(bar_1, bar_2)
    vec1 = BarNodeToVector(shared_node, bar_1)
    vec2 = BarNodeToVector(shared_node, bar_2)
    return vec1, vec2
    return

# Cross product of two vectors
def TwoDCrossProduct(vec1,vec2):
    cross_product = vec1[0] * vec2[1] - vec1[1] * vec2[0]
    return cross_product
    
# Dot product of two vectors
def DotProduct(vec1,vec2):
    dot=0
    for i in range(len(vec1)):
        dot+=vec1[i]*vec2[i]
    return dot

# Cosine of angle from local x vector direction to other vector
def CosineVectors(local_x_vec,other_vec):
   # cos(theta) = (a . b) / (|a| * |b|)
    dot = DotProduct(local_x_vec, other_vec)
    mags = VectorTwoNorm(local_x_vec) * VectorTwoNorm(other_vec)
    return dot / mags
    

# Sine of angle from local x vector direction to other vector
def SineVectors(local_x_vec, other_vec):
    # sin(theta) = (a x b) / (|a| * |b|)
    cross = TwoDCrossProduct(local_x_vec, other_vec)
    mags = VectorTwoNorm(local_x_vec) * VectorTwoNorm(other_vec)
    return cross / mags
 

# Cosine of angle from local x bar to the other bar
def CosineBars(local_x_bar,other_bar):
    # Get vectors originating from the shared joint
    v1, v2 = BarsToVectors(local_x_bar, other_bar)
    # Use our existing vector math
    return CosineVectors(v1, v2)

# Sine of angle from local x bar to the other bar
def SineBars(local_x_bar,other_bar):
    # Get vectors originating from the shared joint
    v1, v2 = BarsToVectors(local_x_bar, other_bar)
    # Use our existing vector math
    return SineVectors(v1, v2)