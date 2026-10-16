Based on the assignment's strict "Original Implementation Requirement," we must eliminate several of the provided papers immediately. For example, Adaptive genetic algorithm based deep feature selector for cancer detection has its source code publicly available on GitHub, and Student timetabling genetic algorithm provides its dataset and code via a Zenodo link. Selecting either of these would violate the core academic integrity requirement of the assignment.

Therefore, I recommend selecting "An Adaptive A\* Algorithm for Mobile Robots Global Path Planning". Graph-search path planning algorithms are mathematically clear, rely on simulated grid maps rather than massive datasets, and this specific paper does not have a publicly available code repository, making it an ideal candidate for independent re-implementation.

Here is the initial Research Paper Analysis and Feasibility assessment for this selected paper:

1. Problem, Objectives, and Contributions The research addresses the core inefficiencies of the traditional A\* algorithm in global path planning for mobile robots—specifically, the generation of too many redundant nodes, excessive computational time in large scenarios, and paths with too many sharp turns. The objective is to optimize the search efficiency and path smoothness. The main contributions are the introduction of an adaptive estimation (heuristic) function, an optimized distance model, and a post-processing redundant point deletion strategy.

2. Proposed Methodology The authors propose three modular improvements to the traditional A\* algorithm:

Adaptive Estimation Function: Dynamically adjusting the heuristic weight to balance exploration and exploitation depending on the robot's proximity to the goal.

Distance Model Optimization: Refining how the heuristic distance is calculated to better reflect the actual movement cost in a 2D grid environment.

Redundant Point Deletion: A smoothing step that eliminates unnecessary intermediary nodes in the generated path to reduce turns and shorten the final route.

3. Dataset(s) Used and Availability The study does not rely on a standard, publicly available empirical dataset. Instead, the experiments are conducted on randomly generated 2D grid maps of varying sizes, specifically 30×30, 60×60, and 100×100 grids. These simulation environments can be easily replicated programmatically.

4. Required Programming Language, Libraries, Frameworks, and Tools

This methodology can be efficiently implemented using standard programming languages like Python or C++.

Libraries: numpy for grid representation and matrix operations, matplotlib for map and path visualization, and standard data structures (like heapq in Python) for managing the Open List.

Computational Resources: A\* and its variants are computationally lightweight. A standard modern PC is entirely sufficient for simulating and evaluating the algorithm on the specified grid sizes without the need for GPUs.

5. Practical Feasibility The proposed methodology is highly feasible to implement within the scope of a university assignment. The A\* algorithm is a fundamental graph search technique, and the proposed improvements rely on geometric and algebraic operations rather than complex machine learning training loops.

6. Sufficiency of Implementation Details The paper provides a strong theoretical basis, outlining the ablation studies (testing the three improvements individually) and comparisons against other algorithms (e.g., Dijkstra, Bidirectional A\*). The conceptual framework for modifying the evaluation function and deleting redundant points is provided clearly.

7. Missing, Unclear, or Difficult to Reproduce Information While the concepts are well-defined, the exact mathematical coefficients or decay rates used in the "adaptive estimation function" might require empirical tuning to match the exact visual paths shown in the paper's figures. Furthermore, because the obstacle placement in the grid maps is random, exact node-for-node reproduction of their specific paths is impossible. However, statistical comparability can easily be achieved by running multiple random map generations.

If you are satisfied with this selection, our next step is to set up the grid environments (30x30, 60x60, 100x100) and implement the baseline traditional A\* algorithm before adding the adaptive modifications.

i asked gemini by providing all the papers and thats what it tells me

…
Yes — Gemini's recommendation is sensible, and I would actually prefer this paper over the timetabling paper given the assignment's strict source-code requirement.

However, I would make one important correction: we should not treat Gemini's claims about source-code availability or the paper's exact experimental details as established until we verify them against the actual PDF and the public web. The assignment explicitly makes that check your responsibility.

Why I agree with the choice
"An Adaptive A Algorithm for Mobile Robots Global Path Planning"\* is a strong assignment candidate because it gives you a very clean reproduction structure:

Original A*
│
├── Adaptive heuristic / estimation
│
├── Improved distance model
│
└── Redundant-point deletion
│
▼
Proposed Adaptive A*
And, importantly, you can independently implement the entire thing rather than relying on a large ML framework.

The biggest advantage
You can make the reproduction experimentally rigorous, rather than simply showing that your algorithm produces a path.

For example:

Algorithm Path Length Search Nodes Runtime Turns
Dijkstra ... ... ... ...
Traditional A* ... ... ... ...
Adaptive A* ... ... ... ...
Then you can perform an ablation:

Variant Adaptive Heuristic Distance Model Point Deletion
A* baseline No No No
A* + H Yes No No
A\* + H + D Yes Yes No
Proposed Yes Yes Yes
That is exactly the sort of evidence your assignment is asking for.

One thing I would change in Gemini's proposed approach
Don't immediately start coding the baseline.

First, we should extract the paper's methodology mathematically.

In particular, we need to identify exactly:

The standard A\* evaluation function used by the paper
The paper's adaptive estimation function
How the adaptive parameter changes
The exact distance model
The redundant-point deletion algorithm
Grid connectivity — 4-neighbor or 8-neighbor
Obstacle generation
Start/goal selection
All parameter values
Baseline algorithms
Evaluation metrics
Number of experiments/runs
Exact experimental map sizes
Any comparison tables/figures
Because this sentence from Gemini is potentially important:

"the exact mathematical coefficients or decay rates used in the adaptive estimation function might require empirical tuning"

We should not assume that yet. If the paper actually specifies the coefficients, we need to use them. If it doesn't, then that becomes a documented reproducibility limitation.

And that's actually useful for your assignment.

I would structure our work in this order
Phase 1 — Verify the paper
Before implementation:

Paper → source-code check → methodology extraction → experimental details

We need to establish that:

The paper satisfies the assignment's Original Implementation Requirement.

Phase 2 — Reproducibility analysis
We'll answer the seven required questions properly, including distinguishing:

explicitly stated information
information inferred from equations
information missing from the paper
assumptions we have to make
Phase 3 — Independent implementation
First:

Traditional A\*
Then:

A\* + Adaptive Estimation
Then:

A\* + Adaptive Estimation

- Distance Model
  Then:

Full Proposed Algorithm

- Redundant Point Deletion
  This is much better than jumping straight into the final algorithm because it gives us the ablation study required for a convincing reproduction.

Phase 4 — Reproduce experiments
We'll implement the relevant map sizes:

30 × 30
60 × 60
100 × 100
and reproduce the paper's experimental conditions as closely as possible.

If the original maps are unavailable, we'll explicitly document that and generate equivalent maps using the paper's described procedure.

Phase 5 — Statistical reproduction
Since random obstacle placement means we probably cannot reproduce the exact path, we shouldn't pretend otherwise.

Instead:

Seed 1
Seed 2
Seed 3
...
Seed N
Then report:

mean
standard deviation
minimum/maximum where useful
That gives us a much stronger argument than reproducing one arbitrary map.

Phase 6 — Comparison
We'll produce the assignment's required table:

Metric Published Result Our Result Difference
Path length
Search nodes
Runtime
Turns
And importantly, we'll not call our result "better" simply because a number happens to be higher/lower. We'll interpret each metric according to whether higher or lower is desirable.

One more important point
Your final report should clearly separate three things:

Original paper

"The authors propose..."

Our implementation

"We independently implemented..."

Our modifications/assumptions

"Because the paper does not specify X, we assumed..."

That distinction is particularly important for this assignment because the professor explicitly wants the implementation to be independently developed.

So yes: I would tentatively select this paper.

But before writing the final analysis or touching the code, upload the PDF of _An Adaptive A Algorithm for Mobile Robots Global Path Planning_ here\*. I can then inspect the actual paper and we can verify Gemini's claims, extract the equations/parameters, and determine exactly what we need to implement.

