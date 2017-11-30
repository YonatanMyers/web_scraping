import numpy as np


def get_end_score(sc):
    state = 1
    res_str = ''
    for l in sc:
        if l == r'(':
            state = 0
        if state != 0:
            res_str += l
        if l == r')':
            state = 1
    res_int = int(res_str)
    return res_int


def get_half_score(sc):
    state = 0
    res_str = ''
    for l in sc:
        if l == r'(':
            state = 1
        if state != 0:
            res_str += l
        if l == r')':
            state = 0
    res_str = res_str.strip('(')
    res_str = res_str.strip(')')
    res_int = int(res_str)
    return res_int


def compute_distribution(in_sorted_vector, n_output_vec_size):
    """
    Under normal sercumstance we would make a histogram but in our condition we do not have manny sample points and no
    heuristic will solve all the cases so we solve the problem by using convolution
    :param in_sorted_vector:   Sample points
    :param n_output_vec_size:  Number of output sample points
    :return: Distribution as explained above
    """
    filter_size = int(n_output_vec_size / 10.0)
    con_filter = np.array([0.0 for i in range(filter_size)], float)
    con_filter.fill(1.0 / float(filter_size))

    padding = (in_sorted_vector[-1] - in_sorted_vector[0]) / 10.0
    fx_x_val = np.linspace(in_sorted_vector[0] - padding, in_sorted_vector[-1] + padding, num=n_output_vec_size)
    fx = np.zeros(n_output_vec_size)

    ii = 0
    for val in in_sorted_vector:
        while ii < len(fx_x_val) and abs(fx_x_val[ii] - val) > abs(fx_x_val[ii+1] - val):
            ii += 1
        fx[ii] += 1

    fx = np.convolve(fx, con_filter, 'same')
    fx = fx / np.sum(fx)

    return fx_x_val, fx
