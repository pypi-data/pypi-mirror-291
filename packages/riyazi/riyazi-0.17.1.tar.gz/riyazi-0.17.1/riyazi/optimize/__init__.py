"""
## The solver-specific methods are:

**scipy.optimize.minimize**

- Nelder-Mead

- Powell

- CG

- BFGS

- Newton-CG

- L-BFGS-B

- TNC

- COBYLA

- SLSQP

- dogleg

- trust-ncg

**scipy.optimize.root**

- hybr

- lm

- broyden1

- broyden2

- anderson

- linearmixing

- diagbroyden

- excitingmixing

- krylov

- df-sane

**scipy.optimize.minimize_scalar**

- brent

- golden

- bounded

**scipy.optimize.root_scalar**

- bisect

- brentq

- brenth

- ridder

- toms748

- newton

- secant

- halley

- scipy.optimize.linprog

- simplex

- interior-point

- revised simplex

- highs

- highs-ds

- highs-ipm

**scipy.optimize.quadratic_assignment**

- faq

- 2opt
=====================================================
Optimization and root finding (:mod:`scipy.optimize`)
=====================================================

.. currentmodule:: scipy.optimize

SciPy ``optimize`` provides functions for minimizing (or maximizing)
objective functions, possibly subject to constraints. It includes
solvers for nonlinear problems (with support for both local and global
optimization algorithms), linear programing, constrained
and nonlinear least-squares, root finding, and curve fitting.

Common functions and objects, shared across different solvers, are:

.. autosummary::
   :toctree: generated/

   show_options - Show specific options optimization solvers.
   OptimizeResult - The optimization result returned by some optimizers.
   OptimizeWarning - The optimization encountered problems.


Optimization
============

Scalar functions optimization
-----------------------------

.. autosummary::
   :toctree: generated/

   minimize_scalar - Interface for minimizers of univariate functions

The `minimize_scalar` function supports the following methods:

.. toctree::

   optimize.minimize_scalar-brent
   optimize.minimize_scalar-bounded
   optimize.minimize_scalar-golden

Local (multivariate) optimization
---------------------------------

.. autosummary::
   :toctree: generated/

   minimize - Interface for minimizers of multivariate functions.

The `minimize` function supports the following methods:

.. toctree::

   optimize.minimize-neldermead
   optimize.minimize-powell
   optimize.minimize-cg
   optimize.minimize-bfgs
   optimize.minimize-newtoncg
   optimize.minimize-lbfgsb
   optimize.minimize-tnc
   optimize.minimize-cobyla
   optimize.minimize-slsqp
   optimize.minimize-trustconstr
   optimize.minimize-dogleg
   optimize.minimize-trustncg
   optimize.minimize-trustkrylov
   optimize.minimize-trustexact

Constraints are passed to `minimize` function as a single object or
as a list of objects from the following classes:

.. autosummary::
   :toctree: generated/

   NonlinearConstraint - Class defining general nonlinear constraints.
   LinearConstraint - Class defining general linear constraints.

Simple bound constraints are handled separately and there is a special class
for them:

.. autosummary::
   :toctree: generated/

   Bounds - Bound constraints.

Quasi-Newton strategies implementing `HessianUpdateStrategy`
interface can be used to approximate the Hessian in `minimize`
function (available only for the 'trust-constr' method). Available
quasi-Newton methods implementing this interface are:

.. autosummary::
   :toctree: generated/

   BFGS - Broyden-Fletcher-Goldfarb-Shanno (BFGS) Hessian update strategy.
   SR1 - Symmetric-rank-1 Hessian update strategy.

Global optimization
-------------------

.. autosummary::
   :toctree: generated/

   basinhopping - Basinhopping stochastic optimizer.
   brute - Brute force searching optimizer.
   differential_evolution - Stochastic optimizer using differential evolution.

   shgo - Simplicial homology global optimizer.
   dual_annealing - Dual annealing stochastic optimizer.
   direct - DIRECT (Dividing Rectangles) optimizer.

Least-squares and curve fitting
===============================

Nonlinear least-squares
-----------------------

.. autosummary::
   :toctree: generated/

   least_squares - Solve a nonlinear least-squares problem with bounds on the variables.

Linear least-squares
--------------------

.. autosummary::
   :toctree: generated/

   nnls - Linear least-squares problem with non-negativity constraint.
   lsq_linear - Linear least-squares problem with bound constraints.

Curve fitting
-------------

.. autosummary::
   :toctree: generated/

   curve_fit -- Fit curve to a set of points.

Root finding
============

Scalar functions
----------------
.. autosummary::
   :toctree: generated/

   root_scalar - Unified interface for nonlinear solvers of scalar functions.
   brentq - quadratic interpolation Brent method.
   brenth - Brent method, modified by Harris with hyperbolic extrapolation.
   ridder - Ridder's method.
   bisect - Bisection method.
   newton - Newton's method (also Secant and Halley's methods).
   toms748 - Alefeld, Potra & Shi Algorithm 748.
   RootResults - The root finding result returned by some root finders.

The `root_scalar` function supports the following methods:

.. toctree::

   optimize.root_scalar-brentq
   optimize.root_scalar-brenth
   optimize.root_scalar-bisect
   optimize.root_scalar-ridder
   optimize.root_scalar-newton
   optimize.root_scalar-toms748
   optimize.root_scalar-secant
   optimize.root_scalar-halley



The table below lists situations and appropriate methods, along with
*asymptotic* convergence rates per iteration (and per function evaluation)
for successful convergence to a simple root(*).
Bisection is the slowest of them all, adding one bit of accuracy for each
function evaluation, but is guaranteed to converge.
The other bracketing methods all (eventually) increase the number of accurate
bits by about 50% for every function evaluation.
The derivative-based methods, all built on `newton`, can converge quite quickly
if the initial value is close to the root.  They can also be applied to
functions defined on (a subset of) the complex plane.

+-------------+----------+----------+-----------+-------------+-------------+----------------+
| Domain of f | Bracket? |    Derivatives?      | Solvers     |        Convergence           |
+             +          +----------+-----------+             +-------------+----------------+
|             |          | `fprime` | `fprime2` |             | Guaranteed? |  Rate(s)(*)    |
+=============+==========+==========+===========+=============+=============+================+
| `R`         | Yes      | N/A      | N/A       | - bisection | - Yes       | - 1 "Linear"   |
|             |          |          |           | - brentq    | - Yes       | - >=1, <= 1.62 |
|             |          |          |           | - brenth    | - Yes       | - >=1, <= 1.62 |
|             |          |          |           | - ridder    | - Yes       | - 2.0 (1.41)   |
|             |          |          |           | - toms748   | - Yes       | - 2.7 (1.65)   |
+-------------+----------+----------+-----------+-------------+-------------+----------------+
| `R` or `C`  | No       | No       | No        | secant      | No          | 1.62 (1.62)    |
+-------------+----------+----------+-----------+-------------+-------------+----------------+
| `R` or `C`  | No       | Yes      | No        | newton      | No          | 2.00 (1.41)    |
+-------------+----------+----------+-----------+-------------+-------------+----------------+
| `R` or `C`  | No       | Yes      | Yes       | halley      | No          | 3.00 (1.44)    |
+-------------+----------+----------+-----------+-------------+-------------+----------------+

.. seealso::

   `scipy.optimize.cython_optimize` -- Typed Cython versions of zeros functions

Fixed point finding:

.. autosummary::
   :toctree: generated/

   fixed_point - Single-variable fixed-point solver.

Multidimensional
----------------

.. autosummary::
   :toctree: generated/

   root - Unified interface for nonlinear solvers of multivariate functions.

The `root` function supports the following methods:

.. toctree::

   optimize.root-hybr
   optimize.root-lm
   optimize.root-broyden1
   optimize.root-broyden2
   optimize.root-anderson
   optimize.root-linearmixing
   optimize.root-diagbroyden
   optimize.root-excitingmixing
   optimize.root-krylov
   optimize.root-dfsane

Linear programming / MILP
=========================

.. autosummary::
   :toctree: generated/

   milp -- Mixed integer linear programming.
   linprog -- Unified interface for minimizers of linear programming problems.

The `linprog` function supports the following methods:

.. toctree::

   optimize.linprog-simplex
   optimize.linprog-interior-point
   optimize.linprog-revised_simplex
   optimize.linprog-highs-ipm
   optimize.linprog-highs-ds
   optimize.linprog-highs

The simplex, interior-point, and revised simplex methods support callback
functions, such as:

.. autosummary::
   :toctree: generated/

   linprog_verbose_callback -- Sample callback function for linprog (simplex).

Assignment problems
===================

.. autosummary::
   :toctree: generated/

   linear_sum_assignment -- Solves the linear-sum assignment problem.
   quadratic_assignment -- Solves the quadratic assignment problem.

The `quadratic_assignment` function supports the following methods:

.. toctree::

   optimize.qap-faq
   optimize.qap-2opt

Utilities
=========

Finite-difference approximation
-------------------------------

.. autosummary::
   :toctree: generated/

   approx_fprime - Approximate the gradient of a scalar function.
   check_grad - Check the supplied derivative using finite differences.


Line search
-----------

.. autosummary::
   :toctree: generated/

   bracket - Bracket a minimum, given two starting points.
   line_search - Return a step that satisfies the strong Wolfe conditions.

Hessian approximation
---------------------

.. autosummary::
   :toctree: generated/

   LbfgsInvHessProduct - Linear operator for L-BFGS approximate inverse Hessian.
   HessianUpdateStrategy - Interface for implementing Hessian update strategies

Benchmark problems
------------------

.. autosummary::
   :toctree: generated/

   rosen - The Rosenbrock function.
   rosen_der - The derivative of the Rosenbrock function.
   rosen_hess - The Hessian matrix of the Rosenbrock function.
   rosen_hess_prod - Product of the Rosenbrock Hessian with a vector.

Legacy functions
================

The functions below are not recommended for use in new scripts;
all of these methods are accessible via a newer, more consistent
interfaces, provided by the interfaces above.

Optimization
------------

General-purpose multivariate methods:

.. autosummary::
   :toctree: generated/

   fmin - Nelder-Mead Simplex algorithm.
   fmin_powell - Powell's (modified) level set method.
   fmin_cg - Non-linear (Polak-Ribiere) conjugate gradient algorithm.
   fmin_bfgs - Quasi-Newton method (Broydon-Fletcher-Goldfarb-Shanno).
   fmin_ncg - Line-search Newton Conjugate Gradient.

Constrained multivariate methods:

.. autosummary::
   :toctree: generated/

   fmin_l_bfgs_b - Zhu, Byrd, and Nocedal's constrained optimizer.
   fmin_tnc - Truncated Newton code.
   fmin_cobyla - Constrained optimization by linear approximation.
   fmin_slsqp - Minimization using sequential least-squares programming.

Univariate (scalar) minimization methods:

.. autosummary::
   :toctree: generated/

   fminbound - Bounded minimization of a scalar function.
   brent - 1-D function minimization using Brent method.
   golden - 1-D function minimization using Golden Section method.

Least-squares
-------------

.. autosummary::
   :toctree: generated/

   leastsq - Minimize the sum of squares of M equations in N unknowns.

Root finding
------------

General nonlinear solvers:

.. autosummary::
   :toctree: generated/

   fsolve - Non-linear multivariable equation solver.
   broyden1 - Broyden's first method.
   broyden2 - Broyden's second method.

Large-scale nonlinear solvers:

.. autosummary::
   :toctree: generated/

   newton_krylov
   anderson

Simple iteration solvers:

.. autosummary::
   :toctree: generated/

   excitingmixing
   linearmixing
   diagbroyden


https://en.wikipedia.org/wiki/Root-finding_algorithms
https://en.wikipedia.org/wiki/List_of_algorithms#Root_finding
https://en.wikipedia.org/wiki/List_of_data_structures
https://en.wikipedia.org/wiki/Outline_of_machine_learning#Machine_learning_algorithms
https://en.wikipedia.org/wiki/Pathfinding#Algorithms_used_in_pathfinding
https://en.wikipedia.org/wiki/List_of_algorithm_general_topics
https://en.wikipedia.org/wiki/List_of_terms_relating_to_algorithms_and_data_structures
https://en.wikipedia.org/wiki/Heuristic

https://en.wikipedia.org/wiki/Quine%E2%80%93McCluskey_algorithm
https://towardsdatascience.com/root-finding-methods-from-scratch-in-python-84040c81a8ba

https://www.geeksforgeeks.org/python-program-to-find-square-root-of-given-number/

# Optimization
### Scalar functions optimization
### Local (multivariate) optimization

# Global optimization

# Least-squares and curve fitting

### Nonlinear least-squares
### Linear least-squares
### Curve fitting


# Root finding

### Scalar functions

# Multidimensional


# Linear programming / MILP


# Assignment problems


# Utilities

### Finite-difference approximation
### Line search
### Hessian approximation
### Benchmark problems
# Legacy functions
## Optimization
### Least-squares
### Root finding


"""

from . import bisection
