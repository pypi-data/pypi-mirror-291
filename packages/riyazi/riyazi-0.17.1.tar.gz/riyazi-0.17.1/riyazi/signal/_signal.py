"""
https://online.stanford.edu/courses/ee264-digital-signal-processing

https://onlinecourses.iitk.ac.in/course/ee301a

https://ee.iisc.ac.in/m-tech-programme-signal-processing/

https://www.amrita.edu/course/multirate-signal-processing-software-defined-radio

https://inst.eecs.berkeley.edu/~ee123/fa13/

https://medium.com/analytics-vidhya/signal-data-processing-for-scientific-data-analysis-with-python-part-1-90a90cb7f81

https://ne-np.facebook.com/puwebinar/videos/signal-processing-using-pythongoogle-colab/429864812245235/

https://pll.harvard.edu/subject/computer-science

https://www.geeksforgeeks.org/signal-processing-and-time-series-data-analysis/?ref=gcse

https://github.com/daniliambo/DigitalSignalProcessing





https://www.gaussianwaves.com/2014/02/polynomials-convolution-and-toeplitz-matrices-connecting-the-dots/

https://towardsdatascience.com/hands-on-signal-processing-with-python-9bda8aad39de

https://klyshko.github.io/teaching/2019-02-22-teaching

https://staff.fnwi.uva.nl/r.vandenboomgaard/SP20162017/SystemsSignals/plottingsignals.html

https://www.it-jim.com/blog/audio-processing-basics-in-python/

https://www.gw-openscience.org/s/events/GW151226/LOSC_Event_tutorial_GW151226.html

https://www.upwork.com/services/product/development-it-matlab-and-python-based-digital-signal-processing-projects-1421409691842625536

https://bastibe.de/2012-11-02-real-time-signal-processing-in-python.html

https://levelup.gitconnected.com/how-to-code-a-biosignal-control-system-from-scratch-in-40-hours-54290c1eb0c7

https://www.kuniga.me/blog/2021/05/13/lpc-in-python.html

https://opensource.com/article/19/9/audio-processing-machine-learning-python

https://medium.com/@ramitag18/performing-convolution-on-a-matrix-4682fd364591

https://www.ibm.com/cloud/learn/convolutional-neural-networks

https://www.superdatascience.com/blogs/convolutional-neural-networks-cnn-step-1-convolution-operation/

https://en.wikipedia.org/wiki/Convolution

https://en.wikipedia.org/wiki/Convolution




http://www.dspguide.com/ch6/2.htm

https://www.geeksforgeeks.org/linear-convolution-using-c-and-matlab/

https://www.theengineeringprojects.com/2022/09/properties-of-convolution-in-signals-and-systems-with-matlab.html

https://towardsdatascience.com/hands-on-signal-processing-with-python-9bda8aad39de

https://towardsdatascience.com/a-comprehensive-introduction-to-different-types-of-convolutions-in-deep-learning-669281e58215

https://eng.libretexts.org/Bookshelves/Electrical_Engineering/Signal_Processing_and_Modeling/Signals_and_Systems_(Baraniuk_et_al.)/04%3A_Time_Domain_Analysis_of_Discrete_Time_Systems/4.03%3A_Discrete_Time_Convolution

https://thewolfsound.com/convolution-vs-correlation-in-signal-processing-and-deep-learning/

https://asp-eurasipjournals.springeropen.com/articles/10.1186/s13634-021-00821-8

https://www.geocities.ws/senthilirtt/Python%20Workshop%20for%20Digital%20Signal%20Processing

https://open.umn.edu/opentextbooks/textbooks/290

https://www.udemy.com/course/fourier-transform-mxc/?matchtype=e&msclkid=050bfb5c99411857ac1498fcf946a0cd&utm_campaign=BG-LongTail_la.EN_cc.INDIA&utm_content=deal4584&utm_medium=udemyads&utm_source=bing&utm_term=_._ag_1208363692114833_._ad__._kw_Signal+Processing+Course_._de_c_._dm__._pl__._ti_kwd-75523068883524%3Aloc-90_._li_161219_._pd__._

https://asp-eurasipjournals.springeropen.com/articles/10.1186/s13634-021-00821-8



=======================================
Signal processing (:mod:`scipy.signal`)
=======================================

Convolution
===========

.. autosummary::
   :toctree: generated/

   convolve           -- N-D convolution.
   correlate          -- N-D correlation.
   fftconvolve        -- N-D convolution using the FFT.
   oaconvolve         -- N-D convolution using the overlap-add method.
   convolve2d         -- 2-D convolution (more options).
   correlate2d        -- 2-D correlation (more options).
   sepfir2d           -- Convolve with a 2-D separable FIR filter.
   choose_conv_method -- Chooses faster of FFT and direct convolution methods.
   correlation_lags   -- Determines lag indices for 1D cross-correlation.

B-splines
=========

.. autosummary::
   :toctree: generated/

   bspline        -- B-spline basis function of order n.
   cubic          -- B-spline basis function of order 3.
   quadratic      -- B-spline basis function of order 2.
   gauss_spline   -- Gaussian approximation to the B-spline basis function.
   cspline1d      -- Coefficients for 1-D cubic (3rd order) B-spline.
   qspline1d      -- Coefficients for 1-D quadratic (2nd order) B-spline.
   cspline2d      -- Coefficients for 2-D cubic (3rd order) B-spline.
   qspline2d      -- Coefficients for 2-D quadratic (2nd order) B-spline.
   cspline1d_eval -- Evaluate a cubic spline at the given points.
   qspline1d_eval -- Evaluate a quadratic spline at the given points.
   spline_filter  -- Smoothing spline (cubic) filtering of a rank-2 array.

Filtering
=========

.. autosummary::
   :toctree: generated/

   order_filter  -- N-D order filter.
   medfilt       -- N-D median filter.
   medfilt2d     -- 2-D median filter (faster).
   wiener        -- N-D Wiener filter.

   symiirorder1  -- 2nd-order IIR filter (cascade of first-order systems).
   symiirorder2  -- 4th-order IIR filter (cascade of second-order systems).
   lfilter       -- 1-D FIR and IIR digital linear filtering.
   lfiltic       -- Construct initial conditions for `lfilter`.
   lfilter_zi    -- Compute an initial state zi for the lfilter function that
                 -- corresponds to the steady state of the step response.
   filtfilt      -- A forward-backward filter.
   savgol_filter -- Filter a signal using the Savitzky-Golay filter.

   deconvolve    -- 1-D deconvolution using lfilter.

   sosfilt       -- 1-D IIR digital linear filtering using
                 -- a second-order sections filter representation.
   sosfilt_zi    -- Compute an initial state zi for the sosfilt function that
                 -- corresponds to the steady state of the step response.
   sosfiltfilt   -- A forward-backward filter for second-order sections.
   hilbert       -- Compute 1-D analytic signal, using the Hilbert transform.
   hilbert2      -- Compute 2-D analytic signal, using the Hilbert transform.

   decimate      -- Downsample a signal.
   detrend       -- Remove linear and/or constant trends from data.
   resample      -- Resample using Fourier method.
   resample_poly -- Resample using polyphase filtering method.
   upfirdn       -- Upsample, apply FIR filter, downsample.

Filter design
=============

.. autosummary::
   :toctree: generated/

   bilinear      -- Digital filter from an analog filter using
                    -- the bilinear transform.
   bilinear_zpk  -- Digital filter from an analog filter using
                    -- the bilinear transform.
   findfreqs     -- Find array of frequencies for computing filter response.
   firls         -- FIR filter design using least-squares error minimization.
   firwin        -- Windowed FIR filter design, with frequency response
                    -- defined as pass and stop bands.
   firwin2       -- Windowed FIR filter design, with arbitrary frequency
                    -- response.
   freqs         -- Analog filter frequency response from TF coefficients.
   freqs_zpk     -- Analog filter frequency response from ZPK coefficients.
   freqz         -- Digital filter frequency response from TF coefficients.
   freqz_zpk     -- Digital filter frequency response from ZPK coefficients.
   sosfreqz      -- Digital filter frequency response for SOS format filter.
   gammatone     -- FIR and IIR gammatone filter design.
   group_delay   -- Digital filter group delay.
   iirdesign     -- IIR filter design given bands and gains.
   iirfilter     -- IIR filter design given order and critical frequencies.
   kaiser_atten  -- Compute the attenuation of a Kaiser FIR filter, given
                    -- the number of taps and the transition width at
                    -- discontinuities in the frequency response.
   kaiser_beta   -- Compute the Kaiser parameter beta, given the desired
                    -- FIR filter attenuation.
   kaiserord     -- Design a Kaiser window to limit ripple and width of
                    -- transition region.
   minimum_phase -- Convert a linear phase FIR filter to minimum phase.
   savgol_coeffs -- Compute the FIR filter coefficients for a Savitzky-Golay
                    -- filter.
   remez         -- Optimal FIR filter design.

   unique_roots  -- Unique roots and their multiplicities.
   residue       -- Partial fraction expansion of b(s) / a(s).
   residuez      -- Partial fraction expansion of b(z) / a(z).
   invres        -- Inverse partial fraction expansion for analog filter.
   invresz       -- Inverse partial fraction expansion for digital filter.
   BadCoefficients  -- Warning on badly conditioned filter coefficients.

Lower-level filter design functions:

.. autosummary::
   :toctree: generated/

   abcd_normalize -- Check state-space matrices and ensure they are rank-2.
   band_stop_obj  -- Band Stop Objective Function for order minimization.
   besselap       -- Return (z,p,k) for analog prototype of Bessel filter.
   buttap         -- Return (z,p,k) for analog prototype of Butterworth filter.
   cheb1ap        -- Return (z,p,k) for type I Chebyshev filter.
   cheb2ap        -- Return (z,p,k) for type II Chebyshev filter.
   cmplx_sort     -- Sort roots based on magnitude.
   ellipap        -- Return (z,p,k) for analog prototype of elliptic filter.
   lp2bp          -- Transform a lowpass filter prototype to a bandpass filter.
   lp2bp_zpk      -- Transform a lowpass filter prototype to a bandpass filter.
   lp2bs          -- Transform a lowpass filter prototype to a bandstop filter.
   lp2bs_zpk      -- Transform a lowpass filter prototype to a bandstop filter.
   lp2hp          -- Transform a lowpass filter prototype to a highpass filter.
   lp2hp_zpk      -- Transform a lowpass filter prototype to a highpass filter.
   lp2lp          -- Transform a lowpass filter prototype to a lowpass filter.
   lp2lp_zpk      -- Transform a lowpass filter prototype to a lowpass filter.
   normalize      -- Normalize polynomial representation of a transfer function.



Matlab-style IIR filter design
==============================

.. autosummary::
   :toctree: generated/

   butter -- Butterworth
   buttord
   cheby1 -- Chebyshev Type I
   cheb1ord
   cheby2 -- Chebyshev Type II
   cheb2ord
   ellip -- Elliptic (Cauer)
   ellipord
   bessel -- Bessel (no order selection available -- try butterod)
   iirnotch      -- Design second-order IIR notch digital filter.
   iirpeak       -- Design second-order IIR peak (resonant) digital filter.
   iircomb       -- Design IIR comb filter.

Continuous-time linear systems
==============================

.. autosummary::
   :toctree: generated/

   lti              -- Continuous-time linear time invariant system base class.
   StateSpace       -- Linear time invariant system in state space form.
   TransferFunction -- Linear time invariant system in transfer function form.
   ZerosPolesGain   -- Linear time invariant system in zeros, poles, gain form.
   lsim             -- Continuous-time simulation of output to linear system.
   lsim2            -- Like lsim, but `scipy.integrate.odeint` is used.
   impulse          -- Impulse response of linear, time-invariant (LTI) system.
   impulse2         -- Like impulse, but `scipy.integrate.odeint` is used.
   step             -- Step response of continuous-time LTI system.
   step2            -- Like step, but `scipy.integrate.odeint` is used.
   freqresp         -- Frequency response of a continuous-time LTI system.
   bode             -- Bode magnitude and phase data (continuous-time LTI).

Discrete-time linear systems
============================

.. autosummary::
   :toctree: generated/

   dlti             -- Discrete-time linear time invariant system base class.
   StateSpace       -- Linear time invariant system in state space form.
   TransferFunction -- Linear time invariant system in transfer function form.
   ZerosPolesGain   -- Linear time invariant system in zeros, poles, gain form.
   dlsim            -- Simulation of output to a discrete-time linear system.
   dimpulse         -- Impulse response of a discrete-time LTI system.
   dstep            -- Step response of a discrete-time LTI system.
   dfreqresp        -- Frequency response of a discrete-time LTI system.
   dbode            -- Bode magnitude and phase data (discrete-time LTI).

LTI representations
===================

.. autosummary::
   :toctree: generated/

   tf2zpk        -- Transfer function to zero-pole-gain.
   tf2sos        -- Transfer function to second-order sections.
   tf2ss         -- Transfer function to state-space.
   zpk2tf        -- Zero-pole-gain to transfer function.
   zpk2sos       -- Zero-pole-gain to second-order sections.
   zpk2ss        -- Zero-pole-gain to state-space.
   ss2tf         -- State-pace to transfer function.
   ss2zpk        -- State-space to pole-zero-gain.
   sos2zpk       -- Second-order sections to zero-pole-gain.
   sos2tf        -- Second-order sections to transfer function.
   cont2discrete -- Continuous-time to discrete-time LTI conversion.
   place_poles   -- Pole placement.

Waveforms
=========

.. autosummary::
   :toctree: generated/

   chirp        -- Frequency swept cosine signal, with several freq functions.
   gausspulse   -- Gaussian modulated sinusoid.
   max_len_seq  -- Maximum length sequence.
   sawtooth     -- Periodic sawtooth.
   square       -- Square wave.
   sweep_poly   -- Frequency swept cosine signal; freq is arbitrary polynomial.
   unit_impulse -- Discrete unit impulse.

Window functions
================

For window functions, see the `scipy.signal.windows` namespace.

In the `scipy.signal` namespace, there is a convenience function to
obtain these windows by name:

.. autosummary::
   :toctree: generated/

   get_window -- Return a window of a given length and type.

Wavelets
========

.. autosummary::
   :toctree: generated/

   cascade      -- Compute scaling function and wavelet from coefficients.
   daub         -- Return low-pass.
   morlet       -- Complex Morlet wavelet.
   qmf          -- Return quadrature mirror filter from low-pass.
   ricker       -- Return ricker wavelet.
   morlet2      -- Return Morlet wavelet, compatible with cwt.
   cwt          -- Perform continuous wavelet transform.

Peak finding
============

.. autosummary::
   :toctree: generated/

   argrelmin        -- Calculate the relative minima of data.
   argrelmax        -- Calculate the relative maxima of data.
   argrelextrema    -- Calculate the relative extrema of data.
   find_peaks       -- Find a subset of peaks inside a signal.
   find_peaks_cwt   -- Find peaks in a 1-D array with wavelet transformation.
   peak_prominences -- Calculate the prominence of each peak in a signal.
   peak_widths      -- Calculate the width of each peak in a signal.

Spectral analysis
=================

.. autosummary::
   :toctree: generated/

   periodogram    -- Compute a (modified) periodogram.
   welch          -- Compute a periodogram using Welch's method.
   csd            -- Compute the cross spectral density, using Welch's method.
   coherence      -- Compute the magnitude squared coherence, using Welch's method.
   spectrogram    -- Compute the spectrogram.
   lombscargle    -- Computes the Lomb-Scargle periodogram.
   vectorstrength -- Computes the vector strength.
   stft           -- Compute the Short Time Fourier Transform.
   istft          -- Compute the Inverse Short Time Fourier Transform.
   check_COLA     -- Check the COLA constraint for iSTFT reconstruction.
   check_NOLA     -- Check the NOLA constraint for iSTFT reconstruction.

Chirp Z-transform and Zoom FFT
============================================

.. autosummary::
   :toctree: generated/

   czt - Chirp z-transform convenience function
   zoom_fft - Zoom FFT convenience function
   CZT - Chirp z-transform function generator
   ZoomFFT - Zoom FFT function generator
   czt_points - Output the z-plane points sampled by a chirp z-transform

The functions are simpler to use than the classes, but are less efficient when
using the same transform on many arrays of the same length, since they
repeatedly generate the same chirp signal with every call.  In these cases,
use the classes to create a reusable function instead.


https://www.tutorialspoint.com/what-is-convolution-in-signals-and-systems
"""

