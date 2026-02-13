#!/usr/bin/env python3
import pandas as pd
import glob
import os
from datetime import datetime

# ==========================================
# 1. DATABASE OF KNOWN RESISTANCE
# ==========================================
known_resistance = {
    # Fluoroquinolones (Cipro) - gyrA
    "gyrA": [
        "p.Ser83Ile", "p.Ser83Tyr", "p.Asp87Gln", 
        "p.Ser84Cys", "p.Ser84Asn", 
        "p.Asn709Asp" 
    ], 
    
    # Fluoroquinolones (Cipro) - parC
    "parC": [
        "p.Ser80Ile", "p.Glu84Lys", 
        "p.Glu486Gln" 
    ], 
    
    # Ampicillin - pbp5
    "pbp5": ["p.Met485Ala", "p.Ser466Lue"], 
    
    # Rifampin - rpoB
    "rpoB": ["p.His489Asp"]
}

# Genes where ANY presence means resistance (Acquired)
acquired_genes = ["vanA", "vanB", "ermB", "tetM"]

# Drug Mapping
drug_map = {
    "gyrA": "Fluoroquinolones (Cipro/Levo)",
    "parC": "Fluoroquinolones",
    "vanA": "Vancomycin",
    "vanB": "Vancomycin",
    "pbp5": "Ampicillin",
    "ermB": "Erythromycin",
    "tetM": "Tetracycline",
    "rpoB": "Rifampicin"
}

# ==========================================
# 2. HTML CSS STYLING
# ==========================================
html_template = """
<html>
<head>
<style>
    body {{ font-family: 'Arial', sans-serif; background-color: #f4f6f9; padding: 20px; }}
    .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
    h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
    th {{ background-color: #2c3e50; color: white; padding: 12px; text-align: left; }}
    td {{ padding: 12px; border-bottom: 1px solid #ddd; }}
    .badge-red {{ background-color: #e74c3c; color: white; padding: 5px 10px; border-radius: 4px; font-weight: bold; font-size: 12px; }}
    .badge-orange {{ background-color: #f39c12; color: white; padding: 5px 10px; border-radius: 4px; font-weight: bold; font-size: 12px; }}
    .badge-green {{ background-color: #27ae60; color: white; padding: 5px 10px; border-radius: 4px; font-weight: bold; font-size: 12px; }}
    .sample-header {{ background-color: #ecf0f1; font-weight: bold; color: #7f8c8d; }}
</style>
</head>
<body>
<div class="container">
    <h1>🧬 MDR Genomic Analysis Report</h1>
    <p><b>Date:</b> {date}</p>
    <table>
        <thead>
            <tr>
                <th>Gene</th>
                <th>AA Change</th>
                <th>Target Drug</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
    </table>
</div>
</body>
</html>
"""

# ==========================================
# 3. PROCESSING LOOP
# ==========================================
table_rows = ""
tsv_files = glob.glob("07_mdr_analysis_snpsift/*_mdr.tsv")

print(f"Generating Report for {len(tsv_files)} samples...")

for file in tsv_files:
    sample_name = os.path.basename(file).replace("_mdr.tsv", "")
    
    # READ DATA (Handles comma-separated lists automatically)
    try:
        df = pd.read_csv(file, sep='\t')
    except Exception as e:
        print(f"Skipping {sample_name}: {e}")
        continue 

    # Add Sample Header
    table_rows += f"<tr class='sample-header'><td colspan='4'>SAMPLE: {sample_name}</td></tr>"

    # Define Genes to watch
    interesting_genes = ["gyrA", "parC", "pbp5", "rpoB", "vanA", "vanB", "ermB", "tetM"]
    
    found_any = False

    for index, row in df.iterrows():
        # Clean up the data (SnpEff sometimes leaves lists like 'gene1,gene2')
        raw_genes = str(row['ANN[*].GENE']).split(',')
        raw_changes = str(row['ANN[*].HGVS_P']).split(',')
        
        # Loop through the list inside the cell
        for i, gene in enumerate(raw_genes):
            if i >= len(raw_changes): break 
            
            change = raw_changes[i]
            
            # 1. Filter: Is this a gene we care about?
            is_target = False
            for target in interesting_genes:
                if target in gene: 
                    is_target = True
                    break
            
            if not is_target:
                continue
                
            # 2. Filter: Skip empty protein changes
            if change == "" or change == "nan" or change == ".":
                continue

            # 3. Logic to determine Badge Color
            status = "Unknown Variant"
            badge_class = "badge-green"

            if gene in acquired_genes:
                status = "RESISTANT (Acquired)"
                badge_class = "badge-red"
            elif gene in known_resistance:
                # Check if exact mutation is in our list
                if any(marker in change for marker in known_resistance[gene]):
                    status = "RESISTANT"
                    badge_class = "badge-red"
                else:
                    status = "Variant (VUS)"
                    badge_class = "badge-orange"
            
            # Add to table
            table_rows += f"""
            <tr>
                <td><b>{gene}</b></td>
                <td>{change}</td>
                <td>{drug_map.get(gene, "Unknown")}</td>
                <td><span class="{badge_class}">{status}</span></td>
            </tr>
            """
            found_any = True

    if not found_any:
        table_rows += "<tr><td colspan='4'><i>No relevant resistance mutations found (Sensitive)</i></td></tr>"

# ==========================================
# 4. SAVE FILE
# ==========================================
current_date = datetime.now().strftime("%Y-%m-%d")
final_html = html_template.format(date=current_date, rows=table_rows)

output_path = "07_mdr_analysis_snpsift/Final_MDR_Report.html"
with open(output_path, "w") as f:
    f.write(final_html)

print(f"Success! Open {output_path}")
