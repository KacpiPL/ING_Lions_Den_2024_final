using RDatasets
using CSV
using DataFrames
using LionsDen

# iris - data set
iris = dataset("datasets", "iris")
iris = filter(row -> row.Species != "virginica", iris)
# normalize
for n in names(iris)
    if n != "Species"
        fnormalize(iris, n)
    end
end
# final variable
iris[!, "Species"] = 1.0 .* (iris[!, "Species"] .== "setosa"); nothing

x_variables = [n for n in names(iris) if n != "Species"]
y_variable = "Species"

# the data
trainData, testData = partitionDataSet(iris, 0.7)

# trainData 70
# testData 30

CSV.write("/home/rpracht/tmp/cvs/trainIris.csv", trainData)
CSV.write("/home/rpracht/tmp/cvs/testIris.csv", testData)
