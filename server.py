from mesa.visualization.ModularVisualization import ModularServer

import model
from model import *
import mesa
# TODO buttons needed for: social_group_size, local_group_size, dynamic/static


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "blue",
                 "r": 0.5}
    return portrayal


grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(SocialPressureModel,
                       [grid],
                       "Social Pressure Model",
                       {"N": 10, "width": 10, "height": 10})

server.port = 8521  # The default
server.launch()
