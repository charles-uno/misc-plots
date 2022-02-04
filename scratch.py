#!/usr/bin/env python3

# one dino with 0 damage on it
dinos = [1]

for _ in range(19):
    # However many dinos we have, we create that many more with each activation
    n = sum(dinos)
    dinos.append(n)
    # Once a dino has been around for 6 iterations, it's out
    dinos = dinos[-6:]
    print(*dinos)

print(sum(dinos), "dinos")
print(6*sum(dinos)+19)

print('hello')
