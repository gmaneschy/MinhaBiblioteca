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

    // Filtros por coluna
    columnFilters.forEach(input => {
        input.addEventListener('input', filterTable);
    });

    // Botão de limpar filtros
    const clearButton = document.getElementById('clear-filters');

    if (clearButton) {
        clearButton.addEventListener('click', () => {
            // Limpa o campo de busca geral
            if (searchInput) {
                searchInput.value = '';
            }

            // Limpa os filtros por coluna
            columnFilters.forEach(input => {
                input.value = '';
            });

            // Reaplica a filtragem (vai mostrar tudo)
            filterTable();
        });
    }

    columnFilters.forEach(input => {
        input.addEventListener('input', filterTable);
    });
});

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}