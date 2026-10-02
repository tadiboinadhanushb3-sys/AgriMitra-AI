from datetime import date
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether, Flowable, ListFlowable, ListItem,
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon, Circle

OUT = r"C:\Users\Cuteb\Desktop\Nexlayer Hackathon\Project_Documentation.pdf"
PAGE_W, PAGE_H = A4
INK = colors.HexColor('#18332B')
GREEN = colors.HexColor('#2C7453')
MINT = colors.HexColor('#EAF3ED')
GOLD = colors.HexColor('#C58C3A')
SLATE = colors.HexColor('#4D5E59')
PALE = colors.HexColor('#F5F8F6')
BORDER = colors.HexColor('#D8E3DD')

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='CoverTitle', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=29, leading=35, textColor=INK, alignment=TA_LEFT, spaceAfter=10))
styles.add(ParagraphStyle(name='CoverSub', parent=styles['Normal'], fontName='Helvetica', fontSize=12, leading=18, textColor=SLATE))
styles.add(ParagraphStyle(name='H1x', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=17, leading=22, textColor=INK, spaceBefore=4, spaceAfter=9, keepWithNext=True))
styles.add(ParagraphStyle(name='H2x', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=11.5, leading=15, textColor=GREEN, spaceBefore=8, spaceAfter=4, keepWithNext=True))
styles.add(ParagraphStyle(name='Bodyx', parent=styles['BodyText'], fontName='Helvetica', fontSize=9, leading=13.3, textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle(name='Smallx', parent=styles['BodyText'], fontName='Helvetica', fontSize=7.5, leading=10.2, textColor=SLATE, spaceAfter=3))
styles.add(ParagraphStyle(name='TableHeadx', parent=styles['BodyText'], fontName='Helvetica-Bold', fontSize=7.4, leading=9.4, textColor=colors.white))
styles.add(ParagraphStyle(name='TableCellx', parent=styles['BodyText'], fontName='Helvetica', fontSize=7.2, leading=9.3, textColor=INK))
styles.add(ParagraphStyle(name='CodeBlockx', parent=styles['Code'], fontName='Courier', fontSize=7.3, leading=10, textColor=INK, backColor=PALE, borderColor=BORDER, borderWidth=0.5, borderPadding=7, spaceBefore=3, spaceAfter=8))
styles.add(ParagraphStyle(name='TOCHeadx', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=20, leading=25, textColor=INK, spaceAfter=12))
styles.add(ParagraphStyle(name='Captionx', parent=styles['BodyText'], fontName='Helvetica-Oblique', fontSize=7.7, leading=10, textColor=SLATE, alignment=TA_CENTER, spaceBefore=4, spaceAfter=9))
styles.add(ParagraphStyle(name='Calloutx', parent=styles['BodyText'], fontName='Helvetica', fontSize=8.4, leading=12, textColor=INK, backColor=MINT, borderColor=GREEN, borderWidth=0.5, borderPadding=8, spaceBefore=4, spaceAfter=9))
styles.add(ParagraphStyle(name='TOC0x', fontName='Helvetica-Bold', fontSize=9, leading=14, leftIndent=0, firstLineIndent=0, textColor=INK, spaceBefore=2))
styles.add(ParagraphStyle(name='TOC1x', fontName='Helvetica', fontSize=8, leading=11, leftIndent=14, firstLineIndent=0, textColor=SLATE))


def P(text, style='Bodyx'):
    return Paragraph(text, styles[style])


def plain(text, style='Bodyx'):
    return P(escape(str(text)), style)


def bullets(items):
    return ListFlowable(
        [ListItem(plain(item), leftIndent=10) for item in items],
        bulletType='bullet', start='circle', leftIndent=15, bulletFontName='Helvetica',
        bulletFontSize=5.5, bulletColor=GREEN, spaceAfter=5,
    )


def table(headers, rows, widths, font='TableCellx'):
    data = [[P(escape(str(x)), 'TableHeadx') for x in headers]]
    for row in rows:
        data.append([P(escape(str(x)).replace('\n', '<br/>'), font) for x in row])
    t = Table(data, colWidths=widths, repeatRows=1, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), GREEN),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, PALE]),
        ('GRID', (0, 0), (-1, -1), 0.35, BORDER),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    return t


class ArchitectureDiagram(Flowable):
    def __init__(self, kind='architecture'):
        super().__init__()
        self.kind = kind
        self.width = 174 * mm
        self.height = 72 * mm if kind == 'architecture' else 62 * mm

    def draw(self):
        c = self.canv
        c.saveState()
        c.scale(0.72, 0.72)
        def box(x, y, w, h, title, subtitle, fill=MINT, stroke=GREEN):
            c.setFillColor(fill); c.setStrokeColor(stroke); c.setLineWidth(0.9)
            c.roundRect(x, y, w, h, 5, stroke=1, fill=1)
            c.setFillColor(INK); c.setFont('Helvetica-Bold', 8.2)
            c.drawCentredString(x + w/2, y + h - 14, title)
            c.setFillColor(SLATE); c.setFont('Helvetica', 6.6)
            for i, line in enumerate(subtitle.split('|')):
                c.drawCentredString(x + w/2, y + h - 27 - i*9, line)
        def arrow(x1, y1, x2, y2, dashed=False):
            c.setStrokeColor(GREEN); c.setFillColor(GREEN); c.setLineWidth(1)
            if dashed: c.setDash(3, 2)
            else: c.setDash()
            c.line(x1, y1, x2, y2)
            c.setDash()
            import math
            angle = math.atan2(y2-y1, x2-x1)
            size = 5
            points = [(x2, y2), (x2-size*math.cos(angle-0.45), y2-size*math.sin(angle-0.45)), (x2-size*math.cos(angle+0.45), y2-size*math.sin(angle+0.45))]
            p = c.beginPath(); p.moveTo(*points[0]); p.lineTo(*points[1]); p.lineTo(*points[2]); p.close()
            c.drawPath(p, fill=1, stroke=0)
        if self.kind == 'architecture':
            box(8, 99, 106, 59, 'Farmer / reviewer', 'Web browser', fill=colors.HexColor('#FFF7E8'), stroke=GOLD)
            box(146, 91, 165, 75, 'React + TypeScript SPA', 'Vite | React Router | Framer Motion|Custom CSS')
            box(345, 91, 165, 75, 'FastAPI service', 'Pydantic request schemas|JSON + multipart routes')
            box(548, 106, 132, 60, 'Demo logic', 'Fixed payloads|Keyword response branches', fill=colors.HexColor('#F8F1E5'), stroke=GOLD)
            box(345, 11, 165, 49, 'SQLAlchemy setup', 'Engine + create_all only|No mapped application entities', fill=colors.HexColor('#F2F4F3'), stroke=SLATE)
            box(548, 11, 132, 49, 'SQLite default', 'Configured file|No tables in current schema', fill=colors.HexColor('#F2F4F3'), stroke=SLATE)
            arrow(114, 128, 146, 128); arrow(311, 128, 345, 128); arrow(510, 128, 548, 128)
            arrow(427, 91, 427, 60, True); arrow(510, 35, 548, 35, True)
            c.setFont('Helvetica-Oblique', 6.5); c.setFillColor(SLATE)
            c.drawString(352, 68, 'Initialization/configuration only; no CRUD data flow')
            box(146, 11, 165, 49, 'Browser localStorage', 'Demo token + user profile|Client-side route guard', fill=colors.HexColor('#FFF7E8'), stroke=GOLD)
            arrow(199, 91, 199, 60, True)
        else:
            box(4, 88, 112, 52, 'User action', 'Form input / selected page|Question / file selection', fill=colors.HexColor('#FFF7E8'), stroke=GOLD)
            box(143, 88, 112, 52, 'Frontend state', 'React component state|Known and optional values')
            box(282, 88, 112, 52, 'HTTP request', 'JSON or multipart|No bearer token sent')
            box(421, 88, 112, 52, 'FastAPI handler', 'Pydantic validation|Static or keyword logic')
            box(560, 88, 112, 52, 'Rendered result', 'JSON displayed in UI|No DB persistence', fill=colors.HexColor('#F8F1E5'), stroke=GOLD)
            arrow(116, 114, 143, 114); arrow(255, 114, 282, 114); arrow(394, 114, 421, 114); arrow(533, 114, 560, 114)
            c.setFont('Helvetica', 6.5); c.setFillColor(SLATE)
            c.drawCentredString(337, 61, 'Crop inputs are accepted, but current recommendation result is predefined.')
            c.drawCentredString(337, 49, 'Disease image bytes are accepted but not analyzed; soil PDF/image OCR is unavailable.')
            c.drawCentredString(337, 37, 'SQLAlchemy/SQLite are initialized but current APIs do not read/write application records.')
        c.restoreState()


