document.addEventListener('DOMContentLoaded', () => {
    let toast = document.querySelector('.toast')
    if (toast) {
        toast.style.opacity = "unset";

        toast.querySelector('button').addEventListener('click', () => {
            toast.remove()
        })
    }
})