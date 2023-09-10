document.addEventListener('DOMContentLoaded', function () {
    var openModalButton = document.getElementById('openModal');
    var modal = document.getElementById('myModal');

    openModalButton.addEventListener('click', function () {
        modal.style.display = 'block';
    });

    modal.addEventListener('click', function (event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});
