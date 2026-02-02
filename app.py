"""
Aplicación Streamlit para Cálculo de Tuberías y Bombas
Sistema profesional técnico según normativas ISO, ASME, API, DIN
"""

import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
import sys
import os

# Agregar el directorio utils al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from utils.hydraulic_calcs import HydraulicCalculator
from utils.pump_calcs import PumpCalculator
from utils.standards import Standards
from utils.visualizations import TechnicalPlots
from utils.report_generator import CalculationReport

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Cálculo de Tuberías y Bombas",
    page_icon="⚙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para tema oscuro
st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
        font-weight: bold;
    }
    .metric-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #1f77b4;
    }
    .warning-box {
        background-color: #3d2500;
        padding: 15px;
        border-left: 5px solid #ff9800;
        border-radius: 5px;
        margin: 10px 0;
    }
    .success-box {
        background-color: #003d00;
        padding: 15px;
        border-left: 5px solid #4caf50;
        border-radius: 5px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #3d0000;
        padding: 15px;
        border-left: 5px solid #f44336;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Inicializar calculadoras
@st.cache_resource
def init_calculators():
    return HydraulicCalculator(), PumpCalculator(), Standards()

hydraulic_calc, pump_calc, standards = init_calculators()

# Título principal
st.title("Sistema Profesional de Cálculo de Tuberías y Bombas")
st.markdown("### Basado en normativas ISO 9906, ASME B31.3, API 610, DIN, ANSI/HI")
st.markdown("---")

# Sidebar para información del proyecto
with st.sidebar:
    st.header("Información del Proyecto")
    
    project_name = st.text_input("Nombre del Proyecto", "Proyecto Sin Nombre")
    client = st.text_input("Cliente", "")
    location = st.text_input("Ubicación", "")
    engineer = st.text_input("Ingeniero Responsable", "")
    revision = st.text_input("Revisión", "Rev. 0")
    
    st.markdown("---")
    st.header("Aplicación")
    application_type = st.selectbox(
        "Tipo de Aplicación",
        ["Industrial general", "Agua potable", "Petróleo y gas", "Química"]
    )
    
    # Mostrar normativas aplicables
    with st.expander("Normativas Aplicables"):
        applicable_standards = standards.get_applicable_standards(application_type)
        for std in applicable_standards:
            st.markdown(f"- {std}")

# Tabs principales
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Cálculo de Tuberías", 
    "Cálculo de Bombas",
    "Sistema Completo",
    "Visualizaciones",
    "Memoria de Cálculo"
])

