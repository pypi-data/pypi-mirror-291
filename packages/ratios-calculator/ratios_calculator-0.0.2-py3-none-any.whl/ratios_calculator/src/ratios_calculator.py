#######New Dataframe
#######Graphs for each year



import numpy as np 
import pandas as pd 
import re
import os

balance_sheet_file_name = input("Enter the balance sheet file path (xlsx): ")
if not os.path.exists(balance_sheet_file_name):
        print("File does not exist.")
        exit()
income_statement_file_name = input("Enter the income statement file path (xlsx): ")
if not os.path.exists(balance_sheet_file_name):
        print("File does not exist.")
        exit()
price_file_name = input("Enter the stock price history file path (xlsx): ")
if not os.path.exists(balance_sheet_file_name):
        print("File does not exist.")
        exit()

df_price = pd.read_excel(price_file_name, skiprows = 15)
df_balance_sheet = pd.read_excel(balance_sheet_file_name)
df_income_statement = pd.read_excel(income_statement_file_name)
is_copy = df_income_statement.copy()
# print(df_income_statement.iloc[:,0])

def unit_conversion(df_balance_sheet, df_income_statement):
    is_unit = df_income_statement.iloc[-1, 0].split()[3].lower()
    bs_unit = df_balance_sheet.iloc[-1, 0].split()[3].lower()

    conversion_factors = {
        'thousands': 1,
        'millions': 1e3,
        'billions': 1e6,
        'trillions': 1e9
    }

    # Ensure factor defaults to 1 if units do not match expected values
    factor = conversion_factors.get(is_unit, 1) / conversion_factors.get(bs_unit, 1) if is_unit in conversion_factors and bs_unit in conversion_factors else 1
    # print(factor)

    skip_keywords = ['EPS', 'Shares Outstanding']

    def convert_row(row):
        # Check if the first cell in the row contains any skip keywords
        if any(keyword in str(row.iloc[0]) for keyword in skip_keywords):
            return row  # Return the row unchanged if it should be skipped
        else:
            # Apply conversion factor to numeric values in the row
            return row.apply(lambda x: x * factor if isinstance(x, (int, float)) else x)
    
    # Apply the convert_row function to each row in the DataFrame
    df_income_statement_converted = df_income_statement.apply(convert_row, axis=1)
    return df_income_statement_converted



df_income_statement = unit_conversion(df_balance_sheet, df_income_statement)

# print(df_income_statement.iloc[46:55, 1])

def fetch_line_data(df, line_title):
    """Reads the data of specific category on balance sheet
    Args: 
        df: balance sheet data
        line_title: title of the category
    
    Returns:
        A list of the data of the desired balance sheet category
    """
    # return df[df.iloc[:, 0].str.contains(re.escape(line_title), na=False, case=False, regex=True)]
    line_data = df[df.iloc[:, 0].str.contains(re.escape(line_title), na=False, case=False, regex=True)]
    if not line_data.empty:
        return line_data.iloc[0, 1:].tolist()
    else:
        return "N/A"

def get_years(data):
    """
    Tries to identify a row containing years formatted as 'MONTH 'YY' and returns them sorted from most recent to least recent.

    Args:
        balance_sheet_file_name: The balance sheet Excel file data which has been already read.

    Returns:
        A sorted list of years on the balance sheet, from most recent to least recent.
    """
    year_pattern = "[A-Z]{3} '\\d{2}"
    for index, row in data.iterrows():
        if row.astype(str).str.contains(year_pattern, regex=True, na=False).any():
            years = [2000 + int(cell.split("'")[1]) for cell in row[1:] if pd.notna(cell)]
            return sorted(set(years), reverse=True)  

    raise ValueError("No row with valid years found in the balance sheet.")

def get_year_and_month(data):
    year_pattern = "[A-Z]{3} '\\d{2}"
    for index, row in data.iterrows():
        if row.astype(str).str.contains(year_pattern, regex=True, na=False).any():
            years = [cell for cell in row[1:] if pd.notna(cell)]
    return years


