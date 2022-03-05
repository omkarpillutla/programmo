document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('form').onsubmit = () =>{
    
        const input = document.querySelector('#task');
    
        const li = document.createElement('li');
    
        li.innerHTML = input.value;
        
        document.querySelector('ul').append(li);


        

        return false;
    }
})