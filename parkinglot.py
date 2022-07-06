#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 12:48:16 2020

@author: dahaeshin
"""

import parkinglot_agent

width = 5

blocks = set()

for x in range(width+1):
    blocks.add((0, x))
    blocks.add((x, 0))
    blocks.add((width,x))
    blocks.add((x, width))

entrance = {(0,0)}
out = {(width, width)}
fee_machine_location = {(4,4)}
active_cars = {(3,3)}
target_parking_space = {(4,2)}
initial_location = (1,1)

parkinglot = parkinglot_agent.Parkinglot(entrance = entrance, out = out, blocks = blocks, target_parking_space = target_parking_space, fee_machine = fee_machine_location, active_cars = active_cars, initial_location = initial_location)
