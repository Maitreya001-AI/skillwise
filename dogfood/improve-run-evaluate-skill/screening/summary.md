# Screening (non-authoritative, burned r2 set, 1 non-blind pass each)

| candidate | mechanism | r2 accuracy | 02 fixed | 06 fixed | 10 recall | 12 |
|---|---|---|---|---|---|---|
| c1 | default-deny rule gate (2 emit conditions) | **10/12** | yes | yes | yes | yes |
| c2 | three-question protocol table | 9/12 | yes | yes | yes | wrong defect |
| c3 | pricing + contrast pair | **10/12** | yes | yes | yes | yes |

**Pick: c1.** Tie with c3 on accuracy, but c3's contrast pair near-verbatim describes r2 seeds
(skill-02/08/10) — its screen score is inflated by construction and may not carry to a fresh set.
c1's rule cites no specific seed. Screening is a selection heuristic only; the gate decides KEEP.
Residual misses (r2 skill-03 nogap costume, skill-05 buried underfill) are a different defect —
out of scope for this edit (one defect per edit).
