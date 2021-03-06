#!/usr/bin/env python3

import helpers

def main():

# GDP vs...
#    pct_white - YES
#    household_size - YES
#    rain_inches - no
#    life_expectancy - no
#    avg_age - no
#    n_legislators - sorta
#    marriage_age - no


# Population vs...


# Area vs...




    helpers.scatter(
        loadfile="data/states.json",
        xkey = "gdp",
        ykey = "marriage_age",
#        title="Larger States Get Less Rain",
#        xlabel="Area (km$^2$)",
#        ylabel="Average Yearly Precipitation (inches)",
        namesize=10,
#        ylim=[0, 80],
        log="x",
        xlim=[1e4, 1e7],
#        xticks=[1e5, 1e6, 1e7, 1e8],
#        xticklabels=[0.1, 1, 10, 100],
        savefile="states.png",

        skip=["US Virgin Islands", "Guam", "American Samoa", "Northern Mariana Islands", "District of Columbia"]
    )


    return







    helpers.scatter(
        loadfile="data/states.json",
        xkey = "population",
        ykey = "pct_white",
        title="Larger States Are Generally More Diverse",
        xlabel="Population (millions)",
        ylabel="Non-Hispanic White Population (%)",
        namesize=10,
        ylim=[0, 100],
        log="x",
        xlim=[1e5, 1e8],
        xticks=[1e5, 1e6, 1e7, 1e8],
        xticklabels=[0.1, 1, 10, 100],
        savefile="state-size-log.png"
    )

    helpers.scatter(
        loadfile="data/states.json",
        xkey = "population",
        ykey = "pct_white",
        title="Are Larger States Generally More Diverse?",
        xlabel="Population (millions)",
        ylabel="Non-Hispanic White Population (%)",
        namesize=10,
        ylim=[0, 100],
        log="",
        trend=False,
        xticks=[0, 1e7, 2e7, 3e7, 4e7],
        xticklabels=[0, 10, 20, 30, 40],
        savefile="state-size-linear.png"
    )

    return




    data = []
    for line in helpers.read_lines("data/states0.txt"):
        name = line[:-2].strip()
        abbrev = line[-2:]
        data.append({"name": abbrev, "full_name": name})
    helpers.dump_json(data, "data/states.json")



# ----------------------------------------------------------------------

if __name__ == "__main__":
    main()
