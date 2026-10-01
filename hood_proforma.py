"""
Pro-Forma Three-Statement Financial Model & Valuation Engine with One-at-a-Time Sensitivity
Company: Robinhood Markets, Inc. (NASDAQ: HOOD)
Lab 10 & Lab 11: Pro-Forma Modeling & Sensitivity Analysis (Including Options Revenue Deep-Dive)
Student: Luca Richey | FIN 43900 (AI Finance Applications, Purdue University)
"""

import copy
import sys


def get_base_assumptions():
    """
    Returns the baseline inputs and assumptions for Robinhood Markets, Inc. (HOOD).
    Sourced from FY2025 Form 10-K and Q2 2026 Form 10-Q filings.
    """
    return {
        # --- Opening Balance Sheet (FY2025 ended Dec 31, 2025, USD millions) ---
        "rev_0": 4473.0,            # FY2025 Total net revenues (10-K Item 8, p. 128)
        "options_rev_0": 1163.0,    # FY2025 Options trading revenue (~26.0% of net rev; $342M Q2 run-rate)
        "other_rev_0": 3310.0,      # Non-options revenue (equities, crypto, events, net interest, gold)
        "options_growth_shift": 0.0,# Company-specific Options volume & PFOF shift
        
        "inv_0": 0.0,               # None: Digital retail broker holds zero physical inventory
        "ppe_0": 154.0,             # Property, software, and equipment, net (10-Q p. 11)
        "other_assets_0": 33722.0,  # Segregated cash, customer receivables, clearing deposits, intangibles
        "cash_0": 4261.0,           # Corporate cash and cash equivalents (10-Q p. 11)
        
        "floor_0": 0.0,             # None: Brokerages have no automotive floor plan notes
        "debt_0": 0.0,              # Long-term borrowings as of Dec 31, 2025 (10-Q p. 11)
        "revolver_0": 0.0,          # Revolving credit facility drawn (10-Q Note 11, p. 38)
        "other_liab_0": 28986.0,    # Payables to users, securities loaned, fractional obligations, AP
        "equity_0": 9151.0,         # Total stockholders' equity (10-Q p. 11)

        # --- Operating Assumptions ---
        "rev_growths": [0.20, 0.18, 0.15, 0.12, 0.10],      # Deceleration from 52% expansion [judgment]
        "gross_margin": 0.9528,                              # Clearing & brokerage cost ratio history [history]
        "sga_ratios": [0.500, 0.480, 0.460, 0.450, 0.450],  # Operating leverage on fixed tech/admin [judgment]
        "depr_ratio": 86.0 / 154.0,                          # FY2025 D&A / opening PP&E [history]
        "impairment": 0.0,                                   # Zero goodwill impairment [judgment]
        "capex": 65.0,                                       # CapEx + capitalized software [judgment]
        "tax_rate": 0.210,                                   # Federal statutory corporate tax rate [history]

        # --- Working Capital & Regulatory Liquidity ---
        "inv_days": 0.0,                                     # No physical merchandise
        "floor_ratio": 0.0,                                  # No floor plan credit
        "other_wc_ratio": 0.010,                             # 1.0% of change in revenue [judgment]

        "min_cash": 1000.0,                                  # Regulatory net capital reserve buffer [judgment]
        "revolver_limit": 1000.0,                            # Committed credit facility [history]
        "revolver_rate": 0.065,                              # SOFR + 1.50% margin [history]

        "repayment": 0.0,                                    # Zero senior notes due until 2029 [guidance]
        "buyback": 500.0,                                    # $1.5B share repurchase authorization [guidance]

        # --- Rates & Valuation Assumptions ---
        "floor_rate": 0.0,                                   # None
        "debt_rate": 0.0483,                                 # 10-year Treasury baseline yield [history]
        "cost_of_equity": 0.1653,                            # Rf 4.83% + Beta 2.34 * ERP 5.0% = 16.53% [history]
        "terminal_growth": 0.030,                            # Long-run nominal GDP growth [judgment]
        "shares": 912.0,                                     # Diluted shares outstanding (million) [history]
        "years": [2026, 2027, 2028, 2029, 2030],
    }


