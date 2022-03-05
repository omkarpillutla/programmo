function filter(arr, fn) 
{
    let res = []
    
    for (let i = 0; i < arr.length; i++)
    {
        if (fn(arr[i]) == true) {
            res.push(arr[i])
        }
    }
    
    return res
}

arr = [0, 1, 2, 3]

function greaterThanOne(n) {
    return n > 1;
}

let result = filter(arr, greaterThanOne)
console.log(result)