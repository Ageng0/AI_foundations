import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

male_facts   = {"George", "David", "Michael", "James", "Liam", "Noah", "Oliver"}
female_facts = {"Mary",   "Susan", "Linda",   "Emma",  "Ava",  "Sophia", "Grace"}

parent_facts = [
    ("George",  "David"),
    ("George",  "Michael"),
    ("Mary",    "David"),
    ("Mary",    "Michael"),
    ("David",   "James"),
    ("David",   "Liam"),
    ("Susan",   "James"),
    ("Susan",   "Liam"),
    ("Michael", "Noah"),
    ("Michael", "Oliver"),
    ("Linda",   "Noah"),
    ("Linda",   "Oliver"),
    ("James",   "Emma"),
    ("James",   "Ava"),
    ("Liam",    "Sophia"),
    ("Noah",    "Grace"),
]

def children_of(p):
    return [c for (par, c) in parent_facts if par == p]

def parents_of(c):
    return [p for (p, ch) in parent_facts if ch == c]

def is_parent(p, c):
    return (p, c) in parent_facts

def is_male(p):
    return p in male_facts

def is_female(p):
    return p in female_facts

def is_father(p, c):
    return is_male(p) and is_parent(p, c)

def is_mother(p, c):
    return is_female(p) and is_parent(p, c)

def grandchildren_of(gp):
    result = []
    for child in children_of(gp):
        result.extend(children_of(child))
    return list(set(result))

def siblings(p):
    result = set()
    for par in parents_of(p):
        for sib in children_of(par):
            if sib != p:
                result.add(sib)
    return result

def is_sibling(a, b):
    return b in siblings(a)

def is_brother(a, b):
    return is_male(a) and is_sibling(a, b)

def is_sister(a, b):
    return is_female(a) and is_sibling(a, b)

def is_uncle(u, n):
    return any(is_brother(u, p) for p in parents_of(n))

def is_aunt(a, n):
    return any(is_sister(a, p) for p in parents_of(n))

def all_cousins(p):
    result = set()
    for par in parents_of(p):
        for sib in siblings(par):
            for c in children_of(sib):
                if c != p:
                    result.add(c)
    return result

def all_ancestors(p, depth=0, max_depth=10):
    if depth >= max_depth:
        return set()
    result = set()
    for par in parents_of(p):
        result.add(par)
        result |= all_ancestors(par, depth + 1, max_depth)
    return result


def sep(title):
    print(f"\n{'─'*55}\n  {title}\n{'─'*55}")

all_people = male_facts | female_facts

print("=" * 55)
print("  CCS 2226 – Task 3: Family Tree (Prolog-style)")
print("=" * 55)

sep("FAMILY MEMBERS")
print(f"  Males  : {', '.join(sorted(male_facts))}")
print(f"  Females: {', '.join(sorted(female_facts))}")

sep("FATHERS")
for p in sorted(all_people):
    for c in sorted(children_of(p)):
        if is_father(p, c):
            print(f"  {p} is father of {c}")

sep("MOTHERS")
for p in sorted(all_people):
    for c in sorted(children_of(p)):
        if is_mother(p, c):
            print(f"  {p} is mother of {c}")

sep("GRANDPARENTS & GRANDCHILDREN")
shown_gp = set()
for p in sorted(all_people):
    gcs = grandchildren_of(p)
    if gcs:
        print(f"  {p:<10} -> grandchildren: {', '.join(sorted(gcs))}")

sep("SIBLINGS")
shown = set()
for person in sorted(all_people):
    sibs = siblings(person)
    if sibs:
        key = frozenset({person} | sibs)
        if key not in shown:
            print(f"  {person} <-> {', '.join(sorted(sibs))}")
            shown.add(key)

sep("UNCLES AND AUNTS")
for person in sorted(all_people):
    uncles = [u for u in sorted(all_people) if is_uncle(u, person)]
    aunts  = [a for a in sorted(all_people) if is_aunt(a, person)]
    if uncles:
        print(f"  {person:<10} uncle(s): {', '.join(uncles)}")
    if aunts:
        print(f"  {person:<10} aunt(s) : {', '.join(aunts)}")

