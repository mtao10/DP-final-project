import numpy as np
import time


def main():
    test_values = [(0, 0), (0, 10), (13, 0),  # edge cases
                   (3, 2), (7, 4), (10, 8),  # regular cases
                   (4, 9), (5, 10),  # k > n cases
                   (15, 10), (20, 10), (25, 10),   # as n increases
                   (30, 10), (30, 15), (30, 20)]  # as k increases

    for t in test_values:
        tic = time.perf_counter()
        res = binomial_simple(t[0], t[1])
        toc = time.perf_counter()
        print('Simple Recursion')
        print(t[0], ' choose ', t[1], ' = ', res)
        r = toc-tic
        print('Runtime: ', r)

        tic_dp = time.perf_counter()
        res_dp = binomial_dp(t[0], t[1])
        toc_dp = time.perf_counter()
        print('Dynamic Programming')
        print(t[0], ' choose ', t[1], ' is ', res_dp)
        rdp = toc_dp - tic_dp
        print('Runtime: ', rdp)
        speed = r/rdp
        if speed > 1:
            print('DP is ', speed, 'times faster than simple recursion')
        else:
            print('Simple recursion is ', rdp/r, 'times faster than DP')
        print('\n')


def binomial_simple(n,k):
    if k == 0 or k == n:
        return 1
    if k == 0 or n == 0 or k > n:
        return 0
    else:
        return binomial_simple(n-1, k-1) + binomial_simple(n-1, k)


def binomial_dp(n, k):
    cvals = np.zeros((n+1, k+1), dtype=int)  # DP table of values for (n choose k) - n rows, k columns

    # DP table leftmost column initialization
    for c in range(0, n+1):  # set (n choose 0) = 1
        cvals[c][0] = 1

    # fill in table (by column) using (n choose k) = (n-1 choose k-1) + (n-1 choose k)
    for j in range(1, k+1):
        for i in range(j, n+1):
            cvals[i][j] = cvals[i-1][j-1] + cvals[i-1][j]

    # desired binomial coefficient is in right-most bottom-most table entry
    return cvals[n][k]


if __name__ == "__main__":
    main()