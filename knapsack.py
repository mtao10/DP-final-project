import numpy as np


def main():
    test_values = [([2, 3, 4, 5, 9], [3, 4, 5, 8, 10], 20)]
    for t in test_values:
        weights = t[0]
        vals = t[1]
        W = t[2]
        n = len(vals)
        r = knapsack_simple(W, weights, vals, n)
        print(r)


def knapsack_simple(max_wght, itm_wghts, itm_vals, n):
    # base case, 0 capacity or 0 items available to take
    if max_wght == 0 or n == 0:
        return 0
    # if the (n-1)th (idx from 0) item doesn't fit, don't include it
    if itm_wghts[n-1] > max_wght:
        return knapsack_simple(max_wght, itm_wghts, itm_vals, n-1)
    # if (n-1)th will fit, see if including it or not results in more benefit
    else:
        return max(itm_vals[n-1] + knapsack_simple(max_wght - itm_wghts[n-1], itm_wghts, itm_vals, n-1),
                   knapsack_simple(max_wght, itm_wghts, itm_vals, n-1))


def knapsack_dp(max_weight, itm_weights, itm_values, n):
    bvals = np.zeros(n+1, max_weight + 1, dtype=int)


if __name__ == "__main__":
    main()
