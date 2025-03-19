
import streamlit as st
from extract_b import extrair_valores_e_contexto

import os

# Desativar WebSocket e configurar CORS
os.environ["STREAMLIT_SERVER_ENABLE_WEBSOCKETS"] = "false"
os.environ["STREAMLIT_SERVER_ENABLE_CORS"] = "true"
os.environ["STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION"] = "false"
os.environ["STREAMLIT_SERVER_ALLOWED_ORIGINS"] = "*"

# Configuração da página
st.set_page_config(
    page_title="Extrator Avançado de Valores Monetários",
    layout="wide",  
)

# CSS personalizado
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #4f92eb; color: black; padding: 10px; border-radius: 8px;
}
.stTextArea textarea {
    border: 2px solid #1f77b4; border-radius: 5px; padding: 10px;
}
.card {
    background-color: #f9f9f9; padding: 15px; border-radius: 8px; margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🔍 Extrator Avançado de Valores Monetários")
    st.markdown("""
    Insira o texto da petição no campo abaixo e clique no botão **Extrair Valores** para identificar os valores monetários.
    """)

    texto_peticao = st.text_area("📝 Texto da Petição", height=250)

    if st.button("Extrair Valores"):
        if texto_peticao.strip():
            with st.spinner("⏳ Processando..."):
                resultados = extrair_valores_e_contexto(texto_peticao)

            if resultados:
                st.subheader("📊 Resultados Encontrados:")
                for item in resultados:
                    entidades = ', '.join([f"{ent[0]} ({ent[1]})" for ent in item['Entidades']]) if item['Entidades'] else "Nenhuma entidade encontrada"
                    st.markdown(f"""
                    <div class="card">
                        <h4>💰 Valor: {item['Valor']}</h4>
                        <p><strong>📌 Contexto:</strong> {item['Contexto']}</p>
                        <p><strong>🔖 Entidades:</strong> {entidades_nomeadas_formatadas(item['Entidades'])}</p>
                    </div>
                    """, unsafe_allow_html=True)
                st.success("✅ Extração concluída com sucesso!")
            else:
                st.warning("⚠️ Nenhum valor monetário encontrado.")
        else:
            st.error("❌ Por favor, insira o texto da petição.")

def entidades_nomeadas_formatadas(entidades):
    if entidades:
        return ', '.join([f"{texto} ({label})" for texto, label in entidades])
    return "Nenhuma entidade encontrada."

if __name__ == "__main__":
    main()