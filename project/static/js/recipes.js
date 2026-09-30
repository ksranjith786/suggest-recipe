(function () {
    function bindRecipeImages(root) {
        var scope = root || document;
        scope.querySelectorAll('.recipe-card__img:not([data-img-bound])').forEach(function (img) {
            img.setAttribute('data-img-bound', '1');

            function showFallback() {
                img.remove();
            }

            img.addEventListener('error', showFallback);

            if (img.complete && img.naturalWidth === 0) {
                showFallback();
            }
        });
    }

    bindRecipeImages(document);

    var sentinel = document.getElementById('recipe-scroll-sentinel');
    var grid = document.getElementById('recipe-grid');
    var loadedCountEl = document.getElementById('recipe-loaded-count');
    var statusEl = document.getElementById('load-more-status');

    if (!sentinel || !grid) {
        return;
    }

    var moreUrl = sentinel.dataset.moreUrl;
    var nextPage = parseInt(sentinel.dataset.nextPage, 10) || 2;
    var hasMore = sentinel.dataset.hasMore === 'true';
    var loading = false;

    var idleEl = statusEl && statusEl.querySelector('.load-more-status__idle');
    var loadingEl = statusEl && statusEl.querySelector('.load-more-status__loading');
    var doneEl = statusEl && statusEl.querySelector('.load-more-status__done');
    var errorEl = statusEl && statusEl.querySelector('.load-more-status__error');

    function setStatus(state) {
        if (!statusEl) return;
        if (idleEl) idleEl.hidden = state !== 'idle';
        if (loadingEl) loadingEl.hidden = state !== 'loading';
        if (doneEl) doneEl.hidden = state !== 'done';
        if (errorEl) errorEl.hidden = state !== 'error';
    }

    function finishPagination() {
        hasMore = false;
        sentinel.remove();
        setStatus('done');
    }

    function loadMore() {
        if (!hasMore || loading || !moreUrl) {
            return;
        }

        loading = true;
        setStatus('loading');

        fetch(moreUrl + '?page=' + encodeURIComponent(String(nextPage)), {
            credentials: 'same-origin',
            headers: { Accept: 'application/json' },
        })
            .then(function (response) {
                if (response.status === 410) {
                    throw new Error('session');
                }
                if (!response.ok) {
                    throw new Error('http');
                }
                return response.json();
            })
            .then(function (data) {
                if (data.html) {
                    grid.insertAdjacentHTML('beforeend', data.html);
                    bindRecipeImages(grid);
                }

                if (loadedCountEl && typeof data.loaded === 'number') {
                    loadedCountEl.textContent = String(data.loaded);
                }

                hasMore = Boolean(data.has_more);
                nextPage = data.next_page || nextPage + 1;
                sentinel.dataset.nextPage = String(nextPage);
                sentinel.dataset.hasMore = hasMore ? 'true' : 'false';

                if (!hasMore) {
                    finishPagination();
                } else {
                    setStatus('idle');
                }
            })
            .catch(function () {
                setStatus('error');
            })
            .finally(function () {
                loading = false;
            });
    }

    if (typeof IntersectionObserver === 'undefined') {
        sentinel.removeAttribute('aria-hidden');
        sentinel.innerHTML = '<button type="button" class="btn-primary btn-primary--small">Load more recipes</button>';
        sentinel.querySelector('button').addEventListener('click', loadMore);
        return;
    }

    var observer = new IntersectionObserver(
        function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    loadMore();
                }
            });
        },
        { rootMargin: '240px 0px' }
    );

    observer.observe(sentinel);
})();