tell gemini to do the next step
Send Gemini this:

We will proceed with “An Adaptive A Algorithm for Mobile Robots Global Path Planning”\* as the selected paper.

Before writing any code, do the next step: perform a complete paper-level methodology and reproducibility extraction from the actual paper I provided.

I want you to carefully inspect the paper and produce a structured implementation specification covering:

Standard A\* baseline

Grid representation

Node representation

Open/Closed lists

Neighbor connectivity (4-neighbor/8-neighbor)

g(n), h(n), and f(n)

Movement costs

Tie-breaking rules, if specified

Adaptive Estimation Function

Give the exact mathematical equation from the paper

Define every variable and parameter

Explain how the adaptive value changes during search

Identify every coefficient, threshold, decay rate, or constant

Explain exactly where it replaces/modifies the standard A\* heuristic

Optimized Distance Model

Give the exact mathematical formulation

Explain how it differs from the standard distance/heuristic calculation

Identify all constants and parameters

Explain exactly how it should be implemented

Redundant Point Deletion / Path Smoothing

Reconstruct the exact algorithm described by the authors

Explain the condition for deleting a point

Explain how collision/obstacle checking is performed

Explain whether the operation changes path length, number of turns, or both

Provide pseudocode based strictly on the paper

Complete Proposed Algorithm

Combine all three modifications into one step-by-step algorithm

Give clear pseudocode for the full proposed Adaptive A\*

Clearly distinguish the original A\* operations from the authors' modifications

Experimental Setup
Extract every experimental detail stated in the paper:

Grid sizes

Map/environment generation

Obstacle generation

Obstacle density, if given

Start and goal positions

Number of experiments/runs

Randomness/random seeds, if provided

Compared algorithms

Parameter values

Evaluation metrics

Hardware/software information

Any other experimental settings

Published Results
Extract the numerical results reported by the paper into tables where possible.
For every result, identify exactly what metric was measured and under what experimental condition.

Reproducibility Audit
Create three categories:

Explicitly specified by the paper

Can be reasonably inferred

Not specified / ambiguous

Pay particular attention to anything we would need to guess when implementing the algorithm.

Implementation Decisions
Based ONLY on the paper, provide a proposed Python implementation specification using:

Python

NumPy

Matplotlib

Python standard library where possible

Do not write the actual implementation yet.

Source-code requirement
Also verify the paper's public implementation status. Search GitHub, GitLab, Papers With Code, the authors' pages, supplementary material, and other relevant sources. Determine whether a complete implementation of the proposed methodology is publicly available. If you find code, explain exactly what it contains and whether it would disqualify this paper under the assignment's “Original Implementation Requirement.”

Important:

Do NOT fill missing information with assumptions and present it as if it came from the paper.

Quote equations accurately, but do not reproduce large portions of the paper verbatim.

Clearly label anything that is your inference.

If the paper is ambiguous, explicitly say so.

Do not start coding yet.

The goal of this step is to create a precise technical specification that we can use to independently implement the paper in the next step.

At the end, give me a “Ready for Implementation” checklist showing what is known, what is missing, and what assumptions will need to be documented.

Based on the provided excerpts of the research article "An Adaptive A\* Algorithm for Mobile Robots Global Path Planning", here is the comprehensive paper-level methodology and reproducibility extraction.

### 1. Standard A\* Baseline

- **Grid Representation:** The environment is represented as a 2D raster/grid map where white cells are passable areas, black cells are obstacles, a red cell is the start, and a blue cell is the destination.

- **Node Representation:** Nodes are represented by their $(x, y)$ grid coordinates.

- **Open/Closed Lists:** The algorithm utilizes standard OPEN_LIST (for nodes to be evaluated) and CLOSE_LIST (for already evaluated nodes) structures.

- **Neighbor Connectivity:** Not explicitly stated in the text, but visual evidence from the simulation maps (Figures 5, 8-12) shows the red path moving diagonally through grid corners. **Inference:** The algorithm uses an 8-neighbor connectivity model.

- **g(n), h(n), and f(n):** The algorithm relies on the standard cost components where $g(n)$ is the cost from the start, $h(n)$ is the estimated cost to the goal, and $f(n)$ is the total estimated path cost.

- **Movement Costs:** Not explicitly specified. **Inference:** Standard geometric costs will be assumed (1 for horizontal/vertical, $\sqrt{2}$ for diagonal).

- **Tie-breaking rules:** Not specified.

### 2. Adaptive Estimation Function

- **Mathematical Equation:** The standard evaluation function is modified to:

  $$f(n) = g(n) + \omega(n) \cdot h(n)$$

  Where the adaptive weight $\omega(n)$ is calculated as:

  $$\omega(n) = \ln\left(1 + e^{\frac{d}{D}}\right)$$

  .

- **Variable Definitions:**
  - $d$: The distance between the current node and the target node.

  - $D$: The distance between the starting node and the target node.

- **Behavior During Search:** When the robot is far from the target (start of search), $d \approx D$, making the weight $\omega(n)$ larger. This focuses the search towards the target, increasing speed. As the robot approaches the target, $d$ decreases, lowering $\omega(n)$ to rely more on actual costs and ensure accurate arrival at the target.

- **Coefficients/Constants:** The equation does not utilize any arbitrary tuned coefficients or decay rates; it relies purely on the dynamic ratio of $d$ to $D$.

- **Modification Point:** This replaces the standard $f(n) = g(n) + h(n)$ step during neighbor evaluation before pushing to the OPEN_LIST.

### 3. Optimized Distance Model

- **Mathematical Formulation:** The paper states the distance model is the "arithmetic mean of Euclidean distance and Manhattan distance". **Inferred Formulation:**

  $$h(n) = \frac{\sqrt{(x_n - x_t)^2 + (y_n - y_t)^2} + (\vert{}x_n - x_t\vert{} + \vert{}y_n - y_t\vert{})}{2}$$

- **Differences from Standard:** Instead of using just one metric, it combines them to balance the directness of Euclidean distance with the grid-aligned penalty of Manhattan distance, improving adaptability in diverse maps.

- **Implementation:** This equation replaces the standard $h(n)$ calculation used in the Adaptive Estimation Function above. Note: The paper implies this is also used to calculate the $d$ and $D$ variables in the weight function, though this is slightly ambiguous.

### 4. Redundant Point Deletion / Path Smoothing

- **Algorithm Description:** The paper states a "redundant point deletion strategy is implemented to remove unnecessary nodes along the route," which specifically targets reducing "corners with angles $\ge 45^\circ$".

- **Missing Information:** The exact mechanical steps, collision/obstacle checking methods (e.g., Line of Sight algorithms), and mathematical conditions for point deletion are **completely missing** from the provided text.

- **Path Effects:** The operation successfully shortens the total path length and reduces the number of turns.

- **Inferred Pseudocode:** Because the exact method is missing, we must infer a standard post-processing Line-of-Sight (LoS) algorithm:

  Plaintext

  function DeleteRedundantPoints(path):
  smooth_path = [path[0]]
  current_index = 0
  while current_index < length(path) - 1:
  furthest_visible_index = current_index + 1
  for i from current_index + 2 to length(path) - 1:
  if LineOfSightClear(path[current_index], path[i]):
  furthest_visible_index = i
  smooth_path.append(path[furthest_visible_index])
  current_index = furthest_visible_index
  return smooth_path

### 5. Complete Proposed Algorithm (Pseudocode)

Plaintext

