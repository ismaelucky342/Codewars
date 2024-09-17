MOD = 998244353

# Precompute modular inverses for numbers 1 to 80000
mod_inverse = [0, 1]  # Inverse of 1 is 1
for num in range(2, 80001):
    mod_inverse.append(((num - mod_inverse[MOD % num]) * (MOD // num) + MOD % num) % MOD)

def height(n, m):
    result = 0
    current_term = 1
    m %= MOD  # Ensure m is within the MOD range
    
    for i in range(1, n + 1):
        current_term = current_term * (m - i + 1) * mod_inverse[i] % MOD
        result = (result + current_term) % MOD
    
    return result % MOD