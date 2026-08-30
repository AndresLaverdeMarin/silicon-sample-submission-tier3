# Tier 3 prediction file — the contract

This file is the build contract for `predictions/team_27_T3_primary_v1.csv`.
Every string below is copied from the repository sources. Do not retype them.

Authoritative sources, in this repository:

| Source | What it defines |
|---|---|
| `scripts/lib/submission_spec.R` | the condition strings, the outcome names, the column names |
| `codebook.csv` | the scale and the units of each outcome |
| `scripts/lib/check_lib.R` | the checks that pass or fail the file |
| `README.md` lines 248-271 | the coverage rule and the point-prediction rule |

`make check` runs `scripts/check.R`. It is the only verdict that counts.

---

## 1. File name and columns

- File name: `predictions/team_27_T3_primary_v1.csv`.
- The name must match `^team_27_T3_(primary|secondary-\d+)_v\d+\.csv$`
  (`scripts/lib/check_lib.R:133-137`).
- Header, exactly, in this order: `condition,outcome,ate`
  (`scripts/lib/submission_spec.R:119`, `tier3_cols`).
- The check tests only that the three columns are present
  (`check_lib.R:449`). Extra columns do not fail. Do not add extra columns.

## 2. The 16 intervention strings

These are the only permitted values of `condition`.
Source: `scripts/lib/submission_spec.R:14-31`, the `interventions` vector.

```
Corporate reliance
Social justice
Interview Prof. Maraun
Funding
Oil industry misinformation
Measurement & modeling (1)
Former skeptics
High public trust
Measurement & modeling (2)
Peer-review
Scientist community helpers
Consensus
Portrait Prof. Cherry
Model accuracy
Interview Prof. Sebille
Extreme weather predictions
```

Warnings about these strings:

- `Measurement & modeling (1)` and `Measurement & modeling (2)` contain an
  ampersand and parentheses. Keep them.
- `Peer-review` has a hyphen and a lower-case `r`.
- `Interview Prof. Maraun`, `Portrait Prof. Cherry` and
  `Interview Prof. Sebille` contain a full stop after `Prof`.
- Only the first word is capitalized in every title. Do not title-case them.
- No condition string contains a comma. So no CSV field needs quotation marks.

## 3. `control` must NOT appear

Tier 3 reports effects against control. A `control` row is a FAIL
(`check_lib.R:452-453`). The file has 16 conditions, not 17.

This is a difference from Tier 1. Tier 1 needs all 17 conditions.

## 4. The 13 outcome names

These are the only permitted values of `outcome`.
Source: `scripts/lib/submission_spec.R:71-78`, the `outcomes` vector.

```
trust_multidimensional
trust_post
distrust_post
funding_perceptions
policy_role_mean
inst_trust_mean
belief_post
concern_mean
policy_general
policy_specific_mean
behavior_mean
donation_ams
newsletter_signup
```

The 12 `trust_competence_*`, `trust_integrity_*`, `trust_benevolence_*` and
`trust_openness_*` items are Tier 1 columns. They are NOT Tier 3 outcomes
(`submission_spec.R:69-70`). An item name in the `outcome` column is a FAIL.

`trust_multidimensional` is the primary outcome. It is the mean of the four
trust subscales (`codebook.csv:59`).

## 5. Row set: 208 rows exactly

- 16 interventions x 13 outcomes = 208 data rows, plus 1 header row = 209 lines.
- Each (condition, outcome) pair must be present exactly one time.
- A missing cell is a FAIL. A duplicate cell is a FAIL.
  Source: `.grid_complete()` in `check_lib.R:396-409`, called at
  `check_lib.R:464-465` with `condition = 16, outcome = 13`.
- An empty `ate` is a FAIL. `NA` is not allowed at Tier 3
  (`.no_na_fail`, `check_lib.R:461`). Tier 2 moderator cells allow `NA`.
  Tier 3 does not.

## 6. Row order

Row order is not checked. `.grid_complete()` uses set operations.

Use the order of the shipped example, so a human can read a diff:

1. condition, in the order of the `interventions` vector above (NOT alphabetical);
2. outcome, in alphabetical order inside each condition.

## 7. The `ate` value: units, sign and range

`ate` is the average treatment effect. It is the mean of the intervention group
minus the mean of the control group, on the outcome's own scale.

| Outcome | Scale of the group mean | Unit of `ate` |
|---|---|---|
| the 11 slider outcomes | 0-100 | points on a 0-100 slider |
| `donation_ams` | 0-10 US dollars | dollars |
| `newsletter_signup` | 0-1 proportion | change in the proportion |

