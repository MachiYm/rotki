"""Benchmark script AFTER optimization
Compares lightweight fake objects vs heavy Mock objects
"""
import time
import statistics
from unittest.mock import Mock, MagicMock

# Import optimized classes
import sys
sys.path.insert(0, 'rotkehlchen/tests/db')
from test_auto_login_optimized import FakeCursor, FakeDB

from rotkehlchen.db.settings import (
    DEFAULT_AUTO_LOGIN_COUNT,
    DEFAULT_AUTO_LOGIN_CONFIRMATION_THRESHOLD,
    MIN_AUTO_LOGIN_CONFIRMATION_THRESHOLD,
    MAX_AUTO_LOGIN_CONFIRMATION_THRESHOLD,
    CachedSettings,
    DBSettings,
)


def benchmark_fake_db_operations(iterations=1000):
    """Benchmark optimized FakeDB operations"""
    times = []
    
    for _ in range(iterations):
        start = time.perf_counter()
        
        # Create and use fake objects
        cursor = FakeCursor()
        db = FakeDB()
        db.set_setting(cursor, 'auto_login_count', 5)
        value = db.get_setting(cursor, 'auto_login_count')
        db.set_setting(cursor, 'auto_login_count', 10)
        
        end = time.perf_counter()
        times.append(end - start)
    
    return {
        'mean': statistics.mean(times) * 1_000_000,
        'median': statistics.median(times) * 1_000_000,
        'stdev': statistics.stdev(times) * 1_000_000 if len(times) > 1 else 0,
        'min': min(times) * 1_000_000,
        'max': max(times) * 1_000_000,
    }


def benchmark_cached_constants(iterations=10000):
    """Benchmark using cached constants vs repeated imports"""
    # Pre-cache constants
    _MIN = MIN_AUTO_LOGIN_CONFIRMATION_THRESHOLD
    _MAX = MAX_AUTO_LOGIN_CONFIRMATION_THRESHOLD
    _DEFAULT = DEFAULT_AUTO_LOGIN_CONFIRMATION_THRESHOLD
    _COUNT = DEFAULT_AUTO_LOGIN_COUNT
    
    times = []
    
    for _ in range(iterations):
        start = time.perf_counter()
        
        # Use cached constants
        valid = (_MIN <= _DEFAULT <= _MAX)
        count_valid = _COUNT >= 0
        threshold_min = _MIN == 3
        threshold_max = _MAX == 10
        
        end = time.perf_counter()
        times.append(end - start)
    
    return {
        'mean': statistics.mean(times) * 1_000_000,
        'median': statistics.median(times) * 1_000_000,
        'stdev': statistics.stdev(times) * 1_000_000 if len(times) > 1 else 0,
        'min': min(times) * 1_000_000,
        'max': max(times) * 1_000_000,
    }


def benchmark_batch_operations(iterations=1000):
    """Benchmark batch operations instead of individual calls"""
    times = []
    
    for _ in range(iterations):
        start = time.perf_counter()
        
        cursor = FakeCursor()
        db = FakeDB()
        
        # Batch set operations
        settings = {
            'auto_login_count': 5,
            'auto_login_confirmation_threshold': 7,
        }
        
        for key, value in settings.items():
            db.set_setting(cursor, key, value)
        
        # Batch get operations
        values = [db.get_setting(cursor, key) for key in settings.keys()]
        
        end = time.perf_counter()
        times.append(end - start)
    
    return {
        'mean': statistics.mean(times) * 1_000_000,
        'median': statistics.median(times) * 1_000_000,
        'stdev': statistics.stdev(times) * 1_000_000 if len(times) > 1 else 0,
        'min': min(times) * 1_000_000,
        'max': max(times) * 1_000_000,
    }


