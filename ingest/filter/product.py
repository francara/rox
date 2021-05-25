
def filterProduct(catalog, row) -> bool:
    print(f'\tFiltering {row[0]}')
    if int(row[0]) % 2 == 0:
        return True
    return False
