// --- CONFIGURAÇÃO ---
const API_URL = 'http://127.0.0.1:8000';

// --- VARIÁVEL GLOBAL PARA GUARDAR O ACERVO COMPLETO ---
let acervoCompleto = [];

// --- SELETORES DE ELEMENTOS DO HTML ---
const plantasGrid = document.getElementById('plantas-grid');
const form = document.getElementById('planta-form');
const plantaIdInput = document.getElementById('planta-id');
const nomePopularInput = document.getElementById('nome_popular');
const nomeCientificoInput = document.getElementById('nome_cientifico');
const familiaInput = document.getElementById('familia');
const origemInput = document.getElementById('origem');
const cuidadosInput = document.getElementById('cuidados');
const clearBtn = document.getElementById('clear-btn');
const searchInput = document.getElementById('search-input');

// --- FUNÇÕES DA API ---

// LER todo o acervo da API
const fetchPlantas = async () => {
    try {
        const response = await fetch(`${API_URL}/plantas/`);
        if (!response.ok) throw new Error('Erro ao buscar plantas');
        acervoCompleto = await response.json();
        displayPlantas(acervoCompleto);
    } catch (error) {
        console.error('Falha ao buscar plantas:', error);
        plantasGrid.innerHTML = '<p style="color: red;">Não foi possível carregar o acervo. A API está rodando?</p>';
    }
};

// SALVAR (Criar ou Atualizar) uma planta
const savePlanta = async (event) => {
    event.preventDefault();
    if (!form.checkValidity()) {
        alert("Por favor, preencha todos os campos obrigatórios.");
        return;
    }

    const id = plantaIdInput.value;
    const plantaData = {
        nome_popular: nomePopularInput.value,
        nome_cientifico: nomeCientificoInput.value,
        familia: familiaInput.value,
        origem: origemInput.value,
        cuidados: cuidadosInput.value,
    };

    const method = id ? 'PUT' : 'POST';
    const url = id ? `${API_URL}/plantas/${id}` : `${API_URL}/plantas/`;

    try {
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(plantaData),
        });
        if (!response.ok) throw new Error(`Erro ao ${id ? 'atualizar' : 'adicionar'} planta`);
        
        clearForm();
        fetchPlantas();
    } catch (error) {
        console.error(`Falha ao salvar planta:`, error);
        alert('Não foi possível salvar a planta.');
    }
};

// DELETAR uma planta
const deletePlanta = async (id) => {
    if (!confirm(`Tem certeza que deseja excluir esta planta da enciclopédia?`)) return;
    try {
        const response = await fetch(`${API_URL}/plantas/${id}`, { method: 'DELETE' });
        if (!response.ok) throw new Error('Erro ao deletar planta');
        fetchPlantas();
    } catch (error) {
        console.error(`Falha ao deletar planta:`, error);
        alert('Não foi possível deletar a planta.');
    }
};

// --- FUNÇÕES DA INTERFACE ---

const clearForm = () => {
    plantaIdInput.value = '';
    form.reset();
};

const prepareEdit = (planta) => {
    plantaIdInput.value = planta.id;
    nomePopularInput.value = planta.nome_popular;
    nomeCientificoInput.value = planta.nome_cientifico;
    familiaInput.value = planta.familia;
    origemInput.value = planta.origem;
    cuidadosInput.value = planta.cuidados;
    form.scrollIntoView({ behavior: 'smooth' });
};

const displayPlantas = (plantas) => {
    plantasGrid.innerHTML = '';
    plantas.forEach(planta => {
        const card = document.createElement('div');
        card.className = 'planta-card';
        card.innerHTML = `
            <div class="card-content">
                <h3>${planta.nome_popular}</h3>
                <p><em>${planta.nome_cientifico}</em></p>
                <p><strong>Família:</strong> ${planta.familia}</p>
                <p><strong>Origem:</strong> ${planta.origem}</p>
                <div class="cuidados"><strong>Cuidados:</strong> ${planta.cuidados}</div>
            </div>
            <div class="card-actions">
                <button class="btn-edit">Editar</button>
                <button class="btn-delete">Excluir</button>
            </div>
        `;
        // Adiciona os eventos nos botões de cada card
        card.querySelector('.btn-edit').addEventListener('click', () => prepareEdit(planta));
        card.querySelector('.btn-delete').addEventListener('click', () => deletePlanta(planta.id));
        plantasGrid.appendChild(card);
    });
};

const handleSearch = (event) => {
    const searchTerm = event.target.value.toLowerCase();
    const plantasFiltradas = acervoCompleto.filter(planta => 
        planta.nome_popular.toLowerCase().includes(searchTerm) || 
        planta.nome_cientifico.toLowerCase().includes(searchTerm) ||
        planta.familia.toLowerCase().includes(searchTerm)
    );
    displayPlantas(plantasFiltradas);
};

// --- EVENT LISTENERS ---
document.addEventListener('DOMContentLoaded', fetchPlantas);
form.addEventListener('submit', savePlanta);
clearBtn.addEventListener('click', clearForm);
searchInput.addEventListener('input', handleSearch);