"""Direct comparison: Mock vs Fake objects performance"""
import time
import statistics
from unittest.mock import Mock, MagicMock

# Import optimized classes
import sys
sys.path.insert(0, 'rotkehlchen/tests/db')
from test_auto_login_optimized import FakeCursor, FakeDB


def benchmark_mock_approach(iterations=1000):
    """Benchmark using Mock objects (original approach)"""
    times = []
    
    for _ in range(iterations):
        start = time.perf_counter()
        
        # Original Mock approach
        mock_cursor = Mock()
        mock_db = MagicMock()
        mock_db.set_setting.return_value = None
        mock_db.get_setting.return_value = 5
        
        value = mock_db.get_setting(mock_cursor, 'auto_login_count')
        mock_db.set_setting(mock_cursor, 'auto_login_count', 10)
        result = mock_db.get_setting(mock_cursor, 'auto_login_count')
        
        end = time.perf_counter()
        times.append(end - start)
    
    return {
        'mean': statistics.mean(times) * 1_000_000,
        'median': statistics.median(times) * 1_000_000,
        'min': min(times) * 1_000_000,
        'max': max(times) * 1_000_000,
    }


def benchmark_fake_approach(iterations=1000):
    """Benchmark using Fake objects (optimized approach)"""
    times = []
    
    for _ in range(iterations):
        start = time.perf_counter()
        
        # Optimized Fake approach
        cursor = FakeCursor()
        db = FakeDB()
        
        db.set_setting(cursor, 'auto_login_count', 5)
        value = db.get_setting(cursor, 'auto_login_count')
        db.set_setting(cursor, 'auto_login_count', 10)
        result = db.get_setting(cursor, 'auto_login_count')
        
        end = time.perf_counter()
        times.append(end - start)
    
    return {
        'mean': statistics.mean(times) * 1_000_000,
        'median': statistics.median(times) * 1_000_000,
        'min': min(times) * 1_000_000,
        'max': max(times) * 1_000_000,
    }


if __name__ == "__main__":
    print("\n" + "="*70)
    print("  MOCK vs FAKE - DIRECT PERFORMANCE COMPARISON")
    print("="*70)
    
    iterations = 1000
    
    print(f"\n[1/2] Benchmarking MOCK approach ({iterations} iterations)...")
    mock_results = benchmark_mock_approach(iterations)
    
    print(f"\n[2/2] Benchmarking FAKE approach ({iterations} iterations)...")
    fake_results = benchmark_fake_approach(iterations)
    
    print("\n" + "="*70)
    print("  RESULTS")
    print("="*70)
    
    print(f"\nMOCK APPROACH (Original):")
    print(f"  Mean:   {mock_results['mean']:.3f} µs")
    print(f"  Median: {mock_results['median']:.3f} µs")
    print(f"  Min:    {mock_results['min']:.3f} µs")
    print(f"  Max:    {mock_results['max']:.3f} µs")
    
    print(f"\nFAKE APPROACH (Optimized):")
    print(f"  Mean:   {fake_results['mean']:.3f} µs")
    print(f"  Median: {fake_results['median']:.3f} µs")
    print(f"  Min:    {fake_results['min']:.3f} µs")
    print(f"  Max:    {fake_results['max']:.3f} µs")
    
    improvement = ((mock_results['mean'] - fake_results['mean']) / mock_results['mean']) * 100
    speedup = mock_results['mean'] / fake_results['mean']
    
    print("\n" + "="*70)
    print("  PERFORMANCE IMPROVEMENT")
    print("="*70)
    print(f"  Time Reduction:  {mock_results['mean'] - fake_results['mean']:.3f} µs")
    print(f"  Improvement:     {improvement:.1f}%")
    print(f"  Speedup:         {speedup:.2f}x faster")
    print("="*70)
    
    # Save comprehensive comparison
    with open('profiling_comparison.txt', 'w') as f:
        f.write("PROFILING RESULTS - MOCK vs FAKE COMPARISON\n")
        f.write("="*70 + "\n\n")
        f.write(f"Test: Auto-login unit tests optimization\n")
        f.write(f"Iterations: {iterations}\n\n")
        f.write("BEFORE (Mock approach):\n")
        f.write(f"  Mean execution time: {mock_results['mean']:.3f} µs\n")
        f.write(f"  Median: {mock_results['median']:.3f} µs\n\n")
        f.write("AFTER (Fake approach):\n")
        f.write(f"  Mean execution time: {fake_results['mean']:.3f} µs\n")
        f.write(f"  Median: {fake_results['median']:.3f} µs\n\n")
        f.write("IMPROVEMENT:\n")
        f.write(f"  Time saved per operation: {mock_results['mean'] - fake_results['mean']:.3f} µs\n")
        f.write(f"  Percentage improvement: {improvement:.1f}%\n")
        f.write(f"  Speedup factor: {speedup:.2f}x\n\n")
        f.write("OPTIMIZATION TECHNIQUES USED:\n")
        f.write("  1. Replaced Mock/MagicMock with lightweight FakeDB class\n")
        f.write("  2. Used __slots__ to reduce memory footprint\n")
        f.write("  3. Direct dictionary access instead of mock return values\n")
        f.write("  4. Cached constants to avoid repeated imports\n")
        f.write("  5. Batch operations where possible\n")
    
    print("\nDetailed comparison saved to: profiling_comparison.txt")