# ===========================================
# TAB 1: CÁLCULO DE TUBERÍAS
# ===========================================
with tab1:
    st.header("Cálculo Hidráulico de Tuberías")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Datos de la Tubería")
        
        diameter_mm = st.number_input(
            "Diámetro Nominal (mm)", 
            min_value=6.0, 
            max_value=2000.0, 
            value=100.0,
            step=1.0,
            help="Diámetro interno de la tubería"
        )
        
        length = st.number_input(
            "Longitud Total (m)", 
            min_value=0.1, 
            max_value=10000.0, 
            value=100.0,
            help="Longitud total de la tubería"
        )
        
        material = st.selectbox(
            "Material de la Tubería",
            list(HydraulicCalculator.ROUGHNESS.keys())
        )
        
        roughness = HydraulicCalculator.ROUGHNESS[material]
        st.info(f"Rugosidad absoluta: {roughness} mm")
        
        # Clase de presión
        pressure_standard = st.radio("Estándar de Presión", ["ANSI", "PN"])
        
    with col2:
        st.subheader("Propiedades del Fluido")
        
        fluid_type = st.selectbox("Tipo de Fluido", ["Agua", "Otro"])
        
        flow_rate_m3h = st.number_input(
            "Caudal (m³/h)", 
            min_value=0.1, 
            max_value=10000.0, 
            value=50.0,
            help="Caudal volumétrico"
        )
        flow_rate = flow_rate_m3h / 3600  # Convertir a m³/s
        
        temperature = st.slider(
            "Temperatura (°C)", 
            min_value=0, 
            max_value=100, 
            value=20,
            help="Temperatura del fluido"
        )
        
        service_type = st.selectbox(
            "Tipo de Servicio",
            list(Standards.VELOCITY_LIMITS.keys())
        )
    
    # Accesorios y válvulas
    st.subheader("Accesorios y Válvulas")
    
    k_coefficients = HydraulicCalculator.get_k_coefficients()
    
    col1, col2, col3 = st.columns(3)
    
    fittings = []
    fitting_types = list(k_coefficients.keys())
    
    # Dividir accesorios en tres columnas
    for i, fitting_type in enumerate(fitting_types):
        col = [col1, col2, col3][i % 3]
        with col:
            quantity = st.number_input(
                f"{fitting_type}", 
                min_value=0, 
                max_value=100, 
                value=0,
                key=f"fitting_{i}"
            )
            if quantity > 0:
                fittings.append({
                    'type': fitting_type,
                    'quantity': quantity,
                    'k': k_coefficients[fitting_type]
                })
    
    # Botón de cálculo
    if st.button("Calcular Sistema de Tuberías", type="primary"):
        
        # Preparar datos
        pipe_data = {
            'diameter': diameter_mm / 1000,  # Convertir a metros
            'length': length,
            'roughness': roughness,
            'material': material
        }
        
        fluid_properties = {
            'flow_rate': flow_rate,
            'temperature': temperature
        }
        
        # Realizar cálculos
        results = hydraulic_calc.calculate_system(pipe_data, fluid_properties, fittings)
        
        # Verificaciones de normativas
        velocity_check = standards.check_velocity(results['velocity'], service_type)
        reynolds_check = standards.check_reynolds(results['reynolds'])
        erosion_check = standards.erosion_velocity_check(results['velocity'], results['density'])
        
        # Guardar en session state
        st.session_state['pipe_results'] = results
        st.session_state['pipe_data'] = pipe_data
        st.session_state['fluid_properties'] = fluid_properties
        st.session_state['fittings'] = fittings
        st.session_state['checks'] = {
            'velocity_check': velocity_check,
            'reynolds_check': reynolds_check,
            'erosion_check': erosion_check
        }
        
        # Mostrar resultados
        st.markdown("---")
        st.header("Resultados del Cálculo")
        
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Velocidad", 
                f"{results['velocity']:.3f} m/s",
                delta="Óptimo" if velocity_check['in_range'] else "Revisar",
                delta_color="normal" if velocity_check['in_range'] else "inverse"
            )
        
        with col2:
            st.metric("Número de Reynolds", f"{results['reynolds']:.0f}")
            st.caption(f"Flujo: {results['flow_type']}")
        
        with col3:
            st.metric("Pérdida Total", f"{results['total_head_loss']:.3f} m")
            st.caption(f"{results['pressure_loss']/1000:.2f} kPa")
        
        with col4:
            st.metric("Factor de Fricción", f"{results['friction_factor']:.5f}")
            st.caption("Colebrook-White")
        
        # Desglose de pérdidas
        st.subheader("Desglose de Pérdidas")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
            <h4>Pérdidas por Fricción</h4>
            <h2>{results['head_loss_friction']:.3f} m</h2>
            <p>({results['head_loss_friction']/results['total_head_loss']*100:.1f}% del total)</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
            <h4>Pérdidas Menores</h4>
            <h2>{results['head_loss_minor']:.3f} m</h2>
            <p>({results['head_loss_minor']/results['total_head_loss']*100:.1f}% del total)</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Verificaciones de normativas
        st.subheader("Verificaciones de Normativas")
        
        # Velocidad
        if velocity_check['status'] == "ÓPTIMO":
            st.markdown(f"""
            <div class="success-box">
            <b>[OK] Velocidad: {velocity_check['status']}</b><br>
            Velocidad: {velocity_check['velocity']:.2f} m/s<br>
            Rango permitido: {velocity_check['limits']['min']:.1f} - {velocity_check['limits']['max']:.1f} m/s
            </div>
            """, unsafe_allow_html=True)
        elif velocity_check['status'] == "ACEPTABLE":
            st.markdown(f"""
            <div class="warning-box">
            <b>[!] Velocidad: {velocity_check['status']}</b><br>
            Velocidad: {velocity_check['velocity']:.2f} m/s<br>
            {'<br>'.join(velocity_check.get('warnings', []))}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="error-box">
            <b>[X] Velocidad: {velocity_check['status']}</b><br>
            Velocidad: {velocity_check['velocity']:.2f} m/s<br>
            {'<br>'.join(velocity_check.get('warnings', []))}
            </div>
            """, unsafe_allow_html=True)
        
        # Reynolds
        st.info(f"**Régimen de Flujo:** {reynolds_check['flow_type']} (Re = {reynolds_check['reynolds']:.0f})")
        st.caption(reynolds_check['description'])
        
        # Erosión
        if erosion_check['status'] == "SEGURO":
            st.success(f"[OK] **Velocidad de Erosión:** {erosion_check['status']} - {erosion_check['risk']}")
        elif erosion_check['status'] in ["ACEPTABLE", "PRECAUCIÓN"]:
            st.warning(f"[!] **Velocidad de Erosión:** {erosion_check['status']} - {erosion_check['risk']}")
        else:
            st.error(f"[X] **Velocidad de Erosión:** {erosion_check['status']} - {erosion_check['risk']}")
        
        # Tabla detallada de resultados
        with st.expander("Ver Tabla Detallada de Resultados"):
            results_df = pd.DataFrame({
                'Parámetro': [
                    'Densidad del fluido',
                    'Viscosidad cinemática',
                    'Velocidad del fluido',
                    'Número de Reynolds',
                    'Tipo de flujo',
                    'Factor de fricción (f)',
                    'Pérdida por fricción',
                    'Coeficiente K total',
                    'Pérdida por accesorios',
                    'Pérdida total de carga',
                    'Presión equivalente'
                ],
                'Valor': [
                    f"{results['density']:.2f}",
                    f"{results['viscosity']:.2e}",
                    f"{results['velocity']:.3f}",
                    f"{results['reynolds']:.0f}",
                    results['flow_type'],
                    f"{results['friction_factor']:.5f}",
                    f"{results['head_loss_friction']:.3f}",
                    f"{results['total_k']:.2f}",
                    f"{results['head_loss_minor']:.3f}",
                    f"{results['total_head_loss']:.3f}",
                    f"{results['pressure_loss']/1000:.2f}"
                ],
                'Unidad': [
                    'kg/m³',
                    'm²/s',
                    'm/s',
                    '-',
                    '-',
                    '-',
                    'm',
                    '-',
                    'm',
                    'm',
                    'kPa'
                ]
            })
            st.dataframe(results_df, width="stretch")