The 11 slider outcomes are `trust_multidimensional`, `trust_post`,
`distrust_post`, `funding_perceptions`, `policy_role_mean`, `inst_trust_mean`,
`belief_post`, `concern_mean`, `policy_general`, `policy_specific_mean` and
`behavior_mean` (`submission_spec.R:81-86`, `scale_0_100`).

Rules for the value:

- **`ate` may be negative.** The shipped example has many negative values.
- **`ate` is NOT range-checked.** `check_lib.R:378-381` says so directly:
  "Tier-3 `ate` is an unbounded difference, so it is intentionally NOT
  range-checked". `README.md:267` repeats it.
- Therefore the check cannot catch a units error. A `newsletter_signup` ATE
  written as a percentage-point change (for example `4.2`) instead of a
  proportion change (`0.042`) passes `make check` and scores badly.
  This is the largest silent failure in the file. Check it by hand.
- `donation_ams` has the same risk. Its ATE is in dollars, and the scale is
  only 0-10. An ATE of `5.0` dollars is almost certainly wrong.
- Direction warning: `funding_perceptions` is reverse-coded. The codebook
  defines it as `100 - funding_5`, so a higher value means the person thinks
  the funding is too low (`codebook.csv:53`). A positive ATE means the
  intervention increased support for more funding.
- Direction warning: `distrust_post` is not reversed. A higher value means more
  distrust. A trust-building intervention gives a negative ATE here and a
  positive ATE on `trust_post`.
- No uncertainty interval is submitted. Only point estimates are scored
  (`README.md:269-271`).

## 8. Decimal precision

No precision rule exists in the check. The shipped example uses 3 decimal
places, and drops trailing zeros (`-2.85`, not `-2.850`). Use 3 decimals for
the slider outcomes and `donation_ams`. Use 4 decimals for
`newsletter_signup`, because its whole scale is only 0-1.

Write the number in plain decimal form. Do not write scientific notation
(`1e-04`). R's `read_csv` parses it, but a human reader cannot check it.

## 9. File format

Copied from the shipped example, byte for byte:

- Encoding UTF-8, no byte-order mark.
- Line ending `\n` (LF), not `\r\n`.
- No quotation marks on any field.
- No index column.
- A final newline at the end of the last row.

## 10. The shipped example, for reference

`predictions/example_T3_primary_v1.csv` was deleted after this note was
written. Its exact format was:

```
condition,outcome,ate
Corporate reliance,behavior_mean,-0.519
Corporate reliance,belief_post,-5.583
Corporate reliance,concern_mean,-1.206
Corporate reliance,distrust_post,-2.85
...
Extreme weather predictions,policy_specific_mean,0.548
Extreme weather predictions,trust_multidimensional,-0.054
Extreme weather predictions,trust_post,-3.233
```

209 lines. 8762 bytes.

## 11. Coupling between `metadata.json` and the file name

The check builds the expected file name from `metadata.json`
(`check_lib.R:135`): `sprintf("^%s_T%s_(primary|secondary-\\d+)_v\\d+\\.csv$", team, tier)`.

So `metadata.json` must say `"tier": 3` and `"team_id": "team_27"`. If the tier
is wrong, the file name check fails, AND the wrong tier's structural check runs
on the file. A Tier 3 file tested as a Tier 1 file fails on every column.

`metadata.json` must also declare
`"coverage": {"interventions": 16, "outcomes": 13}`. Any smaller number is a
FAIL (`check_lib.R:92-101`). Coverage counts the 16 interventions, not the 17
conditions (`README.md:248-256`).

## 12. After you write the CSV

Run these two commands, in this order, from the repository root:

```bash
make manifest   # writes the new sha256 into metadata.json
make check      # the verdict
```

`make manifest` finds the file by the pattern `team_27_T3_primary_v\d+.csv`
(`scripts/manifest.R:33-38`). It fails if no file matches.

`make check` FAILS if the sha256 in `metadata.json` is stale. Always run
`make manifest` after any change to the CSV, even a one-character change.

> **WARNING — the file in `predictions/` is a placeholder.** Every `ate` is
> `0`. It exists only to prove that the row set and the metadata are correct.
> `metadata.json` currently holds the sha256 of THIS placeholder
> (`b0d26b45...`). Overwrite the values, keep the same 208 rows, then run
> `make manifest` and `make check` again.

Also run `make zenodo_citation` if you edit `metadata.json`. `.zenodo.json` is
fully derived from `metadata.json`. It does not update by itself.
