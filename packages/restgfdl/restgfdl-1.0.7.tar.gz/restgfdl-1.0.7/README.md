#pip install restgfdl   using the terminal or cmd propmt you can install at your end 


# api= rs.Function Name ('<END POINT>', '<API KEY >', xml=False, format_csv=False)
# result = api.Get_LastQuote('NSE','SBIN')
# print(result)



import restgfdl as rs

api= rs.GetLastQuote('<END POINT>', '<API KEY >', xml=False, format_csv=False)
result = api.Get_LastQuote('NSE','SBIN')
print(result)


import restgfdl as rs

api= rs.GetLastQuoteShort('<END POINT>', '<API KEY >', xml=False, format_csv=False)
result = api.Get_LastQuoteShort('NSE','SBIN')
print(result)

import restgfdl as rs

api= rs.GetLastQuoteShortWithClose('<END POINT>', '<API KEY >', xml=False, format_csv=False)
result = api.Get_LastQuoteShortWithClose('NSE','SBIN')
print(result)


import restgfdl as rs

api= rs.GetLastQuoteArray('<END POINT>', '<API KEY >', xml=False, format_csv=False)
result = api.GetLastQuoteArray('NFO','NIFTY-I+BANKNIFTY-I+FINNIFTY-I')
print(result)


import restgfdl as rs

api= rs.GetLastQuoteArrayShort('<END POINT>', '<API KEY >', xml=False, format_csv=False)
result = api.Get_LastQuoteArrayShort('NSE','NIFTY-I+BANKNIFTY-I+FINNIFTY-I')
print(result)

import restgfdl as rs

api= rs.GetLastQuoteArrayShortWithClose('<END POINT>', '<API KEY >', xml=False, format_csv=False)
result = api.Get_LastQuoteArrayShortWithClose('NSE','NIFTY-I+BANKNIFTY-I+FINNIFTY-I')
print(result)


import restgfdl as rs

api= rs.GetHistory('<END POINT>', '<API KEY >', xml=True, format_csv=False)
result = api.Get_History('NFO','NIFTY-I','Minute','1','10')  #without from and to parameter only with max count - max record will return 
print(result)


import restgfdl as rs

api= rs.GetHistory('<END POINT>', '<API KEY >', xml=True, format_csv=False)
result = api.Get_History('NFO','NIFTY-I','Minute','1','10','1723779900','1723802400')  #with max ,from and to parameter record will return max reocrd inbwtween those two from and to time frames .
print(result)


import restgfdl as rs

api= rs.GetSnapshot('<END POINT>', '<API KEY >', xml=True, format_csv=False)
result = api.Get_Snapshot('NFO','Minute','1','NIFTY-I+BANKNIFTY-I+FINNIFTY-I') 
print(result)

import restgfdl as rs

api= rs.GetStrikePrices('<END POINT>', '<API KEY >', xml=True, format_csv=False)
result = api.Get_StrikePrices('NFO','','NIFTY') 
print(result)

import restgfdl as rs

api= rs.GetServerInfo('<END POINT>', '<API KEY >', xml=True, format_csv=False)
result = api.Get_ServerInfo() 
print(result)

import restgfdl as rs

api= rs.GetProducts('<END POINT>', '<API KEY >', xml=True, format_csv=False)
result = api.Get_Products('NFO') 
print(result)

import restgfdl as rs

api= rs.GetOptionTypes('<END POINT>', '<API KEY >', xml=True, format_csv=False)
result = api.Get_OptionTypes('NFO') 
print(result)

import restgfdl as rs

api= rs.GetMarketMessages('<END POINT>', '<API KEY >', xml=True, format_csv=False)
result = api.Get_MarketMessages('NFO') 
print(result)


import restgfdl as rs

api= rs.GetExchangeMessages('<END POINT>', '<API KEY >', xml=True, format_csv=False)
result = api.Get_Exchange_Messages('NFO') 
print(result)


import restgfdl as rs

api= rs.GetLastQuoteOptionChain('<END POINT>', '<API KEY >', xml=True, format_csv=False)
result = api.Get_LastQuoteOptionChain('NFO','NIFTY','22AUG2024','CE') 
print(result)


import restgfdl as rs

api= rs.GetLastQuoteOptionGreeksChain('<END POINT>', '<API KEY >', xml=True, format_csv=False)
result = api.Get_LastQuoteOptionGreeksChain('NFO','NIFTY','22AUG2024','CE') 
print(result)

import restgfdl as rs

api= rs.GetLastQuoteOptionGreeks('<END POINT>', '<API KEY >', xml=True, format_csv=False)
result = api.Get_LastQuoteOptionGreeks('NFO','57660') 
print(result)

import restgfdl as rs

api= rs.GetLastQuoteArrayOptionGreeks('<END POINT>', '<API KEY >', xml=True, format_csv=False)
result = api.Get_LastQuoteArrayOptionGreeks('NFO','57660+57661+57662') 
print(result)

import restgfdl as rs

api= rs.GetInstruments('<END POINT>', '<API KEY >', xml=True, format_csv=False)
result = api.Get_Instruments('NFO','NIFTY','FUTIDX','CE','22AUG2024') #UPDATE ON BUILD WILL CHECK AFTER THAT 
print(result)

import restgfdl as rs

api= rs.GetInstrumentsOnSearch('<END POINT>', '<API KEY >', xml=True, format_csv=False)
result = api.Get_InstrumentsOnSearch('NFO','NIFTY','FUTIDX','CE','22AUG2024') #UPDATE ON BUILD WILL CHECK AFTER THAT 
print(result)


import restgfdl as rs

api= rs.GetInstrumentTypes('<END POINT>', '<API KEY >', xml=True, format_csv=False)
result = api.Get_InstrumentTypes('NFO') 
print(result)


import restgfdl as rs

api= rs.GetLimitation('<END POINT>', '<API KEY >', xml=True, format_csv=False)
result = api.Get_Limitation() 
print(result)


import restgfdl as rs

api= rs.GetExchangeSnapshot('<END POINT>', '<API KEY >', xml=True, format_csv=False)
result = api.Get_ExchangeSnapshot('NFO','Minute','1') 
print(result)


import restgfdl as rs

api= rs.GetExpiryDates('<END POINT>', '<API KEY >', xml=True, format_csv=False)
result = api.Get_ExpiryDates('NFO','','NIFTY') 
print(result)
