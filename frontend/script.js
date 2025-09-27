// --- CONFIGURAÇÃO ---
const API_URL = 'http://127.0.0.1:8000';

// --- VARIÁVEL GLOBAL PARA GUARDAR O ACERVO COMPLETO ---
let acervoCompleto = [];

// --- SELETORES DE ELEMENTOS DO HTML ---
const plantasGrid = document.getElementById('plantas-grid');
const form = document.getElementById('planta-form');
// O seletor do 'planta-id' foi removido
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

// INCLUIR uma nova planta
const addPlanta = async (event) => {
    event.preventDefault();
    if (!form.checkValidity()) {
        alert("Por favor, preencha todos os campos obrigatórios.");
        return;
    }

    const plantaData = {
        nome_popular: nomePopularInput.value,
        nome_cientifico: nomeCientificoInput.value,
        familia: familiaInput.value,
        origem: origemInput.value,
        cuidados: cuidadosInput.value,
    };

    try {
        const response = await fetch(`${API_URL}/plantas/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(plantaData),
        });
        if (!response.ok) throw new Error('Erro ao adicionar planta');
        
        form.reset(); // Limpa o formulário
        fetchPlantas(); // Atualiza a lista
    } catch (error) {
        console.error(`Falha ao adicionar planta:`, error);
        alert('Não foi possível adicionar a planta.');
    }
};

// DELETAR uma planta
const deletePlanta = async (id) => {
    if (!confirm(`Tem certeza que deseja excluir esta planta da enciclopédia?`)) return;
    try {
        const response = await fetch(`${API_URL}/plantas/${id}`, { method: 'DELETE' });
        if (!response.ok) throw new Error('Erro ao deletar planta');
        fetchPlantas(); // Atualiza a lista
    } catch (error) {
        console.error(`Falha ao deletar planta:`, error);
        alert('Não foi possível deletar a planta.');
    }
};

// --- FUNÇÕES DA INTERFACE ---

// A função 'prepareEdit' foi removida
// A função 'clearForm' foi simplificada para ser apenas o reset do form
const clearForm = () => {
    form.reset();
};

// Mostra as plantas na tela
const displayPlantas = (plantas) => {
    plantasGrid.innerHTML = '';
    plantas.forEach(planta => {
        const card = document.createElement('div');
        card.className = 'planta-card';
        // O botão 'Editar' foi removido do HTML do card
        card.innerHTML = `
            <div class="card-content">
                <h3>${planta.nome_popular}</h3>
                <p><em>${planta.nome_cientifico}</em></p>
                <p><strong>Família:</strong> ${planta.familia}</p>
                <p><strong>Origem:</strong> ${planta.origem}</p>
                <div class="cuidados"><strong>Cuidados:</strong> ${planta.cuidados}</div>
            </div>
            <div class="card-actions">
                <button class="btn-delete">Excluir</button>
            </div>
        `;
        // Adiciona o evento apenas no botão de excluir
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
form.addEventListener('submit', addPlanta); // Agora o submit sempre adiciona
clearBtn.addEventListener('click', clearForm);
searchInput.addEventListener('input', handleSearch);