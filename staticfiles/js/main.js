document.addEventListener('DOMContentLoaded', function() {
    // Интерактивные звёзды в форме оценки маршрута
    const ratingSection = document.querySelector('.rating-section .star-rating-buttons');
    if (ratingSection) {
        const starInputs = ratingSection.querySelectorAll('input[type="radio"]');
        const starLabels = ratingSection.querySelectorAll('.star-label');
        
        // Подсветка при наведении
        starLabels.forEach(label => {
            label.addEventListener('mouseenter', function() {
                const rating = this.querySelector('input').value;
                highlightStars(rating, starLabels);
            });
            
            label.addEventListener('mouseleave', function() {
                const checkedInput = ratingSection.querySelector('input:checked');
                if (checkedInput) {
                    highlightStars(checkedInput.value, starLabels);
                } else {
                    resetStars(starLabels);
                }
            });
        });
        
        // Подсветка при выборе
        starInputs.forEach(input => {
            input.addEventListener('change', function() {
                highlightStars(this.value, starLabels);
            });
        });
        
        function highlightStars(rating, labels) {
            labels.forEach(label => {
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
        
        function resetStars(labels) {
            labels.forEach(label => {
                const stars = label.querySelector('.stars');
                stars.style.color = '#6c757d';
            });
        }
        
        // Инициализация текущего выбора
        const checkedInput = ratingSection.querySelector('input:checked');
        if (checkedInput) {
            highlightStars(checkedInput.value, starLabels);
        }
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Обработка формы избранного
    const favoriteForms = document.querySelectorAll('form[action*="toggle_favorite"]');
    
    favoriteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const url = this.action;
            const button = this.querySelector('button');
            
            fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.message) {
                    // Динамически обновляем кнопку
                    if (data.is_favorite) {
                        button.innerHTML = '<i class="fas fa-heart me-2"></i> Удалить из избранного';
                        button.classList.remove('btn-outline-danger');
                        button.classList.add('btn-danger');
                    } else {
                        button.innerHTML = '<i class="far fa-heart me-2"></i> Добавить в избранное';
                        button.classList.remove('btn-danger');
                        button.classList.add('btn-outline-danger');
                    }
                    
                    // Показываем уведомление
                    showNotification(data.message, 'success');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Fallback: отправить форму обычным способом
                this.submit();
            });
        });
    });
    
    // Функция для показа уведомлений
    function showNotification(message, type = 'info') {
        // Удаляем старые уведомления
        const oldNotifications = document.querySelectorAll('.custom-notification');
        oldNotifications.forEach(notification => notification.remove());
        
        // Создаем уведомление
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} custom-notification alert-dismissible fade show`;
        notification.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Автоматически скрываем через 3 секунды
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 3000);
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Функция для настройки прогресс-бара
    function setupProgressBar() {
        const progressContainer = document.querySelector('.hike-progress-container');
        if (!progressContainer) return;
        
        const progressBar = progressContainer.querySelector('.hike-progress-bar');
        const progressText = progressContainer.querySelector('.hike-progress-text');
        
        if (progressBar && progressText) {
            // Получаем значение из data-атрибута
            const score = parseInt(progressContainer.dataset.score) || 0;
            const width = Math.min(Math.max(score, 0), 100);
            
            // Устанавливаем ширину
            progressBar.style.width = width + '%';
            
            // Устанавливаем класс цвета
            progressBar.classList.remove('progress-score-low', 'progress-score-medium', 'progress-score-high');
            if (score >= 80) {
                progressBar.classList.add('progress-score-high');
            } else if (score >= 60) {
                progressBar.classList.add('progress-score-medium');
            } else {
                progressBar.classList.add('progress-score-low');
            }
        }
    }
    
    // Запускаем настройку
    setupProgressBar();
    
    // Также настраиваем при изменении размера окна
    window.addEventListener('resize', setupProgressBar);
});