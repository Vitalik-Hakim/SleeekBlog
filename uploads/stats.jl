using Statistics
files_and_dirs = readdir(pwd())  

function count()
    global num =0
    for i in files_and_dirs
        if isfile(i)
            num +=1
        end
    end
end
count()
println(num)
