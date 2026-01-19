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
        
        # Envia o email usando o email_agent com Runner
        from agents import Runner
        await Runner.run(
            email_agent,
            f"Envie um email com o seguinte relatório: {report}"
        )
        
        return f"✅ Relatório enviado com sucesso para {email}!"
        
    except Exception as e:
        return f"❌ Erro ao enviar email: {str(e)}"

# CSS profissional e moderno
custom_css = """
    /* Importar fontes */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Reset global */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Container principal */
    .gradio-container {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        background: #0a0a0a !important;
        min-height: 100vh !important;
    }
    
    body {
        background: #0a0a0a !important;
        overflow-x: hidden !important;
    }
    
    /* Wrapper centralizado */
    .contain {
        max-width: 900px !important;
        margin: 0 auto !important;
        padding: 3rem 1.5rem !important;
    }
    
    /* Header do aplicativo */
    #title-header {
        text-align: center;
        margin-bottom: 3rem;
        padding: 0 1rem;
    }
    
    #title-header h1 {
        font-size: clamp(2.5rem, 5vw, 4rem);
        font-weight: 900;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        letter-spacing: -0.03em;
        line-height: 1.1;
    }
    
    .subtitle {
        font-size: 1.125rem;
        color: #9ca3af;
        font-weight: 400;
        line-height: 1.6;
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* Cards e containers */
    .gr-form, .gr-box, .gr-group {
        background: linear-gradient(145deg, #111111 0%, #0d0d0d 100%) !important;
        border: 1px solid #1f1f1f !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5) !important;
        margin-bottom: 1.5rem !important;
    }
    
    /* Section headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #1f1f1f;
    }
    
    .section-header h3 {
        font-size: 1.25rem;
        font-weight: 700;
        color: #f3f4f6;
        margin: 0;
    }
    
    /* Labels */
    label, .gr-label {
        color: #e5e7eb !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        margin-bottom: 0.75rem !important;
        display: block !important;
    }
    
    /* Inputs */
    textarea, input[type="text"], input[type="email"], .gr-textbox textarea, .gr-textbox input {
        background: #0a0a0a !important;
        border: 2px solid #1f1f1f !important;
        color: #f9fafb !important;
        border-radius: 14px !important;
        padding: 1rem 1.25rem !important;
        font-size: 1rem !important;
        font-weight: 400 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        line-height: 1.5 !important;
    }
    
    textarea:focus, input:focus, .gr-textbox textarea:focus, .gr-textbox input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1) !important;
        outline: none !important;
        background: #0d0d0d !important;
    }
    
    textarea::placeholder, input::placeholder {
        color: #6b7280 !important;
        font-weight: 400 !important;
    }
    
    /* Botão primário */
    .gr-button-primary, button.primary {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
        border: none !important;
        color: white !important;
        padding: 1rem 2.5rem !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 0.02em !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3) !important;
        text-transform: uppercase !important;
    }
    
    .gr-button-primary:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 40px rgba(59, 130, 246, 0.4) !important;
    }
    
    .gr-button-primary:active {
        transform: translateY(-1px) !important;
    }
    
    /* Botão secundário */
    .gr-button-secondary, button.secondary {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        border: none !important;
        color: white !important;
        padding: 0.875rem 2rem !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.02em !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3) !important;
        text-transform: uppercase !important;
    }
    
    .gr-button-secondary:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 40px rgba(16, 185, 129, 0.4) !important;
    }
    
    /* Área do relatório */
    #report-output {
        background: #0d0d0d !important;
        border: 2px solid #1f1f1f !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        color: #e5e7eb !important;
        min-height: 500px !important;
        max-height: 700px !important;
        overflow-y: auto !important;
        line-height: 1.8 !important;
    }
    
    #report-output h1 {
        color: #f9fafb !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
        margin: 2rem 0 1rem 0 !important;
        line-height: 1.2 !important;
    }
    
    #report-output h2 {
        color: #f3f4f6 !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        margin: 1.75rem 0 1rem 0 !important;
        line-height: 1.3 !important;
    }
    
    #report-output h3 {
        color: #e5e7eb !important;
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        margin: 1.5rem 0 0.75rem 0 !important;
    }
    
    #report-output p {
        color: #d1d5db !important;
        line-height: 1.8 !important;
        margin-bottom: 1.25rem !important;
        font-size: 1rem !important;
    }
    
    #report-output em {
        color: #9ca3af !important;
        font-style: italic !important;
    }
    
    #report-output strong {
        color: #f3f4f6 !important;
        font-weight: 600 !important;
    }
    
    #report-output ul, #report-output ol {
        margin: 1rem 0 1rem 1.5rem !important;
        color: #d1d5db !important;
    }
    
    #report-output li {
        margin-bottom: 0.5rem !important;
        line-height: 1.7 !important;
    }
    
    /* Scrollbar personalizada */
    ::-webkit-scrollbar {
        width: 12px;
        height: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0a0a;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #3b82f6 0%, #8b5cf6 100%);
        border-radius: 10px;
        border: 2px solid #0a0a0a;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #2563eb 0%, #7c3aed 100%);
    }
    
    /* Divisor */
    hr {
        border: none !important;
        border-top: 1px solid #1f1f1f !important;
        margin: 2.5rem 0 !important;
        opacity: 0.5 !important;
    }
    
    /* Footer */
    .footer-info {
        text-align: center;
        margin-top: 4rem;
        padding: 2.5rem 2rem;
        background: linear-gradient(145deg, #111111 0%, #0d0d0d 100%);
        border-radius: 20px;
        border: 1px solid #1f1f1f;
    }
    
    .footer-info p {
        color: #9ca3af !important;
        font-size: 0.95rem;
        margin: 0.75rem 0;
        line-height: 1.6;
    }
    
    .footer-info .tip {
        color: #60a5fa !important;
        font-weight: 600;
        font-size: 1rem;
    }
    
    .footer-info a {
        color: #60a5fa !important;
        text-decoration: none !important;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .footer-info a:hover {
        color: #93c5fd !important;
        text-decoration: underline !important;
    }
    
    .footer-info strong {
        color: #f3f4f6 !important;
        font-weight: 600;
    }
    
    /* Status do email */
    #email-status {
        text-align: center;
        padding: 1rem;
        border-radius: 12px;
        margin-top: 1rem;
        font-weight: 500;
    }
    
    /* Loading state */
    .loading {
        position: relative;
        overflow: hidden;
    }
    
    .loading::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.1), transparent);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        100% {
            left: 100%;
        }
    }
    
    /* Responsividade */
    @media (max-width: 768px) {
        .contain {
            padding: 2rem 1rem !important;
        }
        
        #title-header h1 {
            font-size: 2.5rem;
        }
        
        .subtitle {
            font-size: 1rem;
        }
        
        .gr-form, .gr-box, .gr-group {
            padding: 1.5rem !important;
        }
        
        .gr-button-primary {
            padding: 0.875rem 2rem !important;
            font-size: 0.95rem !important;
        }
        
        #report-output {
            padding: 1.5rem !important;
            min-height: 400px !important;
        }
    }
    
    /* Animações sutis */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .gr-form, .gr-box, .gr-group {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Glowing effect no hover dos inputs */
    textarea:hover, input:hover {
        border-color: #2a2a2a !important;
    }
    
    /* Badge style */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: rgba(59, 130, 246, 0.1);
        color: #60a5fa;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
"""

