import numpy as np
import points as pt
from characters import barbarians, dragons, balloons, archers, stealth_archers, healers

class Building:
    def destroy(self,King):
        self.destroyed = True
        if self.type == 'wall':
            self.attack_target(King)
            self.V.remove_wall(self)
        elif self.type == 'hut':
            self.V.remove_hut(self)
        elif self.type == 'cannon':
            self.V.remove_cannon(self)
        elif self.type == 'wizardtower':
            self.V.remove_wizard_tower(self)
        elif self.type == 'townhall':
            self.V.remove_town_hall(self)


class Hut(Building):
    def __init__(self, position, V):
        self.position = position
        self.dimensions = (2, 2)
        self.V = V
        self.destroyed = False
        self.health = 40
        self.max_health = 40
        self.type = 'hut'


class Cannon(Building):
    def __init__(self, position, V, building_level):
        self.position = position
        self.dimensions = (2, 2)
        self.V = V
        self.destroyed = False
        self.health = 60
        self.type = 'cannon'
        self.isShooting = False
        self.building_level = building_level
        self.attack = 4 + building_level
        self.attack_radius = 5 + (building_level//2)
        self.max_health = 60 + 30*building_level
        

    def scan_for_targets(self, King):
        self.isShooting = False

        troops = barbarians + archers + stealth_archers
        for troop in troops:
            if (troop.position[0] - self.position[0])**2 + (troop.position[1] - self.position[1])**2 <= self.attack_radius**2:
                self.isShooting = True
                self.attack_target(troop)
                return

        # for barb in barbarians:
        #     if (barb.position[0] - self.position[0])**2 + (barb.position[1] - self.position[1])**2 <= self.attack_radius**2:
        #         self.isShooting = True
        #         self.attack_target(barb)
        #         return
        # for dragon in dragons:
        #     if (dragon.position[0] - self.position[0])**2 + (dragon.position[1] - self.position[1])**2 <= self.attack_radius**2:
        #         self.isShooting = True
        #         self.attack_target(dragon)
        #         return

        if King.alive == False:
            return

        if (King.position[0] - self.position[0])**2 + (King.position[1] - self.position[1])**2 <= self.attack_radius**2:
            self.isShooting = True
            self.attack_target(King)

    def attack_target(self, target):
        if (self.destroyed == True):
            return
        target.deal_damage(self.attack)


class Wall(Building):
    def __init__(self, position, V, building_level):
        self.position = position
        self.dimensions = (1, 1)
        self.V = V
        self.destroyed = False
        self.health = 20
        self.type = 'wall'
        self.building_level = building_level
        self.max_health = 100 + 40*building_level
        self.explode_attack = 200
        self.tile_range = 2

    def attack_target(self,King):
        troops = barbarians + archers
        if (self.destroyed == True) and (self.building_level >= 3):
            #King
            pos = King.position
            isXrange =  pos[0] >= (self.position[0]-2) and pos[0] <= (self.position[0]+2)
            isYrange =  pos[1] >= (self.position[1]-2) and pos[0] <= (self.position[1]+2)
            if isXrange and isYrange:
                King.deal_damage(self.explode_attack)
            #King
            for troop in troops:
                pos = troop.position
                isXrange =  pos[0] >= (self.position[0]-2) and pos[0] <= (self.position[0]+2)
                isYrange =  pos[1] >= (self.position[1]-2) and pos[0] <= (self.position[1]+2)
                if isXrange and isYrange:
                    troop.deal_damage(self.explode_attack)
            
            for starch in stealth_archers:
                pos = starch.position
                isXrange =  pos[0] >= (self.position[0]-2) and pos[0] <= (self.position[0]+2)
                isYrange =  pos[1] >= (self.position[1]-2) and pos[0] <= (self.position[1]+2)
                if isXrange and isYrange:
                    starch.take_damage_wall = True
                    starch.deal_damage(self.explode_attack)
            


class TownHall(Building):
    def __init__(self, position, V):
        self.position = position
        self.dimensions = (4, 3)
        self.V = V
        self.destroyed = False
        self.health = 100
        self.max_health = 100
        self.type = 'townhall'


class WizardTower(Building):
    def __init__(self, position, V, building_level):
        self.position = position
        self.dimensions = (1, 1)
        self.V = V
        self.destroyed = False
        self.health = 60
        self.type = 'wizardtower'
        self.isShooting = False
        self.building_level = building_level
        self.attack = 4 + building_level
        self.attack_radius = 5 + (building_level//2)
        self.max_health = 60 + 30*building_level

    def scan_for_targets(self, King):
        self.isShooting = False
        troops = barbarians + archers + stealth_archers + dragons + balloons + healers
        for troop in troops:
            if (troop.position[0] - self.position[0])**2 + (troop.position[1] - self.position[1])**2 <= self.attack_radius**2:
                self.isShooting = True
                self.attack_target(troop, 0)
                return

        if King.alive == False:
            return

        if (King.position[0] - self.position[0])**2 + (King.position[1] - self.position[1])**2 <= self.attack_radius**2:
            self.isShooting = True
            self.attack_target(King, 1)

    def attack_target(self, target, isKing):
        if (self.destroyed == True):
            return

        if isKing == 1:
            target.deal_damage(self.attack)
        i = target.position[0] - 1
        j = target.position[1] - 1
        troops = barbarians + archers + stealth_archers + dragons + balloons + healers
        for row in range(i, i+3):
            for col in range(j, j+3):
                if (row < 0 or col < 0):
                    continue
                for troop in troops:
                    if (troop.position[0] == row and troop.position[1] == col):
                        troop.deal_damage(self.attack)


def shoot_cannons(King, V):
    for cannon in V.cannon_objs:
        V.cannon_objs[cannon].scan_for_targets(King)


def shoot_wizard_towers(King, V):
    for tower in V.wizard_tower_objs:
        V.wizard_tower_objs[tower].scan_for_targets(King)
