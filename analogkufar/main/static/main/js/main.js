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
    detailsForm.action = "/details/";  // Замените это на правильный URL путь к представлению деталей
    detailsForm.method = "get";
    detailsForm.className = "details-form";
    detailsForm.innerHTML = `
    {% csrf_token %}
    <input type="hidden" name="ad_id" value="${adId}">
    <button class="buttonMod btn-view-details">Посмотреть детали</button>
`;
    document.body.appendChild(detailsForm);
    detailsForm.submit();

    // Добавляем стиль CSS для изменения курсора
    var div = document.querySelector("div"); // Выбираете нужный div или измените селектор на ваш выбор
    div.style.cursor = "pointer";
}


window.addEventListener('scroll', function() {
    var footer = document.querySelector('footer');
    if (window.scrollY > 0) {
        footer.style.display = 'flex';
    } else {
        footer.style.display = 'none';
    }
});


document.addEventListener('DOMContentLoaded', function() {
  var footer = document.getElementById('footer');

  window.addEventListener('scroll', function() {
    // Check if the user has scrolled to the bottom of the page
    if ((window.innerHeight + window.pageYOffset) >= document.body.offsetHeight) {
      footer.style.display = 'block';
    } else {
      footer.style.display = 'none';
    }
  });
});


//работа с окном покупки
document.getElementById("buyButton").addEventListener("click", function(event) {
  event.preventDefault(); // Предотвратить действие по умолчанию
  document.getElementById("buyModal").style.display = "block"; // Открыть окно
});
//кнопка закрыть в окне
document.getElementById("closeButton").addEventListener("click", function() {
  document.getElementById("buyModal").style.display = "none"; // Закрыть окно
});


$(document).ready(function() {
    $('.formsupport').submit(function(e) {
        e.preventDefault();

        $.ajax({
            url: '',
            type: 'POST',
            data: $(this).serialize(),
            success: function(response) {
                $('.form-container').html(response);  // Заменяем содержимое контейнера на сообщение об успехе
            },
            error: function(xhr, status, error) {
                // Обработка ошибки
            }
        });
    });
});