def run_model(assumptions):
    """
    Reruns the entire linked 3-statement model and valuation engine for Robinhood.
    Recalculates all statements, balance sheet integrity checks, and valuation.
    """
    rev_0 = assumptions["rev_0"]
    options_rev_0 = assumptions.get("options_rev_0", 1163.0)
    other_rev_0 = assumptions.get("other_rev_0", rev_0 - options_rev_0)
    options_growth_shift = assumptions.get("options_growth_shift", 0.0)

    inv_0 = assumptions["inv_0"]
    ppe_0 = assumptions["ppe_0"]
    other_assets_0 = assumptions["other_assets_0"]
    cash_0 = assumptions["cash_0"]
    floor_0 = assumptions["floor_0"]
    debt_0 = assumptions["debt_0"]
    other_liab_0 = assumptions["other_liab_0"]
    equity_0 = assumptions["equity_0"]
    revolver_0 = assumptions["revolver_0"]

    rev_growths = assumptions["rev_growths"]
    gross_margin = assumptions["gross_margin"]
    sga_ratios = assumptions["sga_ratios"]
    depr_ratio = assumptions["depr_ratio"]
    impairment = assumptions["impairment"]
    capex = assumptions["capex"]
    tax_rate = assumptions["tax_rate"]

    inv_days = assumptions["inv_days"]
    floor_ratio = assumptions["floor_ratio"]
    other_wc_ratio = assumptions["other_wc_ratio"]

    min_cash = assumptions["min_cash"]
    revolver_limit = assumptions["revolver_limit"]
    revolver_rate = assumptions["revolver_rate"]

    repayment = assumptions["repayment"]
    buyback = assumptions["buyback"]

    floor_rate = assumptions["floor_rate"]
    debt_rate = assumptions["debt_rate"]

    cost_of_equity = assumptions["cost_of_equity"]
    terminal_growth = assumptions["terminal_growth"]
    shares = assumptions["shares"]
    years = assumptions["years"]

    projections = []

    cur_rev = rev_0
    cur_options = options_rev_0
    cur_other = other_rev_0

    cur_inv = inv_0
    cur_ppe = ppe_0
    cur_other_assets = other_assets_0
    cur_cash = cash_0
    cur_floor = floor_0
    cur_debt = debt_0
    cur_other_liab = other_liab_0
    cur_equity = equity_0
    cur_revolver = revolver_0

    for i, yr in enumerate(years):
        # 1. Income Statement
        prior_rev = cur_rev
        g = rev_growths[i] if isinstance(rev_growths, (list, tuple)) else rev_growths
        gm = gross_margin[i] if isinstance(gross_margin, (list, tuple)) else gross_margin
        sga_r = sga_ratios[i] if isinstance(sga_ratios, (list, tuple)) else sga_ratios
        cx = capex[i] if isinstance(capex, (list, tuple)) else capex
        imp = impairment[i] if isinstance(impairment, (list, tuple)) else impairment

        # Options revenue vs Other revenue growth breakdown
        opt_g = g + options_growth_shift
        other_g = g
        options_rev = cur_options * (1.0 + opt_g)
        other_rev = cur_other * (1.0 + other_g)
        rev = options_rev + other_rev

        gp = rev * gm
        sga = gp * sga_r
        depr = cur_ppe * depr_ratio
        op_inc = gp - sga - depr - imp

        interest = (cur_floor * floor_rate) + (cur_debt * debt_rate) + (cur_revolver * revolver_rate)
        pretax = op_inc - interest
        tax = max(0.0, pretax) * tax_rate
        ni = pretax - tax

        # 2. Balance Sheet except cash
        cogs = rev - gp
        inv = cogs * inv_days / 365.0
        floor = inv * floor_ratio
        ppe = cur_ppe + cx - depr
        delta_rev = rev - prior_rev
        delta_other_wc = other_wc_ratio * delta_rev
        other_assets = cur_other_assets + delta_other_wc - imp
        debt = cur_debt - repayment
        other_liab = cur_other_liab
        equity = cur_equity + ni - buyback

        # 3. Cash Flow / FCFE
        delta_inv = inv - cur_inv
        delta_floor = floor - cur_floor
        fcfe = (ni + depr + imp - cx - delta_inv - delta_other_wc + delta_floor - repayment)

        # 4. Cash and Revolver
        cash_tentative = cur_cash + fcfe - buyback
        revolver = cur_revolver

        if cash_tentative < min_cash:
            draw = min_cash - cash_tentative
            revolver += draw
            cash = min_cash
            revolver_change = draw
        else:
            surplus = cash_tentative - min_cash
            repay = min(surplus, revolver)
            revolver -= repay
            cash = cash_tentative - repay
            revolver_change = -repay

        # Checks
        tot_assets = cash + inv + ppe + other_assets
        tot_liab_eq = floor + debt + revolver + other_liab + equity
        gap = tot_assets - tot_liab_eq
        cash_check = cash >= (min_cash - 1e-4)

        data = {
            "year": yr,
            "label": f"FY{yr}E",
            # IS
            "rev": rev,
            "options_rev": options_rev,
            "other_rev": other_rev,
            "gp": gp,
            "sga": sga,
            "depr": depr,
            "imp": imp,
            "op_inc": op_inc,
            "interest": interest,
            "pretax": pretax,
            "tax": tax,
            "ni": ni,
            # BS
            "cash": cash,
            "inv": inv,
            "ppe": ppe,
            "other_assets": other_assets,
            "tot_assets": tot_assets,
            "floor": floor,
            "debt": debt,
            "revolver": revolver,
            "other_liab": other_liab,
            "tot_liab": floor + debt + revolver + other_liab,
            "equity": equity,
            "tot_liab_eq": tot_liab_eq,
            # CF
            "fcfe": fcfe,
            "delta_inv": delta_inv,
            "delta_other_wc": delta_other_wc,
            "delta_floor": delta_floor,
            "repayment": repayment,
            "buyback": buyback,
            "capex": cx,
            "revolver_change": revolver_change,
            "net_cash_change": cash - cur_cash,
            "opening_cash": cur_cash,
            # Checks
            "gap": gap,
            "cash_check": cash_check
        }
        projections.append(data)

        cur_rev = rev
        cur_options = options_rev
        cur_other = other_rev
        cur_inv = inv
        cur_ppe = ppe
        cur_other_assets = other_assets
        cur_cash = cash
        cur_floor = floor
        cur_debt = debt
        cur_other_liab = other_liab
        cur_equity = equity
        cur_revolver = revolver

    # Integrity verification
    checks_passed = True
    for p in projections:
        if abs(p["gap"]) > 1e-4 or not p["cash_check"]:
            checks_passed = False
            break

    # Valuation
    fcfe_vals = [p["fcfe"] for p in projections]
    pv_fcfe = sum(f / ((1.0 + cost_of_equity) ** (i + 1)) for i, f in enumerate(fcfe_vals))

    fcfe_2030 = fcfe_vals[-1]
    terminal_fcf = (fcfe_2030 + repayment) * (1.0 + terminal_growth)
    if cost_of_equity > terminal_growth:
        terminal_val = terminal_fcf / (cost_of_equity - terminal_growth)
        pv_terminal_val = terminal_val / ((1.0 + cost_of_equity) ** len(years))
        equity_value = pv_fcfe + pv_terminal_val
        share_after_2030 = pv_terminal_val / equity_value if equity_value != 0 else 0.0
        value_per_share = equity_value / shares
        val_valid = True
    else:
        terminal_val = float('nan')
        pv_terminal_val = float('nan')
        equity_value = float('nan')
        share_after_2030 = float('nan')
        value_per_share = float('nan')
        val_valid = False

    return {
        "projections": projections,
        "checks_passed": checks_passed,
        "final_op_inc": projections[-1]["op_inc"],
        "final_fcfe": projections[-1]["fcfe"],
        "final_options_rev": projections[-1]["options_rev"],
        "final_rev": projections[-1]["rev"],
        "valuation": {
            "pv_fcfe": pv_fcfe,
            "terminal_val": terminal_val,
            "pv_terminal_val": pv_terminal_val,
            "equity_value": equity_value,
            "share_after_2030": share_after_2030,
            "shares": shares,
            "value_per_share": value_per_share,
            "val_valid": val_valid,
        }
    }


