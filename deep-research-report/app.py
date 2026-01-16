import gradio as gr
from dotenv import load_dotenv
import sys
import os

# Adicionar o diretório atual ao path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from research_manager import ResearchManager
from email_agent import email_agent, update_recipient_email

load_dotenv(override=True)

async def run(query: str):
    async for chunk in ResearchManager().run(query):
        yield chunk

async def send_report_email(email: str, report: str):
    """Envia o relatório por email"""
    try:
        # Atualiza o email do destinatário
        update_recipient_email(email)
        
        # Envia o email usando o email_agent
        await email_agent.run(f"Envie um email com o seguinte relatório: {report}")
        
        return f"✅ Relatório enviado com sucesso para {email}!"
        
    except Exception as e:
        return f"❌ Erro ao enviar email: {str(e)}"

# CSS customizado para tema dark completo
custom_css = """
    /* Reset e configuração base dark */
    .gradio-container {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%) !important;
        min-height: 100vh !important;
    }
    
    /* Fundo principal escuro */
    body, .dark {
        background-color: #000000 !important;
    }
    
    /* Container principal */
    .contain {
        max-width: 1000px !important;
        margin: auto;
        padding: 2rem !important;
    }
    
    /* Cabeçalho do título */
    #title-header {
        text-align: center;
        margin-bottom: 1.5rem;
        padding: 2rem 0;
        border-bottom: 1px solid #2a2a2a;
    }
    
    #title-header h1 {
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
        animation: gradient 3s ease infinite;
    }
    
    @keyframes gradient {
        0% { filter: hue-rotate(0deg); }
        100% { filter: hue-rotate(360deg); }
    }
    
    /* Subtítulo */
    #subtitle {
        text-align: center;
        color: #9ca3af !important;
        font-size: 1.1rem;
        margin-bottom: 2.5rem;
        font-weight: 300;
    }
    
    /* Todos os grupos e containers */
    .gr-group, .gr-box, .gr-form {
        background: #0f0f0f !important;
        border-radius: 16px !important;
        padding: 24px !important;
        border: 1px solid #2a2a2a !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.5) !important;
    }
    
    /* Labels e textos */
    label, .gr-label, .label-wrap label {
        color: #e5e7eb !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Markdown headers */
    h3 {
        color: #f3f4f6 !important;
        font-weight: 600 !important;
        margin-bottom: 1rem !important;
        font-size: 1.25rem !important;
    }
    
    /* Input de texto */
    textarea, .gr-text-input, .gr-textbox textarea, input[type="email"], .gr-textbox input {
        background: #0f0f0f !important;
        border: 1px solid #2a2a2a !important;
        color: #f3f4f6 !important;
        border-radius: 12px !important;
        padding: 14px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    textarea:focus, .gr-text-input:focus, input[type="email"]:focus, .gr-textbox input:focus {
        border-color: #60a5fa !important;
        box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.1) !important;
        outline: none !important;
        background: #0f0f0f !important;
    }
    
    textarea::placeholder, input[type="email"]::placeholder {
        color: #6b7280 !important;
    }
    
    /* Botão principal */
    .gr-button-primary, button.primary {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
        border: none !important;
        color: white !important;
        padding: 14px 32px !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 1.05rem !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
    }
    
    .gr-button-primary:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(59, 130, 246, 0.4) !important;
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%) !important;
    }
    
    .gr-button-primary:active {
        transform: translateY(0) !important;
    }
    
    /* Botão secundário para email */
    .gr-button-secondary, button.secondary {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        border: none !important;
        color: white !important;
        padding: 12px 24px !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3) !important;
    }
    
    .gr-button-secondary:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px rgba(16, 185, 129, 0.4) !important;
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
    }
    
    /* Área de relatório */
    #report-output {
        background: #0a0a0a !important;
        border: 1px solid #262626 !important;
        border-radius: 12px !important;
        padding: 24px !important;
        color: #e5e7eb !important;
        min-height: 500px !important;
        max-height: 700px !important;
        overflow-y: auto !important;
    }
    
    #report-output * {
        color: #e5e7eb !important;
    }
    
    #report-output h1, #report-output h2, #report-output h3 {
        color: #f9fafb !important;
        margin-top: 1.5rem !important;
        margin-bottom: 1rem !important;
    }
    
    #report-output p {
        line-height: 1.7 !important;
        margin-bottom: 1rem !important;
    }
    
    #report-output em {
        color: #9ca3af !important;
        font-style: italic !important;
    }
    
    /* Scrollbar customizada */
    ::-webkit-scrollbar {
        width: 10px !important;
        height: 10px !important;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a !important;
        border-radius: 10px !important;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #4a4a4a !important;
        border-radius: 10px !important;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #5a5a5a !important;
    }
    
    /* Separador HR */
    hr {
        border: none !important;
        border-top: 1px solid #2a2a2a !important;
        margin: 2rem 0 !important;
    }
    
    /* Footer */
    .footer-info {
        text-align: center;
        margin-top: 3rem;
        padding: 2rem;
        background: #0a0a0a;
        border-radius: 16px;
        border: 1px solid #1a1a1a;
    }
    
    .footer-info p {
        color: #6b7280 !important;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
    
    .footer-info .tip {
        color: #60a5fa !important;
        font-weight: 500;
    }
    
    /* Animação de loading */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    /* Melhorias gerais para elementos Gradio */
    .gr-panel {
        background: #0f0f0f !important;
        border: 1px solid #2a2a2a !important;
    }
    
    .gr-padded {
        padding: 1.5rem !important;
    }
    
    .gr-compact {
        background: #0a0a0a !important;
    }
    
    /* Estado hover para elementos interativos */
    .gr-check-radio:hover {
        background: #1a1a1a !important;
    }
    
    /* Links */
    a {
        color: #60a5fa !important;
        text-decoration: none !important;
    }
    
    a:hover {
        color: #93c5fd !important;
        text-decoration: underline !important;
    }
"""

