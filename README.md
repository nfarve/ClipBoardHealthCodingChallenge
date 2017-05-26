# ClipBoardHealthCodingChallenge
Coding Challenge for ClipBoard Health 

Current implementation process a CSV file and standardizes:
-  the hourly rate (looks for rates described as yearly, biweekly, monthly, weekly, monthly and daily salary)
-  ratio of nurses to patients (searches for ratios given as 1:5, 1-5, 1 to 5 and takes the first value that matches these expressions)
-  experience (finds just the number in the string or takes the average if several values are given

It also places the education level, department and location (using geopy to determine latitude and longitude) in a mongodb database. 

You can query these results using the following API handles:
-  api/records => lists all of the records
-  api/records/department/:departmentid => lists records matching a given department
-  api/records/education/:educationid => lists records matching a given education
-  api/records/salary/:direction/:salaryamount => lists records above or below a salary amount (:direction should be set to "above" or "below")
-  api/records/patientToNurseRatio/:direction/:ratio => lists records above or below a ratio of nurses to patients (:direction should be set to "above" or "below")
-  api/records/experience/:direction/:experience => lists records above or below a number of years of experience (:direction should be set to "above" or "below")