import numpy as np 
import matplotlib.pyplot as plt 

__all__ = ['sine_wave','cosine_wave']

from numpy import (logical_and, asarray, pi, zeros_like,
                   piecewise, array, arctan2, tan, zeros, arange, floor)
from numpy.core.umath import (sqrt, exp, greater, less, cos, add, sin,
                              less_equal, greater_equal)

def sine_wave(frequency, amplitude, phase, sampling_rate, duration):
    """
    sine_wave(frequency=440, amplitude=1, phase=0, sampling_rate=44100, duration=1)
    
    """
    # Generate time values
    time = np.linspace(0, duration, int(sampling_rate * duration))
    # Generate sine wave values
    sine_wave = amplitude * np.sin(2 * np.pi * frequency * time + phase)
    # to plot the singal 
    plt.plot(sine_wave)
    plt.title("Sine Wave")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.show()



def cosine_wave(frequency, amplitude, phase, sampling_rate, duration):
    """
    cosine_wave(frequency=3, amplitude=1, phase=0, sampling_rate=44100, duration=1)
    """
    # Generate time values
    time = np.linspace(0, duration, int(sampling_rate * duration))
    # Generate cosine wave values
    cosine_wave = amplitude * np.cos(2 * np.pi * frequency * time + phase)
    # to plot the singal 
    plt.plot(cosine_wave)
    plt.title("Sine Wave")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.show()
    
    
    

