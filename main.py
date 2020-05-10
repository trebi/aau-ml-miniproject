import json

import numpy as np
import pandas as pd
import tensorflow.compat.v1 as tf

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
       # "data/modcloth_product_1.json": "output/product_1.html",
       # "data/modcloth_product_2.json": "output/product_2.html",
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

        if 'fit' in df:
            df['fit'] = df['fit'].apply(fit_to_ordinal)

        print_df_to_html(df, out_file)
        linear_regression(df)


# linear regression with multiple variables: https://donaldpinckney.com/books/tensorflow/book/ch2-linreg/2018-03-21-multi-variable.html
def linear_regression(df):
    tf.disable_v2_behavior()

    ##
    ## Data pre-processing & model definition
    ##

    X_data = df.filter(['waist', 'quality', 'cup_size', 'hips', 'bra size', 'bust', 'height', 'length', 'fit', 'shoe size', 'shoe width'], axis=1)\
        .to_numpy().transpose()
    # missing data: remove rows with at least one NaN value
    X_data = X_data[~pd.isnull(X_data).any(axis=1)]

    n = X_data.shape[0]

    y_data = df.filter(['size'], axis=1).to_numpy().transpose()

    # Define data placeholders
    x = tf.placeholder(tf.float32, shape=(n, None))
    y = tf.placeholder(tf.float32, shape=(1, None))

    # Hypothesis: y_pred = Ax + b

    # trainable variables
    A = tf.get_variable("A", shape=(1, n))
    b = tf.get_variable("b", shape=())

    # model output
    y_pred = tf.matmul(A, x) + b

    # Cost Function: MSE
    cost = tf.reduce_sum((y_pred - y)**2)

    ##
    ## Training phase
    ##

    # Parameters
    learning_rate = 0.01
    training_epochs = 1000

    # Gradient Descent Optimizer (alternative: AdamOptimizer)
    optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)

    with tf.Session() as session:
        session.run(tf.global_variables_initializer())
        for epoch in range(training_epochs):
            _, current_cost, current_A, current_b = session.run([optimizer, cost, A, b], feed_dict={
                x: X_data,
                y: y_data
            })
            print("epoch = %g, cost = %g, A = %s, b = %g" % (epoch, current_cost, str(current_A), current_b))

        ##
        ## Evaluation phase
        ##

        # compare y and y_pred (model: y_pred = Ax + b)
        predictions = y_pred.eval(feed_dict={x: X_data})
        print(y_data, predictions)


if __name__ == '__main__':
    main()
