"""
Módulo de visualizaciones técnicas con Plotly
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, List, Optional


class TechnicalPlots:
    """
    Generador de gráficos técnicos profesionales
    """
    
    # Tema oscuro personalizado
    DARK_THEME = {
        'plot_bgcolor': '#0e1117',
        'paper_bgcolor': '#0e1117',
        'font_color': '#fafafa',
    }
    
    GRID_CONFIG = {
        'showgrid': True,
        'gridwidth': 1,
        'gridcolor': '#333333',
    }
    
    @staticmethod
    def pump_curves(pump_data: Dict, system_data: Optional[Dict] = None,
                   operating_point: Optional[Dict] = None) -> go.Figure:
        """
        Gráfico de curvas características de la bomba
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Curva H-Q', 'Curva de Eficiencia', 
                          'Curva de Potencia', 'Punto de Operación'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        flow = pump_data['flow'] * 3600  # Convertir a m³/h
        
        # Curva H-Q
        fig.add_trace(
            go.Scatter(x=flow, y=pump_data['head'], 
                      name='Altura (H)', 
                      line=dict(color='#1f77b4', width=3)),
            row=1, col=1
        )
        
        if system_data is not None:
            fig.add_trace(
                go.Scatter(x=flow, y=system_data, 
                          name='Curva del Sistema',
                          line=dict(color='#ff7f0e', width=2, dash='dash')),
                row=1, col=1
            )
        
        if operating_point is not None:
            fig.add_trace(
                go.Scatter(x=[operating_point['flow_operating']*3600], 
                          y=[operating_point['head_operating']],
                          name='Punto de Operación',
                          mode='markers',
                          marker=dict(size=12, color='red', symbol='star')),
                row=1, col=1
            )
        
        # Curva de eficiencia
        fig.add_trace(
            go.Scatter(x=flow, y=pump_data['efficiency']*100,
                      name='Eficiencia (η)',
                      line=dict(color='#2ca02c', width=3)),
            row=1, col=2
        )
        
        # Curva de potencia
        fig.add_trace(
            go.Scatter(x=flow, y=pump_data['power']/1000,
                      name='Potencia (P)',
                      line=dict(color='#d62728', width=3)),
            row=2, col=1
        )
        
        # Punto de operación combinado
        if operating_point is not None:
            q_op = operating_point['flow_operating'] * 3600
            h_op = operating_point['head_operating']
            eff_op = operating_point['efficiency_operating'] * 100
            p_op = operating_point['power_operating'] / 1000
            
            fig.add_trace(
                go.Bar(x=['Caudal (m³/h)', 'Altura (m)', 'Eficiencia (%)', 'Potencia (kW)'],
                      y=[q_op, h_op, eff_op, p_op],
                      marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']),
                row=2, col=2
            )
        
        # Actualizar ejes
        fig.update_xaxes(title_text="Caudal (m³/h)", row=1, col=1, **TechnicalPlots.GRID_CONFIG)
        fig.update_yaxes(title_text="Altura (m)", row=1, col=1, **TechnicalPlots.GRID_CONFIG)
        
        fig.update_xaxes(title_text="Caudal (m³/h)", row=1, col=2, **TechnicalPlots.GRID_CONFIG)
        fig.update_yaxes(title_text="Eficiencia (%)", row=1, col=2, **TechnicalPlots.GRID_CONFIG)
        
        fig.update_xaxes(title_text="Caudal (m³/h)", row=2, col=1, **TechnicalPlots.GRID_CONFIG)
        fig.update_yaxes(title_text="Potencia (kW)", row=2, col=1, **TechnicalPlots.GRID_CONFIG)
        
        # Aplicar tema
        fig.update_layout(
            height=800,
            showlegend=True,
            **TechnicalPlots.DARK_THEME,
            title_text="Curvas Características de la Bomba",
            title_font_size=20,
        )
        
        return fig
    
    @staticmethod
    def hydraulic_profile(distances: List[float], elevations: List[float],
                         pressure_heads: List[float], 
                         labels: Optional[List[str]] = None) -> go.Figure:
        """
        Perfil hidráulico del sistema
        """
        fig = go.Figure()
        
        # Línea de elevación
        fig.add_trace(go.Scatter(
            x=distances, y=elevations,
            name='Elevación del Terreno',
            fill='tozeroy',
            fillcolor='rgba(139, 69, 19, 0.3)',
            line=dict(color='#8B4513', width=2)
        ))
        
        # Línea piezométrica
        total_head = [e + p for e, p in zip(elevations, pressure_heads)]
        fig.add_trace(go.Scatter(
            x=distances, y=total_head,
            name='Línea Piezométrica',
            line=dict(color='#1f77b4', width=3, dash='dash')
        ))
        
        # Línea de energía (incluye velocidad)
        # Se podría agregar el término de velocidad aquí
        
        # Puntos críticos
        if labels:
            for i, label in enumerate(labels):
                if label:
                    fig.add_annotation(
                        x=distances[i], y=total_head[i],
                        text=label,
                        showarrow=True,
                        arrowhead=2,
                        arrowcolor='white',
                        bgcolor='#262730',
                        bordercolor='white'
                    )
        
        fig.update_layout(
            title='Perfil Hidráulico del Sistema',
            xaxis_title='Distancia (m)',
            yaxis_title='Elevación / Altura (m)',
            **TechnicalPlots.DARK_THEME,
            height=500,
            hovermode='x unified',
            xaxis=TechnicalPlots.GRID_CONFIG,
            yaxis=TechnicalPlots.GRID_CONFIG
        )
        
        return fig
    
    @staticmethod
    def loss_breakdown(friction_loss: float, minor_losses: Dict[str, float]) -> go.Figure:
        """
        Gráfico de desglose de pérdidas
        """
        # Preparar datos
        labels = ['Pérdidas por Fricción'] + list(minor_losses.keys())
        values = [friction_loss] + list(minor_losses.values())
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(colors=px.colors.qualitative.Set3)
        )])
        
        fig.update_layout(
            title='Distribución de Pérdidas de Carga',
            **TechnicalPlots.DARK_THEME,
            height=500,
            annotations=[dict(text='Pérdidas<br>Totales', 
                            x=0.5, y=0.5, font_size=14, showarrow=False)]
        )
        
        return fig
    
    @staticmethod
    def reynolds_flow_regime(reynolds_values: List[float], 
                            velocities: List[float],
                            labels: List[str]) -> go.Figure:
        """
        Gráfico de regímenes de flujo
        """
        fig = go.Figure()
        
        colors = ['green' if 4000 < r < 100000 else 
                 'orange' if 2300 <= r <= 4000 else 'red' 
                 for r in reynolds_values]
        
        fig.add_trace(go.Bar(
            x=labels,
            y=reynolds_values,
            marker_color=colors,
            text=[f'Re={r:.0f}<br>v={v:.2f}m/s' 
                  for r, v in zip(reynolds_values, velocities)],
            textposition='outside',
        ))
        
        # Líneas de referencia
        fig.add_hline(y=2300, line_dash="dash", line_color="yellow",
                     annotation_text="Límite Laminar-Transición")
        fig.add_hline(y=4000, line_dash="dash", line_color="green",
                     annotation_text="Límite Transición-Turbulento")
        
        fig.update_layout(
            title='Análisis del Número de Reynolds',
            xaxis_title='Sección',
            yaxis_title='Número de Reynolds',
            yaxis_type='log',
            **TechnicalPlots.DARK_THEME,
            height=500,
            xaxis=TechnicalPlots.GRID_CONFIG,
            yaxis=TechnicalPlots.GRID_CONFIG
        )
        
        return fig
    
    @staticmethod
    def npsh_analysis(flow_range: np.ndarray, npsh_available: float,
                     npsh_required: np.ndarray) -> go.Figure:
        """
        Análisis de NPSH
        """
        fig = go.Figure()
        
        # NPSH Disponible (línea horizontal)
        fig.add_trace(go.Scatter(
            x=flow_range * 3600,
            y=[npsh_available] * len(flow_range),
            name='NPSH Disponible',
            line=dict(color='green', width=3),
        ))
        
        # NPSH Requerido (curva)
        fig.add_trace(go.Scatter(
            x=flow_range * 3600,
            y=npsh_required,
            name='NPSH Requerido',
            line=dict(color='red', width=3, dash='dash'),
        ))
        
        # Zona de seguridad
        fig.add_trace(go.Scatter(
            x=flow_range * 3600,
            y=npsh_required + 0.5,  # Margen de seguridad
            name='NPSH Req. + Margen',
            line=dict(color='orange', width=2, dash='dot'),
        ))
        
        # Área de riesgo de cavitación
        fig.add_hrect(
            y0=0, y1=npsh_available,
            fillcolor="green", opacity=0.1,
            annotation_text="Zona Segura", annotation_position="top left"
        )
        
        fig.update_layout(
            title='Análisis de NPSH - Verificación de Cavitación',
            xaxis_title='Caudal (m³/h)',
            yaxis_title='NPSH (m)',
            **TechnicalPlots.DARK_THEME,
            height=500,
            hovermode='x unified',
            xaxis=TechnicalPlots.GRID_CONFIG,
            yaxis=TechnicalPlots.GRID_CONFIG
        )
        
        return fig
    
    @staticmethod
    def pressure_profile_3d(pipe_network: Dict) -> go.Figure:
        """
        Visualización 3D de la red de tuberías (isométrico simplificado)
        """
        fig = go.Figure()
        
        # Ejemplo de representación 3D
        # En una implementación real, aquí se procesarían los datos de la red
        
        x = [0, 10, 10, 20, 20, 30]
        y = [0, 0, 10, 10, 5, 5]
        z = [0, 0, 3, 3, 8, 8]
        
        fig.add_trace(go.Scatter3d(
            x=x, y=y, z=z,
            mode='lines+markers',
            line=dict(color='cyan', width=6),
            marker=dict(size=8, color='red'),
            text=[f'P{i}' for i in range(len(x))],
        ))
        
        fig.update_layout(
            title='Vista Isométrica del Sistema de Tuberías',
            scene=dict(
                xaxis_title='X (m)',
                yaxis_title='Y (m)',
                zaxis_title='Elevación (m)',
                bgcolor='#0e1117',
            ),
            **TechnicalPlots.DARK_THEME,
            height=600,
        )
        
        return fig
    
    @staticmethod
    def velocity_distribution(sections: List[str], velocities: List[float],
                            limits: Dict) -> go.Figure:
        """
        Distribución de velocidades en el sistema
        """
        fig = go.Figure()
        
        # Barras de velocidad
        colors = ['green' if limits['min'] <= v <= limits['max'] else 'red' 
                 for v in velocities]
        
        fig.add_trace(go.Bar(
            x=sections,
            y=velocities,
            marker_color=colors,
            text=[f'{v:.2f} m/s' for v in velocities],
            textposition='outside',
        ))
        
        # Límites recomendados
        fig.add_hline(y=limits['min'], line_dash="dash", line_color="yellow",
                     annotation_text=f"Mínimo: {limits['min']} m/s")
        fig.add_hline(y=limits['max'], line_dash="dash", line_color="red",
                     annotation_text=f"Máximo: {limits['max']} m/s")
        fig.add_hline(y=limits['recommended'], line_dash="dot", line_color="green",
                     annotation_text=f"Recomendado: {limits['recommended']} m/s")
        
        fig.update_layout(
            title='Distribución de Velocidades en el Sistema',
            xaxis_title='Sección',
            yaxis_title='Velocidad (m/s)',
            **TechnicalPlots.DARK_THEME,
            height=500,
            xaxis=TechnicalPlots.GRID_CONFIG,
            yaxis=TechnicalPlots.GRID_CONFIG
        )
        
        return fig
