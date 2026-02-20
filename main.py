import Simulations.growing_sphere as growing_sphere
import Simulations.butterfly_effect as butterfly_effect
import Simulations.duplicating_balls as duplicating_balls
import Simulations.shrinking_ring as shrinking_ring
import Simulations.bounce_countdown as bounce_countdown

import upload_video
import random

simulation_functions = [
    growing_sphere.simulation,
    growing_sphere.simulation,
    butterfly_effect.simulation,
    butterfly_effect.simulation,
    duplicating_balls.simulation,
    duplicating_balls.simulation,
    shrinking_ring.simulation,
    shrinking_ring.simulation,
    bounce_countdown.simulation,
]

flag = False
file_name = "output_vid"
chosen_simulation = random.choice(simulation_functions)
title = "video"
description = "simulation"

while not flag:
    flag, title, description = chosen_simulation(file_name)
    
file_name = f"{file_name}.mp4"
print()
print()

upload_video.upload_video(file_name, title, description)