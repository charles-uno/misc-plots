#!/usr/bin/env python3

# https://www.holiday-weather.com/lagos/averages/

import helpers

def main():
    return helpers.scatter(
        loadfile="data/cities.json",
#        xkey = "latitude",
        xkey = "population",
#        ykey = "temperature_january_f",
        ykey = "latitude",
#        title="Higher Latitude Means Colder Winter in the Northern Hemisphere",
#        xlabel="Latitude ($^\circ$N)",
        xlabel="Population",
#        ylabel="Average January Temperature ($^\circ$F)",
#        xlim=[0, 80],
        xlim=[1e5, 1e8],
        log="x",
#        ylim=[0, 90],
#        skip=["Seattle", "Seoul", "Sydney", "Sao Paulo", "Lima", "Jakarta", "Kinshasa", "Paris", "Tehran", "Delhi", "Atlanta"],
        savefile="example-plot-linear.png",
    )

# ----------------------------------------------------------------------

if __name__ == "__main__":
    main()
