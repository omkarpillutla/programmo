function reduce(arr, fn) {
    let res = arr[0];

    for (let i = 1; i < arr.length; i++) {
        res = fn(res, arr[i])
    }
    
    return res;
}

let arr = [1, 2, 3, 4]

function sum(x,y) {
    return x + y
}

let result = reduce(arr, sum)
console.log(result)