# Configuração da interface com tema dark
# Theme e CSS serão passados para launch() para compatibilidade com Gradio 6.0
theme_config = gr.themes.Default(
    primary_hue="blue",
    secondary_hue="purple",
    neutral_hue="gray",
    spacing_size="md",
    radius_size="lg",
    font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"]
)

with gr.Blocks(
    title="Deep Research - Ferramenta de Pesquisa Avançada com IA"
) as ui:
    
    # Cabeçalho com título animado
    gr.HTML("""
        <div id="title-header">
            <h1>🔬 Deep Research</h1>
        </div>
    """)
    
    # Subtítulo
    gr.Markdown(
        """<div id="subtitle">
        Ferramenta avançada de pesquisa com IA para análises profundas e relatórios detalhados
        </div>""",
        elem_id="subtitle"
    )
    
    # Container principal
    with gr.Column(scale=1, min_width=320):
        
        # Seção de input
        with gr.Group():
            gr.Markdown("### 🔍 Digite o tópico de pesquisa")
            
            query_textbox = gr.Textbox(
                label="Tópico de Pesquisa",
                placeholder="Ex: Quais são as últimas tendências em inteligência artificial? | Como funciona a computação quântica? | Análise do mercado de criptomoedas...",
                lines=3,
                max_lines=5,
                elem_id="query-input"
            )
            
            # Campo de email
            email_textbox = gr.Textbox(
                label="📧 Email para receber o relatório (opcional)",
                placeholder="seu@email.com",
                lines=1,
                elem_id="email-input"
            )
            
            # Botões centralizados
            with gr.Row():
                gr.Column(scale=1)
                run_button = gr.Button(
                    "Gerar Relatório",
                    variant="primary",
                    size="lg",
                    scale=2,
                    elem_id="run-btn"
                )
                gr.Column(scale=1)
        
        # Separador visual
        gr.Markdown("---")
        
        # Seção de resultados
        with gr.Group():
            gr.Markdown("### Relatório de Pesquisa")
            
            report = gr.Markdown(
                label="",
                value="*Aguardando pesquisa... Digite um tópico acima e clique em 'Iniciar Pesquisa'*",
                elem_id="report-output",
                height=600
            )
            
            # Botão para enviar por email
            with gr.Row():
                gr.Column(scale=1)
                email_button = gr.Button(
                    "📧 Enviar por Email",
                    variant="secondary",
                    size="md",
                    scale=2,
                    elem_id="email-btn",
                    visible=False
                )
                gr.Column(scale=1)
            
            # Status do email
            email_status = gr.Markdown(
                value="",
                elem_id="email-status",
                visible=False
            )
    
    # Footer informativo
    # Footer informativo
    gr.HTML("""
        <div class="footer-info">
            <p class="tip">💡 Dica: Seja específico em suas perguntas para obter resultados mais detalhados</p>
            
            <p style="font-size: 0.9rem; color: #60a5fa; margin: 1rem 0;">
                👨‍💻 Criado por <strong>Lucca Romagnolli</strong> | 
                <a href="https://www.linkedin.com/in/lucca-maximus-6792a1221/" target="_blank" style="color: #60a5fa; text-decoration: none;">
                    🔗 LinkedIn
                </a>
            </p>
            <p style="font-size: 0.8rem; color: #4b5563;">© 2024 Deep Research - Todos os direitos reservados</p>
        </div>
    """)
    # Função para mostrar/esconder botão de email
    def toggle_email_button(report_text):
        if report_text and report_text != "*Aguardando pesquisa... Digite um tópico acima e clique em 'Iniciar Pesquisa'*":
            return gr.update(visible=True)
        return gr.update(visible=False)
    
    # Função para enviar email
    async def send_email_wrapper(email, report):
        if not email or not email.strip():
            return gr.update(value="❌ Por favor, insira um email válido", visible=True)
        
        if not report or report == "*Aguardando pesquisa... Digite um tópico acima e clique em 'Iniciar Pesquisa'*":
            return gr.update(value="❌ Nenhum relatório disponível para enviar", visible=True)
        
        result = await send_report_email(email.strip(), report)
        return gr.update(value=result, visible=True)
    
    # Conectar eventos
    run_button.click(
        fn=run,
        inputs=query_textbox,
        outputs=report,
        show_progress=True
    ).then(
        fn=toggle_email_button,
        inputs=report,
        outputs=email_button
    )
    
    query_textbox.submit(
        fn=run,
        inputs=query_textbox,
        outputs=report,
        show_progress=True
    ).then(
        fn=toggle_email_button,
        inputs=report,
        outputs=email_button
    )
    
    # Evento do botão de email
    email_button.click(
        fn=send_email_wrapper,
        inputs=[email_textbox, report],
        outputs=email_status
    )

# Exportar a UI para uso externo
app = ui

# Lançar aplicação com configurações otimizadas (apenas quando executado diretamente)
# ... existing code ...

# Lançar aplicação com configurações otimizadas (apenas quando executado diretamente)
if __name__ == "__main__":
    # Obter porta do ambiente (Google Cloud Run usa PORT=8080)
    port = int(os.environ.get("PORT", 7860))
    
    ui.launch(
        theme=theme_config,
        css=custom_css,
        inbrowser=False,  # Desabilitar browser automático no Cloud Run
        share=False,
        server_name="0.0.0.0",  # Escutar em todas as interfaces
        server_port=port,       # Usar porta do ambiente
        show_error=True
    )