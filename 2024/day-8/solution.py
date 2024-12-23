from itertools import combinations

def parse_input(filename):
    grid = []
    with open(filename, 'r') as f:
        for ln in f:
            ln = ln.strip()
            if not ln:
                continue
            grid.append(list(ln))
    return grid

def find_antennas():
    ants = {}
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            freq = grid[row][col]
            if freq != '.':
                if freq not in ants:
                    ants[freq] = []
                ants[freq].append((row, col))
    return ants

def dist(p1, p2):
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

def is_aligned(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    return abs((y2-y1) * (x3-x1) - (y3-y1) * (x2-x1)) < 1

def find_antinode(a1, a2):
    rmin = min(a1[0], a2[0])
    rmax = max(a1[0], a2[0])
    cmin = min(a1[1], a2[1])
    cmax = max(a1[1], a2[1])

    nodes = []
    search_range = max(abs(rmax - rmin), abs(cmax - cmin)) * 3

    for r in range(rmin - search_range, rmax + search_range + 1):
        for c in range(cmin - search_range, cmax + search_range + 1):
            pt = (r, c)
            if pt == a1 or pt == a2:
                continue

            if is_aligned(a1, a2, pt):
                d1 = dist(pt, a1)
                d2 = dist(pt, a2)
                if d1 == 4*d2 or d2 == 4*d1:
                    nodes.append(pt)

    return nodes

def find_harmonic_points(a1, a2):
    pts = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            pt = (r, c)
            if pt != a1 and pt != a2 and is_aligned(a1, a2, pt):
                pts.append(pt)
    return pts

def in_bounds(pt):
    return 0 <= pt[0] < len(grid) and 0 <= pt[1] < len(grid[0])

def part_one():
    ants = find_antennas()
    nodes = set()

    for freq, pos in ants.items():
        for a1, a2 in combinations(pos, 2):
            found = find_antinode(a1, a2)
            nodes.update(node for node in found if in_bounds(node))

    return len(nodes)

def part_two():
    ants = find_antennas()
    nodes = set()

    for freq, pos in ants.items():
        if len(pos) < 2:
            continue
        nodes.update(pos)

        for a1, a2 in combinations(pos, 2):
            pts = find_harmonic_points(a1, a2)
            nodes.update(pt for pt in pts if in_bounds(pt))

    return len(nodes)

def main():
    print("Parsing input...")
    global grid
    grid = parse_input('input.txt')

    print("\nProcessing Part 1...")
    result1 = part_one()

    print("\nProcessing Part 2...")
    result2 = part_two()

    print("\n=== Final Results ===")
    print(f"Part 1: Number of unique antinode locations: {result1}")
    print(f"Part 2: Number of unique antinode locations with harmonics: {result2}")

if __name__ == "__main__":
    main()
