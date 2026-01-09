#!/usr/bin/env python3

# pygraphviz install on M1 mac: https://github.com/iriusrisk/startleft/issues/329

__author__ = """Charles Fyfe"""

from enum import Enum
import pygraphviz as pgv

ABORTION_RATE = "abortion\nrate"
CIVIC_TRUST = "civic\ntrust"
CLIMATE_CHANGE = "climate\nchange"
CONCENTRATED_POVERTY = "concentrated\npoverty"
DOMESTIC_VIOLENCE = "domestic\nviolence"
HOUSING_AFFORDABILITY = "housing\naffordability"
HOUSING_SUPPLY = "housing\nsupply"
HOMELESSNESS = "homelessness"
IMMIGRATION = "immigration"
MALE_LONELINESS = "male\nloneliness"
MASS_INCARCERATION = "mass\nincarceration"
MASS_SHOOTINGS = "mass\nshootings"
MASS_TRANSIT = "mass\ntransit"
MILITARIZED_POLICE = "militarized\npolice"
OIL_WARS = "oil\nwars"
OUTSOURCING = "outsourcing"
RACISM = "racism"
REGIONAL_INSTABILITY = "regional\ninstability"
RESTRICTIVE_ZONING = "restrictive\nzoning"
SEX_EDUCATION = "sex\neducation"
SUBSTANCE_ADDICTION = "substance\naddiction"
TRADE_DEALS = "trade\ndeals"
URBAN_SPRAWL = "urban\nsprawl"
WIDESPREAD_CARS = "widespread\ncars"
WIDESPREAD_GUNS = "widespread\nguns"
WORKER_PROTECTIONS = "worker\nprotections"


# strict (no parallel edges), digraph, with attribute rankdir set to 'LR'
A = pgv.AGraph(directed=True, rankdir="LR")
# add node 1 with color red
A.add_edge(HOUSING_SUPPLY, HOUSING_AFFORDABILITY)
A.add_edge(HOUSING_AFFORDABILITY, HOMELESSNESS)
A.add_edge(HOMELESSNESS, MASS_TRANSIT)
A.add_edge(HOMELESSNESS, MASS_TRANSIT)
A.add_edge(MASS_TRANSIT, WIDESPREAD_CARS)
A.add_edge(URBAN_SPRAWL, MASS_TRANSIT)
A.add_edge(WIDESPREAD_GUNS, MASS_SHOOTINGS)
A.add_edge(MASS_SHOOTINGS, CIVIC_TRUST)
A.add_edge(CIVIC_TRUST, WIDESPREAD_GUNS)
A.add_edge(SEX_EDUCATION, ABORTION_RATE)
A.add_edge(SUBSTANCE_ADDICTION, DOMESTIC_VIOLENCE)
A.add_edge(RESTRICTIVE_ZONING, HOUSING_SUPPLY)
A.add_edge(HOMELESSNESS, SUBSTANCE_ADDICTION)
A.add_edge(CLIMATE_CHANGE, REGIONAL_INSTABILITY)
A.add_edge(REGIONAL_INSTABILITY, IMMIGRATION)
A.add_edge(OIL_WARS, REGIONAL_INSTABILITY)
A.add_edge(WIDESPREAD_CARS, CLIMATE_CHANGE)
A.add_edge(WIDESPREAD_CARS, URBAN_SPRAWL)
A.add_edge(RACISM, RESTRICTIVE_ZONING)
A.add_edge(RACISM, CIVIC_TRUST)
A.add_edge(RACISM, MASS_INCARCERATION)
A.add_edge(RACISM, MILITARIZED_POLICE)
A.add_edge(WIDESPREAD_CARS, OIL_WARS)
A.add_edge(IMMIGRATION, RACISM)
A.add_edge(WIDESPREAD_GUNS, MILITARIZED_POLICE)


print(A.string())  # print dot file to standard output
# default layout uses dot, which stretches things out pretty bad
# other options: neato, fdp, twopi
A.layout("neato", args="-Goverlap=scale")

A.draw("flowchart.png")  # write to file