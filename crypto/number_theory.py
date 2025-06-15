import numpy as np

from crypto.crypto_util import RSAUtil


def extend_euclid(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d0, x0, y0 = extend_euclid(b, a % b)
        d, x, y = d0, y0, x0 - a // b * y0
        return d, x, y


def modular_linear_equation_solver(a, b, n):
    d, x_, y_ = extend_euclid(a, n)
    res = []
    if b % d == 0:
        x0 = (x_ * b // d) % n
        for i in range(d):
            res.append((x0 + i * (n // d)) % n)
    return res


def china_mod(kv):
    n = 1
    for k in kv:
        n *= k
    a = 0
    for ni, ai in kv.items():
        mi = n // ni
        a += modular_linear_equation_solver(mi, 1, ni)[0] * mi * ai
    return a % n


def modular_exponentiation(a, b, n):
    c = 0
    d = 1
    arr = []
    x = b
    while x > 0:
        arr.append(x & 1)
        x = x >> 1

    for bi in reversed(arr):
        c = 2 * c
        d = (d * d) % n
        if bi == 1:
            c = c + 1
            d = (d * a) % n
    return d


def pseudo_prime(n):
    if n == 2:
        return True
    return modular_exponentiation(2, n - 1, n) == 1


def witness(a, n):
    t = 1
    while ((n - 1) >> t) & 1 == 0:
        t += 1
    u = (n - 1) >> t
    x0 = modular_exponentiation(a, u, n)
    x1 = x0
    for i in range(1, t + 1):
        x1 = (x0 ** 2) % n
        if x1 == 1 and x0 != 1 and x0 != n - 1:
            return True
        x0 = x1
    if x1 != 1:
        return True
    return False


def miller_rabin(n, s=10):
    if n == 2:
        return True
    a_list = np.random.randint(1, n, s)
    for a in a_list:
        if witness(a, n):
            return False
    return True


def primes(n):
    if n < 2:
        return np.array([], dtype=np.int8)
    lis = np.array([], dtype=np.int8)
    loc = np.ones(n, dtype=np.ubyte)
    for i in range(2, n + 1):
        if i * i <= n and loc[i - 1] == 1:
            lis = np.append(lis, i)
            for j in range(2, n // i + 1):
                loc[j * i - 1] = 0
        elif loc[i - 1] == 1:
            lis = np.append(lis, i)
    return lis, loc


def check_prime(n=1000):
    _, loc = primes(n)
    r1 = []
    r2 = []
    for i in range(2, n + 1):
        is_prime = loc[i-1] == 1
        p1 = pseudo_prime(i)
        p2 = miller_rabin(i, 20)
        if p1 != is_prime:
            r1.append(i)
        if p2 != is_prime:
            r2.append(i)
    print("Traditional pseudo prime number list: %s" % r1)
    print("Miller Rabin pseudo prime number list: %s"% r2)

class RSA:
    def __init__(self, p, q, e):
        self.__p = p
        self.__q = q
        self.__n = p * q
        self.__theta = (p - 1) * (q - 1)
        if e is None:
            i = 1
            while True:
                e = i * 2 + 1
                gcd, _, _ = extend_euclid(self.__theta, e)
                if gcd == 1:
                    break
                else:
                    i += 1
        self.__e = e
        self.__d = modular_linear_equation_solver(e, 1, self.__theta)[0]

    def encrypt(self, m):
        return modular_exponentiation(m, self.__e, self.__n)

    def decrypt(self, m):
        return modular_exponentiation(m, self.__d, self.__n)


if __name__ == '__main__':
    rsa_util = RSAUtil()
    rsa_util.generate_keys()
    public_key = rsa_util.public_key
    private_key = rsa_util.private_key
    print(f"""
    p: {private_key.p}
    q: {private_key.q}
    e: {private_key.e}
    """)

    rsa = RSA(private_key.p, private_key.q, private_key.e)
    encrypto = rsa.encrypt(12345)
    print(encrypto)
    original = rsa.decrypt(encrypto)
    print(original)
