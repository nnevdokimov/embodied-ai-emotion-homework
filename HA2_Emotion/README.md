# HA2 Emotion semantic network

The graph contains the twenty approved Emotion concepts and five supporting WordNet categories. Original terms, noun senses and definitions match the revised HA0. Team members and roles are listed in the notebook.

## Reproduce

Use Python 3.12 and install `requirements.txt`. Run `HA2_network.ipynb` from this folder. All inputs are bundled; no data download is needed. The notebook writes `nodes.csv`, `network.png`, `perturbation.csv` and the graph variants and metrics in `results/`.

`edges.csv` is the baseline edge list. `data/concepts.csv` fixes all 25 nodes, including disconnected nodes. `data/perturbations.csv` fixes the three additions and three subsequent removals. The 300-word interpretation is in `interpretation.md`.

## Relations and sources

IS-A is stored parent → child. Every such edge has a verified WordNet 3.0 ancestor path in `evidence`, with its number of original hypernym steps in `wordnet_hops`. Nodes omitted from this compact inventory are collapsed, so displayed depth counts compact edges rather than original WordNet steps. The bundled `data/wordnet.zip` includes the noun data, license and citation. Source: https://wordnet.princeton.edu/.

The other two relation types are ASSOCIATED-WITH (illustrative co-occurrence, without causality) and METAPHORICAL-SOURCE-FOR (literal source → emotional target). They are authored examples labelled `provenance=seed`, `annotation_origin=generated`; they are not corpus observations or WordNet relations. Only IS-A enters specificity.

## Scores and perturbation

All nodes are nouns. For root-reachable nodes, S_depth = shortest depth / maximum shortest depth. The multiple-parent range uses shortest and longest root paths with that same denominator. S_breadth = 1 − log(1 + descendant count) / log(1 + maximum descendant count). These follow lecture slides 9–10 and the instructor notebook. The alternative expression also present on slide 28 is not used. Disconnected nodes remain in all exports with NA specificity.

The baseline deliberately omits symptom → scar. Additions restore it, add the broader parent emotion → panic, and add anxiety → freeze as an association. The second parent is a valid ancestor shortcut, not a claim that WordNet gives panic two immediate hypernyms. Removals delete fear → panic, feeling → emotion, and the added emotion → panic edge. No nodes change across versions.

Scores are normalized within each graph. `perturbation.csv` also reports changes with the original denominators fixed, separating local structural changes from rescaling. Changes greater than 0.1 and lost/gained root connectivity are reported separately. A deterministic hierarchical layout follows the instructor notebook's fallback; it uses no force-directed placement or random seed.

## Cross-assignment checks

The comparison against HA1 reads the full WordNet depth for the same twenty selected noun senses from data/ha1_depths.csv. Weighted paths recover WordNet steps along the recorded evidence chains. Separate tables report the effect of each removal starting from the added graph and a coverage test adding every immediate WordNet child of flood. All drawings retain baseline coordinates.
