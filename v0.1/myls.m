function random_number = myls(a, b,n)
rand('seed',sum(100*clock))

    random_number = (double(b) - double(a)) * rand(n,2) + double(a);
end