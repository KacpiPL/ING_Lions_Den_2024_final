using CSV
using DataFrames
using LionsDen

SCcsv = CSV.File("loan_data.csv", missingstring = "null")
df = DataFrame(SCcsv)

y_variable = "Loan_Status"
varialbes = [n for n in names(df) if n ∉ [y_variable, "Loan_ID"]]
ds = df[!, [y_variable, varialbes...]]



ds[!, y_variable] = 1.0 .* (ds[!, y_variable] .== "Y")
ds[!, :Gender] = 1.0 .* (ds[!, :Gender] .== "Male") + .5 .* (ds[!, :Gender] .== "")
ds[!, :Married] = 1.0 .* (ds[!, :Married] .== "Yes")
ds[!, :Self_Employed] = 1.0 .* (ds[!, :Self_Employed] .== "Yes")
ds[!, :Dependents] = 1.0 .* (ds[!, :Dependents] .== "3+") + 2/3 .* (ds[!, :Dependents] .== "2") + 1/3 .* (ds[!, :Dependents] .== "1")
ds[!, :Education] = 1.0 .* (ds[!, :Education] .== "Graduate")
fnormalize(ds, "CoapplicantIncome")
fnormalize(ds, "LoanAmount")
fnormalize(ds, "ApplicantIncome")
ds[!, :Loan_Amount_Term]
fnormalize2(ds, "Loan_Amount_Term")
ds[!, :Credit_History] = 1.0 .* (ds[!, :Credit_History] .== "1.0") + .5 .* (ds[!, :Credit_History] .== "")
ds[!, :Property_Area] = 1.0 .* (ds[!, :Property_Area] .== "Urban") + .5 .* (ds[!, :Property_Area] .== "Semiurban")

x_variables = ["Dependents", "Education", "Self_Employed", "ApplicantIncome", "CoapplicantIncome", "LoanAmount", "Loan_Amount_Term", "Credit_History", "Property_Area"]
selected_vars = ds[!, [y_variable, x_variables...]]



# the data
trainData, testData = partitionDataSet(selected_vars, 0.7)


CSV.write("/home/rpracht/tmp/cvs/trainData.csv", trainData)
CSV.write("/home/rpracht/tmp/cvs/testData.csv", testData)

# "trainDataBig.csv"

trainDataBig = vcat([trainData for i in 1:1200]...)
CSV.write("/home/rpracht/tmp/cvs/trainDataBig.csv", trainDataBig)