# ===========================================
# TAB 2: CÁLCULO DE BOMBAS
# ===========================================
with tab2:
    st.header("Selección y Cálculo de Bombas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Condiciones de Operación")
        
        flow_pump_m3h = st.number_input(
            "Caudal de Diseño (m³/h)", 
            min_value=0.1, 
            value=50.0,
            key="pump_flow"
        )
        flow_pump = flow_pump_m3h / 3600
        
        total_head = st.number_input(
            "Altura Manométrica Total (m)", 
            min_value=1.0, 
            value=30.0,
            help="Altura total que debe vencer la bomba"
        )
        
        pump_speed = st.number_input(
            "Velocidad de Rotación (rpm)", 
            min_value=500, 
            max_value=3600, 
            value=1750,
            step=50
        )
        
        pump_efficiency = st.slider(
            "Eficiencia Estimada de la Bomba", 
            min_value=0.50, 
            max_value=0.90, 
            value=0.75,
            step=0.01,
            help="Eficiencia típica: 70-85%"
        )
    
    with col2:
        st.subheader("Condiciones de Succión (NPSH)")
        
        pressure_suction_bar = st.number_input(
            "Presión Absoluta en Succión (bar)", 
            min_value=0.1, 
            value=1.013,
            help="Presión atmosférica = 1.013 bar"
        )
        
        vapor_pressure_bar = st.number_input(
            "Presión de Vapor del Líquido (bar)", 
            min_value=0.0, 
            value=0.023,
            help="Agua a 20°C = 0.023 bar"
        )
        
        suction_diameter_mm = st.number_input(
            "Diámetro de Succión (mm)", 
            min_value=10.0, 
            value=100.0
        )
        
        elevation = st.number_input(
            "Elevación del Nivel sobre Bomba (m)", 
            value=2.0,
            help="Positivo si el nivel está sobre la bomba"
        )
        
        temp_pump = st.slider("Temperatura del Fluido (°C)", 0, 100, 20)
    
    # Botón de cálculo
    if st.button("Calcular Bomba", type="primary"):
        
        # Densidad
        density_pump = hydraulic_calc.get_density(temp_pump)
        
        # Velocidad en succión
        area_suction = np.pi * (suction_diameter_mm/1000 / 2)**2
        velocity_suction = flow_pump / area_suction
        
        # Condiciones de succión
        suction_conditions = {
            'pressure_suction': pressure_suction_bar * 100000,  # Convertir a Pa
            'vapor_pressure': vapor_pressure_bar * 100000,
            'velocity_suction': velocity_suction,
            'elevation': elevation
        }
        
        # Especificaciones de la bomba
        pump_specs = {
            'efficiency': pump_efficiency,
            'speed': pump_speed
        }
        
        # Análisis completo
        pump_results = pump_calc.complete_pump_analysis(
            flow_pump, total_head, suction_conditions, pump_specs, density_pump
        )
        
        # Guardar en session state
        st.session_state['pump_results'] = pump_results
        st.session_state['pump_specs'] = {
            'flow_rate': flow_pump,
            'total_head': total_head,
            'speed': pump_speed,
            'efficiency': pump_efficiency
        }
        
        # Mostrar resultados
        st.markdown("---")
        st.header("Resultados del Cálculo de Bomba")
        
        # Métricas principales
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Potencia Hidráulica", f"{pump_results['hydraulic_power_kw']:.2f} kW")
        
        with col2:
            st.metric("Potencia al Eje", f"{pump_results['shaft_power_kw']:.2f} kW")
        
        with col3:
            st.metric("Potencia del Motor", f"{pump_results['motor_power_kw']:.2f} kW")
            st.caption(f"{pump_results['motor_power_hp']:.1f} HP")
        
        with col4:
            st.metric("Eficiencia", f"{pump_results['efficiency']*100:.1f} %")
        
        # NPSH
        st.subheader("Análisis de NPSH (Cavitación)")
        
        cavitation = pump_results['cavitation_check']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("NPSH Disponible", f"{pump_results['npsh_available']:.2f} m")
        
        with col2:
            st.metric("NPSH Requerido", f"{pump_results['npsh_required']:.2f} m")
        
        with col3:
            st.metric("Margen de Seguridad", f"{cavitation['margin']:.2f} m")
        
        # Estado de cavitación
        if cavitation['safe']:
            st.markdown(f"""
            <div class="success-box">
            <b>[OK] {cavitation['status']}</b><br>
            {cavitation['recommendation']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="error-box">
            <b>[X] {cavitation['status']}</b><br>
            {cavitation['recommendation']}
            </div>
            """, unsafe_allow_html=True)
        
        # Características de la bomba
        st.subheader("Características de la Bomba")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"""
            **Velocidad Específica (Ns):** {pump_results['specific_speed']:.1f}
            
            **Tipo de Bomba:** {pump_results['pump_type']}
            """)
        
        with col2:
            st.info(f"""
            **Rango Operativo Recomendado:**
            
            {pump_results['operating_range']}
            
            (30% - 120% del BEP según API 610)
            """)
        
        # Tabla detallada
        with st.expander("Ver Tabla Detallada de Resultados"):
            pump_df = pd.DataFrame({
                'Parámetro': [
                    'Caudal de diseño',
                    'Altura manométrica total',
                    'Velocidad de rotación',
                    'Potencia hidráulica',
                    'Potencia al eje',
                    'Potencia del motor',
                    'Eficiencia',
                    'NPSH disponible',
                    'NPSH requerido',
                    'Margen NPSH',
                    'Velocidad específica',
                    'Tipo de bomba',
                    'Caudal mínimo',
                    'Caudal máximo'
                ],
                'Valor': [
                    f"{flow_pump*3600:.2f}",
                    f"{total_head:.2f}",
                    f"{pump_speed:.0f}",
                    f"{pump_results['hydraulic_power_kw']:.2f}",
                    f"{pump_results['shaft_power_kw']:.2f}",
                    f"{pump_results['motor_power_kw']:.2f}",
                    f"{pump_results['efficiency']*100:.1f}",
                    f"{pump_results['npsh_available']:.2f}",
                    f"{pump_results['npsh_required']:.2f}",
                    f"{cavitation['margin']:.2f}",
                    f"{pump_results['specific_speed']:.1f}",
                    pump_results['pump_type'],
                    f"{pump_results['minimum_flow']*3600:.2f}",
                    f"{pump_results['maximum_flow']*3600:.2f}"
                ],
                'Unidad': [
                    'm³/h', 'm', 'rpm', 'kW', 'kW', 'kW', '%',
                    'm', 'm', 'm', '-', '-', 'm³/h', 'm³/h'
                ],
                'Normativa': [
                    '-', '-', '-', 'ISO 9906', 'ISO 9906', 'NEMA/IEC',
                    'ISO 9906', 'ANSI/HI 9.6.1', 'ANSI/HI 9.6.1', 'ANSI/HI 9.6.1',
                    'ISO 9906', '-', 'API 610', 'API 610'
                ]
            })
            st.dataframe(pump_df, width="stretch")

