"""
Módulo de exportación de memorias de cálculo en PDF
Utilizando ReportLab para generación profesional de documentos
"""

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle, Paragraph, 
                                Spacer, PageBreak, Image, Frame, PageTemplate)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
from typing import Dict, List
import io


class CalculationReport:
    """
    Generador de memorias de cálculo técnicas profesionales
    """
    
    def __init__(self, filename: str = "memoria_calculo.pdf"):
        self.filename = filename
        self.doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        self.story = []
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configura estilos personalizados"""
        # Título principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtítulo
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2ca02c'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Texto técnico
        self.styles.add(ParagraphStyle(
            name='Technical',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        ))
    
    def add_title_page(self, project_info: Dict):
        """Añade página de título"""
        # Título
        title = Paragraph(
            "MEMORIA DE CÁLCULO<br/>SISTEMA DE TUBERÍAS Y BOMBEO",
            self.styles['CustomTitle']
        )
        self.story.append(title)
        self.story.append(Spacer(1, 2*cm))
        
        # Información del proyecto
        project_data = [
            ['Proyecto:', project_info.get('project_name', 'N/A')],
            ['Cliente:', project_info.get('client', 'N/A')],
            ['Ubicación:', project_info.get('location', 'N/A')],
            ['Fecha:', datetime.now().strftime('%d/%m/%Y')],
            ['Ingeniero:', project_info.get('engineer', 'N/A')],
            ['Revisión:', project_info.get('revision', 'Rev. 0')],
        ]
        
        table = Table(project_data, colWidths=[4*cm, 10*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#262730')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        
        self.story.append(table)
        self.story.append(PageBreak())
    
    def add_section(self, title: str, content: str = ""):
        """Añade una sección"""
        section_title = Paragraph(title, self.styles['CustomHeading'])
        self.story.append(section_title)
        
        if content:
            text = Paragraph(content, self.styles['Technical'])
            self.story.append(text)
        
        self.story.append(Spacer(1, 0.5*cm))
    
    def add_standards_section(self, standards: List[str]):
        """Añade sección de normativas aplicables"""
        self.add_section("1. NORMATIVAS Y CÓDIGOS APLICABLES")
        
        content = "El presente cálculo se ha desarrollado en conformidad con las siguientes normativas y estándares internacionales:"
        self.story.append(Paragraph(content, self.styles['Technical']))
        self.story.append(Spacer(1, 0.3*cm))
        
        for std in standards:
            bullet = Paragraph(f"• {std}", self.styles['Technical'])
            self.story.append(bullet)
        
        self.story.append(Spacer(1, 0.5*cm))
    
    def add_input_data(self, pipe_data: Dict, fluid_data: Dict, fittings: List[Dict]):
        """Añade datos de entrada"""
        self.add_section("2. DATOS DE ENTRADA")
        
        # Datos de la tubería
        self.story.append(Paragraph("<b>2.1 Características de la Tubería</b>", 
                                   self.styles['Technical']))
        
        pipe_table_data = [
            ['Parámetro', 'Valor', 'Unidad'],
            ['Diámetro nominal', f"{pipe_data.get('diameter', 0)*1000:.1f}", 'mm'],
            ['Longitud total', f"{pipe_data.get('length', 0):.2f}", 'm'],
            ['Material', pipe_data.get('material', 'N/A'), '-'],
            ['Rugosidad absoluta', f"{pipe_data.get('roughness', 0):.4f}", 'mm'],
        ]
        
        table = self._create_styled_table(pipe_table_data)
        self.story.append(table)
        self.story.append(Spacer(1, 0.5*cm))
        
        # Datos del fluido
        self.story.append(Paragraph("<b>2.2 Propiedades del Fluido</b>", 
                                   self.styles['Technical']))
        
        fluid_table_data = [
            ['Parámetro', 'Valor', 'Unidad'],
            ['Fluido', fluid_data.get('fluid_type', 'Agua'), '-'],
            ['Caudal', f"{fluid_data.get('flow_rate', 0)*3600:.2f}", 'm³/h'],
            ['Temperatura', f"{fluid_data.get('temperature', 20):.1f}", '°C'],
        ]
        
        table = self._create_styled_table(fluid_table_data)
        self.story.append(table)
        self.story.append(Spacer(1, 0.5*cm))
        
        # Accesorios
        if fittings:
            self.story.append(Paragraph("<b>2.3 Accesorios y Válvulas</b>", 
                                       self.styles['Technical']))
            
            fittings_data = [['Tipo', 'Cantidad', 'Coef. K']]
            for fitting in fittings:
                fittings_data.append([
                    fitting['type'],
                    str(fitting['quantity']),
                    f"{fitting.get('k', 0):.2f}"
                ])
            
            table = self._create_styled_table(fittings_data)
            self.story.append(table)
            self.story.append(Spacer(1, 0.5*cm))
    
    def add_calculations(self, results: Dict):
        """Añade cálculos detallados"""
        self.add_section("3. CÁLCULOS HIDRÁULICOS")
        
        # Parámetros básicos
        calc_data = [
            ['Parámetro', 'Valor', 'Unidad', 'Fórmula/Ref.'],
            ['Velocidad', f"{results.get('velocity', 0):.3f}", 'm/s', 'V = Q/A'],
            ['Número de Reynolds', f"{results.get('reynolds', 0):.0f}", '-', 'Re = VD/ν'],
            ['Tipo de flujo', results.get('flow_type', 'N/A'), '-', 'Criterio: Re'],
            ['Factor de fricción', f"{results.get('friction_factor', 0):.5f}", '-', 'Colebrook-White'],
            ['Pérdida por fricción', f"{results.get('head_loss_friction', 0):.3f}", 'm', 'Darcy-Weisbach'],
            ['Pérdidas menores', f"{results.get('head_loss_minor', 0):.3f}", 'm', 'K·V²/2g'],
            ['<b>Pérdida total</b>', f"<b>{results.get('total_head_loss', 0):.3f}</b>", '<b>m</b>', '-'],
            ['Presión equivalente', f"{results.get('pressure_loss', 0)/1000:.2f}", 'kPa', 'ΔP = ρgH'],
        ]
        
        table = self._create_styled_table(calc_data, col_widths=[5*cm, 3*cm, 2*cm, 4*cm])
        self.story.append(table)
        self.story.append(Spacer(1, 0.5*cm))
        
        # Ecuaciones utilizadas
        self.story.append(Paragraph("<b>3.1 Ecuaciones Fundamentales</b>", 
                                   self.styles['Technical']))
        
        equations = """
        <b>Ecuación de Darcy-Weisbach:</b><br/>
        h<sub>f</sub> = f · (L/D) · (V²/2g)<br/><br/>
        
        <b>Ecuación de Colebrook-White:</b><br/>
        1/√f = -2·log₁₀(ε/3.7D + 2.51/Re√f)<br/><br/>
        
        <b>Número de Reynolds:</b><br/>
        Re = ρVD/μ = VD/ν<br/><br/>
        
        <b>Pérdidas menores:</b><br/>
        h<sub>m</sub> = K · V²/2g
        """
        
        self.story.append(Paragraph(equations, self.styles['Technical']))
        self.story.append(Spacer(1, 0.5*cm))
    
    def add_pump_analysis(self, pump_results: Dict):
        """Añade análisis de la bomba"""
        self.add_section("4. SELECCIÓN Y ANÁLISIS DE BOMBA")
        
        pump_data = [
            ['Parámetro', 'Valor', 'Unidad', 'Normativa'],
            ['Potencia hidráulica', f"{pump_results.get('hydraulic_power_kw', 0):.2f}", 'kW', 'ISO 9906'],
            ['Potencia al eje', f"{pump_results.get('shaft_power_kw', 0):.2f}", 'kW', 'ISO 9906'],
            ['Potencia del motor', f"{pump_results.get('motor_power_kw', 0):.2f}", 'kW', 'NEMA/IEC'],
            ['Potencia motor (HP)', f"{pump_results.get('motor_power_hp', 0):.1f}", 'HP', '-'],
            ['Eficiencia', f"{pump_results.get('efficiency', 0)*100:.1f}", '%', 'ISO 9906'],
            ['NPSH disponible', f"{pump_results.get('npsh_available', 0):.2f}", 'm', 'ANSI/HI 9.6.1'],
            ['NPSH requerido', f"{pump_results.get('npsh_required', 0):.2f}", 'm', 'ANSI/HI 9.6.1'],
            ['Velocidad específica', f"{pump_results.get('specific_speed', 0):.1f}", '-', 'ISO 9906'],
            ['Tipo de bomba', pump_results.get('pump_type', 'N/A'), '-', 'Clasificación Ns'],
        ]
        
        table = self._create_styled_table(pump_data, col_widths=[5*cm, 3*cm, 2*cm, 4*cm])
        self.story.append(table)
        self.story.append(Spacer(1, 0.5*cm))
        
        # Verificación de cavitación
        cavitation = pump_results.get('cavitation_check', {})
        status_color = 'green' if cavitation.get('safe', False) else 'red'
        
        cav_text = f"""
        <b>4.1 Verificación de Cavitación (ANSI/HI 9.6.1)</b><br/>
        <b>Estado:</b> <font color="{status_color}">{cavitation.get('status', 'N/A')}</font><br/>
        <b>Margen:</b> {cavitation.get('margin', 0):.2f} m<br/>
        <b>Recomendación:</b> {cavitation.get('recommendation', 'N/A')}
        """
        
        self.story.append(Paragraph(cav_text, self.styles['Technical']))
        self.story.append(Spacer(1, 0.5*cm))
    
    def add_verification(self, checks: Dict):
        """Añade verificaciones de normativas"""
        self.add_section("5. VERIFICACIÓN DE CUMPLIMIENTO NORMATIVO")
        
        # Verificación de velocidad
        vel_check = checks.get('velocity_check', {})
        vel_status = "✓ CUMPLE" if vel_check.get('in_range', False) else "✗ NO CUMPLE"
        
        vel_text = f"""
        <b>5.1 Velocidad del Fluido (ISO 15649)</b><br/>
        Velocidad: {vel_check.get('velocity', 0):.2f} m/s<br/>
        Rango permitido: {vel_check.get('limits', {}).get('min', 0):.1f} - {vel_check.get('limits', {}).get('max', 0):.1f} m/s<br/>
        Estado: {vel_status}<br/>
        """
        
        self.story.append(Paragraph(vel_text, self.styles['Technical']))
        
        if vel_check.get('warnings'):
            for warning in vel_check['warnings']:
                self.story.append(Paragraph(f"⚠ {warning}", self.styles['Technical']))
        
        self.story.append(Spacer(1, 0.5*cm))
        
        # Verificación de presión
        pressure_check = checks.get('pressure_check', {})
        if pressure_check:
            press_text = f"""
            <b>5.2 Clase de Presión (ASME B31.3 / DIN)</b><br/>
            Presión de operación: {pressure_check.get('operating_pressure', 0):.1f} bar<br/>
            Presión de diseño: {pressure_check.get('design_pressure', 0):.1f} bar<br/>
            Clase recomendada: {pressure_check.get('recommended_class', 'N/A')}<br/>
            """
            self.story.append(Paragraph(press_text, self.styles['Technical']))
            self.story.append(Spacer(1, 0.5*cm))
    
    def add_conclusions(self, conclusions: List[str]):
        """Añade conclusiones"""
        self.add_section("6. CONCLUSIONES Y RECOMENDACIONES")
        
        for i, conclusion in enumerate(conclusions, 1):
            text = Paragraph(f"{i}. {conclusion}", self.styles['Technical'])
            self.story.append(text)
            self.story.append(Spacer(1, 0.2*cm))
    
    def add_image(self, image_path: str, width: float = 15*cm, caption: str = ""):
        """Añade una imagen al documento"""
        try:
            img = Image(image_path, width=width)
            self.story.append(img)
            
            if caption:
                cap = Paragraph(f"<i>{caption}</i>", self.styles['Technical'])
                self.story.append(cap)
            
            self.story.append(Spacer(1, 0.5*cm))
        except:
            pass
    
    def _create_styled_table(self, data: List[List], col_widths: List = None):
        """Crea una tabla con estilo consistente"""
        if col_widths is None:
            col_widths = [5*cm, 4*cm, 3*cm]
        
        table = Table(data, colWidths=col_widths)
        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Body
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        return table
    
    def generate(self):
        """Genera el PDF final"""
        self.doc.build(self.story)
        return self.filename