def align_columns(df_balance_sheet, df_income_statement):
    """
    Aligns the columns of income statement to match those of the balance sheet based on year columns identified.

    Args:
        df_balance_sheet (pd.DataFrame): DataFrame of the balance sheet.
        df_income_statement (pd.DataFrame): DataFrame of the income statement.

    Returns:
        pd.DataFrame: Modified income statement with aligned columns.
    """
    # Identify year columns in both DataFrames
    bs_years = get_years(df_balance_sheet)
    is_years = get_years(df_income_statement)

    # Convert to sets for easy comparison
    set_bs_years = set(bs_years)
    set_is_years = set(is_years)

    # Find year columns in the income statement not in the balance sheet
    years_to_drop = list(set_is_years - set_bs_years)

    year_pattern = "[A-Z]{3} '\\d{2}"
    converted_years = {str(year % 100) for year in years_to_drop}
    columns_to_drop = []
    for index, row in df_income_statement.iterrows():
        if row.astype(str).str.contains(year_pattern, regex=True, na=False).any():
            years = [cell for cell in row if pd.notna(cell) and str(cell).split("'")[1] in converted_years]
    columns_to_drop.extend(years)

    mask = df_income_statement.isin(columns_to_drop).any()
    # Drop these columns
    df_income_statement.drop(columns=df_income_statement.columns[mask], inplace=True)
    
    return df_income_statement

def get_price_for_year_end(data): 
    """Gets the price of the stock at the last day of each year, and puts them in a dictionary.

    Args:
        data: Company stock price data (price_data from above).

    Returns:
        A dictionary with year as key and stock price at end of year as value. 
    """
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)
    last_day_each_year = data.resample('YE').last()
    last_day_each_year.reset_index(inplace=True)
    last_day_each_year['Year'] = last_day_each_year['Date'].dt.strftime('%Y')
    print(last_day_each_year[['Date', 'Price']])
    price_dict = last_day_each_year.set_index('Year')['Price'].to_dict()
    return price_dict


def get_price_for_date(date, data):
    month, year_suffix = date.split()
    year_suffix = year_suffix.replace("'", "")
    full_year = f"20{year_suffix}"
    full_date_str = f"01 {month} {full_year}"
    date = pd.to_datetime(full_date_str, format='%d %b %Y').strftime('%B %Y')  # Note the uppercase 'Y' for four-digit years
    month_year_filter = data['Date'].dt.strftime('%B %Y')== date
    filtered_data = data[month_year_filter]
    mean_price = np.mean(filtered_data['Price'])
    return mean_price

def ratios_of_each_year(numerator_term, denominator_term, ratio_name, df_balance_sheet):
    ratio_name_dic = {}
    years_list = get_year_and_month(df_balance_sheet)
    for index in range (len(years_list)):
        if not isinstance(numerator_term, list) or not isinstance(denominator_term, list):
            ratio_name_dic[f'{ratio_name}{years_list[index]}'] = "N/A"
        else:
            ratio_name_dic[f'{ratio_name}{years_list[index]}'] = round(numerator_term[index]/denominator_term[index], 3) if denominator_term[index] != 0 else "N/A"
    return ratio_name_dic



