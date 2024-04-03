module LionsDen

using JSON
using HTTP
using Random
using DataFrames

export check_connection, load_data, train, check_status,
       fnormalize, fnormalize2, partitionDataSet, get_parameters, score,
       validate

#const HOST = "http://127.0.0.1:8000"
const HOST = "http://ec2-34-252-212-32.eu-west-1.compute.amazonaws.com:8000"

function sendRequest(url::String, body::Union{Nothing, Dict} = nothing)
    if isnothing(body)
        response = HTTP.post("$HOST/$url")
    else
        response = HTTP.post("$HOST/$url", [("Content-Type", "application/json")], json(body))
    end
    
    if response.status != 200
        return "HTTP error status!"
    end
    res = String(response.body)

    j = JSON.parse(res)
end

function check_connection()
    res = sendRequest("test")

    if res["message"] == "OK"
        return "OK"
    else
        return "Something is wrong!"
    end
end

function load_data(user::String, password::String, filename::String, x_variable::Vector{String}, y_variable::String)
    body = Dict("user" => user,
                "password" => password,
                "file_name" => filename,
                "x_variable" => x_variable,
                "y_variable" => y_variable)
    res = sendRequest("load", body)

    return res["message"]
end

function train(user::String, password::String, batch_size::Integer, max_itr::Integer, 
              alfa::AbstractFloat, opt::String, ansatz::String; 
              params=nothing, beta=nothing, beta2=nothing)
    if ansatz ∉ ["SU2", "SU2U4"]
        return "ERROR: Invalid ansatz."
    end
    if opt ∉ ["Eva", "Adam", "RMSprop", "Momentum", "StandardGD"]
        return "ERROR: Invalid optimization method."
    end
    if opt ∈ ["Adam", "RMSprop", "Momentum"] && isnothing(beta)
        return "ERROR: For optimizator $(opt) parameter β has be set."
    end
    if opt == "Adam" && isnothing(beta2)
        return "ERROR: For optimizator Adam parameter β2 has be set."
    end    

    body = Dict("user" => user,
                "password" => password,
                "batch_size" => batch_size,
                "max_itr" => max_itr,
                "alfa" => alfa,
                "opt" => opt,
                "ansatz" => ansatz)

    if !isnothing(params)
        body["params"] = params
    end
    if !isnothing(beta)
        body["beta"] = beta
    end
    if !isnothing(params)
        body["beta2"] = beta2
    end    

    res = sendRequest("train", body)

    return res["message"]
end

function check_status(user::String, password::String)
    body = Dict("user" => user, "password" => password)
    res = sendRequest("status", body)

    return res["message"]
end

function get_parameters(user::String, password::String)
    body = Dict("user" => user, "password" => password)
    res = sendRequest("get_parameters", body)

    return [convert(Float64, e) for e in res["message"]]
end

function score(user::String, password::String, ansatz::String, x, params)
    if ansatz ∉ ["SU2", "SU2U4"]
        return "ERROR: Invalid ansatz."
    end

    body = Dict("user" => user,
                "password" => password,
                "ansatz" => ansatz,
                "input_vec" => x,
                "params" => params)
    res = sendRequest("score", body)

    return res["message"]
end

function validate(user::String, password::String, filename::String, x_variable::Vector{String}, y_variable::String, ansatz::String, params)
    if ansatz ∉ ["SU2", "SU2U4"]
        return "ERROR: Invalid ansatz."
    end

    body = Dict("user" => user,
                "password" => password,
                "ansatz" => ansatz,
                "file_name" => filename,
                "x_variable" => x_variable,
                "y_variable" => y_variable,
                "params" => params)
    res = sendRequest("validate", body)

    return res["message"]
end


function fnormalize(df, name)
    vec = df[!, name]
    minval = minimum(vec)
    maxval = maximum(vec)
    spred = maxval - minval
    
    df[!, name] = (vec .- minval) ./ spred
end


function fnormalize2(df, name)
    v = parse.(Float64, df[df[!, name] .!= "", name])
    minval = minimum(v)
    maxval = maximum(v)
    spred = maxval - minval
    avg = (maxval + minval) / 2

    avg = string(avg)
    avg = avg[1:min(7, length(avg))]

    df[df[!, name] .== "", name] .= avg
    v = parse.(Float64, df[!, name])
    
    df[!, name] = (v .- minval) ./ spred
end

function partitionDataSet(data, at = 0.7)
    n = nrow(data)
    idx = shuffle(1:n)
    train_idx = view(idx, 1:floor(Int, at*n))
    test_idx = view(idx, (floor(Int, at*n)+1):n)
    data[train_idx,:], data[test_idx,:]
end

end # module LionsDen