def no_db_diagram():
    d = Drawing(470, 76)
    d.add(Rect(8, 8, 454, 60, rx=6, ry=6, fillColor=PALE, strokeColor=SLATE, strokeWidth=1, strokeDashArray=[4, 3]))
    d.add(String(235, 48, 'No application entities or relationships are defined', textAnchor='middle', fontName='Helvetica-Bold', fontSize=10, fillColor=INK))
    d.add(String(235, 31, 'SQLAlchemy metadata is initialized; current SQLite catalog contains no tables.', textAnchor='middle', fontName='Helvetica', fontSize=8, fillColor=SLATE))
    d.add(String(235, 18, 'ER diagram is not applicable to the implemented schema.', textAnchor='middle', fontName='Helvetica-Oblique', fontSize=7.5, fillColor=GREEN))
    return d


def cover_canvas(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(INK)
    canvas.rect(0, PAGE_H - 18*mm, PAGE_W, 18*mm, fill=1, stroke=0)
    canvas.setFillColor(GREEN)
    canvas.rect(0, 0, PAGE_W, 8*mm, fill=1, stroke=0)
    canvas.restoreState()


def page_canvas(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(0.55)
        canvas.line(18*mm, PAGE_H - 15*mm, PAGE_W - 18*mm, PAGE_H - 15*mm)
        canvas.setFillColor(SLATE)
        canvas.setFont('Helvetica-Bold', 7)
        canvas.drawString(18*mm, PAGE_H - 11.5*mm, 'AGRIMITRA AI')
        canvas.setFont('Helvetica', 7)
        canvas.drawRightString(PAGE_W - 18*mm, PAGE_H - 11.5*mm, 'Technical Project Documentation')
        canvas.line(18*mm, 15*mm, PAGE_W - 18*mm, 15*mm)
        canvas.setFont('Helvetica', 7)
        canvas.drawString(18*mm, 10.5*mm, 'Version 1.0.0 | 02 October 2026')
        canvas.drawRightString(PAGE_W - 18*mm, 10.5*mm, f'Page {doc.page}')
    canvas.restoreState()


class ReportDoc(BaseDocTemplate):
    def __init__(self, filename):
        super().__init__(filename, pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=21*mm, bottomMargin=21*mm, title='AgriMitra AI - Project Documentation', author='AgriMitra AI Project Team')
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id='normal', leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate(id='main', frames=frame, onPage=page_canvas)])
        self._toc = None

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name in ('H1x', 'H2x'):
            level = 0 if flowable.style.name == 'H1x' else 1
            text = flowable.getPlainText()
            key = f'section-{self.page}-{len(text)}-{abs(hash(text))%100000}'
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level=level, closed=False)
            self.notify('TOCEntry', (level, text, self.page, key))


doc = ReportDoc(OUT)
story = []

# Cover
story.extend([Spacer(1, 24*mm), P('ENGINEERING PROJECT REPORT', 'Smallx'), Spacer(1, 8*mm), P('AgriMitra AI', 'CoverTitle'), P('Smart Agriculture Decision-Support Web Application', 'CoverSub'), Spacer(1, 9*mm)])
story.append(ArchitectureDiagram('architecture'))
story.append(P('Figure 1. High-level architecture of the current implementation. Solid arrows represent the browser/API/demo response path; dashed arrows represent configuration or browser-local session handling.', 'Captionx'))
story.append(Spacer(1, 7*mm))
story.append(table(['Report detail', 'Value'], [
    ('Project name', 'AgriMitra AI'),
    ('Document type', 'Technical project documentation'),
    ('Project version', '1.0.0 (FastAPI and frontend package metadata)'),
    ('Prepared date', '02 October 2026'),
    ('Team members', 'Not specified in the inspected repository'),
    ('Institution / college', 'Not specified in the inspected repository'),
    ('Implementation status', 'Demo-first prototype; sample data and simulated AI-style outputs'),
], [45*mm, 129*mm]))
story.append(Spacer(1, 9*mm))
story.append(P('Submission note: this report documents the source code and configuration inspected in the project. It distinguishes functional UI/API workflows from demo responses and unimplemented integrations.', 'Calloutx'))
story.append(PageBreak())

# TOC
story.append(P('Table of Contents', 'TOCHeadx'))
toc = TableOfContents()
toc.levelStyles = [styles['TOC0x'], styles['TOC1x']]
toc.dotsMinLevel = 0
story.append(toc)
story.append(PageBreak())


def section(title, blocks):
    story.append(P(title, 'H1x'))
    story.extend(blocks)
    story.append(Spacer(1, 3))


def subsection(title, blocks):
    return KeepTogether([P(title, 'H2x'), *blocks])


