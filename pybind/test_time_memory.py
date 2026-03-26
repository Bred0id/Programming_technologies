import time
import random
import psutil
import multiprocessing as mp
from fastdict import FastDict

def benchmark_add(struct, keys, runs):
    total = 0
    for i in range(runs):
        s = struct()
        start = time.perf_counter()
        for k in keys:
            s[k] = k
        total += time.perf_counter() - start
    return total / runs

def benchmark_find(struct, keys, runs):
    total = 0
    for i in range(runs):
        s = struct()
        for k in keys:
            s[k] = k
        start = time.perf_counter()
        for k in keys:
            s[k]
        total += time.perf_counter() - start
    return total / runs

def benchmark_delete(struct, keys, runs):
    total = 0
    for i in range(runs):
        s = struct()
        for k in keys:
            s[k] = k
        start = time.perf_counter()
        for k in keys:
            try:
                del s[k]
            except KeyError:
                pass
        total += time.perf_counter() - start
    return total / runs

def benchmark_repeated_find(struct, keys, repeats, runs):
    total = 0
    for i in range(runs):
        s = struct()
        for k in keys:
            s[k] = k
        s[keys[len(keys)//2]]
        start = time.perf_counter()
        for j in range(repeats):
            s[keys[len(keys)//2]]
        total += time.perf_counter() - start
    return total / runs

def _memory_worker(struct_name, keys, conn):
    if struct_name == "FastDict":
        s = FastDict()
    else:
        s = {}
    for k in keys:
        s[k] = k
    conn.send(True)
    conn.close()
    time.sleep(0.2)

def memory_test(struct_name, keys):
    parent_conn, child_conn = mp.Pipe()
    p = mp.Process(target=_memory_worker, args=(struct_name, keys, child_conn))
    p.start()
    process = psutil.Process(p.pid)
    peak = 0
    ready = False
    while p.is_alive():
        try:
            rss = process.memory_info().rss
            if rss > peak:
                peak = rss
        except psutil.Error:
            break
        if parent_conn.poll():
            ready = parent_conn.recv()
        time.sleep(0.01)
    p.join()
    return peak if ready else 0

def test_random_data():
    n = 1000000
    runs = 3
    print()
    print("RANDOM DATA")
    keys = [random.randint(0,10**9) for i in range(n)]
    print("ADD")
    fd_add = benchmark_add(FastDict,keys,runs)
    d_add = benchmark_add(dict,keys,runs)
    print(f"{'FastDict:':10} {fd_add:.6f} s")
    print(f"{'dict:':10} {d_add:.6f} s")
    print("FIND")
    fd_find = benchmark_find(FastDict,keys,runs)
    d_find = benchmark_find(dict,keys,runs)
    print(f"{'FastDict:':10} {fd_find:.6f} s")
    print(f"{'dict:':10} {d_find:.6f} s")
    print("DELETE")
    fd_del = benchmark_delete(FastDict,keys,runs)
    d_del = benchmark_delete(dict,keys,runs)
    print(f"{'FastDict:':10} {fd_del:.6f} s")
    print(f"{'dict:':10} {d_del:.6f} s")
    print("REPEATED FIND")
    fd_rep = benchmark_repeated_find(FastDict,keys,n,runs)
    d_rep = benchmark_repeated_find(dict,keys,n,runs)
    print(f"{'FastDict:':10} {fd_rep:.6f} s")
    print(f"{'dict:':10} {d_rep:.6f} s")
    print("MEMORY")
    mem_fd = memory_test("FastDict",keys)
    mem_d = memory_test("dict",keys)
    print(f"{'FastDict:':10} {mem_fd/1024:.2f} KB")
    print(f"{'dict:':10} {mem_d/1024:.2f} KB")
    assert True

def test_localized_data():
    n = 1000000
    key_range = 100
    runs = 5
    print()
    print("LOCALIZED DATA")
    keys = [random.randint(1,key_range) for i in range(n)]
    print("ADD")
    fd_add = benchmark_add(FastDict,keys,runs)
    d_add = benchmark_add(dict,keys,runs)
    print(f"{'FastDict:':10} {fd_add:.6f} s")
    print(f"{'dict:':10} {d_add:.6f} s")
    print("FIND")
    fd_find = benchmark_find(FastDict,keys,runs)
    d_find = benchmark_find(dict,keys,runs)
    print(f"{'FastDict:':10} {fd_find:.6f} s")
    print(f"{'dict:':10} {d_find:.6f} s")
    print("DELETE")
    fd_del = benchmark_delete(FastDict,keys,runs)
    d_del = benchmark_delete(dict,keys,runs)
    print(f"{'FastDict:':10} {fd_del:.6f} s")
    print(f"{'dict:':10} {d_del:.6f} s")
    print("REPEATED FIND")
    fd_rep = benchmark_repeated_find(FastDict,keys,n,runs)
    d_rep = benchmark_repeated_find(dict,keys,n,runs)
    print(f"{'FastDict:':10} {fd_rep:.6f} s")
    print(f"{'dict:':10} {d_rep:.6f} s")
    print("MEMORY")
    mem_fd = memory_test("FastDict",keys)
    mem_d = memory_test("dict",keys)
    print(f"{'FastDict:':10} {mem_fd/1024:.2f} KB")
    print(f"{'dict:':10} {mem_d/1024:.2f} KB")
    assert True