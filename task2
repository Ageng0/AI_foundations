import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Polygon
from matplotlib.collections import PatchCollection
import numpy as np

class MapCSP:
    def __init__(self, regions, neighbours, colours):
        self.regions    = regions
        self.neighbours = neighbours
        self.colours    = colours
        self.assignment = {}

    def is_consistent(self, region, colour):
        for neighbour in self.neighbours.get(region, []):
            if self.assignment.get(neighbour) == colour:
                return False
        return True

    def mrv_region(self, assignment):
        unassigned = [r for r in self.regions if r not in assignment]
        return min(unassigned, key=lambda r: sum(1 for c in self.colours if self.is_consistent(r, c)))

    def backtrack(self, assignment):
        if len(assignment) == len(self.regions):
            return assignment
        region = self.mrv_region(assignment)
        for colour in self.colours:
            if self.is_consistent(region, colour):
                assignment[region] = colour
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                del assignment[region]
        return None

    def solve(self):
        solution = self.backtrack({})
        if solution:
            print(f"  Solution found using {len(set(solution.values()))} colour(s).")
        else:
            print("  No solution found.")
        return solution


print("=" * 60)
print("PART (a): Australia Map Colouring")
print("=" * 60)

australia_regions = [
    "Western Australia", "Northern Territory", "South Australia",
    "Queensland", "New South Wales"
]

australia_neighbours = {
    "Western Australia":   ["Northern Territory", "South Australia"],
    "Northern Territory":  ["Western Australia", "South Australia", "Queensland"],
    "South Australia":     ["Western Australia", "Northern Territory", "Queensland", "New South Wales"],
    "Queensland":          ["Northern Territory", "South Australia", "New South Wales"],
    "New South Wales":     ["South Australia", "Queensland"],
}

australia_colours = ["Blue", "Red", "Green"]
csp_aus = MapCSP(australia_regions, australia_neighbours, australia_colours)
aus_solution = csp_aus.solve()

print("\n  Region Assignments:")
for region, colour in aus_solution.items():
    print(f"    {region:<25} -> {colour}")

COLOUR_HEX = {
    "Blue":   "#4472C4",
    "Red":    "#E05252",
    "Green":  "#5AAD5A",
    "Yellow": "#F0C040",
    "Orange": "#E07830",
    "Purple": "#9B59B6",
}

aus_polygons = {
    "Western Australia":   np.array([[0,0],[0,6],[2,6],[2,4],[3,4],[3,0]]),
    "Northern Territory":  np.array([[2,4],[2,6],[5,6],[5,4]]),
    "South Australia":     np.array([[2,0],[2,4],[5,4],[5,2],[6,2],[6,0]]),
    "Queensland":          np.array([[5,4],[5,6],[8,6],[8,2],[6,2],[6,4]]),
    "New South Wales":     np.array([[5,0],[5,2],[6,2],[8,2],[8,0]]),
}

fig, ax = plt.subplots(figsize=(10, 7))
ax.set_facecolor("#A8D8EA")

for region, poly_pts in aus_polygons.items():
    colour_name = aus_solution[region]
    poly = Polygon(poly_pts, closed=True,
                   facecolor=COLOUR_HEX[colour_name],
                   edgecolor='black', linewidth=2)
    ax.add_patch(poly)
    cx = poly_pts[:, 0].mean()
    cy = poly_pts[:, 1].mean()
    short = {"Western Australia": "WA", "Northern Territory": "NT",
             "South Australia": "SA", "Queensland": "QLD", "New South Wales": "NSW"}
    ax.text(cx, cy, short[region], ha='center', va='center',
            fontsize=13, fontweight='bold', color='white',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='black', alpha=0.35, linewidth=0))

ax.set_xlim(-0.2, 8.5)
ax.set_ylim(-0.5, 7)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title("Australia Map Colouring – CSP Solution\n(No two adjacent regions share a colour)",
             fontsize=14, fontweight='bold', pad=15)

legend = [mpatches.Patch(facecolor=COLOUR_HEX[c], edgecolor='black', label=c)
          for c in australia_colours]
ax.legend(handles=legend, loc='lower right', fontsize=11, title="Colours", title_fontsize=11)

plt.tight_layout()
plt.savefig("australia_colouring.png", dpi=130)
plt.show()
print("  Saved: australia_colouring.png")


print("\n" + "=" * 60)
print("PART (b): Nairobi Sub-Counties Colouring")
print("=" * 60)

nairobi_subcounties = [
    "Westlands", "Dagoretti North", "Dagoretti South", "Langata",
    "Kibra", "Roysambu", "Kasarani", "Ruaraka", "Embakasi North",
    "Embakasi West", "Embakasi Central", "Embakasi East", "Embakasi South",
    "Makadara", "Kamukunji", "Starehe", "Mathare"
]

