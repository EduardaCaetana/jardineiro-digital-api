# interface.py
import streamlit as st
import requests
import datetime

API_URL = "http://127.0.0.1:8000"

st.set_page_config(layout="centered", page_title="Jardineiro Digital")
st.title("🌿 Jardineiro Digital")
st.caption("Sua assistente para cuidar de plantas!")

# --- Seção para criar entidades ---
with st.expander("📝 Cadastros Iniciais"):
    st.subheader("Cadastrar Novo Jardineiro")
    with st.form("form_jardineiro", clear_on_submit=True):
        nome_jardineiro = st.text_input("Seu Nome")
        email_jardineiro = st.text_input("Seu Email")
        submit_jardineiro = st.form_submit_button("Cadastrar Jardineiro")
        if submit_jardineiro:
            if nome_jardineiro and email_jardineiro:
                response = requests.post(f"{API_URL}/jardineiros/", json={"nome": nome_jardineiro, "email": email_jardineiro})
                if response.status_code == 201:
                    st.success("Jardineiro cadastrado com sucesso!")
                else:
                    st.error(f"Erro: {response.json().get('detail')}")
            else:
                st.warning("Preencha todos os campos.")
    
    st.subheader("Adicionar Nova Espécie à Enciclopédia")
    # Este formulário permite adicionar novas espécies à base de dados geral
    with st.form("form_especie", clear_on_submit=True):
        nome_popular = st.text_input("Nome Popular da Espécie")
        nome_cientifico = st.text_input("Nome Científico")
        instrucoes = st.text_area("Instruções de Cuidado")
        freq_rega = st.number_input("Frequência de Rega (em dias)", min_value=1, step=1)
        submit_especie = st.form_submit_button("Adicionar Espécie")
        if submit_especie:
            response = requests.post(f"{API_URL}/especies/", json={
                "nome_popular": nome_popular,
                "nome_cientifico": nome_cientifico,
                "instrucoes_de_cuidado": instrucoes,
                "frequencia_rega_dias": freq_rega
            })
            if response.status_code == 200:
                st.success("Nova espécie adicionada à enciclopédia!")
            else:
                st.error("Erro ao adicionar espécie.")


# --- Seção principal para gerenciar plantas ---
st.header("🏡 Meu Jardim")

jardineiro_id = st.number_input("Digite o ID do Jardineiro para ver suas plantas", min_value=1, step=1)

if jardineiro_id:
    # Busca as plantas do jardineiro na API
    response_plantas = requests.get(f"{API_URL}/jardineiros/{jardineiro_id}/plantas/")
    if response_plantas.status_code == 200:
        plantas = response_plantas.json()

        if not plantas:
            st.info("Você ainda não cadastrou nenhuma planta. Adicione uma abaixo!")
        else:
            st.subheader("Minhas Plantas Cadastradas:")
            for planta in plantas:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{planta['apelido']}** (*{planta['especie']['nome_popular']}*)")
                    st.caption(f"Local: {planta['localizacao']}")
                with col2:
                    # Botão para calcular a próxima rega
                    if st.button("Ver Próxima Rega", key=f"rega_{planta['id']}"):
                        response_rega = requests.get(f"{API_URL}/plantas/{planta['id']}/proxima_rega/")
                        if response_rega.status_code == 200:
                            st.info(response_rega.json()['mensagem'])
                
                # Botão para registrar que regou
                if st.button("✅ Reguei Hoje!", key=f"log_{planta['id']}"):
                    requests.post(f"{API_URL}/plantas/{planta['id']}/tarefas/", json={"tipo_tarefa": "Rega"})
                    st.toast(f"Rega registrada para {planta['apelido']}!")
        
        # Formulário para adicionar uma nova planta
        with st.form("form_add_planta", clear_on_submit=True):
            st.subheader("Adicionar Nova Planta ao seu Jardim")
            
            # Busca as espécies disponíveis para o dropdown
            response_especies = requests.get(f"{API_URL}/especies/")
            if response_especies.status_code == 200:
                especies = response_especies.json()
                especie_map = {f"{e['nome_popular']} ({e['nome_cientifico']})": e['id'] for e in especies}
                
                apelido_planta = st.text_input("Apelido da Planta")
                local_planta = st.text_input("Onde ela fica?")
                especie_selecionada = st.selectbox("Selecione a Espécie", options=especie_map.keys())
                
                submit_planta = st.form_submit_button("Adicionar Planta")
                if submit_planta:
                    especie_id_selecionada = especie_map[especie_selecionada]
                    requests.post(
                        f"{API_URL}/jardineiros/{jardineiro_id}/plantas/",
                        json={"apelido": apelido_planta, "localizacao": local_planta, "especie_id": especie_id_selecionada}
                    )
                    st.success(f"{apelido_planta} adicionada ao seu jardim! Atualize a página se necessário.")