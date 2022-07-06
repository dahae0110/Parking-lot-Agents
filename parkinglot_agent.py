#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 12:48:37 2020

@author: dahaeshin
"""

# this class simulates an agent to control parkinglot

class Parkinglot:
  def __init__(self, entrance, out, blocks, active_cars, target_parking_space, fee_machine, initial_location):
    self.initial_location = initial_location    # copy the input
    self.fee_machine = fee_machine
    self.entrance = entrance
    self.out = out
    self.active_cars = active_cars
    self.target_parking_space = target_parking_space
    self.blocks = blocks
    self.player = self.initial_location
    self.feemachine = False
    
    self.radar_sensor = {}    # stores locations of another car
    self.exit_sensor = {}    # stores location of parking fee machine
    
    for p in self.active_cars: # initalise another car's squares
      for l in self.neighbours(p):
        self.radar_sensor[l] = True
    for w in self.fee_machine: # intialise parking fee machine's squares
      for l in self.neighbours(w):
        self.exit_sensor[l] = True
      
      
  def neighbours(self, loc):    # returns neighbours of tuple loc = (x,y) 
    return [(loc[0]+1,loc[1]), (loc[0]-1,loc[1]), (loc[0],loc[1]+1), (loc[0],loc[1]-1)]

  def feemachine_hits(self, location, dx, dy): # scans to see if the feemachine payment was done ('+' area)
    while location not in self.blocks:
      location = (location[0]+dx, location[1]+dy)
      if location in self.fee_machine:
        return True
    return False
  
  def print(self):            # print the board state (useful for debugging)
    print(self.player)
    xmin = min([x for x,y in self.blocks])
    xmax = max([x for x,y in self.blocks])
    ymin = min([y for x,y in self.blocks])
    ymax = max([y for x,y in self.blocks])
    for y in range(ymin, ymax+1):
      for x in range(xmin, xmax+1): 
        if (x,ymax-y) in self.entrance:
          print('/ ', end='')
        elif (x,ymax-y) in self.out:
          print('\ ', end='')
        elif (x,ymax-y) in self.blocks:
          print('| ',end='')
        elif (x,ymax-y) in self.fee_machine:
          print('$ ',end='')
        elif (x,ymax-y) in self.active_cars:
          print('X ',end='')
        elif (x,ymax-y) in self.target_parking_space:
          print('* ',end='')
        elif self.player == (x, ymax - y):
          print('C ',end='')
        else:
          print('| ',end='')
      print("")
    b = self.player in self.radar_sensor       # is their square occupied with another car?
    s = self.player in self.exit_sensor       # did it pay the parking fee?
    print("near another car: " + str(b))      # display for the parkinglot_agent (actuator): showing 3 infos in total
    print("near ticket parking fee machine: " + str(s))
    #print("payed fee: " + str(self.feemachine))
    

  def sim(self, agent):
    t = 0
    self.feemachine = False
    self.player = self.initial_location
    while t < 1000: 
      t+=1

      self.print()

      b = self.player in self.radar_sensor       # is their square occupied with another car?
      s = self.player in self.exit_sensor       # did it pay the parking fee?
      agent.give_senses(self.player, b, s)  # give the agent its senses
      action = agent.get_action()       # get the agents action
      print(action, end='\n\n')

      new_location = self.player
      if action == 'MOVE_UP':             # update the location for moving up/down/left/right
        new_location = (self.player[0], self.player[1]+1)
      elif action == 'MOVE_DOWN':
        new_location = (self.player[0], self.player[1]-1)
      elif action == 'MOVE_LEFT':
        new_location = (self.player[0]-1,self.player[1])
      elif action == 'MOVE_RIGHT':
        new_location = (self.player[0]+1,self.player[1])
      elif not self.feemachine and action[0:5] == 'pay':  # check the agent has the payed their fee
        return 'PAYED THE FEE'
      elif action == 'FEEMACHINE_UP':                      # check to see if the agent payed from the fee_machine
        if self.feemachine_hits(self.player, 0, 1):
          self.fee_machine = {}
          agent.payed_fee()
      elif action == 'FEEMACHINE_DOWN':
        if self.feemachine_hits(self.player, 0, -1):
          self.fee_machine = {}
          agent.payed_fee()
      elif action == 'FEEMACHINE_LEFT':
        if self.feemachine_hits(self.player, -1, 0):
          self.fee_machine = {}
          agent.payed_fee()
      elif action == 'FEEMACHINE_RIGHT':
        if self.feemachine_hits(self.player, 1, 0):
          self.fee_machine = {}
          agent.payed_fee()
      elif action == 'QUIT':
        return 'QUIT'


      if action[0:5] == 'pay':      # remove the 'payed fee' if it was payed
        self.feemachine = True

      if new_location in self.active_cars:   # check if another car is parked (already taken)
        return 'TAKEN'
      if new_location in self.fee_machine: # check if payed by fee_machine
        return 'PAYED'
      if new_location in self.target_parking_space:   # check if found target_parking_space
        return 'PARKED IN THE TARGET PARKING SPACE'

      if new_location not in self.blocks: # if agent ran into a wall, then reset position
        self.player = new_location
      
           
      
  

    


