def lin(l1,l2):
    for i in l1:
        if not i in l2:
            return False
    return True