function AdaptiveAStar(start, target, map):
OPEN_LIST = [start]
CLOSE_LIST = []
D = CalculateDistance(start, target) // Using Arithmetic Mean Distance

    while OPEN_LIST is not empty:
        current = Node in OPEN_LIST with lowest f(n)
        if current == target:
            path = ReconstructPath(current)
            return DeleteRedundantPoints(path)

        move current from OPEN_LIST to CLOSE_LIST

        for neighbor in Get8Neighbors(current):
            if neighbor in CLOSE_LIST or neighbor is Obstacle:
                continue

            tentative_g = current.g + MovementCost(current, neighbor)

            if neighbor not in OPEN_LIST or tentative_g < neighbor.g:
                neighbor.g = tentative_g

                // Optimized Distance Model
                h_euclidean = EuclideanDist(neighbor, target)
                h_manhattan = ManhattanDist(neighbor, target)
                neighbor.h = (h_euclidean + h_manhattan) / 2

                // Adaptive Estimation Function
                d = neighbor.h
                omega = ln(1 + e^(d / D))
                neighbor.f = neighbor.g + omega * neighbor.h

                neighbor.parent = current
                if neighbor not in OPEN_LIST:
                    add neighbor to OPEN_LIST

    return Failure

### 6. Experimental Setup

- **Grid Sizes:** $30 \times 30$, $60 \times 60$, $100 \times 100$.

- **Environments:**
  - 30x30: Irregular outdoor scenes.

  - 60x60: Structured indoor scenes (mazes, corridors).

  - 100x100: Large array-like scenes (photovoltaic stations, dense warehouses).

- **Obstacles:** Maps are constructed programmatically in MATLAB. The specific obstacle density or seed generation is not stated.

- **Start and Goal Positions:**
  - 30x30: Start (2, 2) $\rightarrow$ End (28, 28) AND Start (4, 24) $\rightarrow$ End (29, 2).

  - 60x60: Start (2, 2) $\rightarrow$ End (58, 58) AND Start (4, 54) $\rightarrow$ End (59, 2).

  - 100x100: Start (2, 2) $\rightarrow$ End (99, 99).

- **Compared Algorithms:** Conventional A\*, Dijkstra, Chen's method, Bidirectional A\*, and Zhang's method.

- **Evaluation Metrics:** Planning time (seconds), path length (meters), number of expanded/traversed nodes, number of corners with angles $\ge 45^\circ$.

- **Hardware/Software:** Windows 11, Intel Core i5-1340P @ 1.9 GHz, 16 GB RAM, MATLAB R2023b.

### 7. Published Results

The following results compare the traditional A\* algorithm to the proposed Adaptive A\*.

| **Map Size** | **Start** | **End**  | **Algorithm** | **Time (s)** | **Length (m)** | **Expanded Nodes** | **Corners ≥45∘** |
| ------------ | --------- | -------- | ------------- | ------------ | -------------- | ------------------ | ---------------- |
| **30x30**    | (2, 2)    | (28, 28) | A\*           | 0.03         | 40.30          | 202                | 13               |
| **30x30**    | (2, 2)    | (28, 28) | Adaptive A\*  | 0.01         | 39.92          | 43                 | 6                |
| **30x30**    | (4, 24)   | (29, 2)  | A\*           | 0.04         | 38.21          | 250                | 14               |
| **30x30**    | (4, 24)   | (29, 2)  | Adaptive A\*  | 0.01         | 37.68          | 33                 | 5                |
| **60x60**    | (2, 2)    | (58, 58) | A\*           | 0.25         | 92.08          | 898                | 19               |
| **60x60**    | (2, 2)    | (58, 58) | Adaptive A\*  | 0.04         | 88.81          | 123                | 7                |
| **60x60**    | (4, 54)   | (59, 2)  | A\*           | 0.41         | 118.49         | 1159               | 27               |
| **60x60**    | (4, 54)   | (59, 2)  | Adaptive A\*  | 0.13         | 114.96         | 478                | 13               |

### 8. Reproducibility Audit

- **Explicitly Specified:** The heuristic formula $\omega(n)$, grid sizes, start/goal coordinates, performance metrics, hardware/software setup, and distance model concept.

- **Can Be Reasonably Inferred:** 8-neighbor grid connectivity (from images), movement costs (standard Euclidean rules), and the exact mathematical formula for the arithmetic mean distance model.

- **Not Specified / Ambiguous:**
  - The algorithmic logic for the "redundant point deletion strategy".

  - The specific map generation algorithm (how obstacles are placed/seeded).

  - Whether the variable $d$ in the adaptive function uses the optimized distance model or just standard Euclidean distance.

### 9. Implementation Decisions

To independently implement this in Python:

- **Libraries:** numpy for grid representation and vector math. matplotlib.pyplot for replicating the map visualizations. Standard heapq for managing the OPEN_LIST priority queue.

- **Map Generation:** Because the original map seed is unknown, we will create a map generator that creates random obstacles of varying sizes to approximate the obstacle density seen in Figure 5.

- **Smoothing Assumption:** We will document an assumption that "redundant point deletion" utilizes a Bresenham Line-of-Sight check from the current node to the furthest visible node in the path sequence, as this is the standard geometric method for reducing path turning angles.

### 10. Source-Code Requirement Verification

A search across standard academic repositories (GitHub, GitLab, Papers With Code) yields no publicly available source code
…
This is a good extraction, but I would not mark it fully ready for implementation yet. There are a few places where Gemini has moved from "paper says" to "we infer" too aggressively.

The most important issue is the adaptive heuristic formula and the meaning of
d
d. If we get that wrong, the entire reproduction becomes questionable.

I would send Gemini one more prompt before we code:

Good. Before we begin implementation, perform one final technical verification pass over the actual paper.

Do NOT write code yet.

I want you to resolve or explicitly flag the following issues:

1. Verify the adaptive heuristic mathematically
   Re-read the exact section/equations defining the adaptive estimation function.

We currently have:

f(n) = g(n) + ω(n)h(n)

ω(n) = ln(1 + e^(d/D))

Verify whether this is EXACTLY the equation in the paper, including:

logarithm base

numerator/denominator

parentheses

whether d is Euclidean distance, Manhattan distance, the proposed optimized distance, or something else

whether D is the start-to-goal distance

whether d and D are calculated using the same distance model

whether ω is intended to increase or decrease as the search approaches the goal

Do not infer this from general A\* knowledge. Use the paper's actual definition.

2. Verify the optimized distance model
   Confirm whether the paper explicitly defines:

h(n) = (Euclidean distance + Manhattan distance) / 2

If yes, identify exactly where this equation is used.

If the paper uses a different notation or formulation, reproduce that formulation instead.

Most importantly, determine whether this optimized distance is used for:

h(n)

d

D

all three

or only some of them.

3. Verify the interpretation of the adaptive weight
   Our current explanation says:

"Far from the goal → larger ω → stronger heuristic guidance.
Near the goal → smaller ω → more reliance on g(n)."

Check whether this interpretation is mathematically correct given the actual equation.

Calculate example values of ω for d/D = 1, 0.5, 0.1, and 0 to demonstrate the behavior.

4. Verify the grid movement model
   Do not simply infer 8-neighbor connectivity from the figures.

Search the entire paper for:

4-neighbor

8-neighbor

diagonal movement

neighborhood

movement cost

Euclidean distance

Manhattan distance

If 8-neighbor movement is still not explicitly stated, label it clearly as an implementation assumption.

Also determine whether diagonal movement costs 1, sqrt(2), or something else.

5. Investigate the redundant-point deletion method more deeply
   Search the entire paper for every reference to:

redundant points

redundant node deletion

path smoothing

corners

angle

45°

deletion

optimization after path generation

Determine whether there is an equation, figure, pseudocode, geometric condition, or textual description that Gemini may have missed.

Do NOT automatically assume Line-of-Sight/Bresenham is what the authors used.

If the method is genuinely underspecified, state:

"Not reproducible exactly from the paper."

Then distinguish:

what the authors explicitly say

what our implementation will assume

why our assumption is reasonable.

6. Verify the experimental maps
   We need to know whether the maps are:

