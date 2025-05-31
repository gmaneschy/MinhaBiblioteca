document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('modalConfig');
    const configBtn = document.getElementById('config-btn');

    // Abrir modal
    configBtn.addEventListener('click', function () {
        modal.style.display = 'block';
    });

    // Fechar modal ao clicar fora do conteúdo
    window.addEventListener('click', function (e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Aplicar as preferências ao carregar a página
    aplicarPreferenciasColunas();

    // Adicionar eventos aos checkboxes
    document.querySelectorAll('.col-toggle').forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            const colIndex = parseInt(this.dataset.col);
            const config = JSON.parse(localStorage.getItem('colunasVisiveis')) || {};
            config[colIndex] = this.checked;
            localStorage.setItem('colunasVisiveis', JSON.stringify(config));
            aplicarPreferenciasColunas();
        });
    });
});

// Aplica a exibição de colunas com base nas preferências salvas
function aplicarPreferenciasColunas() {
    const config = JSON.parse(localStorage.getItem('colunasVisiveis')) || {};

    for (let i = 0; i < 8; i++) {
        if (config[i] === undefined) config[i] = true;
    }

    document.querySelectorAll('.col-toggle').forEach(checkbox => {
        const colIndex = parseInt(checkbox.dataset.col);
        checkbox.checked = config[colIndex];

        document.querySelectorAll(`th:nth-child(${colIndex + 1}), td:nth-child(${colIndex + 1})`).forEach(el => {
            el.style.display = config[colIndex] ? '' : 'none';
        });
    });

    localStorage.setItem('colunasVisiveis', JSON.stringify(config));
}

// Fecha o modal manualmente
function fecharModalConfig() {
    document.getElementById('modalConfig').style.display = 'none';
}

// Reseta para todas as colunas visíveis
function resetarColunas() {
    const config = {};
    for (let i = 0; i < 8; i++) {
        config[i] = true;
    }
    localStorage.setItem('colunasVisiveis', JSON.stringify(config));
    aplicarPreferenciasColunas();
}

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}