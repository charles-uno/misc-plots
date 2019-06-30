#!/usr/bin/env python3

# https://www.holiday-weather.com/lagos/averages/

import helpers

def main():
    return helpers.scatter(
        loadfile="data/cities.json",
        xkey = "latitude",
        ykey = "temperature_january_f",
        title="Higher Latitude Means Colder Winter in the Northern Hemisphere",
        xlabel="Latitude ($^\circ$N)",
        ylabel="Average January Temperature ($^\circ$F)",
        xlim=[0, 80],
        ylim=[0, 90],
        skip=["Seattle", "Seoul", "Sydney", "Sao Paulo", "Lima", "Jakarta", "Kinshasa"],
        savefile="example-plot-linear.png",
    )

# ----------------------------------------------------------------------

if __name__ == "__main__":
    main()
