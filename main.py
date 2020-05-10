import json
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow.compat.v1 as tf
import tensorflow_example

def load_data(filename):
    data = []
    with open(filename) as json_file:
        line = json_file.readline()
        while line:
            data.append(json.loads(line))
            line = json_file.readline()
    return data


# transform feet and inches to cm
def ft_and_inch_to_cm(ft_and_inch):
    if isinstance(ft_and_inch, str):
        ft = re.search('([0-9])+ft', ft_and_inch)
        ft = ft.group(1) if ft is not None else 0
        inch = re.search('([0-9])+in', ft_and_inch)
        inch = inch.group(1) if inch is not None else 0
        return int(ft) * 30.48 + int(inch) * 2.54
    return None


def print_df_to_html(df, filename):
    with open(filename, "w") as f:
        f.write('<link href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">')
        f.write('<table class="table">')
        f.write(''.join(df.to_html().splitlines()[1:]))
    print("DataFrame printed to file '" + filename + "'")


# cup size: a, b, c, d, dd, ddd, ... -> 1, 2, 3, 4, 5, 6, ...
def cup_size_to_ordinal(cup_size):
    if str(cup_size).replace('.', '', 1).isdigit():
        return cup_size

    cup_size = str(cup_size)
    slash_pos = cup_size.find("/")
    if slash_pos != -1:
        cup_size = cup_size[:slash_pos]

    if cup_size[0] == "a":
        return 1
    if cup_size[0] == "b":
        return 2
    if cup_size[0] == "c":
        return 3
    if cup_size[0] == "d":
        return 4 + (len(cup_size) - 1)
    return None


# length: slightly short, just right, slightly long -> -1, 0, 1
def length_to_ordinal(length):
    if length == "slightly short":
        return -1
    if length == "just right":
        return 0
    if length == "slightly long":
        return 1
    return None


# shoe width: narrow, average, wide -> -1, 0, 1
def shoe_width_to_ordinal(shoe_width):
    if shoe_width == "narrow":
        return -1
    if shoe_width == "average":
        return 0
    if shoe_width == "wide":
        return 1
    return None


def main():
    datafiles = {
       "data/modcloth_product_1.json": "output/product_1.html",
       "data/modcloth_product_2.json": "output/product_2.html",
       "data/modcloth_product_3.json": "output/product_3.html",
    }

    for in_file, out_file in datafiles.items():
        data = load_data(in_file)
        df = pd.DataFrame(data)

        if 'height' in df:
            df['height'] = df['height'].apply(lambda x: ft_and_inch_to_cm(x))

        if 'cup size' in df:
            df['cup size'] = df['cup size'].apply(lambda x: cup_size_to_ordinal(x))

        if 'length' in df:
            df['length'] = df['length'].apply(lambda x: length_to_ordinal(x))

        if 'shoe width' in df:
            df['shoe width'] = df['shoe width'].apply(lambda x: shoe_width_to_ordinal(x))

        print_df_to_html(df, out_file)


    #tensorflow_example.linear_regression()


if __name__ == '__main__':
    main()
