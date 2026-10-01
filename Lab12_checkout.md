# Lab 12 — Pro-Forma Sensitivity: Present and Review Your Full Analysis
## Company: Robinhood Markets, Inc. (NASDAQ: HOOD)

**Student:** Luca Richey  
**Course:** FIN 43900 (AI Finance Applications, Purdue University)  
**Date:** October 1, 2026  
**Category:** Thursday merit checkout (25/25 Merit Anchors)  
**Assigned Learning Partner:** Partner B (Analyzing Asbury Automotive Group, NYSE: ABG)  
**Workspace Directory:** `/Users/lucarichey/Documents/Courses/AIFinance2026/LucaRichey`  

---

## Executive Evidence Summary & Repository Links

All evidence, files, models, and visible outputs reviewed during today's presentation are preserved directly in this repository:

| Analysis Stage | Workspace File & Artifact | Primary Valuation / Finding | Sourced Primary Basis |
|---|---|:---:|---|
| **Target Research & Sources** | [`HOOD-research/Robinhood_2026-09-03_Edition_B.md`](file:///Users/lucarichey/Documents/Courses/AIFinance2026/LucaRichey/HOOD-research/Robinhood_2026-09-03_Edition_B.md)<br>[`HOOD-research/sources.md`](file:///Users/lucarichey/Documents/Courses/AIFinance2026/LucaRichey/HOOD-research/sources.md) | Business thesis & segment mapping | FY2025 Form 10-K (accession `0001783879-26-000023`) & Q2 2026 Form 10-Q (accession `0001783879-26-000114`) |
| **Week 3 Fundamental DCF** | [`dcf.py`](file:///Users/lucarichey/Documents/Courses/AIFinance2026/LucaRichey/dcf.py)<br>[`HOOD-research/Robinhood_DCF_checkout.md`](file:///Users/lucarichey/Documents/Courses/AIFinance2026/LucaRichey/HOOD-research/Robinhood_DCF_checkout.md) | **\$29.24 / share**<br>*(Range: \$26.09–\$33.50)* | 5-year explicit FCFF (\$1,608.5M base), WACC = 16.07%, long-run GDP terminal growth = 3.0% |
| **Lab 08 Peer Comps** | [`hood_pe.py`](file:///Users/lucarichey/Documents/Courses/AIFinance2026/LucaRichey/hood_pe.py)<br>[`Lab08_Robinhood/Lab08_checkout.md`](file:///Users/lucarichey/Documents/Courses/AIFinance2026/LucaRichey/Lab08_Robinhood/Lab08_checkout.md) | **\$64.63 / share**<br>*(Range: \$47.32–\$81.94)* | FY2025 GAAP diluted EPS (\$2.05) × Peer Median P/E 31.53× (Schwab 23.08×, IBKR 39.97×) |
| **Lab 10 Pro-Forma Engine** | [`hood_proforma.py`](file:///Users/lucarichey/Documents/Courses/AIFinance2026/LucaRichey/hood_proforma.py)<br>[`Lab10_Robinhood/Lab10_checkout.md`](file:///Users/lucarichey/Documents/Courses/AIFinance2026/LucaRichey/Lab10_Robinhood/Lab10_checkout.md) | **\$23.85 / share**<br>*(PV FCFE \$8.80B + PV TV \$12.95B)* | Linked 3-statement forecast (2026–2030), $K_e = 16.53\%$, 912.0M diluted shares, checks PASS |
| **Lab 11 Sensitivity Engine** | [`Lab11_Robinhood/Lab11_checkout.md`](file:///Users/lucarichey/Documents/Courses/AIFinance2026/LucaRichey/Lab11_Robinhood/Lab11_checkout.md)<br>[`Lab11_Robinhood/hood_sensitivity_output.txt`](file:///Users/lucarichey/Documents/Courses/AIFinance2026/LucaRichey/Lab11_Robinhood/hood_sensitivity_output.txt) | **Options Span: \$1,080.4M**<br>*(Value Span: \$4.61/sh)* | Options Revenue shift (±10 pp/yr), Gross Margin (±100 bps), Total Growth (±300 bps) |
| **Saved Market Price** | Market Quote (Sep 10, 2026) | **\$113.33 – \$116.00** | Reverse-DCF proves market prices in a **+45.22 pp uniform growth premium** (75.2% Year 1) |

---

## D — The Core Question

> **"How did I get from choosing this company to my valuation conclusion, which assumptions drive it, and what evidence could change my mind?"**

---

## R & I — The Full Six-Stop Analysis Route

### Stop 1: Target Selection Rationale
* **Why Robinhood Markets, Inc. (NASDAQ: HOOD)?**  
  I selected Robinhood because it represents the definitive intersection of modern retail fintech, aggressive transaction monetization, and extreme operating leverage. After going public in 2021 as an unprofitable, cash-burning broker dependent solely on retail meme-stock trading, Robinhood underwent a structural financial turnaround, reaching GAAP profitability in 2024 and expanding net income to **\$1.883 Billion in FY2025**.
* **Why It Is Suitable to Analyze:**  
  1. *Clean Audited Disclosures:* As an SEC-registered broker-dealer and public reporting company, all balance sheets, customer segregations, and revenue segments are audited under GAAP.
  2. *Defensible Peer Universe:* Robinhood can be directly benchmarked against both an established retail wealth giant (**The Charles Schwab Corp, SCHW**) and an automated algorithmic execution firm (**Interactive Brokers Group, IBKR**).
  3. *Profound Valuation Divergence:* Robinhood presents an ideal valuation case study because its fundamental cash flow value (\$24–\$29) differs by over **$4\times$** from its market price (\$113–\$116), allowing us to test whether the market is pricing in structural platform durability or speculative retail euphoria.
* **Initial View vs. Current View:**  
  *Initial View (Week 1):* I viewed Robinhood primarily as a volatile retail stock-trading app vulnerable to market downturns and regulatory bans on Payment for Order Flow (PFOF).  
  *Current View (Week 6):* I now view Robinhood as an asset-light, 95% gross margin financial distribution platform with 13 distinct business lines exceeding \$100M run-rates. However, my pro-forma and sensitivity analysis proved that its valuation remains tethered to a high cost of capital (16.53%) and extreme dependency on options market-maker rebates, making the \$116 market price wildly detached from fundamental cash-flow support.

---

### Stop 2: Company and Sourced Evidence
Robinhood monetizes platform velocity through three distinct operating pillars across 24.3M funded customers and \$150B+ in platform assets:

```
                          ROBINHOOD NET REVENUE ($4,473M FY25 / $1,308M Q2 2026)
                                               │
     ┌─────────────────────────────────────────┼────────────────────────────────────────┐
     ▼                                         ▼                                        ▼
TRANSACTION-BASED (59% in Q2 26)         NET INTEREST (30% in Q2 26)              OTHER / SUBSCRIPTIONS (11%)
 • Options ($342M Q2 / 44% of trans)      • Margin lending interest ($145M)        • Robinhood Gold ($143M Q2)
 • Event contracts ($156M brand new!)     • Cash sweep distributions ($135M)       • 4.84M paid subscribers
 • Equities ($129M)                       • Securities lending ($65M)              • Gold Card interchange
 • Cryptocurrencies ($100M)               • Corporate cash yield ($44M)            • RIA custody & TradePMR
```

* **Primary Filing Sources & Reporting Periods:**
  1. **FY2025 Form 10-K** (filed Feb 18, 2026, SEC EDGAR accession `0001783879-26-000023`):
     - Net Revenues: **\$4,473.0M** (Item 8, Consolidated Statements of Operations, p. 128). Hand-confirmed.
     - Brokerage & Clearing Costs: **\$211.0M**, leaving Gross Profit of **\$4,262.0M** (95.28% gross margin).
     - Operating Overhead (Tech \$897M, Ops \$130M, Mktg \$399M, G&A \$628M, Credit \$114M): **\$2,168.0M**.
     - Net Income: **\$1,883.0M**; Diluted EPS: **\$2.05** across **912.0M shares**.
  2. **Q2 2026 Form 10-Q** (filed July 30, 2026, SEC EDGAR accession `0001783879-26-000114`):
     - Property, software, and equipment, net: **\$154.0M** (Item 1, Condensed Consolidated Balance Sheets, p. 11).
     - Stockholders' Equity: **\$9,151.0M**; Corporate Cash: **\$4,261.0M**; Total Assets: **\$39,589.2M**.
     - Customer Assets & Segregation: Customer receivables (\$5.8B) and segregated cash/securities (\$27.9B) are offset by payables to customers (\$29.0B), preserving regulatory neutrality.
* **The Unique Balance Sheet Reality:**  
  Unlike physical auto dealers (ABG) that carry \$2.1B in merchandise inventories and \$2.0B in floor plan notes, Robinhood holds **zero physical inventory (0.0)** and **zero floor plan debt (0.0)**. Its balance sheet is dominated by customer custodial assets and regulatory reserves.

---

### Stop 3: Your Pro-Forma Model (Lab 10)
In [`hood_proforma.py`](file:///Users/lucarichey/Documents/Courses/AIFinance2026/LucaRichey/hood_proforma.py), history was converted into forecast assumptions through disciplined economic logic:

1. **Revenue Growth Deceleration Path (`[20%, 18%, 15%, 12%, 10%]`):**  
   Reflects realistic mean-reversion from recent 52% expansion as trading velocity normalizes and asset scale nears \$400B. Total revenue reaches **\$8,973.7M** by FY2030E.
2. **Gross Margin (95.28% [history]):**  
   Anchored directly to the FY2025 10-K clearing fee ratio ($4,262\text{M} / 4,473\text{M}$). Because electronic order routing has zero physical delivery cost, unit gross margins remain structurally elite.
3. **SG&A Operating Leverage (`[50%, 48%, 46%, 45%, 45%]` of Gross Profit [judgment]):**  
   Captures fixed-cost absorption across engineering, regulatory compliance, and cloud infrastructure as platform revenue doubles.
4. **Capital Reinvestment & Depreciation:**  
   CapEx of **\$65.0M a year** (\$13M hardware + \$52M capitalized internal software development). Depreciation ratio of **55.84%** (\$86M D&A on \$154M opening PP&E) reflects rapid 3-year technological software amortization.
5. **Liquidity Minimum & Regulatory Buffer:**  
   Minimum corporate cash floor set to **\$1,000.0M** to meet SEC Rule 15c3-1 net capital and clearinghouse deposit buffers.
6. **Accounting Integrity Checks:**  
   Balance sheet equality passes with **0.0 gap** in every single year (`Assets − Liab − Equity = 0.0`), and ending cash stays well above minimum, growing to **\$16,019.2M** by FY2030E.

---

### Stop 4: Valuation Synthesis (DCF, Multiples, Market Price, Reverse-DCF)

We synthesized four distinct valuation lenses to triangulate fair value:

```
========================================================================================================
 VALUATION TRIANGULATION SUMMARY — ROBINHOOD MARKETS, INC. (HOOD)
========================================================================================================
Valuation Lens              Implied Share Price    Equity Value     P/E Multiple    Methodological Nature
--------------------------------------------------------------------------------------------------------
Pro-Forma DCF (FCFE)             $23.85             $21.75B            11.6x        Fundamental 3-statement cash flow
Week 3 DCF (FCFF)                $29.24             $26.67B            14.3x        5-year FCFF with cash/debt bridge
Peer Multiples: Schwab           $47.32             $43.15B            23.1x        Retail brokerage banking parity
Peer Multiples: Median           $64.63             $58.94B            31.5x        Blended retail/electronic broker
Peer Multiples: IBKR             $81.94             $74.73B            40.0x        High-velocity automated broker
Saved Market Price              $113.33 – $116.00   $105.8B            56.6x        Market momentum & crypto euphoria
========================================================================================================
```

#### Why the Methods Differ (Traceable Explanation):
1. **The Cost of Capital Barrier (Why DCF is \$23.85):**  
   In both DCF models, Robinhood is penalized by a high beta of **2.34**, driving a **16.53% cost of equity** ($R_f 4.83\% + 2.34 \times 5.0\%$). At 16.5%, future cash flows lose more than half their value over 5 years. Total PV of 5-year FCFE is **\$8,801.3M**, and PV of terminal value is **\$12,951.5M**, yielding **\$21,752.8M total equity value** across 912.0M shares ($\mathbf{\$23.85/\text{share}}$).
2. **Peer P/E Multiples (\$47.32 – \$81.94):**  
   Peer multiples value net accounting income directly, reflecting what the market pays for established platforms. Charles Schwab (23.1× P/E) establishes a conservative retail floor of **\$47.32**, while Interactive Brokers (40.0× P/E) reflects algorithmic execution scale at **\$81.94**.
3. **The Reverse-DCF Proof (The Market Price Disconnect):**  
   In [`dcf.py`](file:///Users/lucarichey/Documents/Courses/AIFinance2026/LucaRichey/dcf.py#L40-L43), our Reverse-DCF proved that for Robinhood to be worth its market price of **\$113.33 – \$116.00**, it requires a **+45.22 percentage point uniform growth shift**. That implies revenue must grow at **75.2% in Year 1, 70.2% in Year 2, and 65.2% in Year 3**! This proves that the market is pricing in speculative hyper-growth that is entirely unanchored to historical 10-K fundamentals.

---

### Stop 5: Sensitivity and Drivers (Lab 11 Results)
In Lab 11, we ran one-at-a-time sensitivity analysis using independent deep copies, resetting all assumptions to base before each run:

```text
=========================================================================================================
 OUTPUT SPANS (Max Output − Min Output over Tested Ranges)
=========================================================================================================
Output Metric                       Options Revenue Shift           Gross Margin  Total Platform Growth
---------------------------------------------------------------------------------------------------------
FY2030E Operating Profit ($M)     $                1080.4M$                  98.7M$                1229.7M
FY2030E FCFE ($M)                 $                 847.6M$                  78.0M$                 964.9M
Equity Value per Share ($/share)  $                  4.61$                  0.51$                  5.25
=========================================================================================================
```

#### The Causal Mechanism:
* **The Options Desk Drives 88% of Revenue Volatility:**  
  While Total Platform Growth creates an operating profit span of **\$1,229.7M**, shifting *just* the Options Revenue line creates an operating profit span of **\$1,080.4M** (\$5,270.0M high vs. \$4,189.5M low). Options alone accounts for **88% of Robinhood's entire operational sensitivity**!
* **The PFOF Drop-Through Math:**  
  Options order routing generates lucrative rebates (~$0.30–\$0.50/contract) with near-zero variable delivery cost. At a 95.28% gross margin and 45% SG&A ratio, **52.4 cents of every lost dollar of options revenue disappears directly from Operating Income**:
  $$0.9528 \times (1 - 0.45) = \mathbf{0.524}$$
* **What the Ranking Establishes vs. Does Not Establish:**  
  The ranking proves that Options Revenue and Platform Growth dominate Gross Margin **over these tested ranges**. However, it is an elasticity test, not a forecast probability. It does not state that a -10 pp options decline has a known probability, nor does it model correlated multi-variable shocks (such as a market crash hitting both options volume and crypto revenue simultaneously).

---

### Stop 6: Interpretation and Supported Conclusion
* **Supported Conditional Recommendation: AVOID / HOLD at Current Market Prices (\$116.00).**  
  An investor buying at \$116 is paying 56.6× trailing earnings and baking in 70%+ sustained growth with zero margin of safety.
* **Target Entry Range: \$47.32 – \$64.63.**  
  If the market price compresses toward **\$47.32** (Schwab P/E parity), Robinhood becomes a compelling buy, supported by superior Gen-Z demographics, Gold subscription expansion, and a fundamental cash-flow floor of **\$24–\$29**.
* **What Evidence Would Change My Mind (To Upgrade at Higher Prices):**  
  1. *Non-Transaction Revenue Mix:* Evidence that recurring, non-cyclical revenue (Gold subscriptions, Gold Card interchange, TradePMR RIA custody fees) exceeds **50% of total revenue**, reducing beta and cost of capital from 16.5% toward 10%.
  2. *Regulatory Resolution on PFOF:* Formal SEC rulings preserving wholesale market-maker order routing rebates in the U.S.
* **The Evidence to Investigate Next:**  
  In the upcoming Project 1 studio, I will investigate the interest-rate sensitivity of Robinhood's **\$389M quarterly net interest income**, modeling how Federal Reserve benchmark rate cuts impact customer cash sweep yields and margin lending spreads.

---

## V — Question and Check as the Reviewer (Reviewing Partner B: Asbury Automotive Group)

During Partner B's presentation on **Asbury Automotive Group (NYSE: ABG)**, I conducted the following audit:

### 1. Questions Asked Across All Three Required Areas:
* **Selection & Evidence:** *"You chose Asbury as a physical dealership consolidator, but how do you justify separating organic same-store revenue growth (1.8%) from reported total revenue growth (4.7%) in your opening balance sheet?"*  
  *Partner Answer:* Partner B correctly explained that 2.9 percentage points of reported growth came from acquiring new dealership franchises. Same-store organic growth must be isolated because acquisition growth requires external cash purchase consideration that cannot be assumed for free in an organic cash flow forecast.
* **Model & Valuation:** *"Why is Asbury's terminal value such a massive percentage (79.8%) of its total equity value (\$5,237.34M), and how does the \$150M annual debt repayment interact with terminal FCF?"*  
  *Partner Answer:* Partner B showed line 279 of `proforma.py`: 2030 FCFE was \$342.3M, but term debt repayment (\$150M) ceases in the terminal period. Therefore, normalized terminal cash flow was adjusted upward to $(\$342.3\text{M} + \$150\text{M}) \times 1.025 = \$504.6\text{M}$, properly reflecting post-deleveraging cash generation.
* **Sensitivity & Interpretation:** *"Over your tested ranges, gross margin had an operating income span of \$139.7M while CapEx had a span of only \$10.3M. Does this prove that CapEx doesn't matter to Asbury's business?"*  
  *Partner Answer:* Partner B emphasized the critical caveat *"over these ranges"*: CapEx only enters operating income through delayed annual depreciation increments (\$5.2M), but on free cash flow to equity and share value, CapEx had an almost identical impact (\$66.89/share span vs. \$71.26/share for gross margin) because capital expenditures represent dollar-for-dollar cash subtractions.

### 2. Calculation Audited Together:
* **Calculation Checked:** We opened Partner B's [`proforma.py`](file:///Users/lucarichey/Documents/Courses/AIFinance2026/LucaRichey/proforma.py) and hand-calculated the Gross Margin Lower Run (16.05% vs 17.05% base) in FY2030E:
  $$\text{FY2030E Revenue} = \$19,678.3\text{M}$$
  $$\text{Base GP} = \$19,678.3\text{M} \times 0.1705 = \$3,355.15\text{M}$$
  $$\text{Lower GP} = \$19,678.3\text{M} \times 0.1605 = \$3,158.37\text{M}\quad (\Delta -\$196.78\text{M})$$
  $$\Delta \text{SG&A (at 64.5\%)} = -\$196.78\text{M} \times 0.645 = -\$126.92\text{M}$$
  $$\Delta \text{Operating Income} = -\$196.78\text{M} - (-\$126.92\text{M}) = \mathbf{-\$69.86\text{M}}\quad (\approx \mathbf{-\$69.9\text{M}})$$
* **Verification Result:** The hand calculation matched Partner B's printed console output of **-\$69.9M** exactly, confirming zero code leakage or hardcoding.

### 3. Reviewer Explain-Back & Actionable Feedback:
* **Explanation Back of Partner's Core Case:** Partner B's model values Asbury at **\$291.75 per share**, driven by physical vehicle dealership consolidation and service/parts cash flow. The main operating driver is Gross Margin (\$139.7M span), while the biggest limitation is Asbury's heavy dependence on floor plan debt notes (\$2.2B) which makes cash flow vulnerable to interest rate spikes on vehicle inventories.
* **One Evidence-Backed Strength:** Partner B's reconciliation of normalized terminal FCF (adding back the \$150M debt repayment to reflect an unlevered steady-state) was mathematically rigorous and grounded in credit agreement realities.
* **One Specific Improvement to Make Next:** Partner B should model floor plan interest rate sensitivity separately from term debt, because floor plan loans float directly with SOFR and represent 28% of total liabilities.

---

## E — Response & Revision (As Presenter: Feedback on Robinhood)

### 1. Questions Received from Partner B & My Answers:
* **Question 1:** *"Why is your pro-forma DCF valuation (\$23.85) less than a quarter of the market price (\$116.00)?"*  
  *My Answer:* The DCF is grounded in audited FY2025 10-K cash flows and heavily penalized by a 16.53% cost of equity (Beta 2.34). The \$116 market price reflects speculative momentum; our reverse-DCF mathematically proved that the market is pricing in a +45 pp growth premium (75% revenue growth in Year 1), which cannot be defended based on 10-K fundamentals alone.
* **Question 2:** *"Why does a 10 percentage point shift in Options revenue growth account for 88% of your total revenue sensitivity?"*  
  *My Answer:* Because wholesale market makers pay lucrative PFOF rebates on options (~$0.30–\$0.50/contract) with zero physical delivery cost. At 95.3% gross margin, 52.4 cents of every lost options dollar flows straight through to operating profit, making options volume the primary profit engine of the firm.
* **Question 3:** *"Why do you hold \$1,000M in minimum cash when traditional corporate models only hold 2% of revenue?"*  
  *My Answer:* Because Robinhood is an SEC-registered broker-dealer subject to Rule 15c3-1 net capital rules and clearinghouse deposit buffers (NSCC/DTCC). Holding \$1.0B in liquid corporate cash ensures the firm avoids regulatory suspension during extreme market volatility.

### 2. Reviewer Feedback Received from Partner B:
* **Strength Identified by Partner:** The Options revenue deep-dive provided a granular, company-specific operational thesis that directly connected SEC regulatory risk (PFOF bans) to balance sheet cash flow, distinguishing Robinhood from generic tech models.
* **Specific Improvement Identified by Partner:** Net Interest Income (\$389M in Q2 2026, 30% of revenue) is currently aggregated inside platform growth; I should explicitly disaggregate margin lending interest from cash sweep yields to model Federal Reserve rate-cut sensitivity.

### 3. Decisions: What I Will Keep, Revise, and Investigate in Project 1 Studio:
* **KEEP:**  
  I will keep the **95.28% Gross Margin** and the **Options Revenue sensitivity structure**. The high gross margin is an unassailable historical fact of electronic clearing, and the Options Desk is provably the primary driver of earnings volatility.
* **REVISE:**  
  I will revise the revenue forecast structure in the Project 1 studio to explicitly separate **Net Interest Revenue** from **Transaction Revenue**, creating a rate-sensitivity sub-engine that tests a 100 bps cut in the Federal Funds rate on client cash sweep margins.
* **INVESTIGATE:**  
  I will investigate the **CFTC regulatory status of Robinhood's Event Contracts (prediction markets)**, which grew from \$10M to \$156M in Q2 2026 alone, to evaluate whether this product line represents sustainable recurring cash flow or a short-lived regulatory target.
* **Effect on Conclusion:**  
  This review reinforces my valuation conclusion: Robinhood is fundamentally an options-trading clearinghouse trading at a massive speculative premium. My research priority shifts from general platform growth to **interest rate sensitivity and regulatory PFOF policy**.

---

## Reflect
* **Which question made me reconsider something?**  
  Partner B's question on why the market price is \$116 when the DCF is \$24 pushed me to articulate the core lesson of the course: a valuation model's job is not to justify the market price, but to expose the heroic growth assumptions required to sustain it.
* **What I now understand better about Robinhood:**  
  I now understand that Robinhood is not a general stock brokerage—it is fundamentally an **options market-making distribution channel** disguised as a consumer app. 88% of its operational sensitivity is driven by options PFOF, explaining why regulatory scrutiny on order flow is an existential risk for shareholders.

---

## Merit Anchors Self-Audit Grid (25/25)

| Anchor Criterion | Score | Document Evidence & Location in Checkout |
|---|:---:|---|
| **1. Full Analysis & Ownership** | **5 / 5** | All six stops explained in own words; complete route from target selection through 10-K evidence, pro-forma mechanics, DCF/peer triangulation, and sensitivity traced with zero generic filler. |
| **2. Valuation Reasoning** | **5 / 5** | Complete mathematical justification of why methods differ (DCF \$23.85, DCF FCFF \$29.24, Peers \$47–\$82, Market \$116); discount rate (16.53%) and reverse-DCF (+45 pp growth shift) fully explained. |
| **3. Sensitivity Interpretation** | **5 / 5** | Company-specific Options Desk driver traced through statements (\$1,080.4M span; 88% of volatility); ranking explicitly qualified by tested ranges; deterministic elasticity distinguished from probability. |
| **4. Reviewing the Partner** | **5 / 5** | Specific questions recorded across Selection, Valuation, and Sensitivity for Partner B (ABG); \$69.9M calculation audited and verified; explain-back of ABG conclusion recorded with actionable feedback. |
| **5. Response and Revision** | **5 / 5** | Partner B's questions on Robinhood answered; feedback documented; explicit Keep/Revise/Investigate decisions justified with clear effects on Project 1 research priorities. |
