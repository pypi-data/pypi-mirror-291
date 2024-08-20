Welcome to OASIS_stat's documentation!
======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   readme
   installation
   usage


Installation
============

To install OASIS, use the following pip command:

.. code-block:: bash

   pip install OASIS_stat

This will install the latest version of OASIS from PyPI.

Usage
=====

The package is currently documented primarily in each function's docstring, where a detailed description, along with the input and outputs of each function can be found. For more background on the test, and a detailed description of it's theoretical guarantees and the optimization procedures devised, please refer to the original paper: https://www.pnas.org/doi/10.1073/pnas.2304671121.

**List of Functions:**

- `splitCounts`: Downsamples a matrix. Very slight modification of https://stackoverflow.com/questions/11818215/subsample-a-matrix-python. This downsamples uniformly at random.

- `splitCountsColwise`: Downsamples a matrix columnwise, to ensure that each column is equally well represented in the train/test downsampled matrices.

- `generate_cf_finite_optimized`: Generates optimized column and row embeddings for the finite sample p-value. Tries multiple random initializations and returns the embeddings that maximize the finite sample p-value on the given X.

- `altMaximize`: Generates the optimal column and row embeddings for the asymptotic p-value.

- `compute_test_stat`: Computes the OASIS test statistic.

- `testPval_asymp` : Computes the OASIS asymptotic p-value for a given contingency table, row embedding, and column embedding. In order for the p-value to be valid, the row and column embeddings cannot depend on the input count matrix X.

- `testPval_finite` : Computes the OASIS finite sample p-value bound for a given contingency table, row embedding, and column embedding. Note that in order for the p-value to be valid, the row and column embeddings cannot depend on the input count matrix X. This p-value bound is finite-sample valid, but is not asymptotically uniform (a true p-value).

- `computeChi2Test` : Computes the chi-squared p-value for a contingency table, for easy comparison with OASIS p-values.

- `effectSize_bin` : Computes the effect size measure from the OASIS paper. Binarizes samples into positive and negative groups based on the sign of the column embedding.

- `OASIS_pvalue` : Computes the p-value using the OASIS method. Includes options for asymptotic or finite sample p-values, and can return the optimizing row and column embeddings and test statistic.


Authors
=======

- Tavor Z. Baharav
- David Tse
- Julia Salzman

Please reach out on GitHub with any questions, or directly to tavorb@mit.edu.

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