randomly generated,

manually constructed,

based on real environments,

generated from images,

or manually configured in MATLAB.

Pay particular attention to Figure 5 and all map figures.

Determine whether the paper provides enough information to recreate the actual obstacle layouts.

If exact maps cannot be reconstructed, explicitly state that our reproduction will use newly generated maps rather than claiming to reproduce the exact original maps.

7. Verify all published numerical results
   Go through every result table/figure in the paper and identify:

all algorithms

all map sizes

all start/goal configurations

all reported metrics

all numerical values

Do not limit the extraction to the A* vs Adaptive A* rows if additional experimental results exist.

Create a final "Published Results Available for Reproduction" table.

8. Check for internal inconsistencies
   Look for contradictions between:

equations

text

figures

tables

captions

For example, if the text says one thing but the figures suggest another, flag it.

9. Source-code verification
   For the source-code requirement, do a more rigorous search.

Check:

GitHub

GitLab

Papers With Code

Google/Baidu search results

author names + paper title

author institutional pages

supplementary materials

publisher page

If no complete implementation is found, say:

"No complete publicly available implementation was identified as of [date]."

Do NOT claim that the absence of a repository proves no implementation exists anywhere.

10. Final implementation specification
    After completing the verification, produce a final specification with these exact sections:

A. Confirmed from paper
B. Reasonable implementation assumptions
C. Information that cannot be reproduced
D. Exact baseline A* specification
E. Exact proposed Adaptive A* specification
F. Exact redundant-point deletion specification
G. Experimental protocol
H. Published results to reproduce
I. Reproduction risks
J. Final implementation checklist

The most important requirement is: never silently turn an inference into a fact from the paper.

We need this verification completed before writing the Python implementation.

Based on a rigorous technical verification of the provided paper "An Adaptive A\* Algorithm for Mobile Robots Global Path Planning", here is the resolution of the implementation issues and the final technical specification.

1. Verification of the Adaptive Heuristic
   The mathematical formulation is explicitly defined in the paper as:

$$f(n) = g(n) + \omega(n) \cdot h(n)$$

$$\omega(n) = \ln\left(1 + e^{\frac{d}{D}}\right)$$

Logarithm Base: The paper uses the natural logarithm ($\ln$).

Numerator/Denominator: The ratio is strictly $d$ (current node to target) over $D$ (start to target).

Distance Model for $d$ and $D$: Ambiguous. The text states $d$ is "the distance between the current node and the target node" and $D$ is "the distance between the starting node and the target node". It does not explicitly state whether this uses the standard Euclidean distance or the authors' newly proposed arithmetic mean distance model.

Behavior: Mathematically, $\omega(n)$ decreases as the robot approaches the target, which perfectly aligns with the text.

2. Verification of the Optimized Distance Model
   The paper explicitly defines the optimized distance model as the arithmetic mean of the Euclidean and Manhattan distances.

$$h(n) = \frac{\sqrt{(x_n - x_g)^2 + (y_n - y_g)^2} + \vert{}x_n - x_g\vert{} + \vert{}y_n - y_g\vert{}}{2}$$

Usage: This explicitly replaces the standard $h(n)$ in the total cost estimate function $f(n)$. As noted above, whether it is also used to calculate the $d$ and $D$ scalar variables in the weight function is not explicitly defined.

3. Verification of the Adaptive Weight Interpretation
   Our mathematical interpretation is correct. Let's calculate the bounds using $\omega(n) = \ln(1 + e^{d/D})$:

Start of search ($d = D \rightarrow d/D = 1$): $\omega = \ln(1 + e^1) = \ln(3.718) \approx 1.313$

Midpoint ($d/D = 0.5$): $\omega = \ln(1 + e^{0.5}) = \ln(1 + 1.648) \approx 0.974$

Near target ($d/D = 0.1$): $\omega = \ln(1 + e^{0.1}) = \ln(1 + 1.105) \approx 0.744$

At target ($d = 0 \rightarrow d/D = 0$): $\omega = \ln(1 + e^0) = \ln(2) \approx 0.693$

The weight scales smoothly from a mild overestimation (~1.313) to an underestimation (~0.693) as the search progresses, dynamically shifting priority from the heuristic to the actual movement cost $g(n)$.

4. Verification of the Grid Movement Model
   Explicit mentions: The text states the distance model "can be applied in maps with four directions, or in an eight-directional environment map".

Implementation Assumption: The authors do not explicitly declare which configuration they used for their simulation results. However, Figures 5, 8, 9, and 10 clearly show diagonal pathing. We will firmly assume 8-neighbor connectivity. Movement costs (1 for orthogonal, $\sqrt{2}$ for diagonal) are not stated and will be assumed based on standard A\* geometric principles.

5. Investigation of the Redundant-Point Deletion Method
   Explicit Description: The authors describe a "collinearity determination" process: "starting from the origin, select three nodes from the path node set, and determine whether these three nodes are collinear. If the three nodes are collinear and there are no obstacles between them, delete the intermediate node...".

Missing Information: The paper abruptly ends the explanation with "proceed to Step 3", but Step 3 is completely missing from the provided methodology. Furthermore, checking "collinearity" of grid points naturally implies they form a straight line, but the exact mechanism for checking "no obstacles between them" is unspecified.

Conclusion: Not reproducible exactly from the paper. We will assume a standard Vector Cross-Product collinearity check for consecutive points, followed by a Bresenham Line-of-Sight check to replicate the behavior shown in Figure 4.

6. Verification of the Experimental Maps
   Map Generation: The maps are manually constructed or algorithmically generated in MATLAB representing 30x30 "irregular outdoor scenes", 60x60 "structured indoor scenes", and 100x100 "large array-like scenes".

Conclusion: The exact coordinate placements of the obstacles are not provided. Our reproduction will use newly generated maps matching these descriptive densities and layouts, rather than claiming to reproduce the exact original matrices.

7. Published Results Available for Reproduction
   Based on the text and figures provided, along with the previously extracted data, here are the target metrics for reproduction:

Map Size Start End Algorithm Target Metrics to Compare
30x30 (Irregular) (2, 2) (28, 28) A*, Dijkstra, Bidirectional A*, Adaptive A* Search Time, Path Length, Expanded Nodes
60x60 (Maze) (2, 2) (58, 58) A*, Dijkstra, Bidirectional A*, Adaptive A* Search Time, Path Length, Expanded Nodes
100x100 (Array) (2, 2) (99, 99) A*, Dijkstra, Bidirectional A*, Adaptive A\* Search Time, Path Length, Expanded Nodes 8. Internal Inconsistencies
Missing Steps: The algorithm description for redundant point deletion explicitly references a "Step 3" that does not exist in the text.

Variable Overload: The equation variables $x_n, x_g$ are used to define the heuristic $h(n)$, but the adaptive weight equation relies on $d$ and $D$ without formally linking the two formulas geometrically.

9. Source-Code Verification
   A rigorous search across GitHub, GitLab, Papers With Code, author institutional pages, and standard academic repositories confirms that no complete publicly available implementation was identified as of October 2026. Implementing this logic independently fully satisfies the assignment's "Original Implementation Requirement."

Final Implementation Specification
A. Confirmed from paper

Base algorithm: A\* with OPEN_LIST and CLOSE_LIST.

Cost function: $f(n) = g(n) + \omega(n) \cdot h(n)$.

Weight function: $\omega(n) = \ln(1 + e^{d/D})$.

Distance function $h(n)$: Arithmetic mean of Euclidean and Manhattan distances.

Map sizes: 30x30, 60x60, 100x100.

Start/Goal coordinates: (2,2) to (28,28), (58,58), and (99,99) respectively.

B. Reasonable implementation assumptions

Connectivity: 8-neighbor grid movement with standard geometric costs (1 and $\sqrt{2}$).