nairobi_neighbours = {
    "Westlands":        ["Roysambu", "Kasarani", "Starehe", "Dagoretti North"],
    "Dagoretti North":  ["Westlands", "Dagoretti South", "Kibra", "Starehe"],
    "Dagoretti South":  ["Dagoretti North", "Kibra", "Langata"],
    "Langata":          ["Dagoretti South", "Kibra", "Embakasi West"],
    "Kibra":            ["Dagoretti North", "Dagoretti South", "Langata", "Embakasi West", "Makadara"],
    "Roysambu":         ["Westlands", "Kasarani", "Ruaraka"],
    "Kasarani":         ["Westlands", "Roysambu", "Ruaraka", "Embakasi North", "Mathare"],
    "Ruaraka":          ["Roysambu", "Kasarani", "Embakasi North", "Mathare"],
    "Embakasi North":   ["Kasarani", "Ruaraka", "Embakasi West", "Embakasi Central"],
    "Embakasi West":    ["Langata", "Kibra", "Embakasi North", "Embakasi Central", "Embakasi South"],
    "Embakasi Central": ["Embakasi North", "Embakasi West", "Embakasi East", "Makadara"],
    "Embakasi East":    ["Embakasi Central", "Embakasi South", "Makadara"],
    "Embakasi South":   ["Embakasi West", "Embakasi East"],
    "Makadara":         ["Kibra", "Embakasi Central", "Embakasi East", "Kamukunji"],
    "Kamukunji":        ["Makadara", "Starehe", "Mathare"],
    "Starehe":          ["Westlands", "Dagoretti North", "Kamukunji", "Mathare"],
    "Mathare":          ["Kasarani", "Ruaraka", "Kamukunji", "Starehe"],
}

print("\n  Finding minimum number of colours...")
nairobi_solution = None
min_colours = 0
for num_colours in range(2, 6):
    test_colours = [f"C{i+1}" for i in range(num_colours)]
    csp_nbi = MapCSP(nairobi_subcounties, nairobi_neighbours, test_colours)
    sol = csp_nbi.solve()
    if sol:
        nairobi_solution = sol
        min_colours = num_colours
        print(f"  Minimum colours needed: {min_colours}")
        break

display_colours = ["Blue", "Red", "Green", "Yellow", "Orange", "Purple"]
colour_map_nbi = {f"C{i+1}": display_colours[i] for i in range(min_colours)}

print("\n  Sub-County Assignments:")
for sc in nairobi_subcounties:
    print(f"    {sc:<22} -> {colour_map_nbi[nairobi_solution[sc]]}")

nairobi_positions = {
    "Westlands":        (2, 8),
    "Roysambu":         (5, 9),
    "Kasarani":         (7, 8),
    "Ruaraka":          (7, 6),
    "Mathare":          (6, 7),
    "Starehe":          (4, 7),
    "Kamukunji":        (5, 6),
    "Dagoretti North":  (2, 7),
    "Dagoretti South":  (2, 5.5),
    "Kibra":            (3, 5),
    "Langata":          (2, 4),
    "Makadara":         (5, 5),
    "Embakasi North":   (7, 5),
    "Embakasi West":    (4, 3.5),
    "Embakasi Central": (6, 4),
    "Embakasi East":    (7, 3),
    "Embakasi South":   (5.5, 2.5),
}

tile_w, tile_h = 1.6, 0.9

fig, ax = plt.subplots(figsize=(12, 10))
ax.set_facecolor("#D6EAF8")

drawn_edges = set()
for sc, nbrs in nairobi_neighbours.items():
    x1, y1 = nairobi_positions[sc]
    for nbr in nbrs:
        edge = tuple(sorted([sc, nbr]))
        if edge not in drawn_edges:
            x2, y2 = nairobi_positions[nbr]
            ax.plot([x1, x2], [y1, y2], color='#555555', linewidth=1.2, zorder=1)
            drawn_edges.add(edge)

for sc in nairobi_subcounties:
    x, y = nairobi_positions[sc]
    colour_name = colour_map_nbi[nairobi_solution[sc]]
    rect = FancyBboxPatch((x - tile_w/2, y - tile_h/2), tile_w, tile_h,
                          boxstyle="round,pad=0.08",
                          facecolor=COLOUR_HEX[colour_name],
                          edgecolor='black', linewidth=1.5, zorder=2)
    ax.add_patch(rect)
    label = sc.replace("Embakasi ", "Emb. ")
    ax.text(x, y, label, ha='center', va='center',
            fontsize=7.2, fontweight='bold', color='white', zorder=3,
            bbox=dict(facecolor='none', edgecolor='none'))

ax.set_xlim(0.5, 9.5)
ax.set_ylim(1.5, 10.5)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title(f"Nairobi Sub-Counties Map Colouring – CSP Solution\n"
             f"({min_colours} colours used, 17 sub-counties)",
             fontsize=14, fontweight='bold', pad=15)

used_display = display_colours[:min_colours]
legend = [mpatches.Patch(facecolor=COLOUR_HEX[c], edgecolor='black', label=c)
          for c in used_display]
ax.legend(handles=legend, loc='lower right', fontsize=11, title="Colours", title_fontsize=11)

plt.tight_layout()
plt.savefig("nairobi_colouring.png", dpi=130)
plt.show()
print("  Saved: nairobi_colouring.png")
print("\nDone.")
