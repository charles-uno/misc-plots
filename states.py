#!/usr/bin/env python3

import helpers

def main():

    helpers.scatter(
        loadfile="data/states.json",
        xkey = "population",
        ykey = "pct_white",
        title="Larger States Are Generally More Diverse",
        xlabel="Population",
        ylabel="Non-Hispanic White Population (%)",
        namesize=10,
        ylim=[0, 100],
        log="x",
        xlim=[1e5, 1e8],
        savefile="example-plot-log.png"
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
        savefile="example-plot-lin.png"
    )

    return


    data = helpers.load_json("data/states.json")

    new = {}

    for line in helpers.read_lines("states.in"):

        names = line.split()[:-11]
        # Listed twice...
        name = " ".join(names[:len(names)//2])
        name = name.split("(")[0].strip()
        new[name] = float(line.split()[-4].strip("%"))

    [ print(k, ":", v) for k, v in new.items() ]


    for state in data:
        state["pct_white"] = new[state["full_name"]]

    helpers.dump_json(data, "data/states.json")

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
