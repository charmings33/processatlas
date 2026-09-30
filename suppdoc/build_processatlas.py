"""
build_processatlas.py — build the anonymised ProcessAtlas.ttl from the cleaned
supplementary workbook only.

Source : Ng_et_al_From_Kit_of_Parts_to_Kit_of_Processes_census___polar_cases_coding.xlsx
Sheets : '140'          -> 50 polar cases: descriptors + binary coding against 140 enablers
         'JPR'          -> 217 census records: descriptors only
         'Dependencies' -> 100 directed, cited enabler->enabler edges

No company names, robot names, websites, sites, projects or free-text
descriptions are read or emitted. Everything in the output resolves to a
binary flag, a coded label, an enabler id or a literature citation.

Schema follows jprx_kg.ttl so existing SPARQL continues to run. The
co-occurrence layer is recomputed from the polar coding rather than read from a
matrix sheet, which is equivalent and keeps the release self-contained.
"""
import openpyxl, rdflib
from rdflib import Literal, RDF, RDFS, OWL, Namespace, XSD

SRC = "Ng_et_al_From_Kit_of_Parts_to_Kit_of_Processes_census___polar_cases_coding.xlsx"
OUT = "ProcessAtlas.ttl"
J = Namespace("http://jprx.example.org/ontology#")

CAT = {"AC": "Actor", "RE": "Resource", "CO": "Condition", "AT": "Attribute",
       "PR": "Process", "AR": "Artefact", "VA": "Value", "RI": "Risk"}
CAT_COLOUR = {"Actor": "#e5a027", "Resource": "#5eb5e5", "Condition": "#049d74",
              "Attribute": "#eee450", "Process": "#0e74b1", "Artefact": "#d36027",
              "Value": "#cb79a7", "Risk": "#787878"}
REL = {"enablesCapability", "dependsOn", "hasPrecondition",
       "amplifies", "mitigates", "constrains"}
SUBTYPE = {"CW_": ("Concrete work", "hasConcreteworkSubtype"),
           "SW_": ("Steelwork", "hasSteelworkSubtype")}


def on(v):
    return v in (1, "1", 1.0, True)


def cat_of(eid):
    for p in ("AC", "RE", "CO", "AT", "PR", "AR", "VA", "RI"):
        if eid.startswith(p) and eid[len(p):].isdigit():
            return CAT[p]
    raise SystemExit(f"unrecognised enabler id {eid!r}")


wb = openpyxl.load_workbook(SRC, data_only=True)
g = rdflib.Graph()
g.bind("jprx", J); g.bind("owl", OWL); g.bind("rdfs", RDFS)

# ---- ontology declarations ----
for c in ["Process", "CensusRecord", "Enabler", "Dependency", "CoOccurrence"]:
    g.add((J[c], RDF.type, OWL.Class))
for p in ["activates", "dependencySource", "dependencyTarget", "coEnablerA", "coEnablerB",
          "enablesCapability", "dependsOn", "hasPrecondition",
          "amplifies", "mitigates", "constrains"]:
    g.add((J[p], RDF.type, OWL.ObjectProperty))
for p in ["hasActivationTotal", "hasActivationFrequency", "hasCategory", "hasCategoryColour",
          "hasEnablerId", "hasProcessId", "hasCensusId", "hasLifecyclePhase", "hasMaterial",
          "hasStakeholderTier", "hasBuildingSystem", "hasTask", "hasConcreteworkSubtype",
          "hasSteelworkSubtype", "hasTRL", "censusTRL", "hasAdoptionDriver", "adoptionDriver",
          "isOffsite", "isOnsite", "isOnsiteOutdoor", "isOnsiteIndoor", "isMobileRobot",
          "isPhysicalRobot", "isDigitalRobot", "dependencyRelation", "evidenceLevel",
          "dependencyNote", "citation", "coOccurrenceCount"]:
    g.add((J[p], RDF.type, OWL.DatatypeProperty))
g.add((J.hasConcreteworkSubtype, RDFS.comment,
       Literal("Refines the Concrete work hasTask; not a standalone task")))
g.add((J.hasSteelworkSubtype, RDFS.comment,
       Literal("Refines the Steelwork hasTask; not a standalone task")))

