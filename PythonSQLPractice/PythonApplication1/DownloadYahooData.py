import requests
from bs4 import BeautifulSoup
import pandas as pd
import os 
import json
import pyodbc
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=PCM-9B51SQ2\JINGZHENDATABASE;'
                      'Database=Sample;'
                      'Trusted_Connection=yes;')
dir_path = os.path.dirname(os.getcwd())
filename = dir_path+'\\FTSE100Tickers.json'  
with open(filename,'r') as file_object:  
    data = json.loads(json.load(file_object)) 

Tickers=data['Tickers']
tempTicker=Tickers['0']
hdrs={"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"accept-encoding": "gzip, deflate, br",
"accept-language": "en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7",
"cache-control": "max-age=0",
"dnt": "1",
"sec-fetch-dest": "document",
"sec-fetch-mode": "navigate",
"sec-fetch-site": "none",
"sec-fetch-user": "?1",
"upgrade-insecure-requests": "1",
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"}
FullURL=("https://query1.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/RR.L?lang=en-US&region=US&symbol="
     +tempTicker
+"&padTimeSeries=true&type="
+"annualTaxEffectOfUnusualItems"
+"%2CtrailingTaxEffectOfUnusualItems"
+"%2CannualTaxRateForCalcs"
+"%2CtrailingTaxRateForCalcs"
+"%2CannualNormalizedEBITDA"
+"%2CtrailingNormalizedEBITDA"
+"%2CannualNormalizedDilutedEPS"
+"%2CtrailingNormalizedDilutedEPS"
+"%2CannualNormalizedBasicEPS"
+"%2CtrailingNormalizedBasicEPS"
+"%2CannualTotalUnusualItems"
+"%2CtrailingTotalUnusualItems"
+"%2CannualTotalUnusualItemsExcludingGoodwill"
+"%2CtrailingTotalUnusualItemsExcludingGoodwill"
+"%2CannualNetIncomeFromContinuingOperationNetMinorityInterest"
+"%2CtrailingNetIncomeFromContinuingOperationNetMinorityInterest"
+"%2CannualReconciledDepreciation"
+"%2CtrailingReconciledDepreciation"
+"%2CannualReconciledCostOfRevenue"
+"%2CtrailingReconciledCostOfRevenue"
+"%2CannualEBITDA%2CtrailingEBITDA"
+"%2CannualEBIT%2CtrailingEBIT"
+"%2CannualNetInterestIncome"
+"%2CtrailingNetInterestIncome"
+"%2CannualInterestExpense"
+"%2CtrailingInterestExpense"
+"%2CannualInterestIncome"
+"%2CtrailingInterestIncome"
+"%2CannualContinuingAndDiscontinuedDilutedEPS"
+"%2CtrailingContinuingAndDiscontinuedDilutedEPS"
+"%2CannualContinuingAndDiscontinuedBasicEPS"
+"%2CtrailingContinuingAndDiscontinuedBasicEPS"
+"%2CannualNormalizedIncome"
+"%2CtrailingNormalizedIncome"
+"%2CannualNetIncomeFromContinuingAndDiscontinuedOperation"
+"%2CtrailingNetIncomeFromContinuingAndDiscontinuedOperation"
+"%2CannualTotalExpenses%2CtrailingTotalExpenses"
+"%2CannualRentExpenseSupplemental%2CtrailingRentExpenseSupplemental"
+"%2CannualReportedNormalizedDilutedEPS%2CtrailingReportedNormalizedDilutedEPS"
+"%2CannualReportedNormalizedBasicEPS%2CtrailingReportedNormalizedBasicEPS"
+"%2CannualTotalOperatingIncomeAsReported"
+"%2CtrailingTotalOperatingIncomeAsReported"
+"%2CannualDividendPerShare"
+"%2CtrailingDividendPerShare"
+"%2CannualDilutedAverageShares"
+"%2CtrailingDilutedAverageShares"
+"%2CannualBasicAverageShares"
+"%2CtrailingBasicAverageShares"
+"%2CannualDilutedEPS+"
+"%2CtrailingDilutedEPS"
+"%2CannualDilutedEPSOtherGainsLosses"
+"%2CtrailingDilutedEPSOtherGainsLosses"
+"%2CannualTaxLossCarryforwardDilutedEPS"
+"%2CtrailingTaxLossCarryforwardDilutedEPS"
+"%2CannualDilutedAccountingChange"
+"%2CtrailingDilutedAccountingChange"
+"%2CannualDilutedExtraordinary"
+"%2CtrailingDilutedExtraordinary"
+"%2CannualDilutedDiscontinuousOperations"
+"%2CtrailingDilutedDiscontinuousOperations"
+"%2CannualDilutedContinuousOperations"
+"%2CtrailingDilutedContinuousOperations"
+"%2CannualBasicEPS"
+"%2CtrailingBasicEPS"
+"%2CannualBasicEPSOtherGainsLosses"
+"%2CtrailingBasicEPSOtherGainsLosses"
+"%2CannualTaxLossCarryforwardBasicEPS"
+"%2CtrailingTaxLossCarryforwardBasicEPS"
+"%2CannualBasicAccountingChange"
+"%2CtrailingBasicAccountingChange"
+"%2CannualBasicExtraordinary"
+"%2CtrailingBasicExtraordinary"
+"%2CannualBasicDiscontinuousOperations"
+"%2CtrailingBasicDiscontinuousOperations"
+"%2CannualBasicContinuousOperations"
+"%2CtrailingBasicContinuousOperations"
+"%2CannualDilutedNIAvailtoComStockholders"
+"%2CtrailingDilutedNIAvailtoComStockholders"
+"%2CannualAverageDilutionEarnings"
+"%2CtrailingAverageDilutionEarnings"
+"%2CannualNetIncomeCommonStockholders"
+"%2CtrailingNetIncomeCommonStockholders"
+"%2CannualOtherunderPreferredStockDividend"
+"%2CtrailingOtherunderPreferredStockDividend"
+"%2CannualPreferredStockDividends"
+"%2CtrailingPreferredStockDividends"
+"%2CannualNetIncome"
+"%2CtrailingNetIncome"
+"%2CannualMinorityInterests"
+"%2CtrailingMinorityInterests"
+"%2CannualNetIncomeIncludingNoncontrollingInterests"
+"%2CtrailingNetIncomeIncludingNoncontrollingInterests"
+"%2CannualNetIncomeFromTaxLossCarryforward"
+"%2CtrailingNetIncomeFromTaxLossCarryforward"
+"%2CannualNetIncomeExtraordinary"
+"%2CtrailingNetIncomeExtraordinary"
+"%2CannualNetIncomeDiscontinuousOperations"
+"%2CtrailingNetIncomeDiscontinuousOperations"
+"%2CannualNetIncomeContinuousOperations"
+"%2CtrailingNetIncomeContinuousOperations"
+"%2CannualEarningsFromEquityInterestNetOfTax"
+"%2CtrailingEarningsFromEquityInterestNetOfTax"
+"%2CannualTaxProvision+"
+"%2CtrailingTaxProvision"
+"%2CannualPretaxIncome"
+"%2CtrailingPretaxIncome"
+"%2CannualOtherIncomeExpense"
+"%2CtrailingOtherIncomeExpense"
+"%2CannualOtherNonOperatingIncomeExpenses"
+"%2CtrailingOtherNonOperatingIncomeExpenses"
+"%2CannualSpecialIncomeCharges"
+"%2CtrailingSpecialIncomeCharges"
+"%2CannualGainOnSaleOfPPE"
+"%2CtrailingGainOnSaleOfPPE"
+"%2CannualGainOnSaleOfBusiness"
+"%2CtrailingGainOnSaleOfBusiness"
+"%2CannualOtherSpecialCharges"
+"%2CtrailingOtherSpecialCharges"
+"%2CannualWriteOff+"
+"%2CtrailingWriteOff"
+"%2CannualImpairmentOfCapitalAssets"
+"%2CtrailingImpairmentOfCapitalAssets"
+"%2CannualRestructuringAndMergernAcquisition"
+"%2CtrailingRestructuringAndMergernAcquisition"
+"%2CannualSecuritiesAmortization"
+"%2CtrailingSecuritiesAmortization"
+"%2CannualEarningsFromEquityInterest"
+"%2CtrailingEarningsFromEquityInterest"
+"%2CannualGainOnSaleOfSecurity"
+"%2CtrailingGainOnSaleOfSecurity"
+"%2CannualNetNonOperatingInterestIncomeExpense"
+"%2CtrailingNetNonOperatingInterestIncomeExpense"
+"%2CannualTotalOtherFinanceCost"
+"%2CtrailingTotalOtherFinanceCost"
+"%2CannualInterestExpenseNonOperating"
+"%2CtrailingInterestExpenseNonOperating"
+"%2CannualInterestIncomeNonOperating"
+"%2CtrailingInterestIncomeNonOperating"
+"%2CannualOperatingIncome"
+"%2CtrailingOperatingIncome"
+"%2CannualOperatingExpense"
+"%2CtrailingOperatingExpense"
+"%2CannualOtherOperatingExpenses"
+"%2CtrailingOtherOperatingExpenses"
+"%2CannualOtherTaxes+"
+"%2CtrailingOtherTaxes"
+"%2CannualProvisionForDoubtfulAccounts"
+"%2CtrailingProvisionForDoubtfulAccounts"
+"%2CannualDepreciationAmortizationDepletionIncomeStatement"
+"%2CtrailingDepreciationAmortizationDepletionIncomeStatement"
+"%2CannualDepletionIncomeStatement"
+"%2CtrailingDepletionIncomeStatement"
+"%2CannualDepreciationAndAmortizationInIncomeStatement"
+"%2CtrailingDepreciationAndAmortizationInIncomeStatement"
+"%2CannualAmortization+"
+"%2CtrailingAmortization"
+"%2CannualAmortizationOfIntangiblesIncomeStatement"
+"%2CtrailingAmortizationOfIntangiblesIncomeStatement"
+"%2CannualDepreciationIncomeStatement"
+"%2CtrailingDepreciationIncomeStatement"
+"%2CannualResearchAndDevelopment"
+"%2CtrailingResearchAndDevelopment"
+"%2CannualSellingGeneralAndAdministration"
+"%2CtrailingSellingGeneralAndAdministration"
+"%2CannualSellingAndMarketingExpense"
+"%2CtrailingSellingAndMarketingExpense"
+"%2CannualGeneralAndAdministrativeExpense"
+"%2CtrailingGeneralAndAdministrativeExpense"
+"%2CannualOtherGandA"
+"%2CtrailingOtherGandA"
+"%2CannualInsuranceAndClaims"
+"%2CtrailingInsuranceAndClaims"
+"%2CannualRentAndLandingFees"
+"%2CtrailingRentAndLandingFees"
+"%2CannualSalariesAndWages"
+"%2CtrailingSalariesAndWages"
+"%2CannualGrossProfit"
+"%2CtrailingGrossProfit"
+"%2CannualCostOfRevenue"
+"%2CtrailingCostOfRevenue"
+"%2CannualTotalRevenue"
+"%2CtrailingTotalRevenue"
+"%2CannualExciseTaxes"
+"%2CtrailingExciseTaxes"
+"%2CannualOperatingRevenue"
+"%2CtrailingOperatingRevenue"
+"&merge=false&period1=493590046&period2=1630404859&corsDomain=finance.yahoo.com")
URL=("https://query1.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/RR.L?lang=en-US&region=US&symbol="
     +tempTicker
+"&padTimeSeries=true&type="
+"%2CannualNetIncomeContinuousOperations"
+"&merge=false&period1=493590046&period2=1630404859&corsDomain=finance.yahoo.com")



r = requests.get(URL,headers=hdrs)
encodedText = r.text.encode("utf-8")
soup = BeautifulSoup(encodedText)
jsonResult=json.loads(soup.currentTag.currentTag.currentTag.currentTag.text)
results=jsonResult["timeseries"]['result'][0]['annualNetIncomeContinuousOperations']
date=results[0]['asOfDate']
value=results[0]['reportedValue']['raw']
print('Finished')
