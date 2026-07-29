def edit_distance(str1: str, str2: str) -> int:
    m, n = len(str1), len(str2)

    # dp[i][j] = edit distance between str1[:i] and str2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i  # delete all i characters from str1
    for j in range(n + 1):
        dp[0][j] = j  # insert all j characters to build str2

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # deletion
                    dp[i][j - 1],      # insertion
                    dp[i - 1][j - 1],  # substitution
                )

    return dp[m][n]