def print_table(title, rows, projections, year_labels):
    """Prints formatted financial statement tables."""
    print(f"\n{'=' * 78}")
    print(f" {title.upper()}")
    print(f"{'=' * 78}")
    header = f"{'Line Item':<35}" + "".join([f"{lbl:>10}" for lbl in year_labels])
    print(header)
    print("-" * 78)
    for label, key in rows:
        if key is None:
            print("-" * 78)
            continue
        line = f"{label:<35}"
        for p in projections:
            val = p[key]
            line += f"{val:>10.1f}"
        print(line)


def display_full_statements(model_output, year_labels):
    """Displays standard 3 statements, integrity checks, and valuation summary."""
    projections = model_output["projections"]
    val = model_output["valuation"]

    is_rows = [
        ("Total net revenues", "rev"),
        (" — Options trading revenue", "options_rev"),
        (" — Other platform revenue", "other_rev"),
        ("Gross profit (rev − clearing)", "gp"),
        ("SG&A (tech, ops, mktg, G&A)", "sga"),
        ("Depreciation & amortization", "depr"),
        ("Impairment", "imp"),
        ("Operating income", "op_inc"),
        ("Interest expense", "interest"),
        ("Pretax income", "pretax"),
        ("Income tax provision", "tax"),
        ("Net income", "ni"),
    ]
    print_table("Income Statement (USD millions)", is_rows, projections, year_labels)

    bs_rows = [
        ("Cash and cash equivalents", "cash"),
        ("Inventories (None)", "inv"),
        ("Property, software & equip, net", "ppe"),
        ("Other assets (cust. rec, seg cash)", "other_assets"),
        (None, None),
        ("Total assets", "tot_assets"),
        (None, None),
        ("Floor plan loans (None)", "floor"),
        ("Term debt / senior notes", "debt"),
        ("Revolving credit facility", "revolver"),
        ("Other liabilities (payables/loans)", "other_liab"),
        ("Total liabilities", "tot_liab"),
        ("Stockholders' equity", "equity"),
        (None, None),
        ("Total liabilities & equity", "tot_liab_eq"),
    ]
    print_table("Balance Sheet (USD millions)", bs_rows, projections, year_labels)

    cf_rows = [
        ("Net income", "ni"),
        ("Depreciation & amortization", "depr"),
        ("Impairment", "imp"),
        ("Capital expenditures", "capex"),
        ("Change in inventories", "delta_inv"),
        ("Change in other working capital", "delta_other_wc"),
        ("Change in floor plan notes", "delta_floor"),
        ("Term debt repayment", "repayment"),
        (None, None),
        ("Free cash flow to equity (FCFE)", "fcfe"),
        (None, None),
        ("Share repurchases", "buyback"),
        ("Revolver draw / (repayment)", "revolver_change"),
        ("Net change in cash", "net_cash_change"),
        ("Ending cash balance", "cash"),
    ]
    print_table("Cash Flow Statement / FCFE (USD millions)", cf_rows, projections, year_labels)

    print(f"\n{'=' * 78}")
    print(f" INTEGRITY CHECKS")
    print(f"{'=' * 78}")
    header = f"{'Check':<35}" + "".join([f"{lbl:>10}" for lbl in year_labels])
    print(header)
    print("-" * 78)
    gap_line = f"{'Assets − Liab − Equity (gap)':<35}" + "".join([f"{p['gap']:>10.1f}" for p in projections])
    cash_check_line = f"{'Cash >= Minimum ($1,000M)':<35}" + "".join([f"{'PASS':>10}" if p['cash_check'] else f"{'FAIL':>10}" for p in projections])
    print(gap_line)
    print(cash_check_line)
    print("=" * 78)

    print("\n" + "=" * 78)
    print(" VALUATION SUMMARY — ROBINHOOD MARKETS, INC. (HOOD)")
    print("=" * 78)
    print(f"PV of 5-year FCFE:               ${val['pv_fcfe']:>10.2f}M")
    print(f"Terminal Value (TV):             ${val['terminal_val']:>10.2f}M")
    print(f"PV of Terminal Value:            ${val['pv_terminal_val']:>10.2f}M")
    print(f"Equity Value:                    ${val['equity_value']:>10.2f}M")
    print(f"Share of Value after 2030:        {val['share_after_2030'] * 100:>9.1f}%")
    print(f"Diluted Shares Outstanding:       {val['shares']:>10.1f}M")
    print(f"Model Value per Share:           ${val['value_per_share']:>10.2f}")
    print("=" * 78)


