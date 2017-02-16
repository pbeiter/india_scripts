import numpy as np
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import pandas as pd

plt.style.use('ggplot')

### Data read-in

filename_wind 	= 'supply_curve_output_example.csv'
filename_upv 	= 'supply_curve_output_example.csv'
filename_csp 	= 'supply_curve_output_example.csv'



#col_labels = dat.iloc[:0,].columns[~dat.columns.str.contains('Unnamed:')]
#df.columns = df.iloc[0]
#df = df[1:]
#df = df.astype(float)

### LCOE calculation 
exrate = 66.9525	# 1 USD to IND rupee; Source: https://www.bloomberg.com/quote/USDINR:CUR (as of 02/15/2017)



def LCOE_calc(tech, filename, FCR, CAPEX_gen, FOM_gen, CAPEX_trans, FOM_trans, CAPEX_sub, CAPEX_rd, FOM_rd):

	# Data read-in
	df = pd.read_csv(filename, low_memory = False, header=1)

	df['dist_rd'] = np.random.randint(0,15, len(df))	# Distance to nearest road (km); NEEDS TO BE INCLUDED IN GIS output data file
	NCF = df['ncf']			# Net capacity factor (%)
	dist = df['dist_mi']	# Distance from point to grid (miles)
	dist_rd = df['dist_rd']	# Distance to nearest road (km)

	#LCOE1 = ((FCR * CAPEX + FOM)*1000/(CF * 8760)) // Source: ATB 2016
	#LCOE2 = ((CRF * ProFinFactor * ConFinFactor * (OCC * CapRegMult + GCC) + FOM) * 1000 / (CF * 8760)) // Source: ATB 2016

	df['LCOE_gen'] = (FCR * CAPEX_gen + FOM_gen)*1000 / (NCF * 8760)
	df['LCOE_trans'] = (dist*((FCR*CAPEX_trans + FOM_trans) + (FCR * CAPEX_sub))) / (NCF * 8760) # Two substations required
	df['LCOE_road'] = dist_rd*(FCR*CAPEX_rd + FOM_rd) / (NCF * 8760) # Shivani's formula is different in denominator (value of 50)?
	df['LCOE_tot'] = df['LCOE_gen'] + df['LCOE_trans'] + df['LCOE_road']

	df.to_csv('output_{}.csv'.format(tech))

##Wind

#Technology
lifetime = 25

#Finance parameters
inf =  0.05872 				# Inflation rate in 2015; Source: http://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?end=2015&locations=IN&start=1960&view=chart
dn = 0.108 					# discount rate (nominal) - is this nominal rate?
DF = 0.7 					# debt fraction
RROEn = 0.1276 				# Rate of return on equity (nominal); Same as "interest rate on term"? Is it in real dollars?
RROEr = (1+RROEn)/(1+inf) - 1	# Rate of return on equity (real)
In = 0.1326					# Interest rate (nominal); Same as "interest on working capital"?
Ir = (1+In)/(1+inf)-1		# Interest rate (real) - same as "Interest on working capital"?
TR = 0.40 					# Combined state/federal tax rate - what's the right tax rate in India?
PVD = 1.127					# Present Value of depreciation (MACRS schedule); what's the value for India?
ProFinFactor =  (1 - TR * PVD) / (1 - TR)	# Project finance factor

WACCn = DF*In*(1-TR)+(1-DF)*RROEn	# WACC (nominal) 
WACCr = ((1+((1-DF)*((1+RROEr)*(1+inf)-1)) + (DF*((1+Ir)*(1+inf)-1)*(1-TR))) / (1+inf)) - 1		# WACC (real)

CRFn = WACCn / (1 - (1 / (1 + WACCn)**lifetime))		# Capital recovery factor (nominal)
CRFr = WACCr / (1 - (1 / (1 + WACCr)**lifetime))		# Capital recovery factor (real)

FCR = CRFr * ProFinFactor	# Fixed charge rate; real or nominal?

# Expenditure items

CAPEX_gen = 950			# Capital expenditure for generation ($/kW)
FOM_gen = 1124/exrate 	# Fixed Operation and Maintenance ($/kW); 1,124 INR/kW converted (exchange rate as of 2/16/2017); is this the correct value? what about escalation (Deshmukh et al. 2016)? what about maintenance?

CAPEX_trans = 450 	# Capital expenditure for transmission ($/MW/km)
FOM_trans = 0 		# Fixed Operation and Maintenance for transmission ($/MW/km) What's the value?
CAPEX_sub	= (35000/2) * 2 	# $/substation (2 substations required; Source: Deshmukh et al. (2016)

CAPEX_rd = 407000 / 50	# Capital expenditure for roads ($/MW/km); assuming 50 MW of installed capacity per "Project Opportunity Area"; Source: Deshmukh et al. (2016); Is this correct? 
FOM_rd = 0		# Fixed Operations and Maintenance for roads ($/MW/km); what's the value?

LCOE_calc('wind', filename_wind, FCR, CAPEX_gen, FOM_gen, CAPEX_trans, FOM_trans, CAPEX_sub, CAPEX_rd, FOM_rd)

##UPV parameters

#Technology
lifetime = 25

