*This project has been created as part of the 42 curriculum by ykaf.*

# Fly-In 🛸

A clean and efficient multi-agent drone routing and simulation system written in Python. Fly-In guides a fleet of drones from a start hub to a destination hub in the minimum possible number of discrete simulation turns, respecting zone capacities, corridor bandwidths, and movement restrictions.

---

## 📖 Description

The goal of **Fly-In** is to route $N$ autonomous drones through a network of connected zones in the fewest turns possible without collisions or deadlocks.

### Airspace Rules & Zone Types
- **Zones (Hubs)**: Defined by name, `(x, y)` coordinates, and a maximum simultaneous drone capacity `max_drones` (default: 1).
- **Connections (Corridors)**: Bidirectional links connecting zones with a bandwidth limit `max_link_capacity` (default: 1).
- **Zone Types**:
  - `normal`: Standard zone, movement costs **1 turn**.
  - `priority`: Preferred zone, movement costs **1 turn** (favored during pathfinding).
  - `restricted`: High-risk zone, movement requires **2 turns** to traverse.
  - `blocked`: No-fly zone, completely impassable.
- **Start and End Hubs**: Have infinite capacity; all drones start at `start_hub` and are delivered upon entering `end_hub`.

---

## 🛠️ Instructions

### 1. Installation
Install the project dependencies (`pygame`, `flake8`, `mypy`):
```bash
make install
```
*(or directly using pip: `pip install -r requirements.txt`)*

### 2. Execution
Run the simulation with any map file:
```bash
# Using python directly:
python3 src/main.py maps/easy/01_linear_path.txt

# Or using the Makefile:
make run MAP=maps/hard/01_maze_nightmare.txt
```

### 3. Code Quality & Linting
Ensure full compliance with PEP 8 standards and strict static typing:
```bash
make lint
```

### 4. Cleaning Cache Files
Remove temporary Python bytecode and cache directories:
```bash
make clean
```

---

## 🧠 Algorithm Choices and Implementation Strategy

Fly-In cleanly separates route planning from turn-by-turn physical execution:

### 1. Shortest Path Search (Dijkstra's Algorithm)
We use **Dijkstra's Algorithm** with a priority queue (`heapq`) to find the optimal path considering zone penalties:
- `normal`: weight = 1.0
- `priority`: weight = 1.0 (with prioritized tie-breaking)
- `restricted`: weight = 2.0 (reflecting the 2-turn movement cost)
- `blocked`: pruned (`weight = inf`)

### 2. Multi-Path Discovery (Yen's Algorithm)
To prevent all drones from crowding into a single corridor, we implement **Yen's K-Shortest Loopless Paths Algorithm** ($k=2$) to discover alternative valid routes between start and goal.

### 3. Drone Distribution (Makespan Optimization)
To balance drone traffic across candidate paths, we test all valid allocations $(n_0, n_1)$ using the queuing formula:
$$\text{Time} = \text{cost} + n - 1$$
We pick the distribution that minimizes the total makespan $\max(t_0, t_1)$. We also verify shared bottlenecks (`max_drones == 1`) to prevent traffic bubbles.

### 4. Turn-by-Turn Simulation Engine
The simulation runs in discrete turns:
- **Simultaneous Movements**: Multiple drones advance within the same turn.
- **Deadlock Avoidance**: Active drones are sorted in reverse order (`reverse=True`), moving forward drones first so vacated spaces are instantly available to trailing drones in the same turn.
- **Restricted Zone Handling**: Drones spend turn 1 in transit (`D1-hubA-hubB`) and turn 2 entering the zone (`D1-hubB`).

---

## 🎮 Visual Representation

An interactive graphical visualizer is built using **Pygame**:
- **Automatic Coordinate Projection**: Dynamically maps any arbitrary coordinate scale to fit the window with proportional margins.
- **Color-Coded Zones**:
  - 🟢 **Green**: Start Hub
  - 🔴 **Red**: End Hub
  - 🟠 **Orange**: Restricted Zone
  - 🟡 **Yellow**: Priority Zone
  - 🔵 **Blue**: Normal Zone
  - ⚫ **Gray**: Blocked Zone
- **In-Transit Rendering**: Drones traversing restricted corridors are rendered at the corridor midpoint.
- **Controls**:
  - `[SPACE]`: Advance one turn forward
  - `[LEFT ARROW]`: Step one turn backward
  - `[R]`: Reset to turn 0
  - `HUD`: Displays current turn number and key controls overlay

---

## 📋 Example Input and Output

### Sample Input (`maps/easy/01_linear_path.txt`)
```text
nb_drones: 2
start_hub: start 0 0 [color=green]
hub: waypoint1 1 0 [color=blue]
hub: waypoint2 2 0 [zone=normal color=blue max_drones=1]
end_hub: goal 3 0 [color=red]

connection: start-waypoint1
connection: waypoint1-waypoint2
connection: waypoint2-goal
```

### Expected Terminal Output
```text
D1-waypoint1
D1-waypoint2 D2-waypoint1
D1-goal D2-waypoint2
D2-goal
```

---

## 📚 Resources & AI Usage

### 1. References
- **Dijkstra, E. W. (1959)**: *A note on two problems in connexion with graphs*. Numerische Mathematik.
- **Yen, J. Y. (1971)**: *Finding the K Shortest Loopless Paths in a Network*. Management Science.
- **Pygame Documentation**: https://www.pygame.org/docs/

### 2. Declaration of AI Usage
In accordance with the 42 curriculum guidelines, Artificial Intelligence was utilized as a pair-programming assistant for:
- Discussing algorithm trade-offs between single-source routing and multi-path allocation.
- Brainstorming parser validation edge cases (syntax errors, malformed brackets, negative capacities).
- Refining PEP 257 docstrings and reviewing PEP 484 type annotations for Mypy compliance.
