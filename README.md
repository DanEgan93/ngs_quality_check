<h1>Automating TSHC Quality Checks</h1>


<h2>A script to parse output files from the MiSeq Universal pipeline (TSHC) to determine if quality criteria has been met or not.</h2>
Quality criteria include:
- If any samples within a run have a 20x coverage < 96%
- If number of exons in gene-exon tab == 1419
- If reads are present in the negative control
- If any kinship values in the kinship > 0.48 
- VCF file count
- FASTQ-BAM output check
- Verify bam id check
