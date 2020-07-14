#!/usr/bin/env python3

import helpers

def main():

    data = helpers.load_json("data/states.json")

    if not isinstance(data, dict):
        data = { x["full_name"]:x for x in data }


    key = "marriage_age"

    new = {}
    lines = helpers.read_lines("entry.txt")
    lines = [ x for x in lines if x ]
#    lines = lines[::4]

    for line in lines:


        line = line.split(". ")[-1]
        name, num = line.split(": ", 1)
        new[name] = float(num)



        try:
            name = line.split("\t")[0]
            name = name.split("(")[0].strip()
            new[name] = float(line.split("\t")[1].replace(",", ""))
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