Distance calculation for $\omega$: $d$ and $D$ will be calculated using the standard Euclidean distance to ensure a normalized $0 \le d/D \le 1$ ratio, as using the arithmetic mean could skew the ratio unpredictably.

Map Generation: Random array, maze, and scatter generations will be used to mimic Figures 5a, 5b, and 5c.

C. Information that cannot be reproduced

The exact obstacle placement (seed) of the original MATLAB maps.

The literal "Step 3" of the redundant point deletion strategy.

D. Exact baseline A specification\*

Standard Priority Queue (heapq) implementation.

$f(n) = g(n) + h_{euclidean}(n)$.

8-neighbor expansion, checking bounds and obstacles.

E. Exact proposed Adaptive A specification\*

During neighbor expansion, calculate $h(n)$ using Equation 7.

Calculate Euclidean distance $d$ from neighbor to target.

Calculate $\omega = \ln(1 + e^{d/D})$.

Assign $f(n) = g(n) + \omega \cdot h(n)$ and push to OPEN_LIST.

F. Exact redundant-point deletion specification

Input: Completed path array of $(x,y)$ tuples.

Iterate through path: For three sequential nodes $A, B, C$, check cross-product collinearity. If collinear, remove $B$.

Secondary pass: For remaining nodes, use Bresenham's line algorithm to check for clear line-of-sight between non-adjacent nodes. If clear, delete intermediate nodes.

G. Experimental protocol

Generate three grid maps (30x30, 60x60, 100x100) mimicking the paper's layouts.

Run Baseline A* and Adaptive A* on each map.

Record execution time, path length, and total expanded nodes.

H. Published results to reproduce

Comparison of path length reduction and expanded node reduction between A* and Adaptive A* across the three map scales.

I. Reproduction risks

Because the maps are randomly generated, the absolute path lengths and node counts will not match the paper exactly. We will evaluate success based on the relative percentage improvement of Adaptive A* over standard A*.

J. Final implementation checklist

Write Python Map Generator (Irregular, Maze, Array).

Implement Baseline A\* class.

Implement Adaptive A\* class with custom $f(n)$ and $h(n)$.

Implement Path Smoother (Collinearity + Bresenham).

Write benchmarking script to collect time, length, and node expansion metrics.

Generate Matplotlib visualizations mimicking Figure 5.

…
This is now a solid implementation specification, and I think we can move into implementation.

There is one methodological point I would change before coding:

Do not evaluate reproduction only by relative percentage improvement.

Because we are generating different maps from the original paper, we cannot fairly claim that matching the percentage improvement proves reproduction. We should report both:

Absolute results on our independently generated maps
Relative behavior/improvement of Adaptive A* over baseline A*
Comparison with the paper's reported trends/results
Why exact numerical reproduction is impossible because the original obstacle matrices are unavailable
That distinction will make your Critical Analysis much stronger.

Implementation plan
I recommend we build this incrementally:

Step 1 — Reproducible environment
Create a deterministic map generator:

30 × 30
60 × 60
100 × 100
with fixed random seeds.

We should save the generated maps so that every experiment can be rerun on exactly the same environments.

Step 2 — Baseline A\*
Implement independently:

f
(
n
)
=
g
(
n
)

- h
  (
  n
  )
  f(n)=g(n)+h(n)
  with:

h
(
n
)
=
(
x
n
−
x
g
)
2

- (
  y
  n
  −
  y
  g
  )
  2
  h(n)=
  (x
  n
  ​
  −x
  g
  ​
  )
  2
  +(y
  n
  ​
  −y
  g
  ​
  )
  2

​

and the assumed 8-neighbor movement:

c
orthogonal
=
1
c
orthogonal
​
=1
c
diagonal
=
2
c
diagonal
​
=
2
​

We'll track:

runtime
path length
expanded nodes
number of path points
turns
Step 3 — Proposed Adaptive A\*
Implement the paper's equations:

h
(
n
)
=
(
x
n
−
x
g
)
2

- (
  y
  n
  −
  y
  g
  )
  2
- ∣
  x
  n
  −
  x
  g
  ∣
- ∣
  y
  n
  −
  y
  g
  ∣
  2
  h(n)=
  2
  (x
  n
  ​
  −x
  g
  ​
  )
  2
  +(y
  n
  ​
  −y
  g
  ​
  )
  2

​
+∣x
n
​
−x
g
​
∣+∣y
n
​
−y
g
​
∣
​

then:

ω
(
n
)
=
ln
⁡
(
1

- e
  d
  /
  D
  )
  ω(n)=ln(1+e
  d/D
  )
  and:

f
(
n
)
=
g
(
n
)

- ω
  (
  n
  )
  h
  (
  n
  )
  f(n)=g(n)+ω(n)h(n)
  with our Euclidean
  d
  d and
  D
  D assumption explicitly documented.

Step 4 — Redundant-point deletion
Implement the paper's explicitly described part first:

A ---- B ---- C
If A, B, C are collinear and the segment is obstacle-free:

A ---------------- C
Then implement the missing portion using the documented Bresenham line-of-sight assumption.

We should keep this component modular so we can easily test:

Adaptive A*
Adaptive A* + smoothing
separately.

Step 5 — Ablation experiments
This is particularly important for your marks.

We'll test:

Version Adaptive
ω
ω Optimized
h
h Point deletion
Baseline A* No No No
A* + Adaptive Weight Yes No No
A* + Optimized Distance No Yes No
Adaptive A* Yes Yes No
Full Proposed Yes Yes Yes
This allows us to answer which proposed modification actually contributes to which improvement.

Step 6 — Multiple runs
For each map size, use multiple deterministic maps/seeds rather than one random map.

For example:

30×30 → seeds 1–10
60×60 → seeds 1–10
100×100 → seeds 1–10
Then report:

mean
±
standard deviation
mean±standard deviation
for runtime, path length, expanded nodes, and turns.

Step 7 — Final comparison
We'll eventually have something like:

Map Algorithm Time (s) Path Length Expanded Nodes Turns
30×30 A* ... ... ... ...
30×30 Adaptive A* ... ... ... ...
60×60 A* ... ... ... ...
60×60 Adaptive A* ... ... ... ...
100×100 A\* ... ... ... ...
And then separately compare those trends against the paper.

One important viva point
If the examiner asks:

"Did you reproduce the exact results?"

The technically correct answer will be:

No, exact numerical reproduction was not possible because the paper does not provide the original obstacle matrices or random-generation seeds. We therefore reproduced the methodology and experimental conditions as closely as possible, generated controlled equivalent environments, and evaluated whether the proposed algorithm demonstrated the same qualitative and quantitative trends relative to the baseline.

That's a much stronger answer than claiming that different randomly generated maps somehow reproduce the original numbers.

We are ready for the coding phase.

let's do it then?
Absolutely. Let's build it properly and incrementally, rather than dumping the entire project at once.

We'll start with Phase 1: project structure + deterministic grid environment + baseline A\*. Once that works, we'll add the paper's adaptive components.

Phase 1 goal
By the end of this step we should have:

30×30, 60×60, and 100×100 maps
deterministic obstacle generation
8-neighbor movement
start/goal validation
baseline A*
path reconstruction
path length calculation
expanded-node counting
runtime measurement
Matplotlib visualization
We'll not implement the Adaptive A* yet. That gives us a trustworthy baseline to compare against later.

If you want, I can create the complete starter project files now, including README.md, requirements.txt, map generator, baseline A\*, visualization, and experiment runner.

give prompt to build thid
If you are going to have an AI coding agent build the Phase 1 implementation, use this prompt. It is written to make the agent actually inspect the project, create the files, implement the baseline, and test it, rather than just explain what to do.

:

Phase 1 — Reimplement Adaptive A* Paper: Baseline A* Foundation
You are working on a university research-paper reimplementation project.

The selected paper is:

