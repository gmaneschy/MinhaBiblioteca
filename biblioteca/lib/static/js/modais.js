// Modal de Edição
function abrirModal(id, titulo, autor, editora, tradutor, genero, npaginas, ano, preco) {
    document.getElementById('modal').style.display = 'block';
    document.getElementById('modal-id').value = id;
    document.getElementById('modal-titulo').value = titulo;
    document.getElementById('modal-autor').value = autor;
    document.getElementById('modal-editora').value = editora;
    document.getElementById('modal-tradutor').value = tradutor;
    document.getElementById('modal-genero').value = genero;
    document.getElementById('modal-npaginas').value = npaginas;
    document.getElementById('modal-ano').value = ano;
    document.getElementById('modal-preco').value = preco;
}

function fecharModalEdicao() {
    document.getElementById('modal').style.display = 'none';
}

function salvarLivro(event) {
    event.preventDefault();

    const formData = {
        id: document.getElementById('modal-id').value,
        titulo: document.getElementById('modal-titulo').value,
        autor: document.getElementById('modal-autor').value,
        editora: document.getElementById('modal-editora').value,
        tradutor: document.getElementById('modal-tradutor').value,
        genero: document.getElementById('modal-genero').value,
        npaginas: document.getElementById('modal-npaginas').value,
        ano: document.getElementById('modal-ano').value,
        preco: document.getElementById('modal-preco').value
    };

    if (!formData.titulo || !formData.autor || !formData.editora) {
        alert('Por favor, preencha pelo menos Título, Autor e Editora.');
        return;
    }

    fetch(`/editar/${formData.id}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) throw new Error('Erro na resposta do servidor');
        return response.json();
    })
    .then(data => {
        if (data.id) {
            const linha = document.querySelector(`tr[data-id='${data.id}']`);
            if (linha) {
                linha.cells[0].textContent = data.titulo;
                linha.cells[1].textContent = data.autor;
                linha.cells[2].textContent = data.editora;
                linha.cells[3].textContent = data.tradutor;
                linha.cells[4].textContent = data.genero;
                linha.cells[5].textContent = data.npaginas;
                linha.cells[6].textContent = data.ano;
                linha.cells[7].textContent = data.preco;
            }
            fecharModalEdicao();

        // Dá um refresh suave após 500ms
        setTimeout(() => {
            location.reload();
        }, 100);
        } else {
            alert('Erro ao salvar: ' + (data.error || ''));
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao salvar livro: ' + error.message);
    });
}

// Modal de Anotações
function abrirModalAnotacoes(id, anotacoes) {
    document.getElementById('livro_id').value = id;
    document.getElementById('anotacoes').value = anotacoes !== 'None' ? anotacoes : '';
    document.getElementById('modalAnotacoes').style.display = 'block';
}

function fecharModalAnotacoes() {
    document.getElementById('modalAnotacoes').style.display = 'none';
}

document.getElementById('formAnotacoes').addEventListener('submit', function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    const livroId = formData.get('livro_id');
    const anotacoes = formData.get('anotacoes');

    fetch(this.action, {
        method: 'POST',
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        },
        body: formData
    })
    .then(response => {
        if (!response.ok) throw new Error('Erro no servidor');
        return response.json();
    })
    .then(data => {
        if (data.status === 'ok') {
            const anotacaoBtn = document.querySelector(`a[onclick*="abrirModalAnotacoes(${livroId}, "]`);
            if (anotacaoBtn) {
                anotacaoBtn.setAttribute('onclick', `abrirModalAnotacoes(${livroId}, '${anotacoes.replace(/'/g, "\\'")}')`);
            }
            fecharModalAnotacoes();
            alert('Anotações salvas com sucesso!');
        } else {
            throw new Error(data.erro || 'Erro ao salvar anotações');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert(error.message);
    });
});

function excluirLivro(id, url) {
    if (confirm("Tem certeza que deseja excluir este livro?")) {
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
            },
        })
        .then(response => {
            if (response.ok) {
                // Remove a linha da tabela ou recarrega
                document.querySelector(`tr[data-id="${id}"]`).remove();
            } else {
                alert('Erro ao excluir livro');
            }
        })
        .catch(error => {
            console.error('Erro:', error);
        });
    }
}

function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}