#!/usr/bin/env python3

import helpers

def main():


    return helpers.scatter(
        loadfile="data/states.json",
        xkey = "population",
        ykey = "rain_inches",
        xlabel="Population",
        log="x",
        xlim=[1e5, 1e8],

    )



    data = helpers.load_json("data/states.json")

    new = {}

    for line in helpers.read_lines("data/states2.txt"):
        name = " ".join(line.split()[:-3])
        new[name] = float(line.split()[-3])


    for state in data:
        state["rain_inches"] = new[state["full_name"]]

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