section('1. Project Overview', [
    table(['Item', 'Description'], [
        ('Project name', 'AgriMitra AI'),
        ('Purpose', 'A demo-first web application that brings sample farm, crop, weather, market, crop-health, planning, assistant, and reporting screens into one interface.'),
        ('Problem addressed', 'Agricultural planning touches multiple information areas; this prototype demonstrates presenting these topics in a single navigable experience.'),
        ('Target users', 'Farmers exploring a digital assistant concept, agriculture students, reviewers, and demonstration audiences.'),
        ('Main objectives', 'Demonstrate a farm dashboard; crop recommendation workflow; weather and market panels; crop-health demo; assistant; calendar; knowledge; and printable summary.'),
        ('Key benefits', 'Unified UI, interactive module examples, optional soil report flow, low-friction demonstration, and a clear basis for future integration.'),
    ], [38*mm, 136*mm]),
    P('Important scope qualification: most outputs are fixed sample payloads, local UI constants, or keyword-selected text. This is not a production advisory service and should not be used as the sole basis for real agricultural or financial decisions.', 'Calloutx'),
])

section('2. Problem Statement', [
    P('Farm decisions involve crop choice, water timing, weather exposure, crop health, market context, and seasonal planning. Farmers may have to gather this information from separate sources or depend on local expertise that is not immediately available. A consolidated digital interface can make related information easier to inspect and can demonstrate how decision-support prompts might be presented.'),
    P('AgriMitra AI addresses this presentation and workflow problem as a prototype. The current implementation does not yet solve the underlying data-quality problem: it does not ingest live field sensor readings, authenticated farm records, verified market prices, live meteorological services, or validated agronomic models. Its value is currently demonstrative and educational.'),
])

section('3. Objectives', [bullets([
    'Provide a navigable web application for common farm-planning topics.',
    'Demonstrate a dashboard combining farm metrics, alerts, tasks, weather, market summary, and trend charts.',
    'Allow a crop recommendation request without requiring N, P, K, or pH inputs.',
    'Present a soil-report flow that labels missing soil values and allows review/editing of simple TXT/CSV extraction results.',
    'Demonstrate crop-health image selection, weather impact guidance, keyword-based assistant replies, calendar stages, and a printable report view.',
    'Keep backend APIs and frontend pages separable for future integration with persistent data and real services.',
])])

section('4. Proposed Solution', [
    P('The project uses a React single-page frontend and a FastAPI backend. Public landing, login, and registration pages lead to a client-guarded application shell with dashboard and feature routes. Pages call local HTTP endpoints and render JSON responses. Several pages also have local fallback sample data.'),
    P('The full demo journey starts with a public landing page, proceeds through demo login or registration and a four-step local onboarding form, and then opens the dashboard. Users can inspect sample farm details, choose known field conditions, optionally select a soil report file, request a predefined crop result, ask keyword-matched questions, inspect weather/market/calendar/crop-health examples, and use the browser print dialog on the Reports page.'),
    P('The application is intentionally not described as a trained AI service. Current backend outputs are fixed demonstration data or simple keyword branches; the database layer is initialized but has no application entities or CRUD operations.'),
])

section('5. Key Features', [
])
feature_rows = [
    ('Dashboard and analytics', 'Shows farm summary metrics, weather, tasks, sample alerts, market snapshot, recommendation copy, and four trend charts. Range buttons switch chart arrays. Useful for presenting a consolidated status view. Most data is fixed; 30/90-day chart arrays are frontend constants, not measured history.'),
    ('My Farm', 'Shows a read-only sample farmer/farm profile and operational metrics from `/api/profile` and `/api/dashboard`. There is no create/edit/delete persistence.'),
    ('Soil report flow', 'Asks whether a soil test report is available. Accepts PDF, common image formats, TXT, and CSV selections. Only TXT/CSV text is scanned with simple label/value regexes for N, P, K, and pH. Values are editable in the UI. PDF/image OCR, backend file upload, and report storage are not implemented.'),
    ('Crop recommendation', 'Collects field context and optional soil values; displays a crop, suitability score, reasons, crop facts, and alternatives. Backend returns fixed Tomato, Chilli, and Groundnut entries and does not calculate based on submitted field/nutrient values.'),
    ('Weather', 'Shows a fixed current-condition block, seven-day sample forecast, farming-impact advice, and action guidance. No external weather API is called.'),
    ('AI Crop Doctor', 'Allows local image selection and preview, submits multipart data, and displays a fixed Early Blight diagnosis. Image bytes are not analyzed and confidence is illustrative.'),
    ('AI Assistant', 'Offers suggested prompts and a chat interface. Backend chooses fixed replies with keyword matching. It is not an LLM integration and does not persist messages.'),
    ('Crop Calendar', 'Shows a sample Tomato timeline and recommended activities. A selector offers Tomato, Chilli, and Groundnut, but does not request crop-specific timelines. Task POST echoes the submitted object without persistence.'),
    ('Alerts and insights', 'Dashboard displays alert samples; separate APIs return notification and insight samples. The header notification button is currently visual only.'),
    ('Market intelligence', 'Shows a fixed crop price, trend, demand, location, and comparison list. No verified/live mandi feed is connected.'),
    ('Knowledge Hub', 'Shows static learning cards and sample FAQ/featured content. No CMS or dynamic article store exists.'),
    ('Reports', 'Displays a fixed summary and sample report sections. `window.print()` opens the browser print dialog; this is not server-side PDF generation. Some soil report copy is fixed demo text.'),
    ('Authentication / onboarding', 'Login/register forms call demo endpoints, receive a fixed token/profile, and save session state in localStorage. Onboarding data remains component state and is not saved.'),
]
story.append(table(['Feature', 'Current behavior and user value'], feature_rows, [42*mm, 132*mm]))
story.append(P('Soil provenance and result labeling: no-report submissions are labeled “Preliminary Recommendation.” When “Yes” is selected, the backend labels the result as based on an uploaded report based only on the boolean flag; it does not verify the file or consume its contents. This label must be treated as workflow/demo metadata, not evidence that report analysis occurred.', 'Calloutx'))

section('6. System Architecture', [
    P('The browser runs a React 18 + TypeScript SPA, built and served in development with Vite. React Router provides public routes and nested routes inside the application layout. The frontend calls a FastAPI service over HTTP. FastAPI validates some request bodies with Pydantic and returns dictionaries/lists containing fixed demo content or keyword-based replies.'),
    P('SQLAlchemy creates an engine and declarative base and calls `create_all()` at startup. There are no mapped application models in the repository and no API database reads/writes. The SQLite file therefore does not provide persistence for the displayed farm or session data. Frontend login state is stored in browser localStorage.'),
    ArchitectureDiagram('architecture'),
    P('Figure 2. Current application architecture. The dashed persistence path indicates configured initialization only; it is not an implemented application-data flow.', 'Captionx'),
    P('CORS is configured to allow all origins, methods, and headers. The frontend currently hard-codes the API base URL as `http://localhost:8000`; the `VITE_API_URL` value in Docker Compose is not read by the frontend source.'),
])