def run_sensitivity_analysis(base_assumptions, drivers_config):
    """
    Performs one-at-a-time sensitivity analysis.
    Preserves an isolated base input set, creating a fresh independent copy for every run.
    Recalculates linked accounting quantities, verifies integrity checks, reports
    signed changes and spans, and verifies restored base equality.
    """
    print("\n" + "#" * 90)
    print(" LAB 11: ONE-AT-A-TIME SENSITIVITY ANALYSIS — ROBINHOOD MARKETS (HOOD)")
    print(" FEATURING COMPANY-SPECIFIC DRIVER: OPTIONS TRADING REVENUE (PFOF & VOLUME)")
    print("#" * 90)

    # 1. Run and verify initial base
    base_run = run_model(copy.deepcopy(base_assumptions))
    if not base_run["checks_passed"]:
        raise RuntimeError("Initial baseline run failed accounting integrity checks!")
    
    base_op_inc = base_run["final_op_inc"]
    base_fcfe = base_run["final_fcfe"]
    base_vps = base_run["valuation"]["value_per_share"]

    results = []

    # Store base run summary
    results.append({
        "driver_name": "Base Run",
        "case": "Base",
        "input_val_str": "All Base Inputs",
        "op_inc": base_op_inc,
        "delta_op_inc": 0.0,
        "fcfe": base_fcfe,
        "delta_fcfe": 0.0,
        "vps": base_vps,
        "delta_vps": 0.0,
        "checks": "PASS" if base_run["checks_passed"] else "FAIL",
        "raw_output": base_run,
    })

    # 2. Iterate over drivers
    driver_spans = {}
    for d in drivers_config:
        key = d["key"]
        name = d["name"]
        unit = d["unit"]
        cases = d["cases"]  # list of tuples: (case_label, value, repr_str)

        op_inc_vals = []
        fcfe_vals = []
        vps_vals = []

        for case_label, val, repr_str in cases:
            # Fresh independent deep copy for every run
            run_inputs = copy.deepcopy(base_assumptions)
            run_inputs[key] = val

            output = run_model(run_inputs)
            op = output["final_op_inc"]
            fcfe = output["final_fcfe"]
            vps = output["valuation"]["value_per_share"]
            chk = "PASS" if output["checks_passed"] else "FAIL"

            if chk == "PASS":
                op_inc_vals.append(op)
                fcfe_vals.append(fcfe)
                if output["valuation"]["val_valid"]:
                    vps_vals.append(vps)

            results.append({
                "driver_name": name,
                "case": case_label,
                "input_val_str": repr_str,
                "op_inc": op,
                "delta_op_inc": op - base_op_inc,
                "fcfe": fcfe,
                "delta_fcfe": fcfe - base_fcfe,
                "vps": vps,
                "delta_vps": vps - base_vps,
                "checks": chk,
                "raw_output": output,
            })

        # Calculate spans (max - min across valid runs)
        span_op = max(op_inc_vals) - min(op_inc_vals) if op_inc_vals else float('nan')
        span_fcfe = max(fcfe_vals) - min(fcfe_vals) if fcfe_vals else float('nan')
        span_vps = max(vps_vals) - min(vps_vals) if vps_vals else float('nan')

        driver_spans[name] = {
            "op_inc_span": span_op,
            "fcfe_span": span_fcfe,
            "vps_span": span_vps,
        }

    # 3. Print Sensitivity Comparison Table
    print("\n" + "=" * 98)
    print(" SENSITIVITY RESULTS TABLE: ONE-AT-A-TIME INPUT VARIATIONS")
    print("=" * 98)
    col_fmt = "{:<26} {:<10} {:<24} {:>10} {:>10} {:>12} {:>8}"
    print(col_fmt.format("Operating Driver", "Case", "Input Value / Path", "FY30 OpInc", "FY30 FCFE", "Value/Share", "Checks"))
    print(col_fmt.format("", "", "", "($M)", "($M)", "($/sh)", ""))
    print("-" * 98)

    for r in results:
        vps_str = f"${r['vps']:.2f}" if not (r['vps'] != r['vps']) else "N/A"
        print(col_fmt.format(
            r["driver_name"],
            r["case"],
            r["input_val_str"],
            f"{r['op_inc']:.1f}",
            f"{r['fcfe']:.1f}",
            vps_str,
            r["checks"]
        ))
    print("=" * 98)

    # 4. Print Signed Differences from Base Table
    print("\n" + "=" * 98)
    print(" SIGNED CHANGES FROM BASELINE (Changed Output − Base Output)")
    print("=" * 98)
    col_delta_fmt = "{:<26} {:<10} {:<24} {:>12} {:>12} {:>14}"
    print(col_delta_fmt.format("Operating Driver", "Case", "Input Value / Path", "Δ FY30 OpInc", "Δ FY30 FCFE", "Δ Value/Share"))
    print(col_delta_fmt.format("", "", "", "($M)", "($M)", "($/sh)"))
    print("-" * 98)

    for r in results:
        if r["case"] == "Base" and r["driver_name"] == "Base Run":
            continue
        vps_delta_str = f"{r['delta_vps']:>+10.2f}" if not (r['delta_vps'] != r['delta_vps']) else "N/A"
        print(col_delta_fmt.format(
            r["driver_name"],
            r["case"],
            r["input_val_str"],
            f"{r['delta_op_inc']:>+10.1f}",
            f"{r['delta_fcfe']:>+10.1f}",
            vps_delta_str
        ))
    print("=" * 98)

    # 5. Print Output Spans Table
    print("\n" + "=" * 105)
    print(" OUTPUT SPANS (Max Output − Min Output over Tested Ranges)")
    print("=" * 105)
    span_header = f"{'Output Metric':<34}" + "".join([f"{d['name']:>23}" for d in drivers_config])
    print(span_header)
    print("-" * 105)

    op_line = f"{'FY2030E Operating Profit ($M)':<34}"
    for d in drivers_config:
        op_line += f"${driver_spans[d['name']]['op_inc_span']:>22.1f}M"
    print(op_line)

    fcfe_line = f"{'FY2030E FCFE ($M)':<34}"
    for d in drivers_config:
        fcfe_line += f"${driver_spans[d['name']]['fcfe_span']:>22.1f}M"
    print(fcfe_line)

    vps_line = f"{'Equity Value per Share ($/share)':<34}"
    for d in drivers_config:
        vps_line += f"${driver_spans[d['name']]['vps_span']:>22.2f}"
    print(vps_line)
    print("=" * 105)

    # 6. Deep-Dive Statement Trace Details for Options Trading Revenue
    print("\n" + "=" * 98)
    print(" OPTIONS REVENUE DEEP-DIVE TRACE: HOW OPTIONS SHIFTS FLOW THROUGH STATEMENTS (FY2030E)")
    print("=" * 98)
    trace_fmt = "{:<32} {:>14} {:>16} {:>16} {:>16}"
    print(trace_fmt.format("Statement Line Item ($M)", "Base", "Options -10pp", "Options +10pp", "GM 94.28%"))
    print("-" * 98)

    opt_low_res = [r for r in results if r["driver_name"] == "Options Revenue Shift" and r["case"] == "Lower"][0]["raw_output"]["projections"][-1]
    opt_high_res = [r for r in results if r["driver_name"] == "Options Revenue Shift" and r["case"] == "Higher"][0]["raw_output"]["projections"][-1]
    gm_low_res = [r for r in results if r["driver_name"] == "Gross Margin" and r["case"] == "Lower"][0]["raw_output"]["projections"][-1]
    base_res = results[0]["raw_output"]["projections"][-1]

    trace_items = [
        ("Options Trading Revenue", "options_rev"),
        ("Other Platform Revenue", "other_rev"),
        ("Total Net Revenues", "rev"),
        ("Gross Profit", "gp"),
        ("SG&A Expense", "sga"),
        ("Operating Income", "op_inc"),
        ("Income Tax Provision (21%)", "tax"),
        ("Net Income", "ni"),
        ("Ending Corporate Cash", "cash"),
        ("Free Cash Flow to Equity (FCFE)", "fcfe"),
    ]
    for lbl, k in trace_items:
        print(trace_fmt.format(
            lbl,
            f"{base_res[k]:>14.1f}",
            f"{opt_low_res[k]:>16.1f}",
            f"{opt_high_res[k]:>16.1f}",
            f"{gm_low_res[k]:>16.1f}"
        ))
    print("=" * 98)

    # 7. Restored Base Verification
    print("\n" + "=" * 80)
    print(" RESTORED BASE VERIFICATION")
    print("=" * 80)
    restored_run = run_model(copy.deepcopy(base_assumptions))
    diff_op = abs(restored_run["final_op_inc"] - base_op_inc)
    diff_fcfe = abs(restored_run["final_fcfe"] - base_fcfe)
    diff_vps = abs(restored_run["valuation"]["value_per_share"] - base_vps)

    print(f"Initial Base OpInc:   {base_op_inc:.4f} | Restored Base OpInc:   {restored_run['final_op_inc']:.4f} | Diff: {diff_op:.4e}")
    print(f"Initial Base FCFE:    {base_fcfe:.4f} | Restored Base FCFE:    {restored_run['final_fcfe']:.4f} | Diff: {diff_fcfe:.4e}")
    print(f"Initial Base Val/sh:  ${base_vps:.4f} | Restored Base Val/sh:  ${restored_run['valuation']['value_per_share']:.4f} | Diff: {diff_vps:.4e}")

    tolerance = 1e-4
    if diff_op < tolerance and diff_fcfe < tolerance and diff_vps < tolerance and restored_run["checks_passed"]:
        print(">> RESTORED BASE CHECK: PASSED (Exact match within rounding tolerance; all checks pass)")
    else:
        print(">> RESTORED BASE CHECK: FAILED!")
        raise AssertionError("Restored base does not match initial baseline run!")
    print("=" * 80 + "\n")


