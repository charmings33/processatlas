# Changelog

## 2.0.0 (22 October 2026)

### What changed
| Item | v1 | v2 |
|---|---|---|
| Namespace | http://jprx.example.org/ontology# | https://w3id.org/jprx/ontology# (registration pending) |
| Categories | `hasCategory` literal | 8 OWL classes, subClassOf `Enabler`, pairwise disjoint |
| Colours | `hasCategoryColour` in graph | removed; palette in `buildgraph_recommend.py` only |
| Case class | `jprx:Process` (clashed with Process category) | `jprx:RoboticProcess` |
| Census nodes | untyped | `jprx:CensusRecord` |
| Relations | 6 used + unused `requires`, `standardisationEnables` | exactly 6: enables, requires, presupposes, amplifies, mitigates, constrains |
| Relation type | free text `dependencyRelation` | `hasRelationType` -> SKOS concept (enablement / modulation) |
| Evidence | free text `evidenceLevel` | `hasEvidenceGrade` -> SKOS concept |
| Citations | `citation` literal | `prov:wasDerivedFrom` -> `jprx:Source` (64 sources, DOI where given) |
| Labels | partial | `rdfs:label` + `skos:definition` on every class and property |
| Unused | `jprx:Project` | removed |
| Ontology file | none | `jprx_ontology.ttl` (TBox + vocabularies, 341 triples) |

### Checks
- HermiT (owlready2): consistent, no unsatisfiable classes.
- Negative test (Resource as target of `amplifies`): inconsistent, so disjointness and ranges are active.
- `chainsfromttl.py` and `buildgraph_recommend.py` output identical to v1 (relation names aside).
- Counts unchanged: 140 enablers, 50 cases, 217 census records, 100 dependencies, 8,426 co-occurrence pairs.

### Public release
- The anonymised graph (`ontology/jprx_kg_public.ttl`, 55,815 triples) carries, besides the
  layers above, the firm layer (`jprx:Firm`, pseudonyms `Firm_NNN`, linked by `developedBy`,
  `hasManufacturer`, `hasDistributor`), the typed case-to-enabler links (`usesEnabler` and its
  six subproperties, `achieves`, `exposesTo`), materials, deployment and transition codes, and
  the direct `coOccursWith` edges. The three firm links share the super-property `involvesFirm`;
  a manufacturer or distributor is not a subproperty of developer. Each layer is declared in
  `ontology/jprx_ontology.ttl` (636 triples) with a label,
  definition, domain and range. HermiT reports the released graph consistent; the negative test
  above makes it inconsistent.
- Census technology readiness is read from `censusTRL`, the workbook coding. An older text field,
  kept as `censusTRLText`, disagrees with it on 21 records.
- The census screening column 'IC?' (`icStatus`) is no longer used and is not released.
- Example answers: relation names rewritten in place to the v2 names (`dependsOn` -> `requires`,
  `enablesCapability` -> `enables`, `hasPrecondition` -> `presupposes`); no answer was
  regenerated. One correction: example 8 gave census_RXM29-4 technology readiness level 5,
  from the older text field; the workbook coding is 6, and the answer now says 6.

### Amended in place (22 October 2026, before 2.0.0 was cited or registered)
2.0.0 was first published earlier the same day; these corrections replace the files under
`ontology/2.0.0/` rather than starting 2.0.1, because nothing cited that version yet.
- `jprx:involvesFirm` added (CensusRecord -> Firm), the super-property of `developedBy`,
  `hasManufacturer` and `hasDistributor`; manufacturer and distributor are no longer
  subproperties of `developedBy`. The ontology has 636 triples (was 635).
- `icStatus` (census 'IC?') deprecated and left out of the release; the public graph has
  55,815 triples (was 56,015).
- Definition of `adoptionDriver` corrected ("An adoption driver").
- Records with two or more firms credited (as developer, manufacturer or distributor) are
  called multi-firm involvement, not co-development; the count is unchanged (61 records).
  Example 6 is reworded accordingly, including its question, and its sources are labelled
  "multi-firm involvement".
