# BLAST (Basic Local Alignment Search Tool). workflow

#### **Summary**
This repository contains a latch wf for  BLAST (Basic Local Alignment Search Tool)..

#### **Input**

* Input Data
    - Input squneces in fasta format.
    
* Blast Type
    - BLAST search type. Possible options are blastn, blastp, blastx, and tblastx.
    
 
* Database
    - Provide the name of the database to be used for the BLAST search. Given database should be searchable on the NCBI website, such as nr, refseq_rna, etc. For more details check out https://scicomp.ethz.ch/public/manual/BLAST/BLAST.pdf

* evalue
    - Expect value (E) for saving hits.

* Output format
    - Output formats for the tabular and commaseparated value. For more details see “outfmt” here https://scicomp.ethz.ch/public/manual/BLAST/BLAST.pdf
          
#### **Output**
Alignment file. 

#### **Latch workflow link**
https://console.latch.bio/explore/83495/info
