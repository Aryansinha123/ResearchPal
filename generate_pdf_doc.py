import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(45, 11 * inch - 30, "ResearchPaL | Technical Specification & Architecture")
            self.setFont("Helvetica", 8)
            self.drawRightString(8.5 * inch - 45, 11 * inch - 30, "Multi-Agent Academic RAG System")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(45, 11 * inch - 35, 8.5 * inch - 45, 11 * inch - 35)
            
        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(45, 38, 8.5 * inch - 45, 38)
        
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(45, 26, "ResearchPaL Project Documentation - Functionalities, Tech Stack, User Flow & Benchmarks")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 45, 26, page_str)
        self.restoreState()

def build_pdf(filename="ResearchPaL_Project_Documentation.pdf"):
    # Margins: 45pt left/right (522pt usable width), 40pt top/bottom
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=42,
        bottomMargin=46
    )
    
    styles = getSampleStyleSheet()
    
    # Palette
    primary_color = colors.HexColor("#0F172A")    # Deep Slate
    accent_color = colors.HexColor("#4338CA")     # Indigo 700
    teal_color = colors.HexColor("#0F766E")       # Teal 700
    text_dark = colors.HexColor("#1E293B")        # Slate 800
    bg_light = colors.HexColor("#F8FAFC")         # Slate 50
    border_color = colors.HexColor("#CBD5E1")     # Slate 300

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=primary_color,
        alignment=TA_LEFT,
        spaceAfter=3
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=accent_color,
        alignment=TA_LEFT,
        spaceAfter=10
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=text_dark,
        alignment=TA_JUSTIFY,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=text_dark,
        spaceAfter=3,
        leftIndent=10
    )
    
    table_text = ParagraphStyle(
        'TableText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.8,
        textColor=text_dark
    )
    
    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.white
    )

    callout_text = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.8,
        textColor=colors.HexColor("#1E293B")
    )

    story = []

    # ==================== PAGE 1: TITLE & EXECUTIVE SUMMARY & TECH STACK ====================
    story.append(Paragraph("ResearchPaL", title_style))
    story.append(Paragraph("Multi-Agent Academic RAG Assistant with Layout-Aware Parsing", subtitle_style))
    
    # Executive Summary Box
    summary_html = (
        "<b>Executive Summary:</b> ResearchPaL is a production-grade multi-agent research assistant designed "
        "to solve the critical drawbacks of conventional PDF Question-Answering systems. Standard RAG "
        "pipelines treat scientific PDFs as flat, unformatted plain text, discarding vital information stored in "
        "<b>mathematical formulas, structured tables, visual figures, and page hierarchies</b>. ResearchPaL preserves "
        "complete document topology via layout-aware multi-modal parsing, hybrid dense-sparse retrieval (RRF), "
        "cross-encoder reranking, and a stateful LangGraph agent graph with deterministic page-level citation verification."
    )
    callout_data = [[
        Paragraph(summary_html, callout_text)
    ]]
    callout_table = Table(callout_data, colWidths=[522])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EEF2FF")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#C7D2FE")),
        ('LINEBEFORE', (0,0), (0,-1), 3.5, accent_color),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 8))

    # SECTION 1: TECHNOLOGY STACK IN SHORT
    story.append(Paragraph("1. Technology Stack Architecture", h1_style))
    story.append(Paragraph(
        "The system employs a decoupled, modular architecture emphasizing speed, client-side privacy (BYOK), "
        "and resilient multi-model failovers:", body_style
    ))
    
    tech_data = [
        [Paragraph("Layer", table_header), Paragraph("Technologies & Frameworks", table_header), Paragraph("Key Role & Implementation", table_header)],
        
        [Paragraph("<b>Frontend UI</b>", table_text),
         Paragraph("React 18, Vite, Lucide Icons, KaTeX, Tailwind / Custom Dark Glassmorphism", table_text),
         Paragraph("Responsive workspace with discovery feed, real-time response streaming, clickable citation badge scrolling, and full-screen figure lightbox zoom.", table_text)],
         
        [Paragraph("<b>Backend API</b>", table_text),
         Paragraph("Python 3.10+, FastAPI, Uvicorn, Pydantic v2, HTTPX", table_text),
         Paragraph("Async REST endpoints, Server-Sent streaming (<code>StreamingResponse</code>), background worker thread pool, ArXiv URL rewriting, and magic-byte validation.", table_text)],
         
        [Paragraph("<b>Multi-Agent Graph</b>", table_text),
         Paragraph("LangGraph, LangChain Core", table_text),
         Paragraph("Stateful DAG workflow executing: Intent classification, dynamic context retrieval, cross-encoder reranking, and citation-guarded generation.", table_text)],
         
        [Paragraph("<b>Vector Store & DB</b>", table_text),
         Paragraph("Supabase (PostgreSQL 15+, <code>pgvector</code>, Storage Buckets)", table_text),
         Paragraph("Unified relational storage + vector indexing; 768-dimensional cosine index, PostgreSQL array filtering for multi-doc queries, public figure storage.", table_text)],
         
        [Paragraph("<b>Document Ingestion</b>", table_text),
         Paragraph("PyMuPDF (fitz), Adobe PDF Services API, Gemini Vision / Groq", table_text),
         Paragraph("Dual-mode parser: Basic Mode (fast text extraction) and Advanced Mode (layout-aware JSON structure, tables, and visual diagram bounding boxes).", table_text)],
         
        [Paragraph("<b>Embeddings & Reranker</b>", table_text),
         Paragraph("Jina Embeddings v3 (768d), Gemini Embedding, Jina Reranker v2", table_text),
         Paragraph("Dense semantic vectorization and cross-encoder reranking (refining top-15 retrieved candidates down to top-5 high-signal chunks).", table_text)],
         
        [Paragraph("<b>LLM Providers & Failover</b>", table_text),
         Paragraph("Google Gemini 1.5/2.5/Flash-Lite, OpenAI GPT-4o-mini, Anthropic Claude 3.5, Groq Llama 3.2 Vision", table_text),
         Paragraph("Multi-provider flexibility; automated zero-downtime failover to Groq vision/chat upon encountering Gemini 429 quota exhaustion.", table_text)],
         
        [Paragraph("<b>Security & Privacy</b>", table_text),
         Paragraph("Bring-Your-Own-Key (BYOK), Browser <code>localStorage</code>", table_text),
         Paragraph("Zero server-side persistence of user AI credentials; keys passed ephemerally via request headers and never written to database tables.", table_text)]
    ]
    
    t_tech = Table(tech_data, colWidths=[95, 175, 252])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_tech)
    
    story.append(PageBreak())

    # ==================== PAGE 2: CORE FUNCTIONALITIES & AGENT PIPELINE ====================
    story.append(Paragraph("2. Core Functionalities & System Capabilities", h1_style))
    story.append(Paragraph(
        "ResearchPaL delivers advanced research synthesis through eight specialized engineering capabilities:", body_style
    ))

    func_items = [
        ("Multi-Modal Layout-Aware Parsing", 
         "Unlike naive PDF splitters that discard non-text elements, the ingestion pipeline preserves tables, formulas, and visual figures. In Advanced Mode, Adobe PDF Services parses the document layout tree into structured content blocks, while Gemini/Groq Vision generates natural language semantic summaries of every diagram."),
        
        ("Semantic Text Chunking with Cosine Windowing", 
         "Rather than rigid fixed-character boundaries that sever sentences, ResearchPaL groups text into sentences, computes batch embeddings, and evaluates cosine similarity between adjacent sentences. Chunks only break at natural semantic boundaries (similarity < 0.75), maximizing contextual cohesion."),
        
        ("Hybrid Search with Reciprocal Rank Fusion (RRF)", 
         "Combines dense semantic vector retrieval (Jina/Gemini embeddings) with keyword term matching. Merged using Reciprocal Rank Fusion: Score(d) = 1/(60 + Rank_vector) + 1/(60 + Rank_keyword). This completely eliminates terminology mismatch on exact acronyms and equation names."),
        
        ("Cross-Encoder Reranking (Jina Reranker v2)", 
         "High-recall initial retrieval (k=15) is funneled through a cross-encoder model to compute deep query-passage attention. This delivers a +4.2% Context Precision boost, scoring figure and table metadata directly against user intent before generation."),
        
        ("Multi-Paper Literature Review", 
         "Users can select multiple indexed papers from the library sidebar. The backend queries across composite document IDs in PostgreSQL, synthesizing comparative answers with multi-document attribution."),
        
        ("Grounded Responses & Hallucination Guard", 
         "Every assertion generated by the LLM is anchored by explicit page-level citations (e.g., [Source 1]). An automated post-processing validator scrubs phantom citation indexes that exceed retrieved evidence limits."),
        
        ("Paper Discovery & Direct ArXiv Ingestion", 
         "Integrated with the Papers With Code and ArXiv APIs. Users can search trending research or paste abstract URLs (e.g. arxiv.org/abs/...), which are automatically translated to direct PDF streams and indexed with magic-byte (%PDF) validation."),
        
        ("Interactive Evidence Inspection & Lightbox Zoom", 
         "Clicking a citation badge in the chat dynamically scrolls to and highlights the exact evidence card. Extracted figures and tables can be clicked to open in an ultra-crisp full-resolution modal lightbox.")
    ]

    for idx, (title, desc) in enumerate(func_items, 1):
        story.append(Paragraph(f"<b>{idx}. {title}:</b> {desc}", bullet_style))
        story.append(Spacer(1, 1))

    story.append(Spacer(1, 4))
    story.append(Paragraph("3. LangGraph Multi-Agent Architecture", h1_style))
    story.append(Paragraph(
        "Retrieval and generation are governed by a stateful Directed Acyclic Graph (DAG) built with LangGraph:", body_style
    ))

    agent_data = [
        [Paragraph("Node / Agent", table_header), Paragraph("Function & Trigger Condition", table_header), Paragraph("Output Artifact", table_header)],
        
        [Paragraph("<b>Intent Router</b>", table_text),
         Paragraph("Classifies user query into 4 distinct intents: <code>greetings</code> (fast chat), <code>visual_tabular</code> (prioritize figures/tables), <code>global_synth</code> (broad overview), or <code>doc_search</code>.", table_text),
         Paragraph("State variable: <code>route_decision</code> directing graph execution path.", table_text)],
         
        [Paragraph("<b>Hybrid Retriever</b>", table_text),
         Paragraph("Executes parallel dense pgvector similarity + keyword search across selected document IDs; merges candidate lists via Reciprocal Rank Fusion.", table_text),
         Paragraph("Top-15 candidate document chunks (text, tables, image summaries).", table_text)],
         
        [Paragraph("<b>Jina Reranker</b>", table_text),
         Paragraph("Applies cross-encoder scoring between user prompt and candidate chunks; filters low-relevance noise down to the top 5 most salient contexts.", table_text),
         Paragraph("Reranked top-5 context chunks with relevance score metrics.", table_text)],
         
        [Paragraph("<b>Response Generator</b>", table_text),
         Paragraph("Streams synthesized answer using conversational history, inserting grounded <code>[Source N]</code> markers and appending structured source JSON metadata.", table_text),
         Paragraph("Real-time token stream + verified sources metadata payload.", table_text)]
    ]
    
    t_agent = Table(agent_data, colWidths=[105, 222, 195])
    t_agent.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#334155")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_agent)

    story.append(PageBreak())

    # ==================== PAGE 3: USER FLOW & BENCHMARKS ====================
    story.append(Paragraph("4. End-to-End User Flow & Operational Journey", h1_style))
    story.append(Paragraph(
        "The interaction workflow is designed for frictionless research exploration across four phases:", body_style
    ))

    flow_data = [
        [Paragraph("Phase", table_header), Paragraph("User Action", table_header), Paragraph("System Execution & Background Operations", table_header)],
        
        [Paragraph("<b>Phase 1:<br/>Configuration</b>", table_text),
         Paragraph("1. Open Web Application.<br/>2. Click Settings & enter API keys (Gemini, OpenAI, Anthropic, or Jina).", table_text),
         Paragraph("Keys are validated and saved exclusively to browser <code>localStorage</code> (zero database logging).", table_text)],
         
        [Paragraph("<b>Phase 2:<br/>Paper Ingestion</b>", table_text),
         Paragraph("<b>Option A:</b> Upload local PDF file.<br/><b>Option B:</b> Paste ArXiv URL or click Trending Papers.", table_text),
         Paragraph("1. Backend validates magic bytes (<code>%PDF</code>).<br/>2. Dispatches async ingestion task in FastAPI background thread.<br/>3. PyMuPDF or Adobe Extract parses text, tables & figure bounding boxes.<br/>4. Semantic Chunking breaks text into cohesive paragraphs.<br/>5. Gemini/Groq Vision summarizes visual figures.<br/>6. Jina/Gemini generates 768d embeddings stored in Supabase <code>pgvector</code>.<br/>7. Real-time notification updates library list upon indexing completion.", table_text)],
         
        [Paragraph("<b>Phase 3:<br/>Workspace Setup</b>", table_text),
         Paragraph("Select single paper or multi-select multiple papers from Library Sidebar.", table_text),
         Paragraph("Frontend configures active context scope (<code>document_ids</code>) for targeted queries or comparative literature cross-analysis.", table_text)],
         
        [Paragraph("<b>Phase 4:<br/>Interactive Synthesis</b>", table_text),
         Paragraph("Type research questions (e.g. <i>'Compare ablation results in Table 2 with Figure 4'</i>).", table_text),
         Paragraph("1. Intent Router identifies visual/tabular and comparative requirements.<br/>2. Hybrid search fetches top candidates across all selected papers.<br/>3. Jina Reranker scores candidates and isolates top 5 context passages.<br/>4. Streaming response renders markdown, KaTeX math equations, and citations.<br/>5. Clicking <code>[Source 1]</code> scrolls to and expands the page excerpt.<br/>6. Clicking any figure thumbnail launches high-res Lightbox zoom modal.", table_text)]
    ]
    
    t_flow = Table(flow_data, colWidths=[80, 182, 260])
    t_flow.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), teal_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_flow)
    
    story.append(Spacer(1, 8))

    # SECTION 5: PERFORMANCE EVALUATION & BENCHMARKS
    story.append(Paragraph("5. Empirical Performance & Benchmark Results", h1_style))
    story.append(Paragraph(
        "Evaluated on a curated academic benchmark across 4 research papers with 10 multi-hop questions each:", body_style
    ))

    eval_data = [
        [Paragraph("Benchmark Metric", table_header), Paragraph("Score", table_header), Paragraph("Benchmark Configuration", table_header), Paragraph("Engineering Significance", table_header)],
        
        [Paragraph("<b>Context Recall</b>", table_text), Paragraph("<b>0.927</b>", table_text), Paragraph("Chunk=2500, k=13", table_text), Paragraph("Retrieves 92.7% of all ground-truth evidence required for answers.", table_text)],
        [Paragraph("<b>Context Precision</b>", table_text), Paragraph("<b>0.390</b>", table_text), Paragraph("Hybrid + Jina Reranker", table_text), Paragraph("+4.2% precision boost over standard hybrid search without reranking.", table_text)],
        [Paragraph("<b>MRR</b> (Mean Reciprocal Rank)", table_text), Paragraph("<b>0.757</b>", table_text), Paragraph("Chunk=2500", table_text), Paragraph("First relevant chunk is positioned in top 1-2 search slots on average.", table_text)],
        [Paragraph("<b>Hit@5</b>", table_text), Paragraph("<b>1.000</b>", table_text), Paragraph("Chunk=2500", table_text), Paragraph("100% of all queries locate relevant evidence within the top 5 results.", table_text)],
        [Paragraph("<b>Figure / Table Hit@1</b>", table_text), Paragraph("<b>1.000</b>", table_text), Paragraph("k &ge; 13 (Advanced Mode)", table_text), Paragraph("Perfect retrieval accuracy for visual diagrams and complex table queries.", table_text)],
        [Paragraph("<b>P50 Query Latency</b>", table_text), Paragraph("<b>646 ms</b>", table_text), Paragraph("Default text mode", table_text), Paragraph("Sub-second vector retrieval and rank fusion processing.", table_text)],
        [Paragraph("<b>P50 Response Latency</b>", table_text), Paragraph("<b>2,620 ms</b>", table_text), Paragraph("Full pipeline end-to-end", table_text), Paragraph("Rapid first-token generation and streaming response delivery.", table_text)]
    ]

    t_eval = Table(eval_data, colWidths=[105, 60, 120, 237])
    t_eval.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_eval)

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Generated {filename} successfully!")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "ResearchPaL_Project_Documentation.pdf"
    build_pdf(out_file)