# ---- enablers, from the header rows of sheet '140' ----
ms = wb["140"]
ecol = {}          # enabler id -> column index
for c in range(1, ms.max_column + 1):
    eid = ms.cell(1, c).value
    if isinstance(eid, str) and eid.strip() and eid.strip()[:2] in CAT:
        eid = eid.strip()
        if eid[2:].isdigit():
            ecol[eid] = c
enab = list(ecol)
for e in enab:
    lab = str(ms.cell(2, ecol[e]).value).strip()
    cat = cat_of(e)
    u = J[e]
    g.add((u, RDF.type, J.Enabler))
    g.add((u, RDFS.label, Literal(lab, lang="en")))
    g.add((u, J.hasEnablerId, Literal(e)))
    g.add((u, J.hasCategory, Literal(cat)))
    g.add((u, J.hasCategoryColour, Literal(CAT_COLOUR[cat])))

# ---- descriptor column groups, resolved by the row-1 / row-2 header labels ----
def groups(ws, hdr_row=2, band_row=1):
    """Return {band label: {column label: column index}} using the merged band in row 1."""
    out, band = {}, None
    for c in range(1, ws.max_column + 1):
        b = ws.cell(band_row, c).value
        if isinstance(b, str) and b.strip():
            if b.strip()[:2] in CAT and b.strip()[2:].isdigit():
                band = None
                continue
            band = b.strip()
        h = ws.cell(hdr_row, c).value
        if band and isinstance(h, str) and h.strip():
            out.setdefault(band, {})[h.strip()] = c
    return out


DEPLOY = {"offsite": "isOffsite", "onsite": "isOnsite", "Onsite Outdoor": "isOnsiteOutdoor",
          "Onsite Indoor": "isOnsiteIndoor", "Mobile Robot": "isMobileRobot",
          "Offsite": "isOffsite", "Onsite": "isOnsite",
          "Physical Robot": "isPhysicalRobot", "Digital Robot": "isDigitalRobot"}
STAKE = {"GC", "Trade", "R. Manufacturer", "Robot Manufacturer", "House Maker",
         "Distributor", "Others"}


def emit_record(u, ws, row, grp, stake_cols, trl_pred, driver_pred):
    """Emit the descriptor triples shared by polar cases and census records."""
    for band, cols in grp.items():
        for h, c in cols.items():
            v = ws.cell(row, c).value
            if band == "Deployment":
                pred = DEPLOY.get(h)
                if pred is None:
                    continue
                if pred in ("isOffsite", "isOnsite"):
                    g.add((u, J[pred], Literal(bool(on(v)))))
                elif on(v):
                    g.add((u, J[pred], Literal(True)))
            elif not on(v):
                continue
            elif band == "Material":
                g.add((u, J.hasMaterial, Literal(h)))
            elif band == "Lifecycle Phase":
                g.add((u, J.hasLifecyclePhase, Literal(h)))
            elif band == "Building system":
                g.add((u, J.hasBuildingSystem, Literal(h)))
            elif band.startswith("Adoption Driver"):
                g.add((u, J[driver_pred], Literal(h[3:])))
            elif band == "Construction Task":
                pref = next((p for p in SUBTYPE if h.startswith(p)), None)
                if pref is None:
                    g.add((u, J.hasTask, Literal(h)))
                else:
                    parent, prop = SUBTYPE[pref]
                    pc = cols.get(parent)
                    if pc is not None and on(ws.cell(row, pc).value):
                        g.add((u, J[prop], Literal(h[len(pref):])))
                    else:
                        warns.append(f"{u}: {h}=1 but parent {parent}!=1 -> skipped")
    # stakeholder tiers
    for h, c in stake_cols.items():
        v = ws.cell(row, c).value
        if isinstance(v, (int, float)) and v > 0:
            g.add((u, J.hasStakeholderTier, Literal(h)))
    # TRL, one level per record
    trl = [h for h, c in grp.get("Technology Readiness Level (TRL)", {}).items()
           if on(ws.cell(row, c).value)]
    if len(trl) == 1:
        g.add((u, J[trl_pred], Literal(int(trl[0][3:]), datatype=XSD.integer)))
    elif len(trl) > 1:
        warns.append(f"{u}: multiple TRL flags {trl} -> none emitted")


