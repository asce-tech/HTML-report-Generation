# 📊 HTML Report Generation with IQR Outlier Detection

## 📌 Project Objective

This Python program:
- Accepts a CSV file as input
- Performs Interquartile Range (IQR) outlier analysis on a selected column
- Splits the dataset into outliers and non-outliers
- Generates an interactive **HTML report** with:
  - File and column information
  - Summary statistics
  - Histograms and boxplots for all subsets
- Saves the outlier and non-outlier subsets into separate CSV files

---

## 🧠 Skills Learned

- Parsing and preprocessing CSV files using Python
- CLI-based tool development for data analysis tasks
- Outlier detection using the IQR method
- Generating statistical summaries: mean, median, std, IQR
- Creating plots using `matplotlib`
- HTML report generation with `Jinja2` templating
- Exporting datasets as new CSV files (outliers/non-outliers)

---

## 🧰 Libraries & Technologies

- `pandas`: Data manipulation
- `numpy`: Numerical calculations
- `matplotlib`: Data visualization (boxplots, histograms)
- `jinja2`: HTML templating
- `sys`: Command-line argument handling

---

## 🚀 Steps Performed

1. **Import required libraries**
2. **Read command-line arguments**
3. **Load CSV file**
4. **Extract target column**
5. **Perform IQR-based outlier detection**
6. **Calculate summary statistics**
7. **Split data into outliers and non-outliers**
8. **Generate boxplots and histograms**
9. **Create and save a dynamic HTML report**
10. **Export filtered datasets to CSV**

---

## 🖼️ Screenshots

### 📈 Dataset Summary
![image](https://github.com/user-attachments/assets/6a0b537f-6abb-4f53-aa11-41e069daa846)


### 📉 Histograms & Boxplots
![image](https://github.com/user-attachments/assets/3fa3af29-2cb4-49f3-94c0-313bd81e9f7e)



---

## 📂 Output Files

- `outliers.csv`: Contains outlier records
- `non_outliers.csv`: Contains clean data
- `report.html`: A styled HTML report with stats and plots

## ⚙️ How to Run

```bash
python detect_outliers.py input.csv 2


