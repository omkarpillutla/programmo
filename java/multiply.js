function multiply(n1, n2) {
    console.log(n1, n2)
    if(typeof(n2) == "undefined")
    {
        function double(n2) {
           console.log(n1*n2);
        }
        return double;
    }
    return console.log(n1*n2);
}

const double = multiply(2)
double(2)
