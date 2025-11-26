"""Script to analyze cProfile output and find bottlenecks"""
import pstats
from pstats import SortKey

# Load profile data
p = pstats.Stats('profile_output.prof')

print("=" * 80)
print("TOP 20 FUNCTIONS BY CUMULATIVE TIME")
print("=" * 80)
p.sort_stats(SortKey.CUMULATIVE).print_stats(20)

print("\n" + "=" * 80)
print("TOP 20 FUNCTIONS BY TOTAL TIME")
print("=" * 80)
p.sort_stats(SortKey.TIME).print_stats(20)

print("\n" + "=" * 80)
print("TOP 20 MOST CALLED FUNCTIONS")
print("=" * 80)
p.sort_stats(SortKey.CALLS).print_stats(20)