section('7. Technology Stack', [
    table(['Technology', 'Purpose / evidence'], [
        ('TypeScript, React 18', 'Frontend language and component UI; dependencies in frontend/package.json.'),
        ('Vite 5', 'Frontend development server and production build.'),
        ('React Router 6', 'Client routes and nested application layout.'),
        ('Framer Motion', 'Motion wrapper for the protected content area.'),
        ('Custom CSS', 'Project-owned styling in frontend/src/styles.css; no CSS framework declared.'),
        ('HTML / Google Fonts', 'frontend/index.html uses Inter from Google Fonts.'),
        ('Python 3.12', 'Backend runtime base in backend/Dockerfile; Python 3.12 is used by the verified local setup.'),
        ('FastAPI 0.110.3', 'Backend HTTP routing and OpenAPI service.'),
        ('Pydantic 2.7.4', 'Typed request schema validation.'),
        ('Uvicorn 0.29.0', 'ASGI server.'),
        ('SQLAlchemy 2.0.30', 'Engine/base initialization only; no current mapped entities or application persistence.'),
        ('SQLite', 'Default configured database URL (`sqlite:///./agrimitra.db`).'),
        ('python-multipart', 'Multipart form parsing dependency for the disease endpoint.'),
        ('Docker / Docker Compose', 'Container build and local orchestration configuration.'),
    ], [43*mm, 131*mm]),
    P('Not detected as implemented dependencies: a trained ML framework/model, OpenAI client, weather/market API client, OCR library, mapping service, or frontend component framework.'),
])

section('8. System Modules', [
    table(['Module', 'Route / source', 'Implementation summary'], [
        ('Dashboard', '/', 'Sample KPIs, chart data, weather, tasks, market snapshot, alerts, and recommendation text.'),
        ('My Farm', '/farm', 'Read-only profile assembled from demo profile/dashboard APIs.'),
        ('Soil report', '/crop-recommendation', 'Optional file selection; TXT/CSV regex extraction; PDF/image extraction unavailable; no upload/storage endpoint.'),
        ('Crop Recommendation', '/crop-recommendation', 'Form plus fixed API recommendation result.'),
        ('AI Crop Doctor', '/disease-detection', 'Image preview/multipart request; static diagnosis response.'),
        ('Weather', '/weather', 'Fixed conditions, forecast, farming impacts, and actions.'),
        ('Market', '/market', 'Fixed price and comparison values.'),
        ('Crop Calendar', '/calendar', 'Fixed timeline and activity list; selector only changes heading.'),
        ('AI Assistant', '/chat', 'Keyword-selected static responses.'),
        ('Knowledge Hub', '/knowledge', 'Static learning cards and sample FAQ.'),
        ('Reports', '/reports', 'Fixed summary and browser print action.'),
        ('Authentication', '/login, /register', 'Demo API token/profile; client-side session guard and localStorage.'),
        ('Onboarding', '/onboarding', 'Four-step local form; no API save.'),
    ], [33*mm, 43*mm, 98*mm]),
])

section('9. Complete System Workflow', [
    bullets([
        'Open the public landing page and choose Login or Get Started.',
        'Submit the login or registration form. The backend returns a demo token and sample profile; it does not verify a real account or persist registration.',
        'Complete the onboarding steps. Personal and farm fields remain in browser component state; there is no save endpoint call.',
        'The application shell checks whether a session object exists in localStorage, then displays Dashboard and module navigation.',
        'Review sample dashboard metrics, alerts, tasks, market and chart values.',
        'Open My Farm for the fixed read-only profile. Enter Crop Recommendation to provide known field information and optionally select a soil report.',
        'If no report is available, NPK/pH remain “Not available” and response type is Preliminary. If a report is selected, only TXT/CSV can be parsed client-side; edits are sent as values, but the current backend does not use them to choose the crop.',
        'Open Weather, Market, AI Crop Doctor, AI Assistant, Crop Calendar, and Knowledge Hub for sample outputs.',
        'Open Reports and use the browser print dialog to print or save the displayed report page.',
    ]),
])

section('10. Data Flow', [
    P('Most pages use browser `fetch()` calls to the hard-coded local API base. JSON bodies are used for login, registration, crop recommendations, chat, and calendar task submission. Disease detection submits multipart form data. Results are stored in page-level React state and rendered. Dashboard and My Farm include local fallback values on request failure; several other data pages only show a loading state if their fetch fails.'),
    ArchitectureDiagram('dataflow'),
    P('Figure 3. Generic request/response path and current processing boundary. No application records are persisted by these API handlers.', 'Captionx'),
])

section('11. Database Design', [
    P('Database configuration lives in `backend/app/db.py`. It creates an SQLAlchemy engine using `DATABASE_URL` or defaults to SQLite at `sqlite:///./agrimitra.db`. Startup invokes `Base.metadata.create_all(bind=engine)`. The inspected project contains no ORM model declarations or sessions used for application CRUD.'),
    table(['Database item', 'Current status'], [
        ('Tables / collections', 'None declared in current application source; inspected SQLite catalog is empty.'),
        ('Primary / foreign keys', 'None; no persisted application entities exist.'),
        ('Relationships', 'None.'),
        ('Data shown by endpoints', 'Constructed at request time from Python dictionaries/lists, not read from the database.'),
        ('Login session', 'Stored in browser localStorage as a JSON object, not SQLite.'),
        ('Soil report', 'Not uploaded to backend or stored.'),
    ], [46*mm, 128*mm]),
    P('Figure 4. ER design status. There is no implemented relational schema to diagram.', 'Captionx'),
    no_db_diagram(),
])