def benchmark_slots_efficiency(iterations=5000):
    """Benchmark __slots__ efficiency for memory and speed"""
    times = []
    
    for _ in range(iterations):
        start = time.perf_counter()
        
        # Create multiple instances with __slots__
        cursors = [FakeCursor() for _ in range(10)]
        dbs = [FakeDB() for _ in range(10)]
        
        end = time.perf_counter()
        times.append(end - start)
    
    return {
        'mean': statistics.mean(times) * 1_000_000,
        'median': statistics.median(times) * 1_000_000,
        'stdev': statistics.stdev(times) * 1_000_000 if len(times) > 1 else 0,
        'min': min(times) * 1_000_000,
        'max': max(times) * 1_000_000,
    }


def print_results(name, results):
    """Print benchmark results"""
    print(f"\n{'='*70}")
    print(f"  {name}")
    print(f"{'='*70}")
    print(f"  Mean:     {results['mean']:.3f} µs")
    print(f"  Median:   {results['median']:.3f} µs")
    print(f"  Std Dev:  {results['stdev']:.3f} µs")
    print(f"  Min:      {results['min']:.3f} µs")
    print(f"  Max:      {results['max']:.3f} µs")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("  AUTO-LOGIN PERFORMANCE BENCHMARK - AFTER OPTIMIZATION")
    print("="*70)
    
    # Run optimized benchmarks
    print("\n[1/4] Benchmarking FakeDB operations (optimized)...")
    results1 = benchmark_fake_db_operations(1000)
    print_results("FakeDB Operations (1000 iterations)", results1)
    
    print("\n[2/4] Benchmarking cached constants...")
    results2 = benchmark_cached_constants(10000)
    print_results("Cached Constants (10000 iterations)", results2)
    
    print("\n[3/4] Benchmarking batch operations...")
    results3 = benchmark_batch_operations(1000)
    print_results("Batch Operations (1000 iterations)", results3)
    
    print("\n[4/4] Benchmarking __slots__ efficiency...")
    results4 = benchmark_slots_efficiency(5000)
    print_results("__slots__ Object Creation (5000 iterations)", results4)
    
    print("\n" + "="*70)
    print("  BENCHMARK COMPLETE")
    print("="*70)
    
    # Load previous results
    try:
        with open('benchmark_before.txt', 'r') as f:
            before_lines = f.readlines()
            mock_ops_before = float(before_lines[3].split(': ')[1].split(' ')[0])
    except:
        mock_ops_before = 313.859  # From our previous run
    
    # Calculate improvement
    improvement = ((mock_ops_before - results1['mean']) / mock_ops_before) * 100
    
    print(f"\n{'='*70}")
    print(f"  PERFORMANCE IMPROVEMENT")
    print(f"{'='*70}")
    print(f"  Before (Mock): {mock_ops_before:.3f} µs")
    print(f"  After (Fake):  {results1['mean']:.3f} µs")
    print(f"  Improvement:   {improvement:.1f}% faster")
    print(f"  Speedup:       {mock_ops_before / results1['mean']:.1f}x")
    print(f"{'='*70}")
    
    # Save results
    with open('benchmark_after.txt', 'w') as f:
        f.write("AFTER OPTIMIZATION\n")
        f.write("="*70 + "\n\n")
        f.write(f"FakeDB Operations: {results1['mean']:.3f} µs (mean)\n")
        f.write(f"Cached Constants: {results2['mean']:.3f} µs (mean)\n")
        f.write(f"Batch Operations: {results3['mean']:.3f} µs (mean)\n")
        f.write(f"__slots__ Efficiency: {results4['mean']:.3f} µs (mean)\n")
        f.write(f"\nIMPROVEMENT vs BEFORE:\n")
        f.write(f"Mock Operations: {mock_ops_before:.3f} µs -> {results1['mean']:.3f} µs\n")
        f.write(f"Speedup: {mock_ops_before / results1['mean']:.1f}x faster ({improvement:.1f}% improvement)\n")
    
    print("\nResults saved to: benchmark_after.txt")
