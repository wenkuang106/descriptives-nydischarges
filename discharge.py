import pandas as pd
import statistics
import scipy.stats
from tableone import TableOne
import numpy as np

sparcs = pd.read_csv(r'data\Hospital_Inpatient_Discharges__SPARCS_De-Identified___2016.csv')
sparcs.shape
sparcs.columns

##### Data Cleaning ##### 

## removing all special characters and whitespaces 
sparcs.columns = sparcs.columns.str.replace('[^A-Za-z0-9]+', '_')
## turning all column names into lowercase for easy coding
sparcs.columns = sparcs.columns.str.lower()
sparcs.columns
sparcs.drop([
    'operating_certificate_number',
    'facility_id',
    'zip_code_3_digits',
    'race',
    'discharge_year',
    'apr_drg_description',
    'ccs_diagnosis_description',
    'ccs_procedure_description',
    'apr_mdc_description',
    'apr_severity_of_illness_description',
    'apr_medical_surgical_description',
    'payment_typology_2',
    'payment_typology_3',
], inplace=True, axis=1)
sparcs.columns
sparcs.rename(columns={'health_service_area': 'service area','facility_name':'hospital name'}, inplace=True)
sparcs.columns = sparcs.columns.str.replace('[^A-Za-z0-9]+', '_')
sparcs.columns

sparcs['length_of_stay'] = np.where(sparcs['length_of_stay']==('120 +'), '120', sparcs['length_of_stay'])
sparcs['length_of_stay'] = sparcs['length_of_stay'].astype('int')

sparcs_demographic = sparcs[[
    'age_group',
    'gender',
    'ethnicity',
]]
sparcs_codes = sparcs[[
    'ccs_diagnosis_code',
    'ccs_procedure_code',
    'apr_drg_code',
    'apr_mdc_code',
    'apr_severity_of_illness_code'
]]
sparcs_indicators = sparcs[[
    'abortion_edit_indicator',
    'emergency_department_indicator'
]]

sparcs_demographic.dropna()
sparcs_codes.dropna()
sparcs_indicators.dropna()

#### Descriptive Statistics #### 

sparcs_demographic.describe()
sparcs_codes.describe()
sparcs_indicators.describe()

groupby_er_indicator = sparcs_indicators.groupby('emergency_department_indicator')
groupby_er_indicator.count()

groupby_a_indicator = sparcs_indicators.groupby('abortion_edit_indicator')
groupby_a_indicator.count()

#### Charts via Tableone #### 
columns = ['total_charges', 'total_costs','length_of_stay','type_of_admission']
categorical = ['type_of_admission']
groupby = ['type_of_admission']
mytable = TableOne(sparcs, columns=columns, categorical=categorical, groupby=groupby, pval=False)
print(mytable.tabulate(tablefmt = "fancy_grid"))
mytable.to_csv('data/mytable_type_of_admission.csv')

columns = ['age_group', 'gender','ethnicity']
categorical = ['gender','ethnicity','age_group']
groupby = ['gender']
mytable = TableOne(sparcs, columns=columns, categorical=categorical, groupby=groupby, pval=False)
print(mytable.tabulate(tablefmt = "fancy_grid"))
mytable.to_csv('data/mytable_demographics.csv')