sep("COUSINS")
shown_pairs = set()
for person in sorted(all_people):
    cousins = all_cousins(person)
    if cousins:
        key = frozenset({person} | cousins)
        if key not in shown_pairs:
            print(f"  {person} <-> cousins: {', '.join(sorted(cousins))}")
            shown_pairs.add(key)

sep("ANCESTORS")
for p in sorted(all_people):
    anc = all_ancestors(p)
    if anc:
        print(f"  {p:<10} ancestors: {', '.join(sorted(anc))}")

print("\n" + "=" * 55)
print("  All family-tree queries complete.")
print("=" * 55)


G = nx.DiGraph()
for parent, child in parent_facts:
    G.add_edge(parent, child)

pos = {
    "George":  (3.5, 4),
    "Mary":    (5.5, 4),
    "David":   (2,   3),
    "Susan":   (1,   3),
    "Michael": (5,   3),
    "Linda":   (6.5, 3),
    "James":   (1,   2),
    "Liam":    (3,   2),
    "Noah":    (5,   2),
    "Oliver":  (7,   2),
    "Emma":    (0,   1),
    "Ava":     (2,   1),
    "Sophia":  (3,   1),
    "Grace":   (5,   1),
}

gender_colours = {p: "#4472C4" if p in male_facts else "#E05252" for p in G.nodes()}
node_colour_list = [gender_colours[n] for n in G.nodes()]

fig, ax = plt.subplots(figsize=(13, 8))
nx.draw(G, pos, ax=ax,
        labels={n: n for n in G.nodes()},
        node_color=node_colour_list,
        node_size=2000,
        font_size=9,
        font_weight='bold',
        font_color='white',
        edge_color='#444444',
        width=2,
        arrows=True,
        arrowsize=18)

legend_items = [
    mpatches.Patch(facecolor="#4472C4", label="Male"),
    mpatches.Patch(facecolor="#E05252", label="Female"),
]
ax.legend(handles=legend_items, loc='lower left', fontsize=11)
ax.set_title("Family Tree – CCS 2226 Task 3\n(Grandparents → Parents → Children → Grandchildren)",
             fontsize=13, fontweight='bold')

plt.tight_layout()
plt.savefig("family_tree.png", dpi=130)
plt.show()
print("Saved: family_tree.png")

PROLOG_CODE = """
male(george). male(david). male(michael).
male(james).  male(liam).  male(noah). male(oliver).

female(mary). female(susan). female(linda).
female(emma). female(ava).   female(sophia). female(grace).

parent(george,  david).   parent(george,  michael).
parent(mary,    david).   parent(mary,    michael).
parent(david,   james).   parent(david,   liam).
parent(susan,   james).   parent(susan,   liam).
parent(michael, noah).    parent(michael, oliver).
parent(linda,   noah).    parent(linda,   oliver).
parent(james,   emma).    parent(james,   ava).
parent(liam,    sophia).
parent(noah,    grace).

father(F, C)       :- male(F),   parent(F, C).
mother(M, C)       :- female(M), parent(M, C).
grandparent(GP,GC) :- parent(GP, P), parent(P, GC).
grandchild(GC, GP) :- grandparent(GP, GC).
sibling(X, Y)      :- parent(P, X), parent(P, Y), X \\= Y.
brother(X, Y)      :- male(X),   sibling(X, Y).
sister(X, Y)       :- female(X), sibling(X, Y).
uncle(U, N)        :- brother(U, P), parent(P, N).
aunt(A, N)         :- sister(A, P),  parent(P, N).
cousin(X, Y)       :- parent(PX, X), parent(PY, Y), sibling(PX, PY), X \\= Y.
ancestor(A, D)     :- parent(A, D).
ancestor(A, D)     :- parent(A, X), ancestor(X, D).
"""

with open("family_tree.pl", "w") as f:
    f.write(PROLOG_CODE.strip())
print("Saved: family_tree.pl")
