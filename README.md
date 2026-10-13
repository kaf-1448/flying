*This project has been created as part of the 42 curriculum by ykaf.*

# 🛸 Fly-In: Autonomous Drone Pathfinding & Simulation System

[![Language](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-Pygame%202.6-green.svg)](https://www.pygame.org/)
[![Code Style](https://img.shields.io/badge/Code%20Style-Flake8%20PEP8-brightgreen.svg)](https://flake8.pycqa.org/)
[![Type Checking](https://img.shields.io/badge/Type%20Check-Mypy%20Strict-blueviolet.svg)](https://mypy-lang.org/)

An end-to-end, high-performance Python application for multi-agent drone pathfinding, turn-by-turn discrete traffic simulation, and interactive 2D graphical visualization. Developed as part of the 42 curriculum, Fly-In solves complex multi-agent coordination problems on graphs under dynamic capacity constraints, zone transit penalties, and spatial bottlenecks.

---

## 📖 Description

### 1. Project Goal & Overview
The objective of **Fly-In** is to guide a fleet of autonomous drones ($N$ drones) from a starting base (`start_hub`) to a final destination (`end_hub`) in the **minimum possible number of discrete simulation turns**.

The airspace is structured as a network of landing zones (hubs) interconnected by aerial flight corridors (connections). Navigation is complicated by realistic operational constraints:
- **Spatial Bottlenecks**: Hubs possess strict simultaneous capacity limits (`max_drones`).
- **Bandwidth Limitations**: Aerial corridors restrict the number of drones that may traverse them in a single turn (`max_link_capacity`).
- **Zone Heterogeneity**:
  - `normal`: Standard zones requiring 1 turn to traverse.
  - `priority`: High-speed corridors with preferred routing.
  - `restricted`: Dangerous or turbulent zones requiring a **2-turn transit delay**.
  - `blocked`: No-fly zones strictly inaccessible to all drones.
- **Collision Avoidance**: Drones must never collide in hubs or along flight corridors.

The system autonomously parses and validates map topologies, constructs an in-memory graph model, executes weighted multi-path routing (Dijkstra + Yen's algorithm), simulates multi-agent movements turn-by-turn, and presents the entire mission visually in an interactive Pygame environment.

---

### 2. Graph Theory & Graph Representations in Fly-In

At its core, Fly-In models airspace navigation using mathematical **Graph Theory**:

$$\mathcal{G} = (\mathcal{V}, \mathcal{E})$$

where:
- $\mathcal{V}$ is the set of **Vertices (Hubs / Zones)** representing geographic waypoints.
- $\mathcal{E}$ is the set of **Edges (Connections)** representing valid bidirectional flight corridors between hubs.

#### Graph Classification in Fly-In:
1. **Undirected Graph**: All physical connections are bidirectional. If corridor $u-v$ exists, drones can travel from $u$ to $v$ or from $v$ to $u$ (subject to turn-specific capacity locks).
2. **Weighted Graph**: Edges and hubs are assigned positive cost weights ($\mathcal{W}$) reflecting transit latency and preference:
   - Priority zones: $\text{Weight} = 0.9$ (favorable path).
   - Normal zones: $\text{Weight} = 1.0$ (baseline).
   - Restricted zones: $\text{Weight} = 2.0$ (slow transit).
   - Blocked zones: $\text{Weight} = \infty$ (impassable).
3. **Capacity-Constrained Flow Network**: Unlike classic unconstrained shortest-path graphs, each vertex $v \in \mathcal{V}$ has an upper capacity bound $C_v = \text{max\_drones}(v)$, and each edge $e \in \mathcal{E}$ has a throughput limit $C_e = \text{max\_link\_capacity}(e)$. `start_hub` and `end_hub` have infinite capacity ($C_{\text{start}} = C_{\text{end}} = \infty$).

#### Graph Memory Representation:
We employ an **Adjacency List** representation (`Dict[str, List[str]]`) rather than an Adjacency Matrix:
- **Memory Efficiency**: Fly-In maps are sparse networks ($|\mathcal{E}| \ll |\mathcal{V}|^2$). The adjacency list consumes $O(|\mathcal{V}| + |\mathcal{E}|)$ space compared to $O(|\mathcal{V}|^2)$ for a dense matrix.
- **Fast Neighbor Iteration**: Dijkstra and BFS algorithms can enumerate all outgoing corridors for a hub in $O(\text{deg}(v))$ time rather than scanning all $|\mathcal{V}|$ matrix columns.

---

## 🛠️ Instructions

### 1. Prerequisites
- **Python**: Version `3.10` or higher (`3.14` supported).
- **Make**: GNU Make.
- **Dependencies**: Listed in `requirements.txt` (`pygame`, `mypy`, `flake8`, `rich`).

### 2. Installation
Install all required dependencies using either `make` or `pip`:
```bash
make install
# or directly with pip:
pip install -r requirements.txt
```

### 3. Execution
Launch the simulator and visualizer with any map using `make run`:
```bash
# Run default map (maps/easy/01_linear_path.txt):
make run

# Run any specific map from Easy, Medium, Hard, or Challenger:
make run MAP=maps/easy/02_simple_fork.txt
make run MAP=maps/medium/02_circular_loop.txt
make run MAP=maps/hard/01_maze_nightmare.txt
make run MAP=maps/challenger/01_the_impossible_dream.txt

# Or execute directly via Python:
python3 src/main.py maps/challenger/01_the_impossible_dream.txt
```

### 4. Code Quality & Linting
Validate strict PEP8 styling and static type checking:
```bash
make lint
```

### 5. Cleaning Build Cache
Remove all `__pycache__` artifacts and type checker caches:
```bash
make clean
```

---

## 🧠 Algorithm Choices and Implementation Strategy

### 1. Why Dijkstra's Algorithm?
Standard Breadth-First Search (BFS) treats all graph edges identically ($1 \text{ hop} = 1 \text{ cost}$). However, Fly-In introduces heterogeneous zone penalties (`priority` vs `restricted`).

We implemented **Dijkstra’s Algorithm** with a Min-Heap (`heapq`):
- **Cost Model**:
  $$\text{cost}(u \to v) = \begin{cases} 0.9 & \text{if } v \text{ is priority} \\ 1.0 & \text{if } v \text{ is normal} \\ 2.0 & \text{if } v \text{ is restricted} \\ \infty & \text{if } v \text{ is blocked (pruned)} \end{cases}$$
- **Time Complexity**: $O((|\mathcal{E}| + |\mathcal{V}|) \log |\mathcal{V}|)$, delivering microsecond-level shortest path calculations.

### 2. Multi-Path Optimization: Yen's K-Shortest Paths Algorithm
A single shortest path is insufficient for multi-agent coordination. If 25 drones all attempt to traverse the same optimal path, intense congestion occurs at bottleneck hubs with $\text{max\_drones} = 1$.

To balance drone traffic across multiple corridors, we implemented **Yen’s K-Shortest Loopless Paths Algorithm**:
1. It computes the initial shortest path $P_1$ using Dijkstra.
2. For each path $k \in [1, K-1]$, it iterates over every node (the "spur node") in the root path, temporarily masking preceding edges/nodes to force Dijkstra to find alternative deviation paths.
3. It collects alternative loopless candidate paths in a priority queue and extracts the next best global path $P_k$.
4. **Traffic Distribution**: Drones are distributed across the $K$ diverse paths via round-robin allocation (`paths[i % len(paths)]`), preventing convoy congestion and dramatically reducing total makespan.

### 3. Turn-by-Turn Simulation Engine & Collision Avoidance
The simulation operates as a discrete-event turn engine:
- **Capacity Enforcement**: During each turn, hubs and connections track their occupancy vectors (`occupied` and `edge_used`).
- **Staying-Drone Locking**: If a drone cannot advance because its forward hub is full, it remains in its current hub and marks that hub as occupied, preventing trailing drones from causing a collision.
- **Restricted Zone 2-Turn Traversal**:
  - **Turn 1 (In-Transit)**: Drone departs current hub towards the restricted hub. Recorded as `D<id>-<from>-<to>`. Visualized halfway along the corridor.
  - **Turn 2 (Arrival)**: Drone physically reaches the restricted hub. Recorded as `D<id>-<to>`. Visualized inside the hub.
- **Infinite Terminals**: `start_hub` and `end_hub` bypass capacity limits ($C = \infty$), allowing unlimited simultaneous departures and arrivals.

---

## 🎮 Visual Representation Features

The GUI is built with **Pygame 2.6** inside an Object-Oriented `Visualizer` class:

### 1. Coordinate Auto-Scaling (`_convert_to_pixel`)
Maps use arbitrary coordinate systems (e.g. $[0, 4]$ or $[0, 100]$). The visualizer normalizes coordinates and projects them onto the $1900 \times 800$ canvas with a 60px margin:
$$\text{pixel}_x = \text{margin} + \frac{x - \min(x)}{\max(x) - \min(x)} \times (\text{width} - 2 \times \text{margin})$$
$$\text{pixel}_y = \text{margin} + \frac{y - \min(y)}{\max(y) - \min(y)} \times (\text{height} - 2 \times \text{margin})$$

### 2. Color-Coded Zone Hierarchy
- 🟢 **Start Hub**: Emerald Green `(46, 204, 113)`
- 🔴 **End Hub**: Crimson Red `(231, 76, 60)`
- 🟠 **Restricted Zone**: Orange `(243, 156, 18)`
- 🟡 **Priority Zone**: Yellow `(241, 196, 15)`
- 🔵 **Normal Zone**: Sky Blue `(52, 152, 219)`
- ⚫ **Blocked Zone**: Dark Gray `(80, 80, 80)`

### 3. In-Transit Midpoint Rendering
When a drone enters a restricted zone corridor during Turn 1, the visualizer detects the transit state (`start-junction`) and interpolates the midpoint between both hubs:
$$\text{position}_{\text{drone}} = \left(\frac{x_1 + x_2}{2}, \frac{y_1 + y_2}{2}\right)$$
This gives immediate visual feedback that the drone is actively flying along the corridor rather than tele-transporting.

### 4. Interactive Keyboard Controls
- **`[SPACE]`**: Advance one turn forward.
- **`[LEFT ARROW]`**: Step one turn backward.
- **`[R]`**: Reset simulation to Turn 0.
- **`[ESC]` / Close**: Exit GUI cleanly.
- **HUD Overlay**: Real-time turn counter displayed at $(20, 20)$ (`Turn: current / max`).

---

## 📋 Example Input and Expected Output

### Sample Input Map (`maps/easy/01_linear_path.txt`)
```text
# Easy Level 1: Simple linear path
nb_drones: 2
start_hub: start 0 0 [color=green]
hub: waypoint1 1 0 [color=blue]
hub: waypoint2 2 0 [zone=normal color=blue max_drones=1]
end_hub: goal 3 0 [color=red]

connection: start-waypoint1
connection: waypoint1-waypoint2
connection: waypoint2-goal
```

### Verbatim Simulation Output
```text
D1-waypoint1
D1-waypoint2 D2-waypoint1
D1-goal D2-waypoint2
D2-goal
```

### Multi-Path & Restricted Zone Example (`maps/easy/02_simple_fork.txt`)
```text
D1-start-junction D2-start-junction
D1-junction D2-junction
D1-path_a D2-path_b D3-start-junction D4-start-junction
D1-goal D2-goal D3-junction D4-junction
D3-path_a D4-path_b
D3-goal D4-goal
```
*(Notice D1 and D2 taking 2 turns across the restricted `junction`: Turn 1 in-transit `start-junction`, Turn 2 arrival `junction`)*.

---

## 📚 Resources & AI Usage Description

### 1. References & Literature
- **Dijkstra, E. W. (1959)**: *A note on two problems in connexion with graphs*. Numerische Mathematik, 1, 269–271.
- **Yen, J. Y. (1971)**: *Finding the K Shortest Loopless Paths in a Network*. Management Science, 17(11), 712–716.
- **Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2009)**: *Introduction to Algorithms* (3rd ed.). MIT Press (Graph representation & Single-Source Shortest Paths).
- **Pygame Community (2024)**: *Pygame 2D Engine Documentation*. https://www.pygame.org/docs/

### 2. Declaration of AI Usage
In accordance with the 42 project guidelines, Artificial Intelligence (Large Language Model) was utilized as an engineering pair-programming assistant for:
- **Conceptual & Architectural Guidance**: Discussing trade-offs between BFS vs Dijkstra cost models and multi-path deviation algorithms.
- **Test-Case Brainstorming**: Designing comprehensive suites of malformed map edge cases (brackets, negative capacities, duplicate links, coordinate types) to ensure robust parser validation.
- **GUI Math & Animation Formulations**: Deriving and refining the coordinate auto-scaling projection and restricted-zone midpoint interpolation formulas.
- **Type Checking Compliance**: Providing guidance on strict PEP 484 type annotations for Mypy compliance.

