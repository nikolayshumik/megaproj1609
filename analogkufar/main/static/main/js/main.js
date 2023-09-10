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

function redirectToDetails(adId) {
    var detailsForm = document.createElement('form');
    detailsForm.action = "/details/";  // Update this with the correct URL path to the details view
    detailsForm.method = "get";
    detailsForm.className = "details-form";
    detailsForm.innerHTML = `
    {% csrf_token %}
    <input type="hidden" name="ad_id" value="${adId}">
    <button class="buttonMod btn-view-details">Посмотреть детали</button>
`;
    document.body.appendChild(detailsForm);
    detailsForm.submit();
}


window.addEventListener('scroll', function() {
    var footer = document.querySelector('footer');
    if (window.scrollY > 0) {
        footer.style.display = 'flex';
    } else {
        footer.style.display = 'none';
    }
});