section('12. API Documentation', [
    P('Base URL used by the frontend: `http://localhost:8000`. These routes are defined in `backend/app/main.py`. No API route declares authentication or authorization dependencies. Pydantic-backed request models reject malformed typed bodies with FastAPI validation errors; several other handlers accept generic dictionaries or multipart form fields.'),
    table(['Method and endpoint', 'Request', 'Purpose / response'], [
        ('GET /health', 'None', 'Health status and service name.'),
        ('POST /api/auth/login', 'JSON: email, password', 'Demo token, fixed farmer profile, message. Password is not verified.'),
        ('POST /api/auth/register', 'JSON: name, email, phone, password', 'Demo token and profile with submitted name/email/phone; no account is saved.'),
        ('POST /api/auth/forgot-password', 'JSON object with email', 'Demo reset message; no email is sent.'),
        ('GET /api/profile', 'None', 'Fixed demo farmer profile.'),
        ('GET /api/farms', 'None', 'One fixed sample farm entry.'),
        ('GET /api/dashboard', 'None', 'Farmer profile, summary metrics, weather, market, tasks, insight, sample recommendation, analytics arrays, and alerts.'),
        ('POST /api/crop-recommendation/recommend', 'JSON: location, landArea, soilType, optional N/P/K/pH, temperature, humidity, rainfall, waterAvailability, previousCrop, season, budget, hasSoilReport, soilReportSource', 'Fixed crop list/score plus type, soil status, notes, model label, and timestamp. No report file is accepted; inputs do not change the fixed crop ranking.'),
        ('GET /api/weather', 'None', 'Fixed current conditions, seven-day forecast, actions, farming impacts, and demo source.'),
        ('GET /api/market', 'None', 'Fixed selected crop/location/price/trend/comparisons/demand with demoData flag.'),
        ('GET /api/calendar', 'None', 'Fixed crop, timeline, and recommended activities.'),
        ('POST /api/calendar/task', 'Any JSON object', 'Returns success message and echoes the object; no storage.'),
        ('GET /api/chat', 'None', 'Fixed sample chat messages.'),
        ('POST /api/chat', 'JSON: message string', 'Keyword-selected reply and demoMode flag.'),
        ('GET /api/knowledge', 'None', 'Fixed categories, featured content, article summaries, and FAQs.'),
        ('GET /api/insights', 'None', 'Fixed insight items with severity, reason, action, timestamp.'),
        ('GET /api/reports', 'None', 'Fixed report summary, section labels, demoMode flag, and timestamp.'),
        ('GET /api/notifications', 'None', 'Fixed sample notification list.'),
        ('GET /api/demo', 'None', 'Demo-mode note, farmer profile, and dashboard payload.'),
        ('POST /api/disease-detection/analyze', 'Multipart: optional file; optional imageUrl', 'Fixed Early Blight diagnosis, confidence, symptoms, causes, actions, prevention, consultExpert, demoMode; input image is not analyzed.'),
    ], [38*mm, 60*mm, 76*mm]),
    P('Table 1. API inventory. Response descriptions summarize current handler behavior, not a production contract.', 'Captionx'),
    P('The soil report itself is not sent to an API. The browser includes only optional parsed/edited numeric values and a report flag/source name in the crop-recommendation JSON. `soilReportSource` is accepted but not used by the handler.'),
])

section('13. AI/ML Implementation', [
    table(['Capability', 'Current implementation', 'Inputs and outputs', 'Limitations'], [
        ('Crop recommendation', 'Predefined Python list of crop objects and scores; response label says “Demo Random Forest / Rule-based fallback,” but no model is loaded.', 'Accepts field context and optional N/P/K/pH; returns fixed Tomato, Chilli, Groundnut entries and scores.', 'Submitted values do not influence selection or suitability. Not validated advice.'),
        ('Crop Doctor', 'Static backend response for Early Blight.', 'Accepts optional multipart file/imageUrl; returns disease name, 94.6 confidence, symptoms, causes, actions, prevention.', 'Image is not decoded, classified, or analyzed. Confidence is illustrative.'),
        ('Assistant', 'Python keyword branches on user text and fixed response templates.', 'Message text; returns a text reply and demoMode flag. Some irrigation reply text reads fixed weather payload.', 'No LLM/provider, retrieval, conversation persistence, or contextual farm database.'),
        ('Dashboard guidance/analytics', 'Fixed backend fields and frontend chart arrays.', 'No actual sensor/time-series inputs; returns example metrics, insight, alert, and recommendation copy.', 'Not a computed or historical analytical result.'),
    ], [31*mm, 49*mm, 49*mm, 45*mm]),
    P('The `ml/README.md` describes a future integration area and mentions possible model families, but no model files, training scripts, inference package, or data pipeline are present. Consequently, the project must be described as demo/simulated AI-style guidance rather than implemented machine learning.'),
])

