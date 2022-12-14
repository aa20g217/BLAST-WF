"""
A wf for  BLAST (Basic Local Alignment Search Tool).
"""


import subprocess
from pathlib import Path

from flytekit import LaunchPlan, workflow
from latch.types import LatchDir,LatchFile
from latch import large_task
from latch.resources.launch_plan import LaunchPlan
import os,shutil
from typing import Optional, Annotated
from flytekit.core.annotation import FlyteAnnotation

@large_task
def runwf(fasta_file: Optional[LatchFile],
    aa_sequence: Optional[str],
    output_dir: LatchDir,
    blastType: str = "blastp",db: str = "nr",evalue: str = "10",outfmt: str = "0") -> LatchDir:
    os.mkdir('results')
    os.chdir("/root/results/")

    cmd="/root/blast/bin/"+blastType

    if fasta_file is not None:

        subprocess.run(
            [
                cmd,
                "-query",
                fasta_file.local_path,
                "-db",
                db,
                "-evalue",
                evalue,
                "-outfmt",
                outfmt,
                "-out",
                "result.html",
                "-html","-remote"

            ]
        )
    else:
        text_file = open("input.txt", "w")
        text_file.write(aa_sequence)
        text_file.close()
        subprocess.run(
            [
                blastType,
                "-query",
                "input.txt",
                "-db",
                db,
                "-evalue",
                evalue,
                "-outfmt",
                outfmt,
                "-out",
                "result.html",
                "-html","-remote "

            ]
        )


    local_output_dir = str(Path("/root/results/").resolve())

    remote_path=output_dir.remote_path
    if remote_path[-1] != "/":
        remote_path += "/"

    return LatchDir(local_output_dir,remote_path)

#-> LatchDir
@workflow
def BLAST(output_dir: LatchDir,blastType: str = "blastp",db: str = "nr",evalue: str = "10",outfmt: str = "0",input_sequence_fork: str = "text",
        fasta_file: Optional[
        Annotated[
            LatchFile,
            FlyteAnnotation(
                {
                    "rules": [
                        {
                            "regex": "(.fasta|.fa|.faa|.txt|.fas)$",
                            "message": "Only .fasta, .fa, .fas,.txt, or .faa extensions are valid",
                        }
                    ],
                }
            ),
        ]
    ] = None,
    aa_sequence: Optional[
        Annotated[
            str,
            FlyteAnnotation(
                {
                    "appearance": {
                        "type": "paragraph",
                        "placeholder": ">SequenceOne\nLESPNCDWKNNR...\n>SequenceTwo\nRLENKNNCSPDW...\n>SequenceThree\nCDWKNNENPDEA...",
                    },
                    "rules": [
                        {
                            "message": "Paste a set of sequences in fasta format. The name line must start with `>`.",
                        }
                    ],
                }
            ),
        ]
    ] = None):
    """

    A wf for  BLAST (Basic Local Alignment Search Tool).
    ----

    A wf for  BLAST (Basic Local Alignment Search Tool).

    __metadata__:
        display_name: BLAST (Basic Local Alignment Search Tool)
        author:
            name: Akshay
            email: akshaysuhag2511@gmail.com
            github:
        repository:
        license:
            id: MIT
        flow:
        - section: Fasta Sequences
          flow:
            - fork: input_sequence_fork
              flows:
                text:
                    display_name: Text
                    _tmp_unwrap_optionals:
                        - aa_sequence
                    flow:
                        - params:
                            - aa_sequence
                file:
                    display_name: File
                    _tmp_unwrap_optionals:
                        - fasta_file
                    flow:
                        - params:
                            - fasta_file

        - section: Parameters
          flow:
          - params:
              - blastType
          - params:
              - db
          - params:
              - evalue
          - params:
              - outfmt


        - section: Output Settings
          flow:
          - params:
              - output_dir




    Args:

        fasta_file:
          Select input file. This file must be in FASTA format.

          __metadata__:
            display_name: Input File

        aa_sequence:
            Fasta sequences.

            __metadata__:
                display_name: Fasta Sequence(s)

        input_sequence_fork:

            __metadata__:
                display_name: Input Sequence

        blastType:
            BLAST search type. Possible options are blastn, blastp, blastx, and tblastx.

            __metadata__:
                display_name: BLAST Type

        db:
             Provide the name of the database to be used for the BLAST search. Given database should be searchable on the NCBI website, such as nr, refseq_rna, etc.

            __metadata__:
                display_name: Database

        evalue:
             Expect value (E) for saving hits.

            __metadata__:
                display_name: evalue
        outfmt:
             Output formats for the tabular and commaseparated value. For more details see “outfmt” here https://scicomp.ethz.ch/public/manual/BLAST/BLAST.pdf

            __metadata__:
                display_name: Output format

        output_dir:
          Where to save the results?.

          __metadata__:
            display_name: Output Directory
    """
    return runwf(fasta_file=fasta_file,aa_sequence=aa_sequence,blastType=blastType,db=db,evalue=evalue,outfmt=outfmt,output_dir=output_dir)

LaunchPlan(
    BLAST,
    "Test Data",
    {
        "fasta_file": LatchFile("s3://latch-public/test-data/4148/muscle/input.txt")
    },
)
