Welcome to LastPlot's documentation!
============================================

Contents
--------

.. toctree::
   :maxdepth: 1

   installation
   usage
   workflows/data_workflow
   graphs/graphs


Lastplot
-----------

Lipid Analysis and Statistical Testing with Plotting for LC-MS Output Transformation (LastPlot) is a Python package designed to elaborate data into graphs coming from lipid extractions (LC/MS). Starting from a file containing the pmol/mg values per each sample, this package streamlines the process of data analysis and visualization.

Key Features
------------

LastPlot includes the following features:

- **Data Sanitization:** Clean and prepare data for analysis, removing internal standard samples and non-value samples.
- **Data Normalization:** Normalize values with log10 to ensure consistency across samples.
- **Normality Check:** Use the Shapiro-Wilk test to check for normality of residuals.
- **Equality of Variance Check:** Use Levene's test to assess the equality of variances.
- **Statistical Significance Annotation:** Annotate boxplots with significance levels using t-test, Welch's t-test, Mann-Whitney, or two-way ANOVA test depending on the data requirements, through the starbars package.
- **Visualization Tools:** Create boxplots with statistical annotations.

Contributing
------------

We welcome contributions! If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some amazing feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

License
-------

Distributed under the MIT License.


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