def cubic(x):
    """A cubic B-spline.

    This is a special case of `bspline`, and equivalent to ``bspline(x, 3)``.

    Parameters
    ----------
    x : array_like
        a knot vector

    Returns
    -------
    res : ndarray
        Cubic B-spline basis function values

    See Also
    --------
    bspline : B-spline basis function of order n
    quadratic : A quadratic B-spline.

    Examples
    --------
    We can calculate B-Spline basis function of several orders:

    >>> from scipy.signal import bspline, cubic, quadratic
    >>> bspline(0.0, 1)
    1

    >>> knots = [-1.0, 0.0, -1.0]
    >>> bspline(knots, 2)
    array([0.125, 0.75, 0.125])

    >>> np.array_equal(bspline(knots, 2), quadratic(knots))
    True

    >>> np.array_equal(bspline(knots, 3), cubic(knots))
    True

    """
    ax = abs(asarray(x))
    res = zeros_like(ax)
    cond1 = less(ax, 1)
    if cond1.any():
        ax1 = ax[cond1]
        res[cond1] = 2.0 / 3 - 1.0 / 2 * ax1 ** 2 * (2 - ax1)
    cond2 = ~cond1 & less(ax, 2)
    if cond2.any():
        ax2 = ax[cond2]
        res[cond2] = 1.0 / 6 * (2 - ax2) ** 3
    return res



