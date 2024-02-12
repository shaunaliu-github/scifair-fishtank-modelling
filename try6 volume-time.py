#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 17:23:59 2024

@author: for_phone
"""

import numpy as np

def functionn(n_algae, n_fish, n_zoo, volume):
    resp_zoo = 0.732e-4 #mol CO2 / L day

    #n_algae = 1e-3 * float(input('How many mL of algae?')) #L

    #n_fish = float(input('How many fishes?'))

    #n_zoo = 1e-3 * float(input('How many mL of zooplankton?')) #L

    fish_eat_algae_rate = 0.08  # L/day
    zoo_eat_algae_rate = 0.385173669 #L/L
    fish_eat_zoo_rate = 1 #!!!!!

    photo_rate = 0.00643 * n_algae #mol/day

    resp_fish = 3.54e-4
    resp_algae = 6.43e-3

    o2_lvl=10e-3 * volume
    o2_lethal_lvl_fish = 8.8e-4
    n_algae_production_rate = 1.2 # pop growth per unit time (from a graph)

    zoo_reproduction_rate = 1.1569


    go_on = True

    def food_chain(days, n_algae, n_fish, n_zoo):
        if n_zoo >= 0.1:
            n_zoo -= n_fish * 0.249 * 0.001 * 30 #zoo_consumed in ml
            #sorry had to assume zooplankton density is water
            n_algae = n_algae * n_algae_production_rate
            n_algae -= n_zoo * zoo_eat_algae_rate
            n_zoo = n_zoo * zoo_reproduction_rate


        else:
            n_algae = n_algae - n_fish * fish_eat_algae_rate #- n_zoo * fish_eat_zoo_rate
            n_algae = n_algae * n_algae_production_rate
            n_zoo = n_zoo * zoo_reproduction_rate
        return n_algae

    #endings
    def pop_check(n_algae, n_fish, o2_lvl, go_on):
        if o2_lvl < o2_lethal_lvl_fish:  # ppm

            #print('lethal oxygen levels for fish')
            n_fish = 0
            go_on = False

        if n_algae <= 0:
            #print('no algae left')
            go_on = False

        if n_algae >= 1000:
            #print('death by eutrophication')
            go_on = False


        return n_fish, go_on

    #def biomass_transfer(days, n_algae, n_fish):


    def o2_per_day_update(days, n_algae, n_fish):
        global o2_lvl
        half_full = 0.5*volume
        if n_algae <= half_full:
            o2_lvl = float (photo_rate * n_algae - resp_fish * n_fish - resp_algae * n_algae)
        if n_algae > half_full:
            #print('tank half full with algae. eutrophication?')
            o2_lvl = float (photo_rate * 5 - resp_fish * n_fish - resp_algae * n_algae)

    days = 0


    while go_on and days <= 1000:
        days += 1
        o2_per_day_update(days, n_algae, n_fish)
        n_algae = food_chain(days, n_algae, n_fish, n_zoo)
        n_fish, go_on = pop_check(n_algae, n_fish, o2_lvl, go_on)

    final_day = days
    #print('final_day', final_day)
    return final_day


lst_fish = []
lst_algae = []
lst_zoo = []
lst_day =[0, 0]
lst_volume =[]
lst_finalday = []

#volume = 100
for volume in range(1, 30):
    for n_fish in np.arange(0,50):
        for n_algae in np.arange(0, 0.7*volume):
            for n_zoo in np.arange(0,0.5*volume):
                final_day = functionn(n_fish, n_algae, n_zoo, volume)
           #     lst_fish.append((n_fish))
            #    lst_algae.append((n_algae))
            #    lst_zoo.append((n_zoo))
                if final_day >= lst_day[-1]:
                    lst_day.append(final_day)
    lst_volume.append(volume)
    lst_finalday.append(lst_day[-1])
    lst_day=[0 , 0]




import matplotlib.pyplot as plt
import numpy as np
plt.xlabel('Volume(L)')
plt.ylabel('Days')
plt.scatter(lst_volume, lst_finalday)