#Finance parameters
inf =  0.05872 				# Inflation rate in 2015; Source: http://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?end=2015&locations=IN&start=1960&view=chart
dn = 0.108 					# discount rate (nominal) - is this nominal rate?
DF = 0.7 					# debt fraction
RROEn = 0.1276 				# Rate of return on equity (nominal); Same as "interest rate on term"? Is it in real dollars?
RROEr = (1+RROEn)/(1+inf) - 1	# Rate of return on equity (real)
In = 0.1326					# Interest rate (nominal)
Ir = (1+In)/(1+inf)-1		# Interest rate (real) - same as "Interest on working capital"?
TR = 0.40 					# Combined state/federal tax rate - what's the right tax rate in India?
PVD = 1.127					# Present Value of depreciation (MACRS schedule); what's the value for India?
ProFinFactor =  (1 - TR * PVD) / (1 - TR)	# Project finance factor

WACCn = DF*In*(1-TR)+(1-DF)*RROEn	# WACC (nominal) 
WACCr = ((1+((1-DF)*((1+RROEr)*(1+inf)-1)) + (DF*((1+Ir)*(1+inf)-1)*(1-TR))) / (1+inf)) - 1		# WACC (real)

CRFn = WACCn / (1 - (1 / (1 + WACCn)**lifetime))		# Capital recovery factor (nominal)
CRFr = WACCr / (1 - (1 / (1 + WACCr)**lifetime))		# Capital recovery factor (real)

FCR = CRFr * ProFinFactor	# Fixed charge rate; real or nominal?

# Expenditure items

CAPEX_gen = 810			# Capital expenditure for generation ($/kW)
FOM_gen = 700/exrate 	# Fixed Operation and Maintenance ($/kW); 1,124 INR/kW converted (exchange rate as of 2/16/2017); is this the correct value? what about escalation (Deshmukh et al. 2016)? what about maintenance?

CAPEX_trans = 450 	# Capital expenditure for transmission ($/MW/km)
FOM_trans = 0 		# Fixed Operation and Maintenance for transmission ($/MW/km) What's the value?
CAPEX_sub	= (35000/2) * 2 	# $/substation (2 substations required; Source: Deshmukh et al. (2016)

CAPEX_rd = 407000 / 50	# Capital expenditure for roads ($/MW/km); assuming 50 MW of installed capacity per "Project Opportunity Area"; Source: Deshmukh et al. (2016)
FOM_rd = 0		# Fixed Operations and Maintenance for roads ($/MW/km); what's the value?

LCOE_calc('UPV', filename_upv, FCR, CAPEX_gen, FOM_gen, CAPEX_trans, FOM_trans, CAPEX_sub, CAPEX_rd, FOM_rd)

##CSP parameters

#Technology
lifetime = 25

#Finance parameters
inf =  0.05872 					# Inflation rate in 2015; Source: http://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?end=2015&locations=IN&start=1960&view=chart
dn = 0.108 						# discount rate (nominal) - is this nominal rate?
DF = 0.7 						# debt fraction
RROEn = 0.1276 					# Rate of return on equity (nominal); Same as "interest rate on term"? Is it in real dollars?
RROEr = (1+RROEn)/(1+inf) - 1	# Rate of return on equity (real)
In = 0.1326						# Interest rate (nominal)
Ir = (1+In)/(1+inf)-1			# Interest rate (real) - same as "Interest on working capital"?
TR = 0.40 						# Combined state/federal tax rate - what's the right tax rate in India?
PVD = 1.127						# Present Value of depreciation (MACRS schedule); what's the value for India?
ProFinFactor =  (1 - TR * PVD) / (1 - TR)	# Project finance factor

WACCn = DF*In*(1-TR)+(1-DF)*RROEn	# WACC (nominal) 
WACCr = ((1+((1-DF)*((1+RROEr)*(1+inf)-1)) + (DF*((1+Ir)*(1+inf)-1)*(1-TR))) / (1+inf)) - 1		# WACC (real)

CRFn = WACCn / (1 - (1 / (1 + WACCn)**lifetime))		# Capital recovery factor (nominal)
CRFr = WACCr / (1 - (1 / (1 + WACCr)**lifetime))		# Capital recovery factor (real)

FCR = CRFr * ProFinFactor	# Fixed charge rate; real or nominal?

# Expenditure items

CAPEX_gen = 1850		# Capital expenditure for generation ($/kW)
FOM_gen = 1874/exrate 	# Fixed Operation and Maintenance ($/kW); 1,124 INR/kW converted (exchange rate as of 2/16/2017); is this the correct value? what about escalation (Deshmukh et al. 2016)? what about maintenance?

CAPEX_trans = 450 	# Capital expenditure for transmission ($/MW/km)
FOM_trans = 0 		# Fixed Operation and Maintenance for transmission ($/MW/km) What's the value?
CAPEX_sub	= (35000/2) * 2 	# $/substation (2 substations required; Source: Deshmukh et al. (2016)

CAPEX_rd = 407000 / 50	# Capital expenditure for roads ($/MW/km); assuming 50 MW of installed capacity per "Project Opportunity Area"; Source: Deshmukh et al. (2016)
FOM_rd = 0		# Fixed Operations and Maintenance for roads ($/MW/km); what's the value?

LCOE_calc('CSP', filename_csp, FCR, CAPEX_gen, FOM_gen, CAPEX_trans, FOM_trans, CAPEX_sub, CAPEX_rd, FOM_rd)