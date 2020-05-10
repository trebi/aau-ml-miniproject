import json

import pandas as pd
import tensorflow.compat.v1 as tf
import tensorflow_example
from data_preprocessing import *


def load_data(filename):
    data = []
    with open(filename) as json_file:
        line = json_file.readline()
        while line:
            data.append(json.loads(line))
            line = json_file.readline()
    return data


def print_df_to_html(df, filename):
    with open(filename, "w") as f:
        f.write('<link href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">')
        f.write('<table class="table">')
        f.write(''.join(df.to_html().splitlines()[1:]))
    print("DataFrame printed to file '" + filename + "'")


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
            df['height'] = df['height'].apply(ft_and_inch_to_cm)

        if 'cup size' in df:
            df['cup size'] = df['cup size'].apply(cup_size_to_ordinal)

        if 'length' in df:
            df['length'] = df['length'].apply(length_to_ordinal)

        if 'shoe width' in df:
            df['shoe width'] = df['shoe width'].apply(shoe_width_to_ordinal)

        print_df_to_html(df, out_file)


    #tensorflow_example.linear_regression()


if __name__ == '__main__':
    main()
