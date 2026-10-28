# Commercial Pricing & Scenario Model: An Irish Bakery Loaf

**Business question:** Shop prices for ingredients rose 26–57% in five years, but they add only €0.09 to the cost of a loaf. How much can the bakery's wages, energy and other costs rise before its margin falls below 2021 levels, and what loaf price would protect it?

**Data:**
- CSO table [CPM12, National Average Price](https://data.cso.ie/table/CPM12): monthly average retail prices for 76 everyday items, December 2011 to September 2026. Downloaded 25 October 2026.
- CSO table [CPM24, Consumer Price Index detailed sub-indices](https://data.cso.ie/table/CPM24): monthly price indices (December 2023 = 100), November 1996 to September 2026. Downloaded 28 October 2026.
- National minimum wage: €10.20 an hour from 1 January 2021 ([S.I. 427/2020](https://www.irishstatutebook.ie/2020/en/si/0427.html)) and €14.15 from 1 January 2026 ([WageIndicator](https://wageindicator.org/salary/minimum-wage/minimum-wages-news/2026/minimum-wage-increased-in-ireland-from-01-january-2026-january-01-2026)).

CSO data is published under Creative Commons Attribution 4.0.

**Tools:** Python 3.12 (pandas), Excel (Power Query, what-if analysis), PowerPoint

**Status:** In progress. The CSO data is loaded with Power Query and the Inputs tab holds the bakery's assumptions; the Calculations tab compares September 2026 with September 2021 using real wage and price rises, and Goal Seek finds the price that restores the margin. A scenario table and the summary deck are next.

## Findings so far

1. **Ingredients rose fast in percentage terms but little in euros.** Between September 2021 and September 2026, CSO shop prices rose 26% for flour, 42% for butter, 40% for milk and 57% for sugar. In the bakery's recipe, that adds **€0.09** to each loaf (ingredients €0.328 → €0.421).
2. **The loaf's price rose more in euros.** The shelf price rose 22.6% (€1.364 → €1.672), so the bakery's own price rose **€0.23** a loaf after the retailer's 25% margin.
3. **On ingredients alone, there is no squeeze.** With other costs held flat, weekly operating profit is €3,660 today against €906 in 2021, and the operating margin is 14.6% against 4.4%.
4. **The squeeze is real, and it comes from wages and energy.** Since 2021 the minimum wage rose **38.7%**, the CPI for electricity **49.9%**, fuels **33.5%** and all items **24.0%**. With these rises, the bakery's operating margin is **14.6%** today against **19.1%** in 2021, **4.5 percentage points lower** (weekly profit €3,660 against €3,917).
5. **A 9-cent rise protects the margin.** Goal Seek finds that a shelf price **5.6% higher (€1.77 instead of €1.67)** restores the 2021 operating margin. Holding the price instead would need about **23,900 loaves a week, 19.5% more volume**. (Goal Seek results for the September 2026 data, run 28 October 2026.)

### Why the business question changed

The first version of the model held non-ingredient costs flat. On that basis there was no squeeze: profit was €3,660 a week today against €906 in 2021. Adding real wage and price rises reversed the result, which is why the README records both.


The first question assumed that fast-rising ingredient prices were squeezing the bakery's margin. The Calculations tab tested that premise and the data disagreed: ingredients are about a third of the bakery's price, so a large percentage rise on a small cost added less than the loaf's own price rise. The question now asks about the costs that can create a squeeze.

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

## Method

**Series used.** Five of the 76 CSO items: the product and the main ingredients of a white sliced pan.

| CSO item | Column in the model | Why |
|---|---|---|
| Bread, white sliced pan, large (800g) | Loaf 800g | The product being priced |
| White, self raising flour per 2 kg | Flour 2kg | Main ingredient. Bakeries use strong bread flour, which the CSO does not track, so this is a proxy |
| Butter per lb | Butter lb | Stands in for the fat in the recipe |
| White granulated sugar per 1 kg | Sugar 1kg | Feeds the yeast |
| Full fat milk per 2 litre | Milk 2L | Many sliced pans contain milk |

Eggs are left out: a basic sliced pan has none.

**Power Query** (`model/bakery_pricing_model.xlsx`, query `CSO_Prices`) reads `data/raw/CPM12.csv` and:

1. keeps the month code, item and price columns;
2. drops December 2011 (see data-quality log);
3. keeps the five items above;
4. turns the month code (e.g. `202609`) into a date (1 September 2026);
5. pivots to one row per month and one column per item, with short names that keep the units.

Result: 177 months (January 2012 to September 2026) × 5 prices, no blanks. The first and last rows were checked against the same steps in pandas and match exactly.

**Inputs tab.** Every assumption about the fictional bakery sits on one sheet: the recipe per loaf, what the bakery pays for each ingredient, other costs per loaf, the retailer's margin, VAT, weekly volume and fixed costs. Blue text marks inputs; black text marks formulas. Each input has a unit and a source note. The ingredient prices and other costs are illustrative assumptions, not real quotes.

Two inputs are formulas: the latest CSO month (`=MAX(CSO_Prices[Month])`) and the shelf price for that month (`XLOOKUP`), so both update when the query is refreshed.

**VAT check.** Bread is zero-rated in Ireland only if its fats and sugars are no more than 12% of the flour's weight; otherwise the reduced rate applies ([Revenue](https://www.revenue.ie/en/tax-professionals/tdm/value-added-tax/part03-taxable-transactions-goods-ica-services/Goods/goods-bread.pdf)). The Inputs tab tests the recipe against that limit: 15 g butter + 10 g sugar = 5.2% of 480 g flour, so the loaf is zero-rated.

**Calculations tab.** Compares the latest CSO month with the same month five years earlier (`=EDATE(latest, -60)`). The bakery's ingredient costs in the earlier month are today's costs scaled by the change in CSO shop prices, e.g. 2021 flour cost = today's flour cost × (2021 flour price ÷ today's flour price). Non-ingredient costs in the earlier month are today's divided by (1 + an assumed rise), set on the Inputs tab; 0% means "unchanged". For each month it calculates cost per loaf, the bakery's price after the retailer's margin and VAT, contribution per loaf and margin, weekly profit, operating margin and break-even volume. Changes between two percentages are shown in percentage points.

**Cost rises.** Each non-ingredient cost line in 2021 is today's cost divided by (1 + its own rise), using the closest public measure:

| Cost | Measure | Rise, Sep 2021 to Sep 2026 |
|---|---|---|
| Direct labour | National minimum wage | 38.7% |
| Energy (baking) | CPI electricity (CPM24, CP0451) | 49.9% |
| Distribution | CPI fuels and lubricants (CPM24, CP0722) | 33.5% |
| Packaging and fixed costs | CPI all items (CPM24, CP00) | 24.0% |

Caveats: consumer electricity prices differ from business tariffs, and some bakery staff earn more than the minimum wage. The CPI rises are looked up from the `CPI_Index` query, so they update when the data is refreshed; the two minimum wage rates are typed in and must be updated when the rate changes.

**Power Query, CPI.** The `CPI_Index` query reads `data/raw/CPM24.csv`, keeps the Consumer Price Index statistic (the file also holds 1-month and 12-month % changes for every row), keeps January 2012 onwards and the three series above, turns month codes into dates and pivots to one row per month. Result: 177 months × 3 indices; all 531 values were checked against the CSV and match.

**Goal Seek.** On the Inputs tab, `B41` is the gap between today's operating margin and the comparison month's. Goal Seek sets it to 0 by changing the price change in `B40` (or the weekly volume in `B28`). Goal Seek writes a fixed number, so it must be re-run when the data changes; the inputs are left at 0% and 20,000 loaves.

## Data quality log

| Action | Issue | Rows |
|---|---|---|
| Rejected | December 2011: the first month of the table has no price for any of the five items | 5 |
| Not used | 71 CSO items outside the bakery basket, including 8 items with 119 months blank | 12,638 |
| Not used | CPM24: percentage-change statistics, months before 2012 and sub-indices other than the three used | 369,957 |

## Getting the data

`data/raw/CPM12.csv` is in the repo. `data/raw/CPM24.csv` (54 MB) is not, to keep the repo small. Download it from the CSO and save it under that name:

`https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/CPM24/CSV/1.0/en`

The results in this README use the version downloaded on 28 October 2026 (data to September 2026).

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

The Power Queries read the CSVs from `C:\Projects\commercial-pricing-model\data\raw\`. If you clone the repo somewhere else, open the workbook and change the path in **Data → Get Data → Data Source Settings**, then **Refresh All**.

## Project structure

- `data/raw/CPM12.csv`: CSO average prices as downloaded (never edited)
- `data/raw/CPM24.csv`: CSO price indices as downloaded (not committed; see Getting the data)
- `model/bakery_pricing_model.xlsx`: the Excel model
  - `Inputs`: the bakery's assumptions, cost rises, the pricing decision and the VAT check
  - `Calculations`: cost, margin and profit per loaf, latest month vs five years earlier
  - `CSO_Prices`: the five CSO price series, loaded by Power Query
  - `CPI_Index`: three CSO price indices, loaded by Power Query
- `src/inspect_raw.py`: first inspection of the raw file
- `docs/`: README images

*Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/), with one project convention: `data` is used for adding or updating raw data and mapping files.*
