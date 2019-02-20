def modout(num, power, mod):
    total = num
    for i in range(1, power):
        total = (total * num) % mod
    return total

print modout(723, 11,947)
