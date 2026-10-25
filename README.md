# Commercial Pricing & Scenario Model: An Irish Bakery Loaf

**Business question:** An Irish bakery is pricing a large white sliced pan. What price and volume keep it profitable if ingredient costs keep rising? *(Draft: to be confirmed after the first data review.)*

**Data:** CSO table [CPM12, National Average Price](https://data.cso.ie/table/CPM12): monthly average retail prices in Ireland for 76 everyday items, December 2011 to September 2026 (Creative Commons Attribution 4.0). Downloaded 25 October 2026 from the [CSO API](https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/CPM12/CSV/1.0/en).

**Tools:** Python 3.12 (pandas), Excel (Power Query, what-if analysis), PowerPoint

**Status:** In progress. The data is downloaded and inspected; the Excel model is next.

## First look at the data

`py src\inspect_raw.py` on the September 2026 download:

- 13,528 rows: 76 items × 178 months, all priced in euro.
- 1,387 rows (10%) have no price. Eight items are blank for 119 months each (e.g. wine, plaice, 10 kg potatoes), so they were probably added to or dropped from the survey partway through. To check before using any of them.
- Latest prices (September 2026) of the bakery items:

| Item | Price |
|---|---|
| Bread, white sliced pan, large (800g) | €1.67 |
| Bread, brown sliced pan, large (800g) | €1.86 |
| White, self raising flour per 2 kg | €2.57 |
| Brown, wholemeal flour per 2 kg | €3.24 |
| Butter per lb | €4.24 |
| Large eggs per half dozen | €2.47 |
| White granulated sugar per 1 kg | €1.83 |
| Full fat milk per 2 litre | €2.37 |

These are shop prices paid by consumers, not the wholesale prices a bakery pays, so the model will use them as cost *indices* (how fast costs move) alongside stated assumptions for the bakery's own costs.

## Setup

Requires Windows with [Python 3.12](https://www.python.org/downloads/) and [Git](https://git-scm.com/downloads).

```
git clone https://github.com/Ayoola-droid/commercial-pricing-model.git
cd commercial-pricing-model
py -m venv .venv
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

If PowerShell says "running scripts is disabled on this system", run this once and then activate again:

```
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

| Script | What it does |
|---|---|
| `py src\inspect_raw.py` | Prints the shape, date range, items, missing prices and latest bakery prices in the raw CSO file |

## Project structure

- `data/raw/CPM12.csv`: the CSO table as downloaded (never edited)
- `src/inspect_raw.py`: first inspection of the raw file
- `docs/`: README images

*Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/), with one project convention: `data` is used for adding or updating raw data and mapping files.*
