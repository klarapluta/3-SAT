import random
import time

# === 1. RDZEŃ WASZEGO ALGORYTMU (DO TESTÓW) ===
def simplify(clauses, var, val):
    new_clauses = []
    for clause in clauses:
        is_satisfied = False
        new_clause = []
        for literal in clause:
            v = abs(literal)
            sign = 1 if literal > 0 else 0
            if v == var:
                if val == sign:
                    is_satisfied = True
                    break
            else:
                new_clause.append(literal)
        if not is_satisfied:
            if not new_clause:
                return None
            new_clauses.append(new_clause)
    return new_clauses

def solve(clauses, n_vars, assignments):
    if not clauses:
        return {i: assignments.get(i, 0) for i in range(1, n_vars + 1)}
    clause = clauses[0]
    
    # Ścieżka 1
    l1 = clause[0]
    v1, val1 = abs(l1), (1 if l1 > 0 else 0)
    res1 = simplify(clauses, v1, val1)
    if res1 is not None:
        new_assign = assignments.copy()
        new_assign[v1] = val1
        final = solve(res1, n_vars, new_assign)
        if final: return final
        
    # Ścieżka 2
    if len(clause) >= 2:
        l2 = clause[1]
        v2, val2 = abs(l2), (1 if l2 > 0 else 0)
        res2 = simplify(clauses, v1, 1 - val1)
        if res2 is not None:
            res2 = simplify(res2, v2, val2)
            if res2 is not None:
                new_assign = assignments.copy()
                new_assign[v1], new_assign[v2] = 1 - val1, val2
                final = solve(res2, n_vars, new_assign)
                if final: return final
                
    # Ścieżka 3
    if len(clause) >= 3:
        l3 = clause[2]
        v3, val3 = abs(l3), (1 if l3 > 0 else 0)
        res3 = simplify(clauses, v1, 1 - val1)
        if res3 is not None:
            res3 = simplify(res3, abs(clause[1]), 1 - (1 if clause[1] > 0 else 0))
            if res3 is not None:
                res3 = simplify(res3, v3, val3)
                if res3 is not None:
                    new_assign = assignments.copy()
                    new_assign[v1] = 1 - val1
                    new_assign[abs(clause[1])] = 1 - (1 if clause[1] > 0 else 0)
                    new_assign[v3] = val3
                    final = solve(res3, n_vars, new_assign)
                    if final: return final
    return None

# === 2. FUNKCJA GENERUJĄCA I URUCHAMIAJĄCA TESTY ===
def run_full_benchmark(n, m):
    print(f"Rozpoczynam generowanie i testowanie 10 instancji dla n={n}, m={m}...\n")
    print(f"{'ID Testu':<10} | {'Status wyniku':<18} | {'Czas wykonania':<15}")
    print("-" * 50)
    
    total_time = 0.0
    
    for i in range(1, 11):
        # 1. Generowanie losowej instancji w pamięci (bez potrzeby zapisu wielu plików na dysk)
        clauses = []
        for _ in range(m):
            vars_sample = random.sample(range(1, n + 1), 3)
            clause = [v if random.random() > 0.5 else -v for v in vars_sample]
            clauses.append(clause)
            
        # 2. Pomiar czasu i wykonanie algorytmu
        start_time = time.time()
        result = solve(clauses, n, {})
        end_time = time.time()
        
        execution_time = end_time - start_time
        total_time += execution_time
        
        status = "ROZWIĄZYWALNE" if result is not None else "NIEROZWIĄZYWALNE"
        
        print(f"Test {i:<5} | {status:<18} | {execution_time:.4f} s")
        
    avg_time = total_time / 10
    print("-" * 50)
    print(f"ŚREDNI CZAS DLA n={n}, m={m}: {avg_time:.4f} sekund\n")

# === 3. WYWOŁANIE PROGRAMU ===
# Możesz tu wpisać dowolne wartości, żeby sprawdzić jak program reaguje
run_full_benchmark(n=40, m=200)