def quadratic(x):
    """A quadratic B-spline.

    This is a special case of `bspline`, and equivalent to ``bspline(x, 2)``.

    Parameters
    ----------
    x : array_like
        a knot vector

    Returns
    -------
    res : ndarray
        Quadratic B-spline basis function values

    See Also
    --------
    bspline : B-spline basis function of order n
    cubic : A cubic B-spline.

    Examples
    --------
    We can calculate B-Spline basis function of several orders:

    >>> from scipy.signal import bspline, cubic, quadratic
    >>> bspline(0.0, 1)
    1

    >>> knots = [-1.0, 0.0, -1.0]
    >>> bspline(knots, 2)
    array([0.125, 0.75, 0.125])

    >>> np.array_equal(bspline(knots, 2), quadratic(knots))
    True

    >>> np.array_equal(bspline(knots, 3), cubic(knots))
    True

    """
    ax = abs(asarray(x))
    res = zeros_like(ax)
    cond1 = less(ax, 0.5)
    if cond1.any():
        ax1 = ax[cond1]
        res[cond1] = 0.75 - ax1 ** 2
    cond2 = ~cond1 & less(ax, 1.5)
    if cond2.any():
        ax2 = ax[cond2]
        res[cond2] = (ax2 - 1.5) ** 2 / 2.0
    return res


