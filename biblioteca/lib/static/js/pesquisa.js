document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-input');

    // Seleciona todos os inputs com a classe .column-filter que tenham data-column
    const columnFilters = Array.from(document.querySelectorAll('.column-filter[data-column]'));

    function filterTable() {
        const searchTerm = searchInput?.value.toLowerCase() || '';

        // Cria um mapa de filtros por coluna: { índice: valor }
        const filters = {};
        columnFilters.forEach(input => {
            const colIndex = parseInt(input.dataset.column);
            filters[colIndex] = input.value.toLowerCase();
        });

        document.querySelectorAll('tbody tr').forEach(row => {
            const cells = row.querySelectorAll('td');
            let shouldShow = true;

            // Filtro geral
            if (searchTerm && !Array.from(cells).some(td => td.textContent.toLowerCase().includes(searchTerm))) {
                shouldShow = false;
            }

            // Filtros por coluna
            for (const [index, value] of Object.entries(filters)) {
                if (value && !cells[index]?.textContent.toLowerCase().includes(value)) {
                    shouldShow = false;
                    break;
                }
            }

            row.style.display = shouldShow ? '' : 'none';
        });
    }

    // Eventos
    if (searchInput) {
        searchInput.addEventListener('input', filterTable);
    }

    columnFilters.forEach(input => {
        input.addEventListener('input', filterTable);
    });
});

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}