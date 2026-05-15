import os
import random
import time

# funkcja do wczytania danych wejściowych
def load(data):
    if not os.path.exists(data):
        return None, None, None
    with open(data, 'r') as df:
        lines = df.readlines()
        n_vars, n_clauses = map(int, lines[0].split())
        clauses = [list(map(int, line.split())) for line in lines[1:n_clauses + 1]]
    return n_vars, n_clauses, clauses  # n_vars - liczba zmiennych; n-clauses - liczba klauzul; clauses - klauzule


# funckja do upraszczania formuły (var - zmienna, val - wartość (0, 1), którą przypisujemy zmiennej var)
def simplify(clauses, var, val):
    new_clauses = []
    for clause in clauses:
        is_ok = False
        new_clause = []
        for literal in clause:
            v = abs(literal)  # wyciągamy nr zmiennej
            sign = 1 if literal > 0 else 0
            if v == var:
                if val == sign:
                    is_ok = True
                    break
                else:
                    continue
            else:
                new_clause.append(literal)

        if not is_ok:
            if not new_clause:
                return None
            new_clauses.append(new_clause)
    return new_clauses

def solve(clauses, n_vars, assignments):
    if not clauses:
        # jeżeli dla którejś zmiennej nie została przypisana wartość, to wstawiamy 0
        full_assignments = {i: assignments.get(i, 0) for i in range(1, n_vars+1)}
        return full_assignments

    clause = clauses[0]
    num_literals = len(clause)

    # ścieżka 1 - l1 = True
    l1 = clause[0]
    v1 = abs(l1)
    val1 = (1 if l1 > 0 else 0)
    res1 = simplify(clauses, v1, val1)
    if res1 is not None:
        new_assign = assignments.copy()
        new_assign[v1] = val1
        final = solve(res1, n_vars, new_assign)
        if final: return final

    # Ścieżka 2: l1 = False, l2 = True
    if num_literals >= 2:
        l2 = clause[1]
        v2 = abs(l2)
        val2 = 1 if l2 > 0 else 0
        res2 = simplify(clauses, v1, 1 - val1)
        if res2 is not None:
            res2 = simplify(res2, v2, val2)
            if res2 is not None:
                new_assign = assignments.copy()
                new_assign[v1] = 1 - val1
                new_assign[v2] = val2
                final = solve(res2, n_vars, new_assign)
                if final: return final

    # Ścieżka 3: l1 = False, l2 = False, l3 = True
    if num_literals == 3:
        l3 = clause[2]
        v3 = abs(l3)
        val3 = 1 if l3 > 0 else 0
        res3 = simplify(clauses, v1, 1-val1)
        if res3 is not None:
            res3 = simplify(res3, v2, 1 - val2)
            if res3 is not None:
                res3 = simplify(res3, v3, val3)
                if res3 is not None:
                    new_assign = assignments.copy()
                    new_assign[v1] = 1 - val1
                    new_assign[v2] = 1 - val2
                    new_assign[v3] = val3
                    final = solve(res3, n_vars, new_assign)
                    if final: return final
        return None
    
def generate_instance(n, m, filename="przyklad.txt"):
    with open(filename, 'w') as f:
        f.write(f"{n} {m}\n")
        for _ in range(m):
            vars_sample = random.sample(range(1, n + 1), 3)
            clause = [v if random.random() > 0.5 else -v for v in vars_sample]
            f.write(f"{clause[0]} {clause[1]} {clause[2]}\n")


def main():
    input_file = "przyklad.txt"
    n_vars, n_clauses, clauses = load(input_file)

    if n_vars is None:
        print(f"Błąd: Nie znaleziono pliku {input_file}")
        return

    result = solve(clauses, n_vars, {})

    with open("wynik.txt", "w") as f:
        if result:
            f.write("Status: ROZWIĄZYWALNE\n")
            res_str = " ".join(str(result[i]) for i in range(1, n_vars + 1))
            f.write(f"Rozwiązanie: {res_str}")
        else:
            f.write("Status: NIEROZWIĄZYWALNE\n")


if __name__ == "__main__":
    main()