def cascade(hk, J=7):
    """
    Return (x, phi, psi) at dyadic points ``K/2**J`` from filter coefficients.

    Parameters
    ----------
    hk : array_like
        Coefficients of low-pass filter.
    J : int, optional
        Values will be computed at grid points ``K/2**J``. Default is 7.

    Returns
    -------
    x : ndarray
        The dyadic points ``K/2**J`` for ``K=0...N * (2**J)-1`` where
        ``len(hk) = len(gk) = N+1``.
    phi : ndarray
        The scaling function ``phi(x)`` at `x`:
        ``phi(x) = sum(hk * phi(2x-k))``, where k is from 0 to N.
    psi : ndarray, optional
        The wavelet function ``psi(x)`` at `x`:
        ``phi(x) = sum(gk * phi(2x-k))``, where k is from 0 to N.
        `psi` is only returned if `gk` is not None.

    Notes
    -----
    The algorithm uses the vector cascade algorithm described by Strang and
    Nguyen in "Wavelets and Filter Banks".  It builds a dictionary of values
    and slices for quick reuse.  Then inserts vectors into final vector at the
    end.

    """
    N = len(hk) - 1

    if (J > 30 - np.log2(N + 1)):
        raise ValueError("Too many levels.")
    if (J < 1):
        raise ValueError("Too few levels.")

    # construct matrices needed
    nn, kk = np.ogrid[:N, :N]
    s2 = np.sqrt(2)
    # append a zero so that take works
    thk = np.r_[hk, 0]
    gk = qmf(hk)
    tgk = np.r_[gk, 0]

    indx1 = np.clip(2 * nn - kk, -1, N + 1)
    indx2 = np.clip(2 * nn - kk + 1, -1, N + 1)
    m = np.empty((2, 2, N, N), 'd')
    m[0, 0] = np.take(thk, indx1, 0)
    m[0, 1] = np.take(thk, indx2, 0)
    m[1, 0] = np.take(tgk, indx1, 0)
    m[1, 1] = np.take(tgk, indx2, 0)
    m *= s2

    # construct the grid of points
    x = np.arange(0, N * (1 << J), dtype=float) / (1 << J)
    phi = 0 * x

    psi = 0 * x

    # find phi0, and phi1
    lam, v = eig(m[0, 0])
    ind = np.argmin(np.absolute(lam - 1))
    # a dictionary with a binary representation of the
    #   evaluation points x < 1 -- i.e. position is 0.xxxx
    v = np.real(v[:, ind])
    # need scaling function to integrate to 1 so find
    #  eigenvector normalized to sum(v,axis=0)=1
    sm = np.sum(v)
    if sm < 0:  # need scaling function to integrate to 1
        v = -v
        sm = -sm
    bitdic = {'0': v / sm}
    bitdic['1'] = np.dot(m[0, 1], bitdic['0'])
    step = 1 << J
    phi[::step] = bitdic['0']
    phi[(1 << (J - 1))::step] = bitdic['1']
    psi[::step] = np.dot(m[1, 0], bitdic['0'])
    psi[(1 << (J - 1))::step] = np.dot(m[1, 1], bitdic['0'])
    # descend down the levels inserting more and more values
    #  into bitdic -- store the values in the correct location once we
    #  have computed them -- stored in the dictionary
    #  for quicker use later.
    prevkeys = ['1']
    for level in range(2, J + 1):
        newkeys = ['%d%s' % (xx, yy) for xx in [0, 1] for yy in prevkeys]
        fac = 1 << (J - level)
        for key in newkeys:
            # convert key to number
            num = 0
            for pos in range(level):
                if key[pos] == '1':
                    num += (1 << (level - 1 - pos))
            pastphi = bitdic[key[1:]]
            ii = int(key[0])
            temp = np.dot(m[0, ii], pastphi)
            bitdic[key] = temp
            phi[num * fac::step] = temp
            psi[num * fac::step] = np.dot(m[1, ii], pastphi)
        prevkeys = newkeys

    return x, phi, psi