section('14. Soil Data Handling', [
    P('Soil data is presented in the Crop Recommendation workflow and sample profile/dashboard/report content. There is no dedicated Soil Health route and no direct soil sensor/laboratory integration.'),
    table(['Data category', 'How the current app handles it'], [
        ('Selected file types', 'Input accepts PDF, PNG, JPG/JPEG, WEBP, TXT, and CSV by browser accept attribute. This is a UI filter, not server-side file validation.'),
        ('TXT / CSV extraction', 'Browser reads file text and applies simple label/value regular expressions for nitrogen, phosphorus, potassium, and pH. Extraction is heuristic and may miss formats/units.'),
        ('PDF / image extraction', 'No OCR/parser is implemented. Values remain “Not available.” Files are not submitted to the backend.'),
        ('Review / validation', 'Visible N/P/K/pH fields can be edited before request submission. Numeric parsing maps blank/“Not available”/“n/a” or invalid numbers to null. No scientific-range validation or source verification exists.'),
        ('Measured values', 'No direct measurement is performed by the application. A value appearing in TXT/CSV is content from a user-selected report and has not been independently verified.'),
        ('User-provided values', 'Extracted or edited values are browser form content and may be sent as numbers in the recommendation request.'),
        ('Estimated/demo values', 'Dashboard/profile/report include fixed sample soil pH/moisture/nutrient copy for demonstration; these are not measurements for the current user's field.'),
        ('Unavailable values', 'No-report fields initialize as “Not available”; missing/invalid numeric fields are sent as null. No report values are saved.'),
        ('Backend effect', 'The recommendation schema accepts optional N/P/K/pH and a report flag. Current crop handler does not use these fields to compute the crop result.'),
    ], [42*mm, 132*mm]),
    P('Although the UI says extracted values are from an uploaded report, the backend report-status label is set from the boolean flag, not verified report content. Selecting Yes without a parsable report can therefore still produce a “based on uploaded soil report” label. This is a known demo-flow limitation.', 'Calloutx'),
])

section('15. Security and Privacy', [
    bullets([
        'Authentication is demo-only: the backend returns the fixed string token `demo-jwt-token`; no JWT signing/verification or password database is present.',
        'The login condition accepts the demo email or any non-empty password, so it is not real credential verification. Registration returns a profile but does not persist an account.',
        'The frontend stores the returned session object in localStorage and protects routes only by checking for that object. API endpoints do not enforce token authentication or user authorization.',
        'Passwords are accepted in request bodies but are not hashed/stored by this backend. The UI includes demo defaults; this report intentionally omits credential values.',
        'CORS is configured with wildcard origins, credentials, methods, and headers. This permissive configuration is unsuitable for production without restriction.',
        'Pydantic validates typed login/register/recommendation payloads. Generic dictionary endpoints have limited schema-level validation. File type/size/content checks are not implemented server-side.',
        'No API keys are required by current code. Environment template entries for JWT/OpenAI/weather keys are not consumed. Do not place secrets in frontend code or commit them.',
        'The app uses plain HTTP localhost in the current development setup; no TLS, rate limiting, audit logging, CSRF protection, or production secrets management is configured.',
        'The uploaded soil report stays in browser state; it is not sent to or retained by the backend. However, no production privacy notice or data-retention policy is implemented.',
    ]),
    P('Security posture: suitable only for local demonstration/evaluation with sample data. A production deployment requires real identity, backend authorization, restricted CORS, secure transport, validation, privacy controls, and secret management.'),
])

section('16. Installation and Setup', [
    P('Prerequisites confirmed by package/container configuration: Windows PowerShell or compatible terminal; Python 3.12 recommended (backend Docker image uses Python 3.12); Node.js 20 recommended (frontend Docker image uses Node 20); npm; optional Docker Desktop with Compose.'),
    P('Backend setup (run from repository root):'),
    P('py -3.12 -m venv .venv312<br/>.\\.venv312\\Scripts\\Activate.ps1<br/>Set-Location backend<br/>python -m pip install -r requirements.txt<br/>python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000', 'CodeBlockx'),
    P('Run the backend from `backend/` so the default relative SQLite URL resolves there. Startup invokes SQLAlchemy `create_all()`; since no mapped entities exist, no application tables are created.'),
    P('Frontend setup (in a second terminal, from repository root):'),
    P('Set-Location frontend<br/>npm ci<br/>npm run dev', 'CodeBlockx'),
    P('Open `http://localhost:5173`; the frontend source calls `http://localhost:8000`. Backend health endpoint: `http://localhost:8000/health`.'),
    P('Production frontend build and preview:'),
    P('Set-Location frontend<br/>npm run build<br/>npm run preview', 'CodeBlockx'),
    P('The build script runs `tsc -b && vite build`. `npm run preview` serves the built frontend at port 4173. It is a preview server, not a configured production host.'),
    P('Optional Docker Compose demo (repository root):'),
    P('docker compose up --build', 'CodeBlockx'),
    P('Compose maps backend port 8000 and frontend port 5173. The frontend source hard-codes localhost:8000; the Compose `VITE_API_URL` variable is not consumed by source code.'),
])

section('17. Environment Variables', [
    P('`.env.example` is a template. The inspected source does not call `load_dotenv()`. Variables must be provided to the process/container to take effect. No secret values are included in this report.'),
    table(['Variable', 'Purpose in current code', 'Required / consumed?'], [
        ('DATABASE_URL', 'SQLAlchemy connection URL; defaults to `sqlite:///./agrimitra.db`.', 'Optional; consumed by backend db.py.'),
        ('PORT', 'Port read by the `if __name__ == "__main__"` Uvicorn launch block.', 'Optional; not used by Docker CMD, which uses 8000.'),
        ('BACKEND_PORT', 'Listed in .env.example.', 'Not read by current source/config.'),
        ('FRONTEND_PORT', 'Listed in .env.example.', 'Not read by current source; Vite port is configured in vite.config.ts.'),
        ('JWT_SECRET', 'Listed in .env.example.', 'Not consumed; no JWT signing is implemented.'),
        ('OPENAI_API_KEY', 'Listed in .env.example.', 'Not consumed; no OpenAI/LLM client is present.'),
        ('WEATHER_API_KEY', 'Listed in .env.example.', 'Not consumed; weather endpoint returns demo data.'),
        ('VITE_API_URL', 'Set in docker-compose.yml.', 'Not read by frontend source; API base is hard-coded.'),
    ], [39*mm, 88*mm, 47*mm]),
])

section('18. User Guide', [
    subsection('18.1 Sign in or register', [P('Open the landing page. Choose Login or Get Started. The login page is prefilled for the demo; submit the displayed form. Registration accepts name, email, phone, and password but does not create a persistent account. After success, the frontend stores the demo session and navigates to onboarding.')]),
    subsection('18.2 Complete onboarding', [P('Move through Personal Details, Farm Details, Preferences, and Complete Profile with Next/Back. The final Continue button navigates to `/`. Values are local UI state only and are not persisted to backend farm records.')]),
    subsection('18.3 Review Dashboard and farm profile', [P('Use the sidebar to open Dashboard and My Farm. Dashboard chart range buttons switch among sample arrays. My Farm is read-only and displays the sample profile/metrics.')]),
    subsection('18.4 Request a crop recommendation', [P('Open Crop Recommendation. Choose Yes or No for a soil test report. With No, keep N/P/K/pH as Not available and provide known field context. With Yes, select a supported file; TXT/CSV may populate values from simple text patterns, while PDF/image values remain unavailable. Review and edit shown values, then select Generate recommendation. The result is predefined and should be treated as illustrative.')]),
    subsection('18.5 Use other modules', [P('Weather and Market show sample data. AI Crop Doctor accepts an image for the demo flow but returns a fixed diagnosis. AI Assistant accepts a question or suggested prompt and returns a keyword-selected response. Crop Calendar shows a sample growth timeline. Knowledge Hub shows static educational cards and FAQs.')]),
    subsection('18.6 View a report and sign out', [P('Open Reports and use Download Report as PDF to invoke the browser print dialog; select Save as PDF in the browser if desired. Use Logout in the sidebar to clear the local session. This is not a server-generated farm report or a persistent account sign-out.'), P('Screenshots: no screenshot files were present in the inspected project, so none are included in this report.')]),
])

section('19. Testing / User Acceptance Testing', [
    P('The repository does not include an automated test suite. The table below is a practical manual UAT checklist derived from current screens/API behavior; expected outcomes describe the implementation, not independently executed test results.'),
    table(['Test case', 'Steps', 'Expected result'], [
        ('Login flow', 'Open Login, submit its visible demo form.', 'API returns the demo session; frontend stores it and navigates to onboarding. Not real credential verification.'),
        ('Registration flow', 'Submit name/email/phone/password on Register.', 'API returns a demo token/profile. No account is created in a database.'),
        ('Route guard/logout', 'Open a protected route without session; then log out.', 'Unauthenticated route redirects to login; logout clears local session.'),
        ('Onboarding', 'Advance/back through all four steps and continue.', 'Local form values appear in summary; no persistent save occurs.'),
        ('Dashboard', 'Open dashboard and change 7/30/90 range.', 'Metric cards and charts render; range updates displayed sample chart series.'),
        ('No soil report', 'Select No; submit recommendation.', 'N/P/K/pH are not required; result includes Preliminary Recommendation and unavailable-soil status.'),
        ('TXT/CSV soil report', 'Select a text file containing supported label/value text; inspect and edit fields.', 'Simple matches may populate N/P/K/pH; edits are included in the JSON request. Backend still returns fixed crop list.'),
        ('PDF/image soil report', 'Select PDF or image in Yes path.', 'File may be selected, but automatic values remain unavailable; no OCR/backend upload occurs.'),
        ('Weather', 'Open Weather.', 'Current conditions, forecast, and farming-impact sections render fixed data.'),
        ('Assistant', 'Ask an irrigation, crop, disease, or rain question.', 'A fixed keyword-selected reply is appended; no LLM call or stored history.'),
        ('Disease demo', 'Select a leaf image and Analyze.', 'Image preview appears and static Early Blight response is shown irrespective of image content.'),
        ('Reports', 'Open Reports and activate PDF button.', 'Browser print dialog opens for the rendered page.'),
        ('API validation', 'Send malformed typed request JSON to a Pydantic route.', 'FastAPI returns its standard request validation response, typically HTTP 422.'),
    ], [31*mm, 66*mm, 77*mm]),
])

section('20. Error Handling', [
    table(['Condition', 'Current behavior / gap'], [
        ('Invalid typed request', 'FastAPI/Pydantic returns standard validation errors. Generic dict routes provide little schema validation.'),
        ('Authentication failure', 'Login can raise HTTP 401 only if both demo-email condition and non-empty password condition fail; with a required non-empty password, this is not a meaningful credential check. Frontend login displays caught error text.'),
        ('Frontend fetch failure', 'Dashboard and My Farm provide local fallback data. Chat shows a connection error reply. Several pages (weather, market, calendar, reports, knowledge, disease/recommendation) do not consistently expose a dedicated fetch-error state and may remain loading or reject unhandled.'),
        ('Missing recommendation values', 'Optional N/P/K/pH are represented as null; no-report state is explicitly labeled in the result. No numeric-range validation is implemented.'),
        ('File selection/extraction', 'Browser accept attribute limits picker choices but is not a security boundary. TXT/CSV parse failures fall back to unavailable values. PDF/image OCR does not exist; no server upload, file-size check, or content validation.'),
        ('Assistant/API errors', 'Chat page catches request errors; other page requests vary in error handling. Keyword assistant always returns a normal fixed response for unmatched text.'),
        ('Database errors', 'No application CRUD path exists. Database engine initialization failures can prevent backend startup; no custom database error handling is defined.'),
        ('Empty states', 'Most pages render a loading message until data arrives. Crop recommendation, disease, and chat have initial empty or welcome states.'),
    ], [42*mm, 132*mm]),
])

section('21. Deployment', [
    P('No cloud deployment platform, production hostname, CI/CD pipeline, TLS configuration, or production environment profile is present in the inspected repository. Dockerfiles and `docker-compose.yml` support a local container demonstration only.'),
    table(['Component', 'Current deployment configuration'], [
        ('Backend container', 'Python 3.12 slim image; installs backend/requirements.txt; runs Uvicorn on 0.0.0.0:8000.'),
        ('Frontend container', 'Node 20 Alpine image; installs dependencies; runs Vite development server on 0.0.0.0:5173. Dockerfile does not build/serve static production assets.'),
        ('Compose', 'Builds the two local services and maps host ports 8000 and 5173.'),
        ('Database', 'Default SQLite relative file; no persistent volume is configured in Compose and no application tables exist.'),
        ('Frontend production build', '`npm run build` creates `frontend/dist`; no production web-server/container or hosting config is supplied.'),
        ('Environment', 'Compose sets PORT for backend and VITE_API_URL for frontend; the latter is not read by source, backend Docker command uses port 8000 directly.'),
    ], [42*mm, 132*mm]),
])

section('22. Project Structure', [
    P('Important source/configuration files (generated dependencies, virtual environments, and build artifacts omitted):'),
    P('.<br/>├── .env.example<br/>├── .gitignore<br/>├── docker-compose.yml<br/>├── backend/<br/>│   ├── Dockerfile<br/>│   ├── requirements.txt<br/>│   └── app/<br/>│       ├── __init__.py<br/>│       ├── db.py<br/>│       └── main.py<br/>├── frontend/<br/>│   ├── Dockerfile<br/>│   ├── index.html<br/>│   ├── package.json<br/>│   ├── package-lock.json<br/>│   ├── vite.config.ts<br/>│   ├── tsconfig*.json<br/>│   └── src/<br/>│       ├── App.tsx<br/>│       ├── main.tsx<br/>│       ├── styles.css<br/>│       ├── components/Layout.tsx<br/>│       └── pages/<br/>│           ├── LandingPage.tsx<br/>│           ├── LoginPage.tsx<br/>│           ├── RegisterPage.tsx<br/>│           ├── OnboardingPage.tsx<br/>│           ├── DashboardPage.tsx<br/>│           ├── FarmPage.tsx<br/>│           ├── CropRecommendationPage.tsx<br/>│           ├── DiseaseDetectionPage.tsx<br/>│           ├── WeatherPage.tsx<br/>│           ├── MarketPage.tsx<br/>│           ├── CalendarPage.tsx<br/>│           ├── ChatBotPage.tsx<br/>│           ├── KnowledgeHubPage.tsx<br/>│           └── ReportsPage.tsx<br/>└── ml/<br/>    └── README.md (future integration notes; no model implementation)', 'CodeBlockx'),
    P('`backend/agrimitra.db` is present in the working tree but ignored by `.gitignore`; the inspected catalog has no tables. Root README.md and DOCUMENTATION.md exist but this PDF is the requested generated submission deliverable.'),
])

section('23. UI / Screen Documentation', [
    table(['Screen', 'Purpose / contents / user actions'], [
        ('Landing `/`', 'Public introduction, feature summaries, workflow steps, dashboard preview, login/register links.'),
        ('Login `/login`', 'Email/password form, demo note, submit, create-account and forgot-password navigation (forgot link points to landing, not the API route).'),
        ('Register `/register`', 'Name, phone, email, password form; submits demo registration.'),
        ('Onboarding `/onboarding`', 'Four-step personal/farm/preferences form and summary; Continue navigates to dashboard without saving.'),
        ('Dashboard `/` protected index', 'Metric cards, recommendation panel, trend charts/range controls, weather, tasks, market snapshot, alerts.'),
        ('My Farm `/farm`', 'Profile and farm status summary; read-only display.'),
        ('Crop Recommendation `/crop-recommendation`', 'Report Yes/No toggle, upload and editable N/P/K/pH fields, field inputs, soil-testing info, result/alternatives.'),
        ('AI Crop Doctor `/disease-detection`', 'Image picker/preview, Analyze action, static diagnosis, confidence, symptoms, actions.'),
        ('Weather `/weather`', 'Current conditions, farming impact, forecast cards.'),
        ('Market `/market`', 'Selected crop/market summary, sample price, demand, comparisons.'),
        ('Crop Calendar `/calendar`', 'Crop selector, stage timeline, recommended activity list.'),
        ('AI Assistant `/chat`', 'Prompt suggestions, local chat messages, message form and loading indicator.'),
        ('Knowledge Hub `/knowledge`', 'Learning cards, selected article detail, FAQ list.'),
        ('Reports `/reports`', 'Sample profile/crop summary, report section labels, details, browser print button.'),
        ('Shared shell', 'Sidebar navigation, profile label, logout, visual notification control, topbar; notification button has no interactive panel.'),
    ], [45*mm, 129*mm]),
    P('No application screenshots were found in the repository. The architecture and data-flow visuals in this report are original technical diagrams, not screenshots or representations of a specific screen.', 'Calloutx'),
])

section('24. Limitations', [bullets([
    'Demo farmer/profile/farm values and most API responses are fixed; no user/farm persistence or multi-farm data model exists.',
    'Login/register are not secure authentication; passwords are not verified or stored and APIs have no authorization.',
    'Crop ranking/suitability is hard-coded and independent of request inputs; displayed confidence/scores are illustrative.',
    'Dashboard analytics are sample arrays, not calculated historical observations or live telemetry.',
    'Weather and market panels are not connected to external providers and must not be treated as current forecasts or prices.',
    'Disease endpoint does not analyze image bytes; the same static diagnosis is returned for any image or no image.',
    'Assistant is keyword/template logic, not an LLM; it does not retain chat history.' ,
    'Soil upload supports file selection; only simple TXT/CSV regex extraction exists. PDF/image OCR, comprehensive lab parsing, server validation, and report storage are absent.',
    'When the report flag is true, the API labels the output as based on a report even if it has no extracted values; flag is not proof of document processing.',
    'Recommendation inputs are accepted but not used to calculate the fixed output. Some report screen copy includes fixed soil values regardless of report provenance.',
    'Database setup contains no declared tables or application reads/writes; onboarding and generated outputs are not persisted.',
    'Several pages do not provide robust API error states; CORS is permissive; no production deployment pipeline, TLS, logging, rate limits, or automated tests are configured.',
    'Docker Compose runs the Vite development server, not a hardened production frontend service.'
])])

section('25. Future Enhancements', [bullets([
    'Implement secure account registration, password hashing, signed expiring tokens, API authorization, and role-aware access.',
    'Add mapped relational entities and CRUD services for users, farms, crop cycles, soil tests, tasks, notifications, chat, and reports, with migrations and backups.',
    'Implement robust soil report upload/OCR for PDF and image formats, file validation, unit/range checks, field-level provenance, farmer verification, consent, and retention controls.',
    'Replace fixed recommendation lists with an evaluated agronomic model or transparent rule engine that demonstrably uses input values and returns calibrated uncertainty.',
    'Integrate verified weather, market, geospatial, and agricultural knowledge providers with source/time attribution and failure handling.',
    'Use validated computer-vision inference for disease detection with safe confidence reporting and expert escalation.',
    'Replace keyword chat with an explicitly configured service or retrieval-based assistant grounded in current user-authorized farm data; preserve privacy and cite sources.',
    'Persist measured sensor/time-series data and calculate analytics from actual observations; integrate optional IoT/satellite feeds only after validation.',
    'Make crop calendars crop/location/season-specific and persist actionable tasks/reminders.',
    'Add automated backend/frontend tests, accessibility and mobile checks, structured logs, monitoring, CI/CD, deployment manifests, TLS, and environment-specific configuration.',
    'Add multilingual UI and locally reviewed agricultural terminology where user research supports it.'
])])

section('26. Conclusion', [
    P('AgriMitra AI is a full-stack demonstration of a unified smart-agriculture interface. Its React frontend and FastAPI backend organize sample farm, crop, weather, market, crop-health, assistant, calendar, knowledge, and reporting workflows in one application. The optional soil-report interaction also reduces the expectation that a farmer know NPK/pH values before exploring a recommendation.'),
    P('The current project is best evaluated as a working prototype: most data and recommendation outputs are illustrative, authentication is not production-secure, the configured SQLite layer has no application schema, and no trained model or external data service is integrated. These limitations are documented so reviewers can distinguish the useful product concept from capabilities that remain future work.'),
])

section('27. Viva / Presentation Summary', [
    subsection('Project in One Sentence', [P('AgriMitra AI is a demo-first web application that brings sample farm, crop-planning, weather, crop-health, market, assistant, calendar, and reporting workflows into one agricultural decision-support interface.')]),
    subsection('30-Second Explanation', [P('Farmers make connected decisions about crops, soil, water, weather, crop health, and timing, but information can be scattered. AgriMitra AI demonstrates a single web interface for these topics. A React and TypeScript frontend calls a FastAPI backend and presents a dashboard, optional soil-report flow, crop recommendations, weather and market panels, an assistant, crop calendar, crop-health demo, and printable report. The current outputs are sample/demo data rather than verified live advice or trained ML predictions.')]),
    subsection('2-Minute Explanation', [P('AgriMitra AI is a full-stack prototype for presenting farm decision-support workflows in one place. The problem it explores is that farm planning spans multiple information areas: crop choice, soil context, water and weather decisions, crop-health monitoring, market conditions, and seasonal activity planning. The application begins with a landing and demo authentication flow, followed by local onboarding and a dashboard that combines sample metrics, alerts, tasks, recommendation copy, and charts.'), P('The frontend is built with React, TypeScript, Vite, React Router, Framer Motion, and custom CSS. The backend uses FastAPI, Pydantic, and Uvicorn. SQLAlchemy is configured with SQLite, but the current project has no mapped entities or persisted application records. Crop recommendations, weather, market, calendar, disease diagnosis, and much of the dashboard are predefined demonstration payloads. The assistant uses keyword matching; it does not call an LLM. The crop recommendation page lets farmers continue without NPK/pH values and select a soil report, but only simple TXT/CSV text patterns are parsed. PDF/image OCR and report persistence are not implemented, and the crop result is currently fixed.'), P('The technical value is the cohesive workflow and replaceable full-stack structure, plus explicit provenance/missing-value presentation in the soil flow. The next engineering step is to connect validated data sources and persistent entities, add real security, and evaluate transparent models before positioning outputs as operational agricultural guidance.')]),
    subsection('Key Technologies', [P('React 18, TypeScript, Vite, React Router, Framer Motion, custom CSS, Python 3.12, FastAPI, Pydantic, Uvicorn, SQLAlchemy, SQLite configuration, Docker, and Docker Compose.')]),
    subsection('Key Innovation', [P('The prototype’s differentiator is its integrated decision-support journey across several farm topics and a recommendation workflow that does not force farmers to invent NPK/pH values when no soil report is available. This is a product/workflow demonstration, not a claim of novel trained AI or validated agronomic performance.')]),
])

story.append(Spacer(1, 5))
story.append(P('End of report. Source audit scope: repository files, frontend routes/pages, backend routes and schemas, package/dependency manifests, environment template, Docker configuration, and SQLite catalog inspected on 02 October 2026.', 'Smallx'))

doc.multiBuild(story)
print(f'Created: {OUT}')