# Configuração do tema
theme_config = gr.themes.Base(
    primary_hue="blue",
    secondary_hue="purple",
    neutral_hue="slate",
    spacing_size="lg",
    radius_size="lg",
    font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"]
).set(
    body_background_fill="*neutral_950",
    body_background_fill_dark="*neutral_950",
    background_fill_primary="*neutral_900",
    background_fill_primary_dark="*neutral_900",
    background_fill_secondary="*neutral_800",
    background_fill_secondary_dark="*neutral_800",
)

with gr.Blocks(title="Deep Research - Pesquisa Avançada com IA") as ui:
    
    # Header
    gr.HTML("""
        <div id="title-header">
            <h1>🔬 Deep Research</h1>
            <p class="subtitle">
                Ferramenta profissional de pesquisa com IA para análises detalhadas e relatórios completos
            </p>
        </div>
    """)
    
    # Seção de Input
    with gr.Group():
        gr.HTML("""
            <div class="section-header">
                <span style="font-size: 1.5rem;">🔍</span>
                <h3>Defina seu Tópico de Pesquisa</h3>
            </div>
        """)
        
        query_textbox = gr.Textbox(
            label="Tópico de Pesquisa",
            placeholder="Ex: Tendências em inteligência artificial generativa | Impactos da computação quântica | Análise do mercado financeiro...",
            lines=4,
            max_lines=6
        )
        
        email_textbox = gr.Textbox(
            label="Email para Recebimento (Opcional)",
            placeholder="seu@email.com",
            lines=1
        )
        
        with gr.Row():
            gr.Column(scale=1)
            run_button = gr.Button(
                "🚀 Iniciar Pesquisa",
                variant="primary",
                size="lg",
                scale=3
            )
            gr.Column(scale=1)
    
    # Divisor
    gr.HTML("<hr style='margin: 3rem 0;'>")
    
    # Seção de Resultados
    with gr.Group():
        gr.HTML("""
            <div class="section-header">
                <span style="font-size: 1.5rem;">📊</span>
                <h3>Relatório Detalhado</h3>
            </div>
        """)
        
        report = gr.Markdown(
            value="*✨ Pronto para começar! Digite um tópico acima e clique em 'Iniciar Pesquisa' para gerar um relatório completo.*",
            elem_id="report-output"
        )
        
        with gr.Row():
            gr.Column(scale=1)
            email_button = gr.Button(
                "📧 Enviar por Email",
                variant="secondary",
                size="md",
                scale=2,
                visible=False
            )
            gr.Column(scale=1)
        
        email_status = gr.Markdown(
            value="",
            elem_id="email-status",
            visible=False
        )
    
    # Footer
    gr.HTML("""
        <div class="footer-info">
            <p class="tip">💡 Dica Profissional: Perguntas específicas geram análises mais precisas e detalhadas</p>
            <p style="margin-top: 1.5rem;">
                <span style="color: #6b7280;">Desenvolvido por</span> 
                <strong>Lucca Romagnolli</strong> 
                <span style="color: #6b7280;">|</span> 
                <a href="https://www.linkedin.com/in/lucca-maximus-6792a1221/" target="_blank">
                    🔗 LinkedIn
                </a>
            </p>
            <p style="font-size: 0.875rem; color: #4b5563; margin-top: 1rem;">
                © 2024 Deep Research - Tecnologia de Pesquisa Avançada
            </p>
        </div>
    """)
    
    # Funções de controle
    def toggle_email_button(report_text):
        if report_text and not report_text.startswith("*✨"):
            return gr.update(visible=True)
        return gr.update(visible=False)
    
    async def send_email_wrapper(email, report):
        if not email or not email.strip():
            return gr.update(
                value="<div style='background: rgba(239, 68, 68, 0.1); color: #ef4444; padding: 1rem; border-radius: 12px; border: 1px solid rgba(239, 68, 68, 0.2);'>❌ Por favor, insira um email válido</div>",
                visible=True
            )
        
        if not report or report.startswith("*✨"):
            return gr.update(
                value="<div style='background: rgba(239, 68, 68, 0.1); color: #ef4444; padding: 1rem; border-radius: 12px; border: 1px solid rgba(239, 68, 68, 0.2);'>❌ Nenhum relatório disponível para enviar</div>",
                visible=True
            )
        
        result = await send_report_email(email.strip(), report)
        
        if result.startswith("✅"):
            return gr.update(
                value=f"<div style='background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 1rem; border-radius: 12px; border: 1px solid rgba(16, 185, 129, 0.2);'>{result}</div>",
                visible=True
            )
        else:
            return gr.update(
                value=f"<div style='background: rgba(239, 68, 68, 0.1); color: #ef4444; padding: 1rem; border-radius: 12px; border: 1px solid rgba(239, 68, 68, 0.2);'>{result}</div>",
                visible=True
            )
    
    # Eventos
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
    
    email_button.click(
        fn=send_email_wrapper,
        inputs=[email_textbox, report],
        outputs=email_status
    )

app = ui

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    
    ui.launch(
        theme=theme_config,
        css=custom_css,
        inbrowser=False,
        share=False,
        server_name="0.0.0.0",
        server_port=port,
        show_error=True
    )