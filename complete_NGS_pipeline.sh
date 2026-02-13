#!/bin/bash
# Pipeline: MDR Genomic Epidemiology Analysis
# Developed by: Manoj Devadiga

# --- SAFETY HEADER ---
set -e          # Stop if any command fails
set -u          # Stop if an undefined variable is used (typo protection)
set -o pipefail # Catch errors inside piped commands

ref="GCF_009734005.1_ASM973400v2_genomic.fna"
Raw_data= "raw_files/"

# Verify raw data exists before starting
if [ ! -d "$Raw_data" ]; then
    echo "Error: Directory '$Raw_data' not found."
    exit 1
fi

#step 1 FASTQC
# t indicates core of the computer.More core means more speed 
#01_raw_QC-folder to store fastqc result
#Create the output folder first
mkdir -p 01_raw_QC
fastqc ${Raw_data}/*.fastq.gz -o 01_raw_QC/ -t 16

#Step 2 TRIMMOMATIC
# 1. Make sure the output folder exists
mkdir -p 02_trimmomatic

# 2. Run the loop
for file1 in raw_files/*_1.fastq.gz; do
   
   # Define file2
   file2="${file1/_1.fastq.gz/_2.fastq.gz}"

   # Run Trim Galore
   # Added: -o 02_trimmomatic/
   trim_galore --paired --illumina --fastqc -j 8 \
   -o 02_trimmomatic/ \
   "$file1" "$file2"

done

#step 3 INDEXING OF REFERNCE SEQUENCE
bwa index ${ref}

#step 4 ALIGNMENT
#Create the output folder first
mkdir -p 03_alignment
# 1. Loop through files
for file1 in 02_trimmomatic/*_val_1.fq.gz; do
    
    # FIX: Replace the ENTIRE suffix so "_1" becomes "_2"
    file2="${file1/_1_val_1.fq.gz/_2_val_2.fq.gz}"

    # Sample Name
    sample=$(basename "$file1" _1_val_1.fq.gz)

    # Read Group
    rg="@RG\tID:${sample}\tLB:lib1\tPL:ILLUMINA\tSM:${sample}"

    echo "Processing: $sample (Looking for pair: $file2)"

    # Run BWA (12 threads)
    bwa mem -t 12 -R "$rg" \
    ${ref} \
    "$file1" "$file2" > "03_alignment/${sample}_aligned.sam"

done

#step 5 SAM to BAM
for file in 03_alignment/*.sam; do
    
    # 1. FIX: Changed "$ile" to "$file"
    sample=$(basename "$file" .sam)
    
    echo "Processing: $sample"

    # 2. Sort (Outputting to _sorted.bam)
    samtools sort -@ 12 -o "03_alignment/${sample}_sorted.bam" "$file"
    
    # 3. Index (Now it matches the file above)
    samtools index "03_alignment/${sample}_sorted.bam"

done

#step 6 REMOVE DUPLICATE SEQUENCE
# Loop through ONLY the sorted BAM files
for file in 03_alignment/*_sorted_read.bam; do
    
    # 1. Clean the sample name
    # Removes "_aligned_sorted_read.bam" to get just "india"
    sample=$(basename "$file" _aligned_sorted_read.bam)
    
    echo "Marking Duplicates for: $sample"

    # 2. Run GATK (Fixed Order!)
    # --java-options comes FIRST
    # MarkDuplicates comes SECOND
    gatk --java-options "-Xmx4g" MarkDuplicates \
      -I "$file" \
      -O "03_alignment/${sample}_dedup.bam" \
      -M "03_alignment/${sample}_dup_metrics.txt" \
      --REMOVE_DUPLICATES true \
      --CREATE_INDEX true

done

#step 7 VARIANT CALLING
# 1. Create output folder
mkdir -p 04_variants
# Loop through files
for file in 03_alignment/*_dedup.bam; do
    
    sample=$(basename "$file" _dedup.bam)
    echo "Calling Variants for: $sample"

    # Added: --native-pair-hmm-threads 4
    # This uses 4 cores for the heavy math
    gatk --java-options "-Xmx4g" HaplotypeCaller \
      -R ${ref} \
      -I "$file" \
      -O "04_variants/${sample}_raw.vcf" \
      -ploidy 1 \
      --native-pair-hmm-threads 4

done

#Step 8 VARIANT FILE FILTERING
# 1. Create the output folder first
mkdir -p 05_filtered_vcfs

# 2. Loop through raw VCFs
for file in 04_variants/*_raw.vcf; do
    
    # Get clean sample name
    sample=$(basename "$file" _raw.vcf)
    
    echo "Filtering Variants for: $sample"

    # Fix: VariantFiltration (not Varient)
    gatk VariantFiltration \
      -R ${ref} \
      -V "$file" \
      -O "05_filtered_vcfs/${sample}_filtered.vcf" \
      --filter-name "LowQual" \
      --filter-expression "QD < 2.0 || FS > 60.0 || MQ < 40.0 || SOR > 3.0"

done

#step  VARIANT FILE ANNOTATION

#Create the Output folder first
mkdir -p 06_annoted_snpeff_vcf
# Loop through filtered VCF files
for file in 05_filtered_vcfs/*_filtered.vcf; do
    
    # Get clean sample name
    sample=$(basename "$file" _filtered.vcf)
    
    echo "Annotating: $sample"

    # Run SnpEff (One single > to save the file)
    snpEff -c snpEff.config \
      Enterococcus_faecium_ASM973400v2 \
      "$file" \
      > "06_annoted_snpeff_vcf/${sample}_annotated.vcf"

done

#step  ANNOTATED VARIENT FILE ARRANGING AND REMOVE MESSYTHING
# 1. Create the output folder first
mkdir -p 07_mdr_analysis_snpsift

# 2. Run the loop with the CORRECT folder name (annoted)
for file in 06_annoted_snpeff_vcf/*_annotated.vcf; do
    
    sample=$(basename "$file" _annotated.vcf)
    echo "Fixing Table for: $sample"

    # Run SnpSift with the comma separator fix
    SnpSift extractFields -s "," "$file" \
      CHROM POS REF ALT \
      "ANN[*].GENE" "ANN[*].HGVS_P" "ANN[*].IMPACT" \
      > "07_mdr_analysis_snpsift/${sample}_mdr.tsv"
done

# --- FINAL STEP: AUTOMATED REPORTING ---
echo "Bioinformatics Analysis Complete."

if [ -f "MDR_visualization.py" ]; then
    echo "Launching Python Visualization..."
    python3 mdr_visualizer.py
else
    echo "Warning: mdr_visualizer.py not found. Report not generated."
fi