warns = []

# ---- polar cases ----
g140 = groups(ms)
stake140 = {h: c for h in STAKE for c in [None]
            if False}  # placeholder, filled below
stake140 = {}
for c in range(1, ms.max_column + 1):
    h = ms.cell(2, c).value
    if isinstance(h, str) and h.strip() in STAKE and ms.cell(1, c).value is None:
        stake140[h.strip()] = c

npolar = 0
edges = 0
coding = {}
for r in range(3, ms.max_row + 1):
    pid = ms.cell(r, 1).value
    if not (isinstance(pid, str) and pid.startswith("RP")):
        continue
    npolar += 1
    u = J[pid]
    g.add((u, RDF.type, J.Process))
    g.add((u, J.hasProcessId, Literal(pid)))
    acts = [e for e in enab if on(ms.cell(r, ecol[e]).value)]
    coding[pid] = set(acts)
    edges += len(acts)
    for e in acts:
        g.add((u, J.activates, J[e]))
    g.add((u, J.hasActivationTotal, Literal(len(acts))))
    emit_record(u, ms, r, g140, stake140, "hasTRL", "hasAdoptionDriver")

# ---- census records ----
js = wb["JPR"]
gJPR = groups(js)
stakeJPR = {}
for c in range(1, js.max_column + 1):
    h = js.cell(2, c).value
    if isinstance(h, str) and h.strip() in STAKE:
        stakeJPR[h.strip()] = c
ncensus = 0
for r in range(3, js.max_row + 1):
    rid = js.cell(r, 1).value
    if not isinstance(rid, str) or not rid.strip():
        continue
    rid = rid.strip()
    ncensus += 1
    u = J[f"census_{rid}"]
    g.add((u, RDF.type, J.CensusRecord))
    g.add((u, J.hasCensusId, Literal(rid)))
    emit_record(u, js, r, gJPR, stakeJPR, "censusTRL", "adoptionDriver")

# ---- dependencies ----
enab_set = set(enab)
ndep = 0
for row in list(wb["Dependencies"].iter_rows(values_only=True))[1:]:
    if not row or not row[0]:
        continue
    did, src, _, _, rel, tgt, _, _, ev, note, cit = row[:11]
    if src not in enab_set or tgt not in enab_set:
        warns.append(f"{did}: bad enabler ref {src}/{tgt}")
        continue
    ndep += 1
    d = J[did]
    g.add((d, RDF.type, J.Dependency))
    g.add((d, J.dependencySource, J[src]))
    g.add((d, J.dependencyTarget, J[tgt]))
    g.add((d, J.dependencyRelation, Literal(rel)))
    if ev:
        g.add((d, J.evidenceLevel, Literal(ev)))
    if note:
        g.add((d, J.dependencyNote, Literal(note)))
    if cit:
        g.add((d, J.citation, Literal(cit)))
    if rel in REL:
        g.add((J[src], J[rel], J[tgt]))
    else:
        warns.append(f"{did}: unknown relation {rel!r} -> reified only")

# ---- activation frequency + weighted co-occurrence, recomputed from the coding ----
freq = {e: sum(1 for s in coding.values() if e in s) for e in enab}
for e in enab:
    g.add((J[e], J.hasActivationFrequency, Literal(freq[e])))
ncooc = 0
for i, a in enumerate(enab):
    for b in enab[i + 1:]:
        c = sum(1 for s in coding.values() if a in s and b in s)
        if c <= 0:
            continue
        n = J[f"cooc_{a}_{b}"]
        g.add((n, RDF.type, J.CoOccurrence))
        g.add((n, J.coEnablerA, J[a]))
        g.add((n, J.coEnablerB, J[b]))
        g.add((n, J.coOccurrenceCount, Literal(c)))
        ncooc += 1

g.serialize(destination=OUT, format="turtle")
print(f"WROTE {OUT}")
print(f"enablers={len(enab)}  polar_cases={npolar}  census_records={ncensus}")
print(f"activation_edges={edges}  dependencies={ndep}  co-occurrence_edges={ncooc}")
print(f"total_triples={len(g)}")
for w in warns:
    print("WARN", w)
