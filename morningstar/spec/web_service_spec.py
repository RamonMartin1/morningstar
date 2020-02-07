from enum import Enum


class FieldCode(Enum):
    """ Morningstar Field Codes (Request)

    Morningstar_Morningstar_Web_Services_Specification_v5.0.pdf - Page 68
    """

    Symbol = "H1"
    Exchange = "H2"
    SecurityType = "H3"
    RootSymbol = "S2"
    ListedCurrency = "S9"
    CompanyName = "S12"
    AdditionalCompanyName = "S13"
    ISIN = "S19"
    ContractName = "S31"
    Country = "S34"
    LocalInstrumentCode = "S33"
    PrimaryMIC = "S676"
    WKN = "S722"
    MorningstarPerformanceID = "D2124"
    CUSIP = "S1012"
    SEDOL = "S1013"
    MorningstarIndustry = "S1041"
    MorningstarGroup = "S1042"
    MorningstarSector = "S1043"
    MorningstarID = "S3059"
    VenueFIGICode = "S2995"
    CountryFIGICode = "S1405"
    ShareClassFIGICode = "S1407"
    GlobalIDInvestmentType = "S1735"
    Dividend = "S1364"
    DividendCurrency = "S3096"
    DividendRecordDate = "S3094"
    SplitRatioNew = "S734"
    SplitRatioOld = "S735"
    SplitDate = "S740"
    SymbolAtExchange = "S726" # ticker at given exchange, e.g. UBSG for UBS at SIX exchange
    Description = "S3379" 
    MarketCapitaliztion = "S1315"
    DividendYield = "S1086"
    PriceEarningsRatio = "S1367"
    DebtEquityRatio = "S534"
    PriceBookRatio = "S1081"
    ListingStartDate = "S555"
    ListingEndDate = "S556"
    PrimaryExchange = "S724"

class FieldNames(Enum):
    """ Morningstar Field Names (Response)

    Morningstar_Morningstar_Web_Services_Specification_v5.0.pdf - Page 68
    """
    Symbol = "Symbol"
    Exchange = "Exchange"
    SecurityType = "Security Type"
    # RootSymbol = ""
    ListedCurrency = "Listed Currency"
    CompanyName = "Company name"
    # AdditionalCompanyName = ""
    ISIN = "ISIN code"
    # ContractName = ""
    Country = "Country"
    LocalInstrumentCode = "Local instrument cod"
    PrimaryMIC = ""
    # WKN = ""
    MorningstarPerformanceID = "MS Performance ID"
    # CUSIP =
    # SEDOL = ""
    MorningstarIndustry = "Morningstar Industry"
    MorningstarGroup = "Morningstar Group Na"
    MorningstarSector = "Morningstar Sector N"
    MorningstarID = "MS Investment ID (Se"
    VenueFIGICode = "FIGI code"
    CountryFIGICode = "FIGI country code"
    ShareClassFIGICode = "Shareclass-level FIG"
    GlobalIDInvestmentType = "Global ID investment"
    Dividend = "Dividend per share"
    DividendCurrency = "The currency of the "
    DividendRecordDate = "The Record date of a "
    SplitRatioNew = "Ratio New - Corporat"
    SplitRatioOld = "Ratio Old - Corporat"
    SplitDate = "Effective Date - Cor"
    SymbolAtExchange = "EDI Local flag" 
    Description = "MS Medium Business D" 
    MarketCapitaliztion = "Market Cap"
    DividendYield = "Dividend Yield"
    PriceEarningsRatio = "PE Ratio"
    DebtEquityRatio = "Debt to equity ratio"
    PriceBookRatio = "Price to Book"
    ListingStartDate = "Listing start date ("
    ListingEndDate = "Listing end date (st"
    PrimaryExchange = "EDI Primary Exchange"

    # Additional Fields?
    # "Listing market for t":"182",


class FilterTag(Enum):
    """ Morningstar filters to be attached to the request

    Morningstar_Morningstar_Web_Services_Specification_v5.0.pdf - Page 67
    """
    Symbol = "symbol"
    Exchange = "exchange"
    SecurityType = "security"
    RootSymbol = "rootsymbol"
    ListedCurrency = "currency"
    CompanyName = "name"
    ISIN = "isin"
    PrimaryMIC = "mic"
    MorningstarPerformanceID = "perfid"
    CUSIP = "cusip"
    SEDOL = "sedol"
    MorningstarID = "investmentID"
    VenueFIGICode = "VenueFigi"
    CountryFIGICode = "CountryFigi"
    ShareClassFIGICode = "ShareClassFigi"
    GlobalIDInvestmentType = "GIDInvestmentType"
