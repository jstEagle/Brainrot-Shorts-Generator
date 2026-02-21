"""
Test script for Brainrot Shorts Generator.

Generates a single video using a chosen simulation WITHOUT uploading to YouTube.
Useful for testing visuals, debugging, and verifying new simulations.

Usage:
    python test_simulation.py                     # List available simulations
    python test_simulation.py growing_sphere      # Run a specific simulation
    python test_simulation.py 1                   # Run by number
    python test_simulation.py all                 # Run every simulation once
"""

import sys
import time

SIMULATIONS = {
    1: ('growing_sphere',    'Simulations.growing_sphere'),
    2: ('shrinking_ring',    'Simulations.shrinking_ring'),
    3: ('butterfly_effect',  'Simulations.butterfly_effect'),
    4: ('duplicating_balls', 'Simulations.duplicating_balls'),
    5: ('bounce_countdown',  'Simulations.bounce_countdown'),
    6: ('time_countdown',    'Simulations.time_countdown'),
    7: ('gravity_well',      'Simulations.gravity_well'),
    8: ('chain_reaction',    'Simulations.chain_reaction'),
    9: ('pendulum_wave',     'Simulations.pendulum_wave'),
}


def print_menu():
    print("=" * 50)
    print("  Brainrot Shorts Generator - Test Runner")
    print("=" * 50)
    print()
    print("Available simulations:")
    print()
    for num, (name, _) in SIMULATIONS.items():
        print(f"  {num}. {name}")
    print()
    print("Usage:")
    print(f"  python {sys.argv[0]} <name_or_number>")
    print(f"  python {sys.argv[0]} all")
    print()
    print("Examples:")
    print(f"  python {sys.argv[0]} growing_sphere")
    print(f"  python {sys.argv[0]} 1")
    print(f"  python {sys.argv[0]} all")


def find_simulation(query):
    """Find a simulation by name or number."""
    # Try as number
    try:
        num = int(query)
        if num in SIMULATIONS:
            return [SIMULATIONS[num]]
    except ValueError:
        pass

    # Try as name (exact or partial match)
    query_lower = query.lower()
    for num, (name, module) in SIMULATIONS.items():
        if name == query_lower:
            return [(name, module)]

    # Partial match
    matches = []
    for num, (name, module) in SIMULATIONS.items():
        if query_lower in name:
            matches.append((name, module))
    return matches


def run_simulation(name, module_path):
    """Import and run a single simulation."""
    import importlib

    print()
    print("=" * 50)
    print(f"  Running: {name}")
    print("=" * 50)
    print()

    output_name = f"test_{name}"
    module = importlib.import_module(module_path)

    start_time = time.time()
    attempt = 0

    while True:
        attempt += 1
        if attempt > 1:
            print(f"\n  Attempt {attempt} (previous run returned failure, retrying...)\n")

        success, title, description = module.simulation(output_name)

        if success:
            elapsed = time.time() - start_time
            print()
            print(f"  Success!")
            print(f"  Output:      {output_name}.mp4")
            print(f"  Title:       {title}")
            print(f"  Description: {description}")
            print(f"  Time:        {elapsed:.1f}s")
            print()
            return True

        if attempt >= 3:
            print(f"\n  Failed after {attempt} attempts. Skipping {name}.\n")
            return False


def main():
    if len(sys.argv) < 2:
        print_menu()
        return

    query = sys.argv[1]

    # Run all simulations
    if query.lower() == 'all':
        results = {}
        for num, (name, module_path) in SIMULATIONS.items():
            success = run_simulation(name, module_path)
            results[name] = success

        print()
        print("=" * 50)
        print("  Results Summary")
        print("=" * 50)
        for name, success in results.items():
            status = "PASS" if success else "FAIL"
            print(f"  [{status}] {name}")
        print()
        passed = sum(1 for s in results.values() if s)
        print(f"  {passed}/{len(results)} passed")
        return

    # Run specific simulation
    matches = find_simulation(query)

    if not matches:
        print(f"  No simulation matching '{query}' found.\n")
        print_menu()
        return

    if len(matches) > 1:
        print(f"  Multiple matches for '{query}':")
        for name, _ in matches:
            print(f"    - {name}")
        print(f"\n  Please be more specific.")
        return

    name, module_path = matches[0]
    run_simulation(name, module_path)


if __name__ == '__main__':
    main()
