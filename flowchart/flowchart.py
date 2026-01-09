#!/usr/bin/env python3

# pygraphviz install on M1 mac: https://github.com/iriusrisk/startleft/issues/329

__author__ = """Charles Fyfe"""

from enum import Enum
import pygraphviz as pgv

ABORTION_RATE = "abortion\nrate"
CAR_OWNERSHIP = "car\nownership"
CIVIC_TRUST = "civic\ntrust"
DOMESTIC_VIOLENCE = "domestic\nviolence"
HOUSING_AFFORDABILITY = "housing\naffordability"
HOUSING_SUPPLY = "housing\nsupply"
HOMELESSNESS = "homelessness"
MALE_LONELINESS = "male\nloneliness"
MASS_INCARCERATION = "mass\nincarceration"
MASS_SHOOTINGS = "mass\nshootings"
MASS_TRANSIT = "mass\ntransit"
SEX_EDUCATION = "sex\neducation"
SUBSTANCE_ADDICTION = "substance\naddiction"
URBAN_DENSITY = "urban\ndensity"
WIDESPREAD_GUNS = "widespread\nguns"



# strict (no parallel edges), digraph, with attribute rankdir set to 'LR'
A = pgv.AGraph(directed=True, strict=True, rankdir="LR")
# add node 1 with color red
A.add_edge(HOUSING_SUPPLY, HOUSING_AFFORDABILITY)
A.add_edge(HOUSING_AFFORDABILITY, HOMELESSNESS)
A.add_edge(HOMELESSNESS, MASS_TRANSIT)
A.add_edge(HOMELESSNESS, MASS_TRANSIT)
A.add_edge(MASS_TRANSIT, CAR_OWNERSHIP)
A.add_edge(URBAN_DENSITY, MASS_TRANSIT)
A.add_edge(WIDESPREAD_GUNS, MASS_SHOOTINGS)
A.add_edge(MASS_SHOOTINGS, CIVIC_TRUST)
A.add_edge(CIVIC_TRUST, WIDESPREAD_GUNS)
A.add_edge(SEX_EDUCATION, ABORTION_RATE)
A.add_edge(SUBSTANCE_ADDICTION, DOMESTIC_VIOLENCE)

print(A.string())  # print dot file to standard output
A.layout("dot")  # layout with dot
A.draw("flowchart.png")  # write to file