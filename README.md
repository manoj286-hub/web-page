🧬 MDR Genomic Epidemiology Pipeline
Automated NGS Analysis for Multidrug Resistance in Enterococcus faecium

Developed by: Manoj Devadiga

Institution: Father Muller Research Centre (Internship Project)

Focus: Clinical Genomic Surveillance & Bioinformatics

📌 Project Overview
Multidrug-resistant (MDR) Enterococcus faecium is a critical priority pathogen often associated with hospital-acquired infections. This project focuses on the genomic epidemiology of E. faecium, specifically detecting resistance mutations and acquired antimicrobial resistance (AMR) genes from Next-Generation Sequencing (NGS) data.

This pipeline automates the entire bioinformatics workflow—from raw FASTQ reads to a clinical-grade HTML report—identifying resistance mechanisms against:

Vancomycin (vanA, vanB)

Fluoroquinolones (gyrA, parC)

Ampicillin (pbp5)

Erythromycin & Tetracycline (ermB, tetM)

Rifampicin (rpoB)

⚙️ Methodology (Pipeline Workflow)
The pipeline (complete_NGS_pipeline.sh) executes the following 10 steps sequentially:

Auto-Configuration: Automatically builds a custom SnpEff database using the provided reference genome (.fna) and annotation (.gff).

Quality Control: Checks raw read quality using FastQC.

Trimming: Removes adapters and low-quality bases using Trim Galore.

Alignment: Maps reads to the reference genome (ASM973400v2) using BWA-MEM.

Processing: Sorts and indexes alignments using Samtools.

Deduplication: Marks PCR duplicates using GATK MarkDuplicates.

Variant Calling: Identifies SNPs and Indels using GATK HaplotypeCaller (Ploidy 1).

Filtering: Removes low-quality variants using GATK VariantFiltration (Hard filtering standards).

Annotation: Predicts the functional effect of variants using SnpEff.

Reporting: Extracts AMR-relevant mutations and generates a color-coded HTML dashboard using a custom Python script.

🛠️ Prerequisites
To run this pipeline, you need a Linux environment with Conda installed.

Required Tools (Installed via Conda)
FastQC & Trim Galore

BWA & Samtools

GATK4 (Genome Analysis Toolkit)

SnpEff & SnpSift

Python 3 (with pandas library)

🚀 Installation & Usage
1. Clone the Repository
Download the pipeline to your local machine:

Bash
git clone https://github.com/manoj286-hub/MDR-Genomic-Analysis.git
cd MDR-Genomic-Analysis
2. Install Dependencies
We have provided an environment.yml to create the exact Conda environment used in this project:

Bash
# Create the environment
conda env create -f environment.yml

# Activate the environment
conda activate mdr_pipeline
Install the Python requirements for the reporting tool:

Bash
pip install -r requirements.txt
3. Prepare Your Data
The pipeline expects your raw data in a specific folder structure:

Create a folder named raw_files inside the project directory.

Place your paired-end FASTQ files inside.

File naming format: sample_1.fastq.gz and sample_2.fastq.gz

4. Run the Pipeline
Grant execution permissions and run the master script:

Bash
chmod +x complete_NGS_pipeline.sh mdr_visualizer.py
./complete_NGS_pipeline.sh
📊 Output Results
After the pipeline finishes, you will find results in organized folders:

01_raw_QC/: Quality reports for your raw reads.

04_variants/: Raw VCF files containing all mutations.

07_mdr_analysis_snpsift/: The final output folder.

📄 Final_MDR_Report.html: Open this in your browser to view the resistance profile.

📄 *_mdr.tsv: Tabular data of resistance mutations for Excel analysis.

📂 Repository Structure
complete_NGS_pipeline.sh: The main bash script that runs the analysis.

mdr_visualizer.py: Python script that generates the HTML report.

snpEff.config: Configuration file for the variant annotation tool.

GCF_...fna & GCF_...gff: Reference genome files for E. faecium.

requirements.txt: List of Python libraries needed.

environment.yml: List of bioinformatics tools needed.

📞 Contact
Manoj Devadiga
Bioinformatics Intern, Father Muller Research Centre
[manojdevadiga286@gmail.com]