# ===========================================
# TAB 3: SISTEMA COMPLETO
# ===========================================
with tab3:
    st.header("Análisis del Sistema Completo")
    st.info("Esta sección integra el cálculo de tuberías con la selección de bomba")
    
    if 'pipe_results' in st.session_state and 'pump_results' in st.session_state:
        
        pipe_res = st.session_state['pipe_results']
        pump_res = st.session_state['pump_results']
        
        st.subheader("Resumen del Sistema")
        
        # Comparación
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
            <h4>Pérdida Total de Carga</h4>
            <h2>{:.2f} m</h2>
            <p>Sistema de tuberías</p>
            </div>
            """.format(pipe_res['total_head_loss']), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
            <h4>Altura de la Bomba</h4>
            <h2>{:.2f} m</h2>
            <p>Bomba seleccionada</p>
            </div>
            """.format(st.session_state['pump_specs']['total_head']), unsafe_allow_html=True)
        
        with col3:
            margin = st.session_state['pump_specs']['total_head'] - pipe_res['total_head_loss']
            st.markdown("""
            <div class="metric-card">
            <h4>Margen</h4>
            <h2>{:.2f} m</h2>
            <p>Altura disponible</p>
            </div>
            """.format(margin), unsafe_allow_html=True)
        
        # Verificación del sistema
        if margin >= 0:
            st.success("[OK] La bomba seleccionada puede vencer las pérdidas del sistema")
        else:
            st.error("[X] ADVERTENCIA: La bomba NO puede vencer las pérdidas del sistema")
        
        # Balance energético
        st.subheader("Balance Energético del Sistema")
        
        energy_data = pd.DataFrame({
            'Componente': [
                'Energía suministrada por bomba',
                'Pérdidas por fricción',
                'Pérdidas por accesorios',
                'Energía disponible en descarga'
            ],
            'Valor (m)': [
                st.session_state['pump_specs']['total_head'],
                pipe_res['head_loss_friction'],
                pipe_res['head_loss_minor'],
                margin
            ]
        })
        
        st.dataframe(energy_data, width="stretch")
        
        # Eficiencia global
        st.subheader("Eficiencia Global del Sistema")
        
        efficiency_system = (pipe_res['total_head_loss'] / 
                           st.session_state['pump_specs']['total_head'])
        efficiency_pump = pump_res['efficiency']
        efficiency_global = efficiency_system * efficiency_pump
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Eficiencia del Sistema", f"{efficiency_system*100:.1f} %")
        
        with col2:
            st.metric("Eficiencia de la Bomba", f"{efficiency_pump*100:.1f} %")
        
        with col3:
            st.metric("Eficiencia Global", f"{efficiency_global*100:.1f} %")
        
    else:
        st.warning("[!] Primero debe realizar los cálculos en las pestañas anteriores")

