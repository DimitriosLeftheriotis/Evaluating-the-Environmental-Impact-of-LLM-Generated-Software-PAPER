def edit_distance(str1: str, str2: str) -> int:
    m, n = len(str1), len(str2)
    
    # Create a DP table with dimensions (m + 1) x (n + 1)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i  # Deleting all characters from str1 to match empty str2
    for j in range(n + 1):
        dp[0][j] = j  # Inserting all characters to match str2 from empty str1
        
    # Populate the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # No operation needed
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],    # Deletion
                    dp[i][j - 1],    # Insertion
                    dp[i - 1][j - 1] # Substitution
                )
                
    return dp[m][n]