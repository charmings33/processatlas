ProcessAtlas: anonymised supplementary data
===========================================

Supplementary material for:

  Ng, M. S., Dillenburger, B., Hu, R., Kojio, R., Bock, T.
  From Kit of Parts to Kit of Processes: anatomising Robotic Construction
  in Japan. Submitted to Automation in Construction.

The live querying interface is at https://charmings33.github.io/processatlas/
The coding of the 50 polar cases is at
https://charmings33.github.io/processatlas/suppdoc/


Files
-----

Ng_et_al_From_Kit_of_Parts_to_Kit_of_Processes_census___polar_cases_coding.xlsx
    The coding data, in three sheets.
      140           50 polar cases (RP1-RP50), binary coded against the
                    140-enabler DfDFAB ontology of Ng et al. (2022), with
                    descriptor columns for stakeholder tier, deployment,
                    material, lifecycle phase, TRL, adoption driver,
                    building system and construction task.
      JPR           217 census records, descriptor columns only.
      Dependencies  100 directed enabler-to-enabler edges (DEP1-DEP100),
                    each with a relation type, an evidence grade, a note
                    and a literature citation.

ProcessAtlas.ttl
    The knowledge graph serialised as Turtle, built from the workbook above.

build_processatlas.py
    The build script. Run it in this directory to regenerate ProcessAtlas.ttl
    from the workbook. Requires Python 3 with openpyxl and rdflib.

        pip install openpyxl rdflib
        python3 build_processatlas.py


Contents of ProcessAtlas.ttl
----------------------------

    enablers                140
    polar cases             50
    census records          217
    activation edges        2,553
    dependencies            100
    co-occurrence edges     8,426
    total triples           42,136

Namespace: http://jprx.example.org/ontology#

Classes: Process (polar case), CensusRecord, Enabler, Dependency,
CoOccurrence.

Each enabler carries its identifier, its verbatim label from Ng et al. (2022),
its category and the category colour of that source. Each polar case carries
its jprx:activates edges to the enablers it draws on, its activation total and
its descriptors. Each census record carries descriptors only. Each dependency
is reified with its relation, evidence grade, note and citation, and is also
asserted as a direct edge between the two enablers. The co-occurrence layer and
the per-enabler activation frequencies are recomputed from the polar coding.


Anonymisation, and the triple count
-----------------------------------

The paper reports a knowledge graph of 44,644 triples. This released file
contains 42,136. The difference is the identifying layer, which has been
removed for confidentiality: company names in English and Japanese, robot and
product names, free-text process descriptions and firm websites. No coded value
has been altered, added or removed. Every analytical result reported in the
paper is computed from the coding, which is released here in full.

The released file therefore reproduces the counts, distributions, bundles,
chains and query structures reported in the paper, but not the firm-level and
product-level identification of individual processes. Queries that return
named firms or products run against the full graph through the Process Atlas
interface linked above.

The underlying census source documentation is retained for confidentiality
reasons.


Citation
--------

Please cite the paper above when using these data.