“An Adaptive A Algorithm for Mobile Robots Global Path Planning”\*

The goal of this phase is NOT to implement the proposed Adaptive A\* algorithm yet.

For Phase 1, build a clean, reproducible implementation of the experimental foundation and conventional A baseline\*. Later phases will add the paper's adaptive heuristic, optimized distance model, path smoothing, experiments, and comparison against the published results.

1. First inspect the project
   Before creating or modifying files:

Inspect the existing project structure.

Inspect any existing AGENTS.md, CLAUDE.md, README.md, configuration files, and source files.

If the project already has conventions, follow them.

Do not unnecessarily replace or restructure existing code.

If there is an existing agent/instruction file, follow it.

After inspection, create a clean implementation structure if one does not already exist.

Recommended structure:

adaptive-astar-reimplementation/
│
├── README.md
├── requirements.txt
├── run_baseline.py
│
├── src/
│ ├── **init**.py
│ ├── config.py
│ ├── grid_map.py
│ ├── astar.py
│ ├── metrics.py
│ ├── visualization.py
│ └── experiments.py
│
├── tests/
│ └── test_astar.py
│
├── results/
│ ├── maps/
│ ├── figures/
│ └── .gitkeep
│
└── docs/
└── assumptions.md
You may adjust the structure if the existing project has a better convention.

2. Important research context
   The paper works on 2D grid/raster environments for mobile robot global path planning.

The paper describes:

2D grid maps

passable and obstacle cells

start and destination nodes

OPEN/CLOSED lists

A\* search

4- or 8-direction movement

path planning time

path length

number of expanded/traversed nodes

path corners

map sizes of:

30 × 30

60 × 60

100 × 100

The paper's exact obstacle matrices/seeds are not available.

Therefore:

Do NOT claim that our generated maps reproduce the original paper maps.

Instead, create deterministic synthetic maps that approximately represent the environment styles described by the paper.

All assumptions must be explicitly documented.

3. Coordinate convention
   The paper uses coordinates that appear to be 1-based.

For example:

30 × 30
Start: (2, 2)
Goal: (28, 28)

Start: (4, 24)
Goal: (29, 2)
60 × 60
Start: (2, 2)
Goal: (58, 58)

Start: (4, 54)
Goal: (59, 2)
100 × 100
Start: (2, 2)
Goal: (99, 99)
Python uses 0-based indexing.

Implement a clear conversion between paper coordinates and Python coordinates.

Do not silently mix coordinate systems.

4. Grid map representation
   Implement a reusable GridMap abstraction.

Requirements:

NumPy-backed grid

obstacle/free-cell representation

width/height

coordinate validation

is_free()

neighbor generation

start/goal validation

ability to save/load maps

Use something simple such as:

True = obstacle
False = free
or the inverse, but document it clearly and use it consistently.

5. 8-neighbor movement
   For Phase 1, implement 8-direction movement.

The eight possible moves are:

(-1, -1)
(-1, 0)
(-1, +1)
( 0, -1)
( 0, +1)
(+1, -1)
(+1, 0)
(+1, +1)
Movement costs:

horizontal/vertical = 1
diagonal = sqrt(2)
This is an implementation assumption because the paper does not provide enough detail to uniquely determine the exact movement-cost implementation.

Document this assumption.

Also decide how diagonal corner cutting is handled.

Prefer:

Diagonal movement is allowed only when the two adjacent orthogonal cells are free.
Document this explicitly as an assumption.

Make this behavior configurable rather than hard-coded if practical.

6. Conventional A* implementation
   Implement a clean standalone A* algorithm.

Use:

f(n) = g(n) + h(n)
For the baseline:

h(n) = Euclidean distance from n to goal
That means:

h(n) = sqrt((x_n - x_g)^2 + (y_n - y_g)^2)
Use:

heapq priority queue

g_score

parent/came-from map

CLOSED set

deterministic tie handling

path reconstruction

Do not use a library implementation of A\*.

The purpose is to independently reimplement the algorithm.

7. A\* result object
   Do not return only a path.

Create a structured result such as:

@dataclass
class SearchResult:
success: bool
path: list[tuple[int, int]] | None
path_length: float
expanded_nodes: int
runtime_seconds: float
You may include additional useful fields such as:

discovered_nodes
unique_expanded_nodes
but keep the API simple.

8. Runtime measurement
   Measure only the actual path-planning algorithm.

Use:

time.perf_counter()
Do NOT include:

map generation

file saving

visualization

plotting

printing

inside the measured A\* runtime.

Document this.

Because these grids are relatively small, runtime can be noisy. For Phase 1 a single deterministic run is acceptable, but structure the code so later experiments can perform multiple repetitions.

9. Path length
   Implement path-length calculation independently from A\*.

For each consecutive pair of path nodes:

horizontal/vertical = 1
diagonal = sqrt(2)
Sum all movement costs.

Example:

length = sum(distance(p_i, p_i+1))
Return the result as a floating-point number.

10. Expanded-node metric
    Track the number of nodes expanded by A\*.

Define this clearly in the documentation.

Prefer counting nodes when they are actually removed from the priority queue and processed as the current node.

Also consider tracking:

unique_expanded_nodes
separately if nodes can be reopened.

Do not pretend that this exactly matches the paper's definition unless the paper explicitly defines it.

11. Corner/turn metric
    Implement a reusable metric for the number of path direction changes.

For every three consecutive path points:

p1 -> p2 -> p3
calculate the change in direction.

Count a corner if the direction-change angle is:

> = 45 degrees
> The paper's exact angle calculation is not sufficiently detailed, so document the interpretation used.

Do not yet modify the path based on this metric.

12. Synthetic map generation
    Create deterministic map generators for the three environment categories described in the paper.

30 × 30
Represent an irregular outdoor-style environment.

Use irregular obstacle clusters/rectangles.

60 × 60
Represent a structured indoor/maze-like environment.

Use walls, corridors, or structured obstacle blocks.

100 × 100
Represent a large structured environment similar to dense warehouse/PV-array layouts.

Use repeated obstacle structures/blocks.

The exact obstacle placement from the paper is unavailable.

Therefore the generated maps are experimental approximations, not reproductions of the original maps.

13. Deterministic seeds
    Every generated map must be reproducible.

Use:

numpy.random.default_rng(seed)
Do not use uncontrolled global randomness.

For example:

30x30 -> seed 3030
60x60 -> seed 6060
100x100 -> seed 100100
You may choose better seed values, but make them explicit and deterministic.

14. Guarantee valid experiments
    The map generator must ensure:

start is inside the grid

goal is inside the grid

start is free

goal is free

a valid path exists

If a generated map does not satisfy these conditions, regenerate it deterministically using the next seed/attempt.

Do not manually modify maps after generation in a way that breaks reproducibility.

15. Paper scenarios
    Create configuration objects for these scenarios.

30x30
(2,2) -> (28,28)
(4,24) -> (29,2)

60x60
(2,2) -> (58,58)
(4,54) -> (59,2)

100x100
(2,2) -> (99,99)
Keep the coordinates in the configuration in paper-style 1-based coordinates.

Convert them to Python coordinates at the appropriate boundary.

16. Visualization
    Create a reusable Matplotlib visualization function.

It should display:

obstacles

free cells

start

goal

planned path

Do not hard-code a specific visual style unnecessarily.

Save figures to:

results/figures/
Use filenames containing:

map size
environment style
seed
start/goal identifier
Example:

astar_30x30_irregular_seed3030_case1.png
The visualization must not affect measured runtime.

17. Experiment runner
    Create:

run_baseline.py
Running:

python run_baseline.py
should:

generate the deterministic maps

save the generated maps

run conventional A\*

calculate:

runtime

path length

expanded nodes

number of corners

save figures

print a clean experiment table

save results to CSV

Example result columns:

