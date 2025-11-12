README — Transfer Entropy Analysis Script (CulculateTansferEntropy.py)

Overview
This script is a Python program that performs Transfer Entropy (TE) analysis automatically using the Java Information Dynamics Toolkit (JIDT: https://github.com/jlizier/jidt).
It reads multiple CSV files from a specified data folder, calculates the transfer entropy between specific signal pairs (e.g., R→H, H→R), and outputs the results as CSV files.

Main Features
- Uses the JIDT Java library (infodynamics.jar) via JPype to calculate TE from Python
- Computes TE for multiple specified delays (delaylist)
- Performs bidirectional analysis (R→H and H→R) separately
- Merges calculated TE results with questionnaire data (Questioneer.csv) by ID
- Saves output files with filenames that include the analysis parameters (k, l, t, delay)

Project Structure
project_root/
├─ CulculateTansferEntropy.py     # Main script
├─ Storage/                       # Folder containing input CSV data
├─ Result/                        # Folder for output CSV results
├─ Questioneer.csv                 # Questionnaire data
└─ JIDT/
    └─ infodynamics.jar           # JIDT library

Execution Environment
- Python 3.10.0
- Java JDK 25 (must include jvm.dll)
- Required Python libraries:
  jpype1
  numpy
  pandas
- The JIDT library (infodynamics.jar) must be installed locally

How to Run
1. Adjust the following path variables according to your local environment:
   - jarLocation
   - jvmpath
   - InfodynamicsPath
2. Place input CSV files in the Storage folder
3. Place Questioneer.csv in the same directory as the script
4. Modify the analysis parameters and output settings (lines 110–116) as needed
5. Run the script from the command line:
   python CulculateTansferEntropy.py
6. The results will be saved automatically in the Result/ folder

Input File Format
The script reads CSV files from the Storage/ folder and analyzes each column as a time series.
The expected input format is as follows:

HLH,HRH,RLH,RRH
0.85,0.90,0.96,0.93
0.90,0.91,0.97,0.95
0.85,0.90,0.97,0.98
0.86,0.89,0.96,1.00
0.85,0.89,0.95,0.97

Column Descriptions
HLH : Height of the human’s left hand above the ground
HRH : Height of the human’s right hand above the ground
RLH : Height of the robot’s left hand above the ground
RRH : Height of the robot’s right hand above the ground

Notes
- All columns must have the same number of samples
- Missing values (NaN) are automatically filled with 0
- The first row must contain column headers
- UTF-8 or Shift-JIS encoding is recommended for CSV files

Output File Format
For each file ID, the following columns are included in the output:

When delaylist = [0, 5, 10, 20, 30]:
  RtoHd=0, 5, 10, 20, 30, Max
  HtoRd=0, 5, 10, 20, 30, Max

Questionnaire data from Questioneer.csv are merged into the same output file.

Notes
- The JVM is launched only once, during the first calculation
- Missing values are automatically replaced with zeros
- By modifying the delaylist and the output headers, you can compare TE results under different delay conditions
