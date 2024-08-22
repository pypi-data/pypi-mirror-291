# Lipid Analysis and Statistical Testing with Plotting for LC-MS Output Transformation (LastPlot)

## What is it

LastPlot is a Python package designed to elaborate data into graphs coming from lipid extractions (LC/MS).
Starting from a file containing the **pmol/mg** values per each sample, this package streamlines the process of data
analysis and visualization.

## Features

LastPlot includes the following features:

- Data Sanitization: Clean and prepare data for analysis, removing internal standard samples and non value samples.
- Data Normalization: Normalize values with log10 to ensure consistency across samples.
- Normality Check: Use the Shapiro-Wilk test to check for normality of residuals.
- Equality of Variance Check: Use Levene's test to assess the equality of variances.
- Statistical Significance Annotation: Annotate boxplots with significance levels using t-test, Welch's t-test, or
  Mann-Whitney test depending on the data requirements, through the starbars package.
- Visualization Tools: Create boxplots to aid in data interpretation.

## Installation

You can install the package via pip:

```
pip install lastplot
```

\
Alternatively, you can install the package from the source:

```
git clone https://github.com/elide-b/lastplot.git
cd lastplot
pip install .
```

## Usage

Here is one example of how to use LastPlot:

```
import lastplot

# Example usage
df = lastplot.data_workflow(
    file_path="My project.xlsx",
    data_sheet="Data Sheet",
    mice_sheet="Mice ID Sheet",
    output_path="C:/Users/[YOUR-USERNAME]/Documents/example",
    control_name="WT",
    experimental_name=["FTD", "BPD", "HFD"]
)

lastplot.zscore_graph_lipid(
    df_final=df,
    control_name="WT",
    experimental_name=["FTD", "BPD", "HFD"]
    output_path="C:/Users/[YOUR-USERNAME]/Documents/example",
    palette="tab20b_r",
    show=True,
)
```

Returns graphs.

## Examples

For more detailed examples, please check the [example](https://github.com/elide-b/lastplot/tree/master/example)
folder.

## Contributing

We welcome contributions!
If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also
simply open an issue with the tag **"enhancement"**.

To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some amazing feature'`).
4. Push to the branch (`git push origin feature-branch`)
5. Open a pull request

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.
