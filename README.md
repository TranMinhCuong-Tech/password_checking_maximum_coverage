<div align="center">

```bash
                    ██████╗  █████╗ ███████╗███████╗██╗    ██╗ ██████╗ ██████╗ ██████╗ 
                    ██╔══██╗██╔══██╗██╔════╝██╔════╝██║    ██║██╔═══██╗██╔══██╗██╔══██╗
                    ██████╔╝███████║███████╗███████╗██║ █╗ ██║██║   ██║██████╔╝██║  ██║
                    ██╔═══╝ ██╔══██║╚════██║╚════██║██║███╗██║██║   ██║██╔══██╗██║  ██║
                    ██║     ██║  ██║███████║███████║╚███╔███╔╝╚██████╔╝██║  ██║██████╔╝
                    ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝ ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝ 
                                                                                        
                     ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗██╗███╗   ██╗ ██████╗      
                    ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██║████╗  ██║██╔════╝      
                    ██║     ███████║█████╗  ██║     █████╔╝ ██║██╔██╗ ██║██║  ███╗     
                    ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██║██║╚██╗██║██║   ██║     
                    ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗██║██║ ╚████║╚██████╔╝     
                     ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝       
```

</div>
# Password Checking Maximum Coverage

## Table of Contents

- [Overview](#overview)
- [Wiki & Theory](#wiki--theory)
- [Project Goal](#project-goal)
- [NP Problem Used in This Project](#np-problem-used-in-this-project)
- [What Maximum Coverage Means](#what-maximum-coverage-means)
- [How the Project Works](#how-the-project-works)
- [Algorithms](#algorithms)
- [Folder Structure](#folder-structure)
- [How to Run](#how-to-run)
- [Output Format](#output-format)
- [Notes on Rules](#notes-on-rules)

## Overview

`password_checking_maximum_coverage` is an academic project for studying **algorithmic complexity** through a classic NP-Hard optimization problem: **Maximum Coverage**.

The goal is not just to check passwords. Instead, the project is designed to:

- model a real problem as a combinatorial optimization problem
- compare greedy, randomized search, hill climbing, local search, beam search, dynamic programming, 0-1 integer linear programming, and Lagrangian relaxation approaches
- show the difference between exact and approximate solutions
- demonstrate why NP-Hard problems become expensive as the input size grows

## Wiki & Theory

The full theoretical explanation and detailed project description are stored in:

- [wiki.md](wiki.md)

That file includes:

- NP and NP-Hard theory
- Maximum Coverage theory
- detailed analysis of every algorithm in `algorithms/`
- a file-by-file explanation of the project
- a detailed explanation of how Maximum Coverage is implemented here

## Project Goal

The main idea of the project is:

- take a real password list in `real_passwords.txt`
- take a mutated password list in `mutated_passwords.txt`
- treat each `rule` as a string transformation
- if the transformed result matches a password in the real password set, that password is considered covered
- choose exactly `k` rules so that the number of covered real passwords is maximized

This helps illustrate:

- how a practical problem can be mapped to an NP-Hard model
- how sets can be represented directly with `set` and `frozenset`
- how exact and approximate methods trade accuracy for speed

## NP Problem Used in This Project

The NP-Hard problem used in this project is **Maximum Coverage**.

In short:

- there is a universe set `U`
- there are many subsets `S1, S2, ..., Sm`
- you may choose at most `k` subsets
- the objective is to maximize the size of the union of the chosen subsets

Formula:

```text
maximize |S1 ∪ S2 ∪ ... ∪ Sk|
subject to choose at most k sets
```

In this project:

- `U` is the set of real passwords
- each `rule` defines a subset of real passwords that can be matched through mutation
- the solver must choose `k` rules that cover the largest number of real passwords

## What Maximum Coverage Means

Imagine:

- you have 100 users
- each marketing campaign reaches a different group of users
- you can only run 3 campaigns
- you want those 3 campaigns to reach as many users as possible

That is Maximum Coverage.

The important part is:

- subsets may overlap
- picking two very similar subsets may waste one of your `k` choices
- the goal is to balance coverage and overlap

## How the Project Works

The workflow is:

1. Load all real passwords from `real_passwords.txt`
2. Load all mutated passwords from `mutated_passwords.txt`
3. The user chooses the number of rules `k`
4. The user selects an algorithm
5. The program applies each rule as a transformation
6. If a transformed result matches a password in the mutated set, the corresponding real password is counted as covered
7. The selected algorithm chooses the best `k` rules according to its strategy
8. The result is printed and saved to an output file

Implementation-wise:

- `rules.py` stores the rule catalog and the rules menu
- `coverage_problem.py` contains the core Maximum Coverage logic
- `pwd_checking.py` provides the algorithm selection menu
- `__init__.py` is the main entry point

## Algorithms

The project includes 8 solving strategies, grouped by implementation and understanding difficulty.

### Easy

#### 1. Greedy

At each step, choose the rule that covers the largest number of newly covered passwords.

- fast and easy to explain
- does not always guarantee the optimal answer
- a common approximation strategy for Maximum Coverage

#### 2. Randomized Search

Randomly sample many feasible `k`-rule subsets and keep the best one.

- simple heuristic
- easy to implement
- useful as a baseline for stochastic exploration

#### 3. Hill Climbing

Start from a good initial solution and repeatedly apply the best improving swap.

- local improvement strategy
- easy to understand
- can get stuck in local optima

#### 4. Local Search

Start from a random feasible solution and improve it using first-improvement swaps.

- simple neighborhood search
- good for demonstrating iterative improvement
- usually slower than greedy but still practical for small inputs

### Medium

#### 5. Beam Search

Expand multiple partial solutions at once and keep only the best `beam_width` candidates at each depth.

- more flexible than greedy
- easier than full exhaustive search
- trades accuracy for a controlled search width

#### 6. Dynamic Programming

Use recursion with memoization to avoid recomputing repeated states.

- exact solution
- practical only for small instances because the state space grows quickly
- a good example of state optimization

### Hard

#### 7. ILP + PuLP + CBC

Formulate the problem as a 0-1 integer linear programming model and solve it with PuLP + CBC.

- exact
- uses binary decision variables and linear coverage constraints
- demonstrates how an optimization solver can handle Maximum Coverage directly

#### 8. Lagrangian Relaxation

Relax the cardinality constraint and tune a penalty multiplier iteratively.

- advanced optimization idea
- useful for explaining penalty-based approximation
- practical heuristic for this project

## Folder Structure

```text
.
├── __init__.py
├── README.md
├── wiki.md
├── banner.png
├── coverage_problem.py
├── pwd_checking.py
├── rules.py
├── real_passwords.txt
├── mutated_passwords.txt
├── real_passwords_500_NCSC_breach_derived.txt
├── mutated_passwords_1500.txt
├── output_*.txt
└── algorithms
    ├── Beam_Search.py
    ├── Dynamic_Programming.py
    ├── Greedy.py
    ├── Hill_Climbing.py
    ├── ILP_PuLP_CBC.py
    ├── Lagrangian_Relaxation.py
    ├── Local_Search.py
    ├── Randomized_Search.py
    └── __init__.py
```

## How to Run

The main file is `__init__.py`.

## Environment Setup

The project uses a virtual environment so that dependencies stay isolated from your global Python installation.

### 1. Create a virtual environment

#### Windows

```bash
py -m venv .venv
```
or 

```bash
python -m venv .venv
```

#### Linux / macOS

```bash
python3 -m venv .venv
```
or

```bash
py -m venv .venv
```

### 2. Activate the virtual environment

#### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks the script, run this once in the same terminal:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Windows Command Prompt

```bat
.venv\Scripts\activate.bat
```

#### Linux / macOS

```bash
source .venv/bin/activate
```

### 3. Install dependencies

Install all required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

#### Windows

```bash
py -m pip install -r requirements.txt
```

If your system uses `python3`, you can also run:

```bash
python3 -m pip install -r requirements.txt
```

### 4. Run the project

Run it with:

```bash
py __init__.py
```

If your system requires `python3`, use:

```bash
python3 __init__.py
```

On Windows, you can use `py __init__.py` or `py -3 __init__.py` depending on how Python is installed.

Program flow:

1. The banner and short description are displayed
2. The rules catalog is shown
3. You enter the number of rules `k`
4. You choose an algorithm from the menu
5. The program runs and prints the result

### Menu Keys

#### Rules Menu

- `0` or `e`: exit the program
- `1` to `20`: choose the number of rules

#### Algorithm Menu

- `1`: Greedy
- `2`: Randomized Search
- `3`: Hill Climbing
- `4`: Local Search
- `5`: Beam Search
- `6`: Dynamic Programming
- `7`: ILP + PuLP + CBC
- `8`: Lagrangian Relaxation
- `0`: return to the previous menu
- `-1` or `e`: exit the program

## Output Format

Each solver writes its result to a separate output file, for example:

- `output_greedy_k3.txt`
- `output_randomized_k4.txt`
- `output_hill_k4.txt`
- `output_local_k4.txt`
- `output_beam_k4.txt`
- `output_dp_k7.txt`
- `output_ILP_PuLP_CBC_k10.txt`
- `output_lagrangian_k10.txt`

The output usually includes:

- the selected rules
- the covered real passwords
- the coverage ratio

## Notes on Rules

In the current version, `rules.py` is not a simple boolean checker anymore.

Instead:

- each rule is a string transformation
- the rule is applied to passwords
- the transformed result is matched against the password dataset

This design matches the Maximum Coverage idea:

- start from a large input set
- generate candidate subsets through transformations
- choose the best `k` sets according to the coverage objective

If you want, I can also:

1. translate `wiki.md` into English
2. make the README shorter and more polished for GitHub
3. add a "Quick Start" section with example runs
