import Testing.annihilatingBalls as annihilatingBalls

flag = False
file_name = "test_vid"
chosen_simulation = annihilatingBalls.simulation(file_name)
title = "test"
description = "simulation"

while not flag:
    flag, title, description = chosen_simulation(file_name)