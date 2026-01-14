document.addEventListener('DOMContentLoaded', function() {
    // Интерактивные звёзды в форме
    const starInputs = document.querySelectorAll('.star-rating-buttons input[type="radio"]');
    const starLabels = document.querySelectorAll('.star-rating-buttons .star-label');
    
    // Подсветка при наведении
    starLabels.forEach(label => {
        label.addEventListener('mouseenter', function() {
            const rating = this.querySelector('input').value;
            highlightStars(rating);
        });
        
        label.addEventListener('mouseleave', function() {
            const checkedInput = document.querySelector('.star-rating-buttons input:checked');
            if (checkedInput) {
                highlightStars(checkedInput.value);
            } else {
                resetStars();
            }
        });
    });
    
    // Подсветка при выборе
    starInputs.forEach(input => {
        input.addEventListener('change', function() {
            highlightStars(this.value);
        });
    });
    
    function highlightStars(rating) {
        starLabels.forEach(label => {
            const labelRating = label.querySelector('input').value;
            const stars = label.querySelector('.stars');
            
            if (labelRating <= rating) {
                // Заполненные звёзды
                stars.innerHTML = '';
                for (let i = 0; i < 5; i++) {
                    const star = document.createElement('i');
                    star.className = i < labelRating ? 'fas fa-star' : 'far fa-star';
                    stars.appendChild(star);
                }
                stars.style.color = '#ffc107';
            } else {
                // Пустые звёзды
                stars.innerHTML = '';
                for (let i = 0; i < 5; i++) {
                    const star = document.createElement('i');
                    star.className = i < labelRating ? 'fas fa-star' : 'far fa-star';
                    stars.appendChild(star);
                }
                stars.style.color = '#6c757d';
            }
        });
    }
    
    function resetStars() {
        starLabels.forEach(label => {
            const stars = label.querySelector('.stars');
            stars.style.color = '#6c757d';
        });
    }
    
    // Инициализация текущего выбора
    const checkedInput = document.querySelector('.star-rating-buttons input:checked');
    if (checkedInput) {
        highlightStars(checkedInput.value);
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Обработка формы избранного
    const favoriteForms = document.querySelectorAll('form[action*="toggle-favorite"]');
    
    favoriteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const url = this.action;
            
            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    // Показать сообщение
                    alert(data.message);
                    // Перезагрузить страницу
                    window.location.reload();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Fallback: отправить форму обычным способом
                this.submit();
            });
        });
    });
});