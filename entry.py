#!/usr/bin/env python3

import helpers

def main():

    data = helpers.load_json("data/nations.json")

    key = "area_km2"

    new = {}
    lines = helpers.read_lines("entry.txt")

    lines = lines[::4]

    for line in lines:

        try:
            name = line.split("\t")[1]
            name = name.split("(")[0].strip()
            new[name] = float(line.split("\t")[2].replace(",", ""))
        except Exception:
            pass

    [ print(k, ":", v) for k, v in new.items() ]

    for name, val in new.items():
        if name not in data:
            data[name] = {}
        data[name][key] = val

    # Clean up the data
    cleaned = {}
    for k, v in data.items():
        key = rmchars(k, ".")
        key = key.replace("Saint", "St")
        if key in cleaned:
            cleaned[key].update(v)
        else:
            cleaned[key] = v
        cleaned[key]["name"] = key


    return helpers.dump_json(cleaned, "foo.json")


def rmchars(text, chars):
    for c in chars:
        text = text.replace(c, "")
    return text

# ----------------------------------------------------------------------

if __name__ == "__main__":
    main()
