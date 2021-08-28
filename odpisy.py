#!/usr/bin/env python
from math import ceil
from prettytable import PrettyTable

## GLOBALS AND STUFF ###########################################################

# Vsechno je indexovano podle skupin od 1, napriklad:
# neco[1] = 1. skupina
# neco[2] = 2. skupina
# ...

ROVNOMERNE = 0
ZRYCHLENE  = 1

# Doba odepisovani podle skupin.
doba = [ 0, 3, 5, 10, 20, 30, 50 ]

# ROVNOMERNE __________________________________________________________________
# Sazba pro prvni rok, pro dalsi roky a sazba pro zvysenou vstupni cenu
sazbaPrvni   = [ 0, 20.00, 11.00, 05.50, 2.15, 1.4, 1.02 ]
sazbaDalsi   = [ 0, 40.00, 22.25, 10.50, 5.15, 3.4, 2.02 ]
sazbaZvysena = [ 0, 33.30, 20.00, 10.00, 5.00, 3.4, 2.00 ]

# ZRYCHLENE ___________________________________________________________________
# Koeficienty pro prvni rok, pro dalsi roky a pro zvysenou vstupni cenu
koeficientPrvni   = [ 0, 3, 5, 10, 20, 30, 50 ]
koeficientDalsi   = [ 0, 4, 6, 11, 21, 31, 51 ]
koeficientZvysena = koeficientPrvni

## UTILS #######################################################################

def get_int(msg: str) -> int:
    return int("".join(input(msg).split()))

def is_invalid(skupina: int) -> int:
    if skupina < 1 or skupina > 6:
        return 1
    return 0


def parallelTables(first: PrettyTable, second: PrettyTable) -> None:
    first  = first.get_string().split('\n')
    second = second.get_string().split('\n')
    lineLen = len(first[0])

    sazba1 = f"Sazba pro 1. rok:     {sazbaPrvni[skupina]:.2f}%"
    sazba2 = f"Sazba pro dalsi roky: {sazbaDalsi[skupina]:.2f}%"
    koeficient1 = f"Koeficient pro 1. rok:     {koeficientPrvni[skupina]}"
    koeficient2 = f"Koeficient pro dalsi roky: {koeficientDalsi[skupina]}"
    padding = "    "

    print(sazba1 + padding, end=(" " * (lineLen - len(sazba1))))
    print(koeficient1)
    print(sazba2 + padding, end=(" " * (lineLen - len(sazba2))))
    print(koeficient2)
    for i in range(0, len(first)):
        print(first[i], end=padding)
        print(second[i])
    print("ROVNOMERNE" + padding, end=(" " * (lineLen - len("ROVNOMERNE"))))
    print("ZRYCHLENE")

## CALCS #######################################################################

def rovnomerne(castka: int, skupina: int, rok: int) -> int:
    if rok == 1:
        return int(ceil(castka * sazbaPrvni[skupina] / 100))
    return int(ceil(castka * sazbaDalsi[skupina] / 100))


def zrychlene(castka: int, skupina: int, rok: int) -> int:
    if rok == 1:
        return int(ceil(castka / koeficientPrvni[skupina]))
    return int(ceil((2 * castka) / (koeficientDalsi[skupina] - (rok - 1))))


def calculate(typ: int, vstupniCena: int, skupina: int) -> PrettyTable:
    if is_invalid(skupina):
        return 1

    table = PrettyTable()
    table.field_names = ["Rok", "Odpis", "Opravky", "Zustatek"]

    opravky  = 0
    zustatek = vstupniCena
    for rok in range(1, doba[skupina]+1):
        if typ == ROVNOMERNE:
            odpis = rovnomerne(vstupniCena, skupina, rok)
        else:
            odpis = zrychlene(zustatek, skupina, rok)

        opravky  += odpis
        zustatek -= odpis

        str_odpis    = f"{odpis:_}".replace('_', ' ')
        str_opravky  = f"{opravky:_}".replace('_', ' ')
        str_zustatek = f"{zustatek:_}".replace('_', ' ')
        table.add_row([rok, str_odpis, str_opravky, str_zustatek])

    return table

## MAIN ########################################################################

if __name__ == "__main__":
    cena    = get_int("Cena:    ")
    skupina = get_int("Skupina: ")
    print("-------------------------------------------------------------------")

    r = calculate(ROVNOMERNE, cena, skupina)
    z = calculate(ZRYCHLENE, cena, skupina)

    if r == 1 or z == 1:
        print("Skupina musi byt v rozmezi 1-6")
        exit(1)

    parallelTables(r, z)
