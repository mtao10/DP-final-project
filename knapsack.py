import numpy as np


def main():
    test_values = [([3, 4], [2, 1], 0),
                   ([], [], 24),
                   ([2, 3, 4, 5, 9], [3, 4, 5, 8, 10], 20),
                   ([3, 2, 4, 1], [100, 20, 60, 40], 5),
                   ([5, 5, 5, 4, 10], [15, 17, 3, 18, 21], 23),
                   ([12, 13, 34, 45, 1123, 12, 14, 5, 123, 123, 6, 345, 67, 3, 2],
                        [100, 31, 44, 4, 123, 120, 4, 52, 23, 73, 60, 34, 71, 13, 21], 1700)]
    for t in test_values:
        weights = t[0]
        vals = t[1]
        W = t[2]
        n = len(vals)
        r = knapsack_simple(W, weights, vals, n)
        print('Weights:', weights)
        print('Values:', vals)
        print('Knapsack Capacity:', W)
        print('Using simple recursion, the optimal knapsack value is', r)

        (s, itms) = knapsack_dp(W, weights, vals, n)
        print('Using DP, the optimal knapsack value is', r)
        print('The (value, weight) item pairs in the optimal knapsack are: ', itms)
        print('\n')


def knapsack_simple(max_wght, itm_wghts, itm_vals, n):
    # base case, 0 capacity or 0 items available to take
    if max_wght == 0 or n == 0:
        return 0
    # if the (n-1)th (idx from 0) item doesn't fit, don't include it
    if itm_wghts[n-1] > max_wght:
        return knapsack_simple(max_wght, itm_wghts, itm_vals, n-1)
    # if (n-1)th will fit, see if including it or not results in more value
    else:
        return max(itm_vals[n-1] + knapsack_simple(max_wght - itm_wghts[n-1], itm_wghts, itm_vals, n-1),
                   knapsack_simple(max_wght, itm_wghts, itm_vals, n-1))


def knapsack_dp(max_weight, itm_weights, itm_values, n):
    # DP table
    # number of items available = # of rows
    # {0, 1,..., max weight} = columns
    bvals = np.zeros((n+1, max_weight + 1), dtype=int)

    # fill in DP table by row
    for i in range(1, n+1):
        for j in range(1, max_weight+1):
            if itm_weights[i-1] > j:
                # if ith item can't be included in knapsack with weight limit j
                # then optimal weight is the optimal weight with i-1 items
                bvals[i][j] = bvals[i-1][j]
            else:
                # check if optimal to include ith item or not
                bvals[i][j] = max(bvals[i-1][j],
                                  itm_values[i-1] + bvals[i-1][j - itm_weights[i-1]])

    # find items that produced optimal value by backtracking through DP table
    # start at bottom-most right-most entry of DP table
    itm_list = []
    wght_left = max_weight
    for i in range(n, 0, -1):
        # if optimal value w/ item i is not equal to optimal value w/ everything before i
        # then we took item i in the knapsack
        if bvals[i][wght_left] != bvals[i-1][wght_left]:
            itm_list.append((itm_values[i-1], itm_weights[i-1]))
            wght_left = wght_left - itm_weights[i-1]

    opt_value = bvals[n][max_weight]
    return opt_value, itm_list


if __name__ == "__main__":
    main()
