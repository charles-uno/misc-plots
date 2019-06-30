#!/usr/bin/env python3

# https://www.holiday-weather.com/lagos/averages/

import helpers

def main():
    # Log axes
    helpers.scatter(
        loadfile="data/nations.json",
        xkey = "population",
        ykey = "size_km2",
        log="xy",
        title="Larger Countries Generally Have More People",
        xlabel="Population",
        ylabel="Land Area (km$^2$)",
        xticks=[1e5, 1e6, 1e7, 1e8, 1e9, 1e10],
        yticks=[1e2, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8],
        skip=["Jamaica", "Germany", "Spain"],
        savefile="example-plot-log.png",
    )
    # Linear axes
    helpers.scatter(
        loadfile="data/nations.json",
        xkey = "population",
        ykey = "size_km2",
        title="Do Larger Countries Generally Have More People?",
        xlabel="Population",
        ylabel="Land Area (km$^2$)",
        xticks=[0, 1e9, 2e9],
        xticklabels=["0", "1B", "2B"],
        yticks=[0, 0.5e7, 1e7, 1.5e7, 2e7],
        yticklabels=["0", "5M", "10M", "15M", "20M"],
        skip=["Jamaica", "Germany", "Spain"],
        savefile="example-plot-linear-bad.png",
    )

# ----------------------------------------------------------------------

if __name__ == "__main__":
    main()
