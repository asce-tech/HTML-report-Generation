import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from jinja2 import Template

def load_data(filename, col_index, has_header):
    header = 0 if has_header else None

    try:
        data = pd.read_csv(filename, header=header)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        sys.exit(1)

    if not has_header:
        data.columns = [f"Column {i}" for i in range(len(data.columns))]

    if col_index >= len(data.columns):
        print(f"Invalid column index {col_index}. Only {len(data.columns)} columns available.")
        sys.exit(1)
    return data, data.columns[col_index]

def iqr_outlier_detection(data, col_idx):
    col_data = data[col_idx]
    q1 = col_data.quantile(0.25)
    q3 = col_data.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = data[(col_data < lower_bound) | (col_data > upper_bound)]
    non_outliers = data[(col_data >= lower_bound) & (col_data <= upper_bound)]
    return outliers, non_outliers, iqr, lower_bound, upper_bound

def save_datasets(data, filename, suffix):
    output_file = f"{filename}_{suffix}.csv"
    data.to_csv(output_file, index=False)
    return output_file

def plot_data(data, col_idx, suffix):
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    axes[0].hist(data[col_idx], bins=30, color='skyblue', edgecolor='black')
    axes[0].set_title(f"{suffix} - Histogram")
    axes[0].set_xlabel(f"{col_idx} (Values)")
    axes[0].set_ylabel("Frequency")
    axes[1].boxplot(data[col_idx], patch_artist=True)
    axes[1].set_title(f"{suffix} - Boxplot")
    axes[1].set_ylabel(f"{col_idx} (Values)")
    combined_file = f"{suffix}_combined_plot.png"
    plt.tight_layout()
    plt.savefig(combined_file)
    plt.close()
    return combined_file

def generate_html_report(filename, col_index, col_idx, stats, histograms, iqr_values, output_html="Final_report.html"):
    template_str = """
    <html>
    <head>
        <title>Final Project Report</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                line-height: 1.6; 
            }
            h1 {
                text-align: center;
                color: #333;
            }
            h2 {
                color: #444;
                border-bottom: 2px solid #ccc;
                padding-bottom: 5px;
            }
            table {
                width: 50%;
                margin: 20px auto;
                border-collapse: collapse;
            }
            table, th, td {
                border: 1px solid #ddd;
            }
            th, td {
                padding: 10px;
                text-align: left;
            }
            th {
                background-color: #f4f4f4;
            }
            .center {
                text-align: center;
            }
            img {
                display: block;
                margin: 20px auto;
                max-width: 80%;
            }
        </style>
    </head>
    <body>
        <h1>Final Project Report</h1>

        <h2>Dataset Information</h2>
        <p><b>File Name:</b> {{ filename }}</p>
        <p><b>Column Index:</b> {{ col_index }}</p>
        <p><b>Column Name:</b> {{ col_idx }}</p>

        <h2>Dataset Statistics</h2>
        <table>
            <tr><th>Statistic</th><th>Original Dataset</th><th>Outliers</th><th>Non-Outliers</th></tr>
            {% for stat in stats %}
            <tr>
                <td>{{ stat }}</td>
                <td>{{ stats[stat].original }}</td>
                <td>{{ stats[stat].outliers }}</td>
                <td>{{ stats[stat].non_outliers }}</td>
            </tr>
            {% endfor %}
            <tr>
                <td>IQR</td>
                <td>{{ iqr_values.original }}</td>
                <td>N/A</td>
                <td>N/A</td>
            </tr>
        </table>

        <h2>Histograms & Boxplots</h2>
        <div class="center">
            <h3>Original Dataset</h3>
            <img src="{{ histograms.original }}" alt="Original Combined Plot">

            <h3>Outliers</h3>
            <img src="{{ histograms.outliers }}" alt="Outliers Combined Plot">

            <h3>Non-Outliers</h3>
            <img src="{{ histograms.non_outliers }}" alt="Non-Outliers Combined Plot">
        </div>
    </body>
    </html>
    """
    template = Template(template_str)
    html_content = template.render(
        filename=filename, col_index=col_index, col_idx=col_idx, stats=stats,
        histograms=histograms, iqr_values=iqr_values
    )
    with open(output_html, "w") as f:
        f.write(html_content)

def main():
    args = sys.argv
    if len(args) < 3:
        print("Usage: python script.py <filename> <column_index> [-h for header]")
        sys.exit(1)
    filename = args[1]
    col_index = int(args[2])
    has_header = len(args) > 3 and args[3] == "-h"
    data, col_idx = load_data(filename, col_index, has_header)
    outliers, non_outliers, iqr, lower_bound, upper_bound = iqr_outlier_detection(data, col_idx)
    save_datasets(outliers, filename, "outliers")
    save_datasets(non_outliers, filename, "nonoutliers")
    stats = {
        'Min': {
            'original': data[col_idx].min(),
            'outliers': outliers[col_idx].min(),
            'non_outliers': non_outliers[col_idx].min()
        },
        'Max': {
            'original': data[col_idx].max(),
            'outliers': outliers[col_idx].max(),
            'non_outliers': non_outliers[col_idx].max()
        },
        'Mean': {
            'original': data[col_idx].mean(),
            'outliers': outliers[col_idx].mean(),
            'non_outliers': non_outliers[col_idx].mean()
        },
        'Median': {
            'original': data[col_idx].median(),
            'outliers': outliers[col_idx].median(),
            'non_outliers': non_outliers[col_idx].median()
        },
        'Standard Deviation': {
            'original': data[col_idx].std(),
            'outliers': outliers[col_idx].std(),
            'non_outliers': non_outliers[col_idx].std()
        }
    }
    histograms = {}
    histograms['original'] = plot_data(data, col_idx, 'original')
    histograms['outliers'] = plot_data(outliers, col_idx, 'outliers')
    histograms['non_outliers'] = plot_data(non_outliers, col_idx, 'non_outliers')
    iqr_values = {'original': iqr}
    generate_html_report(filename, col_index, col_idx, stats, histograms, iqr_values)

if __name__ == "__main__":
    main()