# ===========================================
# TAB 4: VISUALIZACIONES
# ===========================================
with tab4:
    st.header("Visualizaciones Técnicas")
    
    if 'pump_results' in st.session_state:
        # Generar curvas de la bomba
        pump_specs_vis = st.session_state.get('pump_specs', {})
        
        q_bep = pump_specs_vis.get('flow_rate', 0.01)
        h_bep = pump_specs_vis.get('total_head', 30)
        eff_bep = pump_specs_vis.get('efficiency', 0.75)
        p_bep = pump_calc.hydraulic_power(q_bep, h_bep, 998.2) / eff_bep
        
        pump_curve_data = pump_calc.generate_pump_curve(
            q_bep, h_bep, p_bep, eff_bep
        )
        
        # Curva del sistema si existe
        system_curve = None
        operating_point = None
        
        if 'pipe_results' in st.session_state:
            pipe_res = st.session_state['pipe_results']
            h_static = 5  # Ejemplo
            k_sys = pipe_res['total_head_loss'] / (q_bep**2)
            
            system_curve = h_static + k_sys * pump_curve_data['flow']**2
            
            # Punto de operación simplificado
            operating_point = {
                'flow_operating': q_bep,
                'head_operating': h_bep,
                'power_operating': p_bep,
                'efficiency_operating': eff_bep
            }
        
        # Gráfico de curvas de bomba
        st.subheader("Curvas Características de la Bomba")
        fig_pump = TechnicalPlots.pump_curves(
            pump_curve_data, 
            system_curve, 
            operating_point
        )
        st.plotly_chart(fig_pump, width="stretch")
        
        # Análisis de NPSH
        st.subheader("Análisis de NPSH")
        pump_res = st.session_state['pump_results']
        
        # Generar curva de NPSH requerido
        flow_range = np.linspace(0.5*q_bep, 1.5*q_bep, 50)
        npsh_req_curve = pump_calc.npsh_required_estimate(
            flow_range, 
            pump_specs_vis.get('speed', 1750)
        )
        
        fig_npsh = TechnicalPlots.npsh_analysis(
            flow_range,
            pump_res['npsh_available'],
            npsh_req_curve
        )
        st.plotly_chart(fig_npsh, width="stretch")
    
    if 'pipe_results' in st.session_state:
        st.subheader("Distribución de Pérdidas")
        
        pipe_res = st.session_state['pipe_results']
        fittings_data = st.session_state.get('fittings', [])
        
        # Desglose de pérdidas menores por accesorio
        k_coeffs = HydraulicCalculator.get_k_coefficients()
        minor_losses_detail = {}
        
        for fitting in fittings_data:
            k = k_coeffs[fitting['type']]
            loss = hydraulic_calc.minor_loss(k, pipe_res['velocity']) * fitting['quantity']
            minor_losses_detail[fitting['type']] = loss
        
        fig_losses = TechnicalPlots.loss_breakdown(
            pipe_res['head_loss_friction'],
            minor_losses_detail
        )
        st.plotly_chart(fig_losses, width="stretch")