def perform_financial_analysis(df_balance_sheet, df_income_statement, df_price):
    """Determines data based on the focus of analysis provided by user input.
    
    Args:
        df (pd.DataFrame): DataFrame containing balance sheet data.
    
    Returns:
        tuple: A tuple containing lists of data for assets and liabilities based on the analysis focus.
    """
    df_income_statement = unit_conversion(df_balance_sheet, df_income_statement)

    matched_income_statement = align_columns(df_balance_sheet, df_income_statement)
    most_recent_year = get_year_and_month(df_balance_sheet)[0]
    previous_years = str(get_years(df_balance_sheet)[-1]) + "-" + str(get_years(df_balance_sheet)[1])
    
    # LIQUIDITY
    total_current_assets = fetch_line_data(df_balance_sheet, 'Total Current Assets')
    total_current_liabilities = fetch_line_data(df_balance_sheet, 'Total Current Liabilities')
    inventories = fetch_line_data(df_balance_sheet, 'Inventories')
    Cash_and_Equivalents = fetch_line_data(df_balance_sheet, 'Cash & Short-Term Investments')

    dict_liq_current = ratios_of_each_year(total_current_assets, total_current_liabilities, 'Current Ratio', df_balance_sheet)
    dict_liq_quick = ratios_of_each_year((np.array(total_current_assets) - np.array(inventories)).tolist(), total_current_liabilities, 'Quick Ratio', df_balance_sheet)
    dict_liq_cash = ratios_of_each_year(Cash_and_Equivalents, total_current_liabilities, 'Cash Ratio', df_balance_sheet)

    dict_liq = {**dict_liq_current, **dict_liq_quick, **dict_liq_cash}
      
    # SOLVENCY
    total_liabilities = fetch_line_data(df_balance_sheet, 'Total Liabilities')
    total_shareholders_equity = fetch_line_data(df_balance_sheet, "Total Shareholders' Equity")
    operating_income = fetch_line_data(matched_income_statement, 'EBIT (Operating Income)')
    interest_expense = fetch_line_data(matched_income_statement, 'Interest Expense')

    dict_solv_Debt_to_Equity = ratios_of_each_year(total_liabilities, total_shareholders_equity, 'Debt to Equity Ratio', df_balance_sheet)
    dict_solv_Interest_Coverage = ratios_of_each_year(operating_income, interest_expense, 'Interest Coverage Ratio', df_balance_sheet)

    dict_solv = {**dict_solv_Debt_to_Equity, **dict_solv_Interest_Coverage}

    # EFFICIENCY
    fixed_assets = fetch_line_data(df_balance_sheet, 'Fixed Assets')
    sales = fetch_line_data(matched_income_statement, 'Sales')
    total_assets = fetch_line_data(df_balance_sheet, 'Total Assets')
    cost_of_goods = fetch_line_data(matched_income_statement, 'Cost of Goods Sold (COGS) incl. D&A')
    average_inventories = fetch_line_data(df_balance_sheet, 'Inventories')
    dict_eff_Asset_Turnover = ratios_of_each_year(sales, total_assets, 'Asset Turnover Ratio', df_balance_sheet)
    dict_eff_Inventory_Turnover = ratios_of_each_year(cost_of_goods, average_inventories, 'Inventory Turnover Ratio', df_balance_sheet)
    dict_eff_Fixed_Asset_Turnover = ratios_of_each_year(sales, fixed_assets, 'Fixed Asset Turnover Ratio', df_balance_sheet)

    dict_eff = {**dict_eff_Asset_Turnover, **dict_eff_Inventory_Turnover, **dict_eff_Fixed_Asset_Turnover}
    

    # PROFITABILITY
    net_income = fetch_line_data(matched_income_statement, 'Net Income')
    comprehensive_income = fetch_line_data(df_income_statement, 'Comprehensive Income - Hedging Gain/Loss')
    ebitda = fetch_line_data(df_income_statement, 'EBITDA')
    net_sales = fetch_line_data(matched_income_statement, 'Net Sales')
    gross_profit = fetch_line_data(matched_income_statement, 'Gross Profit')
    operating_profit = fetch_line_data(matched_income_statement, 'Operating Profit')
    total_liabilities = fetch_line_data(df_balance_sheet, 'Total Liabilities')

    dict_prof_ROA = ratios_of_each_year(net_income, total_assets, 'Return on Assets ROA', df_balance_sheet)
    dict_prof_ROE = ratios_of_each_year(net_income, total_shareholders_equity, 'Return on Equity ROE', df_balance_sheet)
    dict_prof_Comprehensive_ROA_rec = ratios_of_each_year(comprehensive_income, total_assets, 'Comprehensive - ROA', df_balance_sheet)
    dict_prof_Comprehensive_ROE_rec = ratios_of_each_year(comprehensive_income, total_shareholders_equity, 'Comprehensive - ROE', df_balance_sheet)
    dict_prof_Gross_Profit_Margin = ratios_of_each_year(gross_profit, sales, 'Gross Profit Margin', df_balance_sheet)
    dict_prof_Operating_Profit_Margin = ratios_of_each_year(operating_profit, sales, 'Operating Profit Margin', df_balance_sheet)
    dict_prof_EBITDA_Margin = ratios_of_each_year(ebitda, sales, 'EBITDA Margin', df_balance_sheet)
    dict_prof_Net_Profit_Margin = ratios_of_each_year(net_income, sales, 'Net Profit Margin', df_balance_sheet)
    dict_prof_Return_on_Invested_Capital = ratios_of_each_year(operating_profit, np.array(total_liabilities) + np.array(total_shareholders_equity).tolist(), 'Return on Invested Capital', df_balance_sheet)
    

    dict_prof = {**dict_prof_ROA, **dict_prof_ROE, **dict_prof_Comprehensive_ROA_rec, **dict_prof_Comprehensive_ROE_rec, **dict_prof_Gross_Profit_Margin, **dict_prof_Operating_Profit_Margin, **dict_prof_EBITDA_Margin, **dict_prof_Net_Profit_Margin, **dict_prof_Return_on_Invested_Capital}

    # Market Performance Context
    # PE Ratio
    dict_MP = {}
    years = get_year_and_month(df_balance_sheet)
    EPS_diluted = fetch_line_data(matched_income_statement, 'EPS (diluted)')
    EPS_basic = fetch_line_data(matched_income_statement, "EPS (basic)")
    stock_prices_of_years = [get_price_for_date(year, df_price) for year in years]
    dict_MP_P_E_Ratio = ratios_of_each_year(stock_prices_of_years, EPS_basic, 'Price to Earnings Ratio (P/E)', df_balance_sheet)
    dict_MP_Reverse_P_E = ratios_of_each_year(EPS_diluted, stock_prices_of_years, 'Reverse PE Ratio', df_balance_sheet)
    dict_MP_P_d_E_Ratio = ratios_of_each_year(stock_prices_of_years, EPS_diluted, 'Price to Diluted Earnings Ratio', df_balance_sheet)
    dict_MP_Reverse_P_d_E_Ratio = ratios_of_each_year(EPS_diluted, stock_prices_of_years, 'Reverse Diluted PE Ratio', df_balance_sheet)
    
    # Market Book Ratio
    Book_Value_per_Share = fetch_line_data(df_balance_sheet, 'Book Value per Share')
    dict_MP_M_B_Ratio = ratios_of_each_year(stock_prices_of_years, Book_Value_per_Share, 'Market to Book Ratio', df_balance_sheet)
    
    
    dict_MP = {**dict_MP_P_E_Ratio, **dict_MP_Reverse_P_E, **dict_MP_P_d_E_Ratio, **dict_MP_Reverse_P_d_E_Ratio, **dict_MP_M_B_Ratio}
    
    # LEVERAGE
    Minority_Interest = fetch_line_data(df_balance_sheet, "Minority Interest Under Canadian GAAP")
    
    dict_lev_Debt_ratio = ratios_of_each_year(total_liabilities, total_assets, 'Debt Ratio', df_balance_sheet)
    dict_lev_Alt_debt_ratio = ratios_of_each_year(total_liabilities, Minority_Interest, 'Alternative Debt Ratio', df_balance_sheet)
    dict_lev_Equity_ratio = ratios_of_each_year(total_shareholders_equity, total_assets, 'Equity Ratio', df_balance_sheet)

    dict_lev = {**dict_lev_Debt_ratio, **dict_lev_Alt_debt_ratio, **dict_lev_Equity_ratio}

    # COVERAGE
    EBIT = fetch_line_data(matched_income_statement, 'EBIT (Operating Income)')
    interest_expense = fetch_line_data(matched_income_statement, 'Interest Expense')
    depreciation_amortization = fetch_line_data(matched_income_statement, 'Depreciation & Amortization Expense')
    CMLTD = fetch_line_data(df_balance_sheet, 'ST Debt & Curr. Portion LT Debt')
    operating_cash_flow = fetch_line_data(matched_income_statement, 'Operating Cash Flow')

    dict_cov_interest_coverage = ratios_of_each_year(EBIT, interest_expense, 'Interest Coverage Ratio', df_balance_sheet)
    dict_cov_fixed_charge_covereage = ratios_of_each_year(EBIT, (np.array(interest_expense) + np.array(CMLTD)).tolist(), 'Fixed-Charge Coverage Ratio', df_balance_sheet)
    dict_cov_cash_flow_coverage = ratios_of_each_year((np.array(net_income) + np.array(depreciation_amortization)).tolist(), CMLTD, 'Cash Flow Coverage Ratio', df_balance_sheet)
    dict_cov_operating_cash_flow = ratios_of_each_year(operating_cash_flow, total_current_liabilities, 'Operating Cash Flow Ratio', df_balance_sheet)

    dict_cov = {**dict_cov_interest_coverage, **dict_cov_fixed_charge_covereage, **dict_cov_cash_flow_coverage, **dict_cov_operating_cash_flow}

    # Creating DataFrames
    liquidity_df = pd.DataFrame(list(dict_liq.items()), columns=['Metric', 'Value'])

    liquidity_df['Focus'] = 'Liquidity'

    solvency_df = pd.DataFrame(list(dict_solv.items()), columns=['Metric', 'Value'])
    solvency_df['Focus'] = 'Solvency'

    efficiency_df = pd.DataFrame(list(dict_eff.items()), columns=['Metric', 'Value'])
    efficiency_df['Focus'] = 'Efficiency'

    profitability_df = pd.DataFrame(list(dict_prof.items()), columns=['Metric', 'Value'])
    profitability_df['Focus'] = 'Profitability'

    market_performance_df = pd.DataFrame(list(dict_MP.items()), columns=['Metric', 'Value'])
    market_performance_df['Focus'] = 'Market Performance'

    leverage_df = pd.DataFrame(list(dict_lev.items()), columns=['Metric', 'Value'])
    leverage_df['Focus'] = 'Leverage'

    coverage_df = pd.DataFrame(list(dict_cov.items()), columns=['Metric', 'Value'])
    coverage_df['Focus'] = 'Coverage'

    df_combined = pd.concat([liquidity_df, solvency_df, efficiency_df, profitability_df, market_performance_df, leverage_df, coverage_df], ignore_index=True)
    
    # The focus is only displayed next to the first term
    # df_combined['Focus'] = df_combined['Focus'].where(df_combined['Focus'] != df_combined['Focus'].shift(), "")
    
    df_combined = df_combined[['Focus', 'Metric', 'Value']]

    # Display the Entire DataFrame
    pd.set_option('display.max_rows', None)  
    pd.set_option('display.max_columns', None)  
    pd.set_option('display.width', None)  
    pd.set_option('display.max_colwidth', None)  