map_size
environment
seed
case
start
goal
success
runtime_seconds
path_length
expanded_nodes
corners_ge_45 18. Save generated maps
Save the exact maps used for experiments.

For example:

results/maps/30x30_irregular_seed3030.npz
results/maps/60x60_maze_seed6060.npz
results/maps/100x100_array_seed100100.npz
This is important for reproducibility.

A future run should be able to load the exact same map rather than regenerate it.

19. Unit tests
    Create tests for at least:

Test 1 — Empty grid
A\* should find a path.

Test 2 — Completely blocked goal
A\* should correctly return failure.

Test 3 — Diagonal movement
Verify diagonal movement has cost:

sqrt(2)
Test 4 — Obstacle avoidance
Verify the path does not pass through obstacles.

Test 5 — Path reconstruction
Verify the first node is start and final node is goal.

Test 6 — Path length
Verify a known simple path has the expected length.

Run:

python -m unittest discover -s tests -v
and make sure all tests pass.

20. Documentation
    Create a README explaining:

Project
This is a research-paper reimplementation of:

“An Adaptive A\* Algorithm for Mobile Robots Global Path Planning”

Current phase
Phase 1 implements:

Grid environment
Synthetic deterministic maps
8-neighbor movement
Conventional A\*
Euclidean heuristic
Path reconstruction
Path length
Expanded nodes
Corner metric
Runtime measurement
Visualization
Experiment runner
Explicitly state:

Adaptive A\* is intentionally NOT implemented in this phase.

21. Assumptions documentation
    Create:

docs/assumptions.md
Document every paper ambiguity.

At minimum:

8-neighbor connectivity

movement costs

diagonal corner-cutting rule

Euclidean baseline heuristic

coordinate conversion

node-expansion definition

corner-angle definition

synthetic map generation

deterministic seeds

inability to reproduce the original obstacle matrices exactly

Use language such as:

The paper does not explicitly specify X. Therefore, this implementation assumes Y.

Do NOT present assumptions as facts from the paper.

22. Requirements
    Keep dependencies minimal.

Prefer:

numpy
matplotlib
Do not add large libraries unless necessary.

The A\* algorithm itself must be implemented manually.

23. Code quality requirements
    Follow these rules:

Python type hints

dataclasses where useful

meaningful function names

small reusable functions

no duplicated algorithmic logic

no global mutable state

clear docstrings

comments only where they explain non-obvious research decisions

deterministic behavior

no unnecessary abstraction

no notebook-only implementation

no hard-coded absolute paths

The project should run on Windows, Linux, and macOS.

Use pathlib.Path for filesystem paths.

24. Important research integrity rule
    Do not fabricate published results.

Do not put the paper's reported numbers into the experimental output and label them as our results.

Our Phase 1 results are independently generated results.

Later, we will create a separate comparison table:

Metric | Published Paper | Our Implementation | Difference
Only verified values from the paper should appear in the published-results column.

25. Do NOT implement yet
    Do NOT implement any of these in Phase 1:

adaptive weight

optimized distance heuristic

redundant point deletion

path smoothing

final Adaptive A\*

paper comparison

ablation study

Those belong to later phases.

However, design the code so that the future Adaptive A* implementation can reuse the existing A* framework.

For example, the search algorithm should make it reasonably easy to replace:

f = g + h
with a future:

f = g + omega \* h
without rewriting the entire project.

26. Final verification
    After implementation:

Run the unit tests.

Run the baseline experiment.

Verify all scenarios have valid paths.

Verify CSV results are generated.

Verify figures are generated.

Verify maps are saved.

Check for Python errors/warnings.

Check imports from a clean environment.

Do not leave debugging code or temporary files.

Give me a concise summary of:

files created

commands executed

tests passed

experiment results

assumptions made

anything that remains uncertain

Most importantly:

Do the implementation, do not merely describe how to implement it.

Phase 1 — Reimplement Adaptive A* Paper: Baseline A* Foundation
You are working on a university research-paper reimplementation project.

The selected paper is:

“An Adaptive A Algorithm for Mobile Robots Global Path Planning”\*

The goal of this phase is NOT to implement the proposed Adaptive A\* algorithm yet.

For Phase 1, build a clean, reproducible implementation of the experimental foundation and conventional A baseline\*. Later phases will add the paper's adaptive heuristic, optimized distance model, path smoothing, experiments, and comparison against the published results.

1. First inspect the project
   Before creating or modifying files:

Inspect the existing project structure.
Inspect any existing AGENTS.md, CLAUDE.md, README.md, configuration files, and source files.
If the project already has conventions, follow them.
Do not unnecessarily replace or restructure existing code.
If there is an existing agent/instruction file, follow it.
After inspection, create a clean implementation structure if one does not already exist.

Recommended structure:

adaptive-astar-reimplementation/
│
├── README.md
├── requirements.txt
├── run_baseline.py
│
├── src/
│ ├── **init**.py
│ ├── config.py
│ ├── grid_map.py
│ ├── astar.py
│ ├── metrics.py
│ ├── visualization.py
│ └── experiments.py
│
├── tests/
│ └── test_astar.py
│
├── results/
│ ├── maps/
│ ├── figures/
│ └── .gitkeep
│
└── docs/
└── assumptions.md
You may adjust the structure if the existing project has a better convention.

2. Important research context
   The paper works on 2D grid/raster environments for mobile robot global path planning.

The paper describes:

2D grid maps
passable and obstacle cells
start and destination nodes
OPEN/CLOSED lists
A\* search
4- or 8-direction movement
path planning time
path length
number of expanded/traversed nodes
path corners
map sizes of:
30 × 30
60 × 60
100 × 100
The paper's exact obstacle matrices/seeds are not available.

Therefore:

Do NOT claim that our generated maps reproduce the original paper maps.

Instead, create deterministic synthetic maps that approximately represent the environment styles described by the paper.

All assumptions must be explicitly documented.

3. Coordinate convention
   The paper uses coordinates that appear to be 1-based.

For example:

30 × 30
Start: (2, 2)
Goal: (28, 28)

Start: (4, 24)
Goal: (29, 2)
60 × 60
Start: (2, 2)
Goal: (58, 58)

Start: (4, 54)
Goal: (59, 2)
100 × 100
Start: (2, 2)
Goal: (99, 99)
Python uses 0-based indexing.

Implement a clear conversion between paper coordinates and Python coordinates.

Do not silently mix coordinate systems.

4. Grid map representation
   Implement a reusable GridMap abstraction.

Requirements:

NumPy-backed grid
obstacle/free-cell representation
width/height
coordinate validation
is_free()
neighbor generation
start/goal validation
ability to save/load maps
Use something simple such as:

True = obstacle
False = free

or the inverse, but document it clearly and use it consistently.

5. 8-neighbor movement
   For Phase 1, implement 8-direction movement.

The eight possible moves are:

(-1, -1)
(-1, 0)
(-1, +1)
( 0, -1)
( 0, +1)
(+1, -1)
(+1, 0)
(+1, +1)
Movement costs:

horizontal/vertical = 1
diagonal = sqrt(2)
This is an implementation assumption because the paper does not provide enough detail to uniquely determine the exact movement-cost implementation.

Document this assumption.

Also decide how diagonal corner cutting is handled.

Prefer:

Diagonal movement is allowed only when the two adjacent orthogonal cells are free.
Document this explicitly as an assumption.

Make this behavior configurable rather than hard-coded if practical.

6. Conventional A* implementation
   Implement a clean standalone A* algorithm.

Use:

f(n) = g(n) + h(n)
For the baseline:

h(n) = Euclidean distance from n to goal
That means:

h(n) = sqrt((x_n - x_g)^2 + (y_n - y_g)^2)
Use:

heapq priority queue
g_score
parent/came-from map
CLOSED set
deterministic tie handling
path reconstruction
Do not use a library implementation of A\*.

