(function () {
    var form = document.getElementById('pantry-form');
    if (!form) return;

    var countEl = document.getElementById('ingredient-count');
    var checkboxes = form.querySelectorAll('input[name="ingredient"]');
    var choices = form.querySelectorAll('.chip__input');
    var previewEl = document.getElementById('selected-ingredients-preview');

    function chipLabel(input) {
        var label = input.closest('.chip');
        var face = label && label.querySelector('.chip__face');
        return face ? face.textContent.trim() : input.value;
    }

    function syncChipState(input) {
        var label = input.closest('.chip');
        if (!label) return;
        label.classList.toggle('is-selected', input.checked);
    }

    function renderPreview(selected) {
        if (!previewEl) return;

        previewEl.innerHTML = '';

        if (selected.length === 0) {
            var empty = document.createElement('span');
            empty.className = 'choice-summary__empty';
            empty.textContent = 'Pick at least one ingredient';
            previewEl.appendChild(empty);
            return;
        }

        selected.slice(0, 5).forEach(function (name) {
            var item = document.createElement('span');
            item.className = 'choice-summary__pill';
            item.textContent = name;
            previewEl.appendChild(item);
        });

        if (selected.length > 5) {
            var more = document.createElement('span');
            more.className = 'choice-summary__more';
            more.textContent = '+' + String(selected.length - 5) + ' more';
            previewEl.appendChild(more);
        }
    }

    function updateCount() {
        var n = 0;
        var selected = [];
        checkboxes.forEach(function (cb) {
            syncChipState(cb);
            if (cb.checked) {
                n += 1;
                selected.push(chipLabel(cb));
            }
        });
        if (countEl) countEl.textContent = String(n);
        renderPreview(selected);
    }

    checkboxes.forEach(function (cb) {
        cb.addEventListener('change', updateCount);
    });

    choices.forEach(function (input) {
        syncChipState(input);

        input.addEventListener('change', function () {
            if (input.type === 'radio') {
                form.querySelectorAll('input[name="' + input.name + '"]').forEach(syncChipState);
            } else {
                syncChipState(input);
            }
        });

        input.addEventListener('pointerdown', function () {
            var label = input.closest('.chip');
            if (label) label.classList.add('is-pressing');
        });

        ['pointerup', 'pointercancel', 'blur'].forEach(function (eventName) {
            input.addEventListener(eventName, function () {
                var label = input.closest('.chip');
                if (label) label.classList.remove('is-pressing');
            });
        });
    });

    form.addEventListener('submit', function (e) {
        var selected = 0;
        checkboxes.forEach(function (cb) {
            if (cb.checked) selected += 1;
        });
        if (selected === 0) {
            e.preventDefault();
            if (countEl) {
                countEl.textContent = '0 — pick at least one';
                countEl.parentElement.style.color = 'var(--dew-danger)';
            }
        }
    });

    updateCount();
})();