############# NEW DATAFRAME ##############
    year_pattern = re.compile(r"[A-Z]{3} '\d{2}")
    year_range_pattern = re.compile(r"\d{4}-\d{4}")


    def extract_time_period(metric):
        # Find all matches of the year pattern
        match = year_pattern.findall(metric)
        if match:
            # If a match is found, return the last occurrence
            return match[-1]
        # If no match is found, return 'Unknown' or a default value
        elif any(year_range_pattern.findall(metric)):
            return year_range_pattern.search(metric).group()
        return 'Unknown'
    
    def clean_metric_name(metric):
        metric = year_pattern.sub('', metric)
        # Remove any year range like "2014-2022" from the metric name
        metric = year_range_pattern.sub('', metric)
        # Strip any remaining leading or trailing whitespace
        return metric.strip()

    df_combined['Time'] = df_combined['Metric'].apply(extract_time_period)
    df_combined['Metric'] = df_combined['Metric'].apply(clean_metric_name)  

    df_combined['Metric'] = df_combined['Focus'] + "_" + df_combined['Metric']
    df_combined.drop(columns='Focus', inplace=True)  # Drop the original 'Focus' column as it's now part of 'Metric'
    print(df_combined)

    # Pivot the table to form a DataFrame with a multi-level column index
    result_df = df_combined.pivot_table(
        index='Time',
        columns='Metric',
        values='Value',
        aggfunc='first'
    )

    # Optionally, you can create a more explicit multi-level column header
    result_df.columns = pd.MultiIndex.from_tuples(
        [(col.split('_')[0], col.split('_')[1]) for col in result_df.columns], names=['Focus', 'Metric']
    )

    result_df.reset_index(inplace=True)  # Ensure 'Time' is a column for the operations
    result_df['Time'] = pd.to_datetime(result_df['Time'].str.replace("'", ""), format='%b %y')
    result_df.sort_values('Time', ascending=False, inplace=True)
    result_df['Time'] = result_df['Time'].dt.strftime('%b \'%y')

    # print(result_df['Time'])

    # Save to CSV
    result_df.to_csv('ratios.csv', index=False)

    # Display the DataFrame
    # print(result_df)  
    # ratio_names = result_df.columns.get_level_values(1).unique().tolist()
    ratio_names = [' - '.join(col) if isinstance(col, tuple) else col for col in result_df.columns][1:]
    # print(ratio_names)

    # Now, ratio_names contains all the unique ratio names

    # Return the DataFrame for further use
    return result_df



df_ratios = perform_financial_analysis(df_balance_sheet, df_income_statement, df_price)
print(df_ratios)