def main():
    base_assumptions = get_base_assumptions()
    year_labels = [f"FY{yr}E" for yr in base_assumptions["years"]]

    # Run and display full base pro-forma model
    base_output = run_model(copy.deepcopy(base_assumptions))
    display_full_statements(base_output, year_labels)

    # Define sensitivity specifications:
    # 1. Options Revenue Shift (Company-Specific Volume & PFOF Driver):
    #    Base: 0.0% shift (tracks 20% down to 10%)
    #    Lower: -10.0 percentage points per year (-10pp; e.g. SEC PFOF restrictions, retail options slump)
    #    Higher: +10.0 percentage points per year (+10pp; e.g. 0DTE retail option surge, index options)
    # 2. Platform Gross Margin (Clearing & Transaction Costs):
    #    Base: 95.28%
    #    Lower: 94.28% (-100 bps)
    #    Higher: 96.28% (+100 bps)
    # 3. Overall Platform Revenue Growth Path (Multi-Year Trajectory):
    #    Base: [20%, 18%, 15%, 12%, 10%]
    #    Lower: [17%, 15%, 12%, 9%, 7%] (-3pp)
    #    Higher: [23%, 21%, 18%, 15%, 13%] (+3pp)
    base_rev_growths = base_assumptions["rev_growths"]
    lower_rev_growths = [round(g - 0.03, 4) for g in base_rev_growths]
    higher_rev_growths = [round(g + 0.03, 4) for g in base_rev_growths]

    drivers_config = [
        {
            "key": "options_growth_shift",
            "name": "Options Revenue Shift",
            "unit": "pp",
            "cases": [
                ("Lower", -0.10, "-10pp / yr (PFOF curb)"),
                ("Base", 0.0, "Base (20%→10%)"),
                ("Higher", 0.10, "+10pp / yr (0DTE surge)"),
            ]
        },
        {
            "key": "gross_margin",
            "name": "Gross Margin",
            "unit": "pp",
            "cases": [
                ("Lower", 0.9428, "94.28% (-100 bps)"),
                ("Base", 0.9528, "95.28% (Base)"),
                ("Higher", 0.9628, "96.28% (+100 bps)"),
            ]
        },
        {
            "key": "rev_growths",
            "name": "Total Platform Growth",
            "unit": "path (pp)",
            "cases": [
                ("Lower", lower_rev_growths, "17%→7% (-3pp)"),
                ("Base", base_rev_growths, "20%→10% (Base)"),
                ("Higher", higher_rev_growths, "23%→13% (+3pp)"),
            ]
        }
    ]

    # Run sensitivity analysis
    run_sensitivity_analysis(base_assumptions, drivers_config)


if __name__ == "__main__":
    main()
