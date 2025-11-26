"""Benchmark script for profiling auto-login tests
Measures precise timing for optimization comparison
"""
import time
import statistics
from unittest.mock import Mock, MagicMock, patch

# Import the functions we want to benchmark
from rotkehlchen.db.settings import (
    DEFAULT_AUTO_LOGIN_COUNT,
    DEFAULT_AUTO_LOGIN_CONFIRMATION_THRESHOLD,
    MIN_AUTO_LOGIN_CONFIRMATION_THRESHOLD,
    MAX_AUTO_LOGIN_CONFIRMATION_THRESHOLD,
    CachedSettings,
    DBSettings,
)


def benchmark_cached_settings_operations(iterations=1000):
    """Benchmark CachedSettings get/set operations"""
    times = []
    
    for _ in range(iterations):
        # Setup
        cached = CachedSettings()
        settings = DBSettings()
        settings.auto_login_count = 5
        cached.initialize(settings)
        
        # Measure
        start = time.perf_counter()
        
        # Operations
        value = cached.get_entry('auto_login_count')
        cached.update_entry('auto_login_count', 10)
        result = cached.get_entry('auto_login_count')
        
        end = time.perf_counter()
        times.append(end - start)
    
    return {
        'mean': statistics.mean(times) * 1_000_000,  # microseconds
        'median': statistics.median(times) * 1_000_000,
        'stdev': statistics.stdev(times) * 1_000_000 if len(times) > 1 else 0,
        'min': min(times) * 1_000_000,
        'max': max(times) * 1_000_000,
    }


def benchmark_validation_checks(iterations=10000):
    """Benchmark validation logic"""
    times = []
    
    for _ in range(iterations):
        start = time.perf_counter()
        
        # Validation operations
        valid = (MIN_AUTO_LOGIN_CONFIRMATION_THRESHOLD <= 
                DEFAULT_AUTO_LOGIN_CONFIRMATION_THRESHOLD <= 
                MAX_AUTO_LOGIN_CONFIRMATION_THRESHOLD)
        
        count_valid = DEFAULT_AUTO_LOGIN_COUNT >= 0
        threshold_min = MIN_AUTO_LOGIN_CONFIRMATION_THRESHOLD == 3
        threshold_max = MAX_AUTO_LOGIN_CONFIRMATION_THRESHOLD == 10
        
        end = time.perf_counter()
        times.append(end - start)
    
    return {
        'mean': statistics.mean(times) * 1_000_000,  # microseconds
        'median': statistics.median(times) * 1_000_000,
        'stdev': statistics.stdev(times) * 1_000_000 if len(times) > 1 else 0,
        'min': min(times) * 1_000_000,
        'max': max(times) * 1_000_000,
    }


def benchmark_mock_operations(iterations=1000):
    """Benchmark Mock object creation and usage"""
    times = []
    
    for _ in range(iterations):
        start = time.perf_counter()
        
        # Create and use mocks
        mock_cursor = Mock()
        mock_db = MagicMock()
        mock_db.set_setting.return_value = None
        mock_db.get_setting.return_value = 5
        
        # Simulate operations
        value = mock_db.get_setting(mock_cursor, 'auto_login_count')
        mock_db.set_setting(mock_cursor, 'auto_login_count', 10)
        
        end = time.perf_counter()
        times.append(end - start)
    
    return {
        'mean': statistics.mean(times) * 1_000_000,
        'median': statistics.median(times) * 1_000_000,
        'stdev': statistics.stdev(times) * 1_000_000 if len(times) > 1 else 0,
        'min': min(times) * 1_000_000,
        'max': max(times) * 1_000_000,
    }


def benchmark_singleton_pattern(iterations=5000):
    """Benchmark singleton pattern access"""
    times = []
    
    for _ in range(iterations):
        start = time.perf_counter()
        
        # Access singleton
        instance1 = CachedSettings()
        instance2 = CachedSettings()
        is_same = instance1 is instance2
        
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
    """Print benchmark results in a nice format"""
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
    print("  AUTO-LOGIN PERFORMANCE BENCHMARK - BEFORE OPTIMIZATION")
    print("="*70)
    
    # Run benchmarks
    print("\n[1/4] Benchmarking CachedSettings operations...")
    results1 = benchmark_cached_settings_operations(1000)
    print_results("CachedSettings Operations (1000 iterations)", results1)
    
    print("\n[2/4] Benchmarking validation checks...")
    results2 = benchmark_validation_checks(10000)
    print_results("Validation Checks (10000 iterations)", results2)
    
    print("\n[3/4] Benchmarking mock operations...")
    results3 = benchmark_mock_operations(1000)
    print_results("Mock Operations (1000 iterations)", results3)
    
    print("\n[4/4] Benchmarking singleton pattern...")
    results4 = benchmark_singleton_pattern(5000)
    print_results("Singleton Pattern Access (5000 iterations)", results4)
    
    print("\n" + "="*70)
    print("  BENCHMARK COMPLETE")
    print("="*70)
    
    # Save results to file
    with open('benchmark_before.txt', 'w') as f:
        f.write("BEFORE OPTIMIZATION\n")
        f.write("="*70 + "\n\n")
        f.write(f"CachedSettings Operations: {results1['mean']:.3f} µs (mean)\n")
        f.write(f"Validation Checks: {results2['mean']:.3f} µs (mean)\n")
        f.write(f"Mock Operations: {results3['mean']:.3f} µs (mean)\n")
        f.write(f"Singleton Pattern: {results4['mean']:.3f} µs (mean)\n")
    
    print("\nResults saved to: benchmark_before.txt")
