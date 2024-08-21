""" 
=============================================
Integration and ODEs (:mod:`scipy.integrate`)
=============================================

.. currentmodule:: scipy.integrate

Integrating functions, given function object
============================================

.. autosummary::
   :toctree: generated/

   quad          -- General purpose integration
   quad_vec      -- General purpose integration of vector-valued functions
   dblquad       -- General purpose double integration
   tplquad       -- General purpose triple integration
   nquad         -- General purpose N-D integration
   fixed_quad    -- Integrate func(x) using Gaussian quadrature of order n
   quadrature    -- Integrate with given tolerance using Gaussian quadrature
   romberg       -- Integrate func using Romberg integration
   newton_cotes  -- Weights and error coefficient for Newton-Cotes integration
   IntegrationWarning -- Warning on issues during integration
   AccuracyWarning  -- Warning on issues during quadrature integration

Integrating functions, given fixed samples
==========================================

.. autosummary::
   :toctree: generated/

   trapezoid            -- Use trapezoidal rule to compute integral.
   cumulative_trapezoid -- Use trapezoidal rule to cumulatively compute integral.
   simpson              -- Use Simpson's rule to compute integral from samples.
   romb                 -- Use Romberg Integration to compute integral from
                        -- (2**k + 1) evenly-spaced samples.

.. seealso::

   :mod:`scipy.special` for orthogonal polynomials (special) for Gaussian
   quadrature roots and weights for other weighting factors and regions.

Solving initial value problems for ODE systems
==============================================

The solvers are implemented as individual classes, which can be used directly
(low-level usage) or through a convenience function.

.. autosummary::
   :toctree: generated/

   solve_ivp     -- Convenient function for ODE integration.
   RK23          -- Explicit Runge-Kutta solver of order 3(2).
   RK45          -- Explicit Runge-Kutta solver of order 5(4).
   DOP853        -- Explicit Runge-Kutta solver of order 8.
   Radau         -- Implicit Runge-Kutta solver of order 5.
   BDF           -- Implicit multi-step variable order (1 to 5) solver.
   LSODA         -- LSODA solver from ODEPACK Fortran package.
   OdeSolver     -- Base class for ODE solvers.
   DenseOutput   -- Local interpolant for computing a dense output.
   OdeSolution   -- Class which represents a continuous ODE solution.


Old API
-------

These are the routines developed earlier for SciPy. They wrap older solvers
implemented in Fortran (mostly ODEPACK). While the interface to them is not
particularly convenient and certain features are missing compared to the new
API, the solvers themselves are of good quality and work fast as compiled
Fortran code. In some cases, it might be worth using this old API.

.. autosummary::
   :toctree: generated/

   odeint        -- General integration of ordinary differential equations.
   ode           -- Integrate ODE using VODE and ZVODE routines.
   complex_ode   -- Convert a complex-valued ODE to real-valued and integrate.


Solving boundary value problems for ODE systems
===============================================

.. autosummary::
   :toctree: generated/

   solve_bvp     -- Solve a boundary value problem for a system of ODEs.
 # noqa: E501


## how to solve integration using simpsons rule in python?

**Numerical integration is the approximate computation f an integral using numerical techniques Methods for integrating function given function object.**

`quad` General purpose Integration

`dblquad` General purpose double Integration 

`nquad` General Purpose Fold Integration 

`fixed_quad` Gaussian quadrature, order n 

`quadrature` Gaussian quadrature to tolerance

`romberg` Romberg Integration 

`trapz` Trapezoidal rule 

`cumtrapz` Trapezoidal rule to cumulatively compute integrate 

`simps` Simpson's ruel 

`romb` Romberg Integration 

`polyint` Analytical polynomail Integration (Numpy)


"""