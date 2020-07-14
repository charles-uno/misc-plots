#!/usr/bin/env python3

# https://www.holiday-weather.com/lagos/averages/

import helpers

def main():

    # Log axes
    helpers.scatter(
        loadfile="data/nations.json",
        xkey = "population",
        ykey = "area_km2",
        log="xy",
        title="Larger Countries Generally Have More People",
        xlabel="Population",
        ylabel="Land Area (km$^2$)",
        namesize=8,
        xticks=[1e5, 1e6, 1e7, 1e8, 1e9, 1e10],
        yticks=[1e2, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8],
#        skip=["Jamaica", "Germany", "Spain", "Albania", "Nigeria", "Vietnam", "Jordan", "France", "Turkey", "South Africa", "Micronesia", "Norway", "Australia", "Venezuela", "Argentina", "Brazil", "Mexico", "Ghana"],
        savefile="example-plot-log.png",
    )
    # Linear axes
    helpers.scatter(
        loadfile="data/nations.json",
        xkey = "population",
        ykey = "area_km2",
        title="Do Larger Countries Generally Have More People?",
        trend=False,
        xlabel="Population (millions)",
        ylabel="Land Area (millions of km$^2$)",
        namesize=8,
        xticks=[0, 5e8, 1e9, 1.5e9, 2e9],
        xticklabels=["0", "500", "1000", "1500", "2000"],
        yticks=[0, 0.5e7, 1e7, 1.5e7, 2e7],
        yticklabels=["0", "5", "10", "15", "20"],
#        skip=["Jamaica", "Germany", "Spain", "Albania", "Nigeria", "Vietnam", "Jordan", "France", "Turkey", "South Africa", "Micronesia", "Norway", "Australia", "Venezuela", "Argentina", "Brazil", "Mexico", "Ghana"],
        savefile="example-plot-linear-bad.png",
    )

# ----------------------------------------------------------------------

if __name__ == "__main__":
    main()