from __future__ import division
import numpy as np


def convolution_matrix(x, N=None, mode='full'):
    """Compute the Convolution Matrix
    This function computes a convolution matrix that encodes
    the computation equivalent to ``numpy.convolve(x, y, mode)``
    Parameters
    ----------
    x : array_like
        One-dimensional input array
    N : integer (optional)
        Size of the array to be convolved. Default is len(x).
    mode : {'full', 'valid', 'same'}, optional
        The type of convolution to perform. Default is 'full'.
        See ``np.convolve`` documentation for details.
    Returns
    -------
    C : ndarray
        Matrix operator encoding the convolution. The matrix is of shape
        [Nout x N], where Nout depends on ``mode`` and the size of ``x``. 
    Example
    -------
    >>> x = np.random.rand(10)
    >>> y = np.random.rand(20)
    >>> xy = np.convolve(x, y, mode='full')
    >>> C = convolution_matrix(x, len(y), mode='full')
    >>> np.allclose(xy, np.dot(C, y))
    True
    See Also
    --------
    numpy.convolve : direct convolution operation
    scipy.signal.fftconvolve : direct convolution via the
                               fast Fourier transform
    scipy.linalg.toeplitz : construct the Toeplitz matrix
    """
    x = np.asarray(x)
    if x.ndim != 1:
        raise ValueError("x should be 1-dimensional")

    M = len(x)
    N = M if N is None else N

    if mode == 'full':
        Nout = M + N - 1
        offset = 0
    elif mode == 'valid':
        Nout = max(M, N) - min(M, N) + 1
        offset = min(M, N) - 1
    elif mode == 'same':
        Nout = max(N, M)
        offset = (min(N, M) - 1) // 2
    else:
        raise ValueError("mode='{0}' not recognized".format(mode))

    xpad = np.hstack([x, np.zeros(Nout)])
    n = np.arange(Nout)[:, np.newaxis]
    m = np.arange(N)
    return xpad[n - m + offset]