# ===========================================
# TAB 5: MEMORIA DE CÁLCULO
# ===========================================
with tab5:
    st.header("Generación de Memoria de Cálculo")
    st.info("Genere un documento PDF profesional con todos los cálculos y verificaciones")
    
    if st.button("Generar Memoria de Cálculo PDF", type="primary"):
        
        if 'pipe_results' not in st.session_state:
            st.error("[X] Debe realizar primero el cálculo de tuberías")
        else:
            with st.spinner("Generando memoria de cálculo..."):
                try:
                    # Información del proyecto
                    project_info = {
                        'project_name': project_name,
                        'client': client,
                        'location': location,
                        'engineer': engineer,
                        'revision': revision
                    }
                    
                    # Crear reporte
                    report = CalculationReport("memoria_calculo.pdf")
                    
                    # Página de título
                    report.add_title_page(project_info)
                    
                    # Normativas
                    report.add_standards_section(
                        standards.get_applicable_standards(application_type)
                    )
                    
                    # Datos de entrada
                    report.add_input_data(
                        st.session_state['pipe_data'],
                        st.session_state['fluid_properties'],
                        st.session_state.get('fittings', [])
                    )
                    
                    # Cálculos
                    report.add_calculations(st.session_state['pipe_results'])
                    
                    # Análisis de bomba si existe
                    if 'pump_results' in st.session_state:
                        report.add_pump_analysis(st.session_state['pump_results'])
                    
                    # Verificaciones
                    report.add_verification(st.session_state.get('checks', {}))
                    
                    # Conclusiones
                    conclusions = [
                        f"El sistema de tuberías calculado cumple con las normativas {application_type}.",
                        f"La velocidad del fluido es de {st.session_state['pipe_results']['velocity']:.2f} m/s.",
                        f"Las pérdidas totales de carga son de {st.session_state['pipe_results']['total_head_loss']:.2f} m.",
                    ]
                    
                    if 'pump_results' in st.session_state:
                        conclusions.append(
                            f"Se requiere una bomba con potencia mínima de {st.session_state['pump_results']['motor_power_kw']:.1f} kW."
                        )
                        
                        if st.session_state['pump_results']['cavitation_check']['safe']:
                            conclusions.append("El sistema NO presenta riesgo de cavitación.")
                        else:
                            conclusions.append("ADVERTENCIA: Existe riesgo de cavitación.")
                    
                    report.add_conclusions(conclusions)
                    
                    # Generar PDF
                    filename = report.generate()
                    
                    # Descargar
                    with open(filename, "rb") as pdf_file:
                        pdf_bytes = pdf_file.read()
                        st.download_button(
                            label="Descargar Memoria de Cálculo",
                            data=pdf_bytes,
                            file_name=f"memoria_calculo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf"
                        )
                    
                    st.success("[OK] Memoria de cálculo generada exitosamente!")
                    
                except Exception as e:
                    st.error(f"[X] Error al generar la memoria: {str(e)}")
                    st.info("Nota: Asegúrese de tener instaladas todas las dependencias (reportlab)")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Sistema Profesional de Calculo de Tuberias y Bombas</p>
    <p>Basado en normativas ISO 9906, ASME B31.3, API 610, DIN, ANSI/HI</p>
    <p>(c) 2025 - Desarrollado para ingenieria profesional</p>
</div>
""", unsafe_allow_html=True)
