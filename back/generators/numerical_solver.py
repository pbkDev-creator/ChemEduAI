def solve_heat_conduction(k, A, T1, T2, L):

    deltaT = T1 - T2

    Q = (k * A * deltaT) / L

    solution = f"""
HEAT CONDUCTION SOLUTION

--------------------------------------

STEP 1 — GIVEN DATA

k = {k} W/mK

A = {A} m²

T1 = {T1} °C

T2 = {T2} °C

L = {L} m

--------------------------------------

STEP 2 — FORMULA

Q = kA(T1 - T2)/L

--------------------------------------

STEP 3 — SUBSTITUTE VALUES

Q = ({k} × {A} × ({T1} - {T2})) / {L}

--------------------------------------

STEP 4 — CALCULATE

Q = {Q:.2f} W

--------------------------------------

FINAL ANSWER

Heat Transfer Rate = {Q:.2f} W
"""

    return solution