The purpose is to independently reimplement the algorithm.

7. A\* result object
   Do not return only a path.

Create a structured result such as:

@dataclass
class SearchResult:
success: bool
path: list[tuple[int, int]] | None
path_length: float
expanded_nodes: int
runtime_seconds: float
You may include additional useful fields such as:

discovered_nodes
unique_expanded_nodes
but keep the API simple.

8. Runtime measurement
   Measure only the actual path-planning algorithm.

Use:

time.perf_counter()

Do NOT include:

map generation
file saving
visualization
plotting
printing
inside the measured A\* runtime.

Document this.

Because these grids are relatively small, runtime can be noisy. For Phase 1 a single deterministic run is acceptable, but structure the code so later experiments can perform multiple repetitions.

9. Path length
   Implement path-length calculation independently from A\*.

For each consecutive pair of path nodes:

horizontal/vertical = 1
diagonal = sqrt(2)
Sum all movement costs.

Example:

length = sum(distance(p_i, p_i+1))

Return the result as a floating-point number.

10. Expanded-node metric
    Track the number of nodes expanded by A\*.

Define this clearly in the documentation.

Prefer counting nodes when they are actually removed from the priority queue and processed as the current node.

Also consider tracking:

unique_expanded_nodes
separately if nodes can be reopened.

Do not pretend that this exactly matches the paper's definition unless the paper explicitly defines it.

11. Corner/turn metric
    Implement a reusable metric for the number of path direction changes.

For every three consecutive path points:

p1 -> p2 -> p3
calculate the change in direction.

Count a corner if the direction-change angle is:

> = 45 degrees
> The paper's exact angle calculation is not sufficiently detailed, so document the interpretation used.

Do not yet modify the path based on this metric.

12. Synthetic map generation
    Create deterministic map generators for the three environment categories described in the paper.

30 × 30
Represent an irregular outdoor-style environment.

Use irregular obstacle clusters/rectangles.

60 × 60
Represent a structured indoor/maze-like environment.

Use walls, corridors, or structured obstacle blocks.

100 × 100
Represent a large structured environment similar to dense warehouse/PV-array layouts.

Use repeated obstacle structures/blocks.

The exact obstacle placement from the paper is unavailable.

Therefore the generated maps are experimental approximations, not reproductions of the original maps.

13. Deterministic seeds
    Every generated map must be reproducible.

Use:

numpy.random.default_rng(seed)
Do not use uncontrolled global randomness.

For example:

30x30 -> seed 3030
60x60 -> seed 6060
100x100 -> seed 100100
You may choose better seed values, but make them explicit and deterministic.

14. Guarantee valid experiments
    The map generator must ensure:

start is inside the grid
goal is inside the grid
start is free
goal is free
a valid path exists
If a generated map does not satisfy these conditions, regenerate it deterministically using the next seed/attempt.

Do not manually modify maps after generation in a way that breaks reproducibility.

15. Paper scenarios
    Create configuration objects for these scenarios.

30x30
(2,2) -> (28,28)
(4,24) -> (29,2)

60x60
(2,2) -> (58,58)
(4,54) -> (59,2)

100x100
(2,2) -> (99,99)
Keep the coordinates in the configuration in paper-style 1-based coordinates.

Convert them to Python coordinates at the appropriate boundary.

16. Visualization
    Create a reusable Matplotlib visualization function.

It should display:

obstacles
free cells
start
goal
planned path
Do not hard-code a specific visual style unnecessarily.

Save figures to:

results/figures/
Use filenames containing:

map size
environment style
seed
start/goal identifier
Example:

astar_30x30_irregular_seed3030_case1.png
The visualization must not affect measured runtime.

17. Experiment runner
    Create:

run_baseline.py
Running:

python run_baseline.py

should:

generate the deterministic maps
save the generated maps
run conventional A\*
calculate:
runtime
path length
expanded nodes
number of corners
save figures
print a clean experiment table
save results to CSV
Example result columns:

map_size
environment
seed
case
start
goal
success
runtime_seconds
path_length
expanded_nodes
corners_ge_45 18. Save generated maps
Save the exact maps used for experiments.

For example:

results/maps/30x30_irregular_seed3030.npz
results/maps/60x60_maze_seed6060.npz
results/maps/100x100_array_seed100100.npz
This is important for reproducibility.

A future run should be able to load the exact same map rather than regenerate it.

19. Unit tests
    Create tests for at least:

Test 1 — Empty grid
A\* should find a path.

Test 2 — Completely blocked goal
A\* should correctly return failure.

Test 3 — Diagonal movement
Verify diagonal movement has cost:

sqrt(2)
Test 4 — Obstacle avoidance
Verify the path does not pass through obstacles.

Test 5 — Path reconstruction
Verify the first node is start and final node is goal.

Test 6 — Path length
Verify a known simple path has the expected length.

Run:

python -m unittest discover -s tests -v
and make sure all tests pass.

20. Documentation
    Create a README explaining:

Project
This is a research-paper reimplementation of:

“An Adaptive A\* Algorithm for Mobile Robots Global Path Planning”

Current phase
Phase 1 implements:

Grid environment
Synthetic deterministic maps
8-neighbor movement
Conventional A\*
Euclidean heuristic
Path reconstruction
Path length
Expanded nodes
Corner metric
Runtime measurement
Visualization
Experiment runner
Explicitly state:

Adaptive A\* is intentionally NOT implemented in this phase.

21. Assumptions documentation
    Create:

docs/assumptions.md
Document every paper ambiguity.

At minimum:

8-neighbor connectivity
movement costs
diagonal corner-cutting rule
Euclidean baseline heuristic
coordinate conversion
node-expansion definition
corner-angle definition
synthetic map generation
deterministic seeds
inability to reproduce the original obstacle matrices exactly
Use language such as:

The paper does not explicitly specify X. Therefore, this implementation assumes Y.

Do NOT present assumptions as facts from the paper.

22. Requirements
    Keep dependencies minimal.

Prefer:

numpy
matplotlib
Do not add large libraries unless necessary.

The A\* algorithm itself must be implemented manually.

23. Code quality requirements
    Follow these rules:

Python type hints
dataclasses where useful
meaningful function names
small reusable functions
no duplicated algorithmic logic
no global mutable state
clear docstrings
comments only where they explain non-obvious research decisions
deterministic behavior
no unnecessary abstraction
no notebook-only implementation
no hard-coded absolute paths
The project should run on Windows, Linux, and macOS.

Use pathlib.Path for filesystem paths.

24. Important research integrity rule
    Do not fabricate published results.

Do not put the paper's reported numbers into the experimental output and label them as our results.

Our Phase 1 results are independently generated results.

Later, we will create a separate comparison table:

Metric | Published Paper | Our Implementation | Difference
Only verified values from the paper should appear in the published-results column.

25. Do NOT implement yet
    Do NOT implement any of these in Phase 1:

adaptive weight
optimized distance heuristic
redundant point deletion
path smoothing
final Adaptive A\*
paper comparison
ablation study
Those belong to later phases.

However, design the code so that the future Adaptive A* implementation can reuse the existing A* framework.

For example, the search algorithm should make it reasonably easy to replace:

f = g + h

with a future:

f = g + omega \* h
without rewriting the entire project.

26. Final verification
    After implementation:

Run the unit tests.
Run the baseline experiment.
Verify all scenarios have valid paths.
Verify CSV results are generated.
Verify figures are generated.
Verify maps are saved.
Check for Python errors/warnings.
Check imports from a clean environment.
Do not leave debugging code or temporary files.
Give me a concise summary of:
files created
commands executed
tests passed
experiment results
assumptions made
anything that remains uncertain
Most importantly:

Do the implementation, do not merely describe how to implement it.

⋮⋮⋮⋮⋮⋮⋮⋮⋮⋮⋮⋮
