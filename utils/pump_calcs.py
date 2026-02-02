"""
Módulo de cálculos para bombas centrífugas
Según normativas ISO 9906, API 610, ANSI/HI 9.6.3
"""

import numpy as np
from typing import Dict, Tuple, List, Optional
import warnings


class PumpCalculator:
    """
    Calculadora profesional para bombas centrífugas
    Basada en normativas ISO 9906, API 610, ANSI/HI 9.6.3
    """
    
    GRAVITY = 9.81  # m/s²
    
    def __init__(self):
        self.efficiency_data = None
        self.curve_data = None
    
    @staticmethod
    def hydraulic_power(flow_rate: float, head: float, density: float, 
                       gravity: float = GRAVITY) -> float:
        """
        Potencia hidráulica (útil) según ISO 9906
        
        Args:
            flow_rate: Caudal (m³/s)
            head: Altura manométrica total (m)
            density: Densidad del fluido (kg/m³)
            gravity: Aceleración de la gravedad (m/s²)
            
        Returns:
            Potencia hidráulica (W)
        """
        return density * gravity * flow_rate * head
    
    @staticmethod
    def shaft_power(hydraulic_power: float, efficiency: float) -> float:
        """
        Potencia al eje (brake horsepower)
        
        Args:
            hydraulic_power: Potencia hidráulica (W)
            efficiency: Eficiencia de la bomba (0-1)
            
        Returns:
            Potencia al eje (W)
        """
        if efficiency <= 0 or efficiency > 1:
            raise ValueError("La eficiencia debe estar entre 0 y 1")
        return hydraulic_power / efficiency
    
    @staticmethod
    def motor_power(shaft_power: float, motor_efficiency: float = 0.95, 
                   safety_factor: float = 1.15) -> float:
        """
        Potencia del motor requerida según NEMA/IEC
        
        Args:
            shaft_power: Potencia al eje (W)
            motor_efficiency: Eficiencia del motor (típico 0.90-0.95)
            safety_factor: Factor de seguridad (típico 1.10-1.20)
            
        Returns:
            Potencia del motor (W)
        """
        return (shaft_power / motor_efficiency) * safety_factor
    
    @staticmethod
    def npsh_available(pressure_suction: float, vapor_pressure: float, 
                      velocity_suction: float, elevation: float, 
                      density: float, gravity: float = GRAVITY) -> float:
        """
        NPSH disponible (Net Positive Suction Head Available)
        Según ISO 9906 y ANSI/HI 9.6.1
        
        Args:
            pressure_suction: Presión absoluta en la succión (Pa)
            vapor_pressure: Presión de vapor del líquido a temp. de bombeo (Pa)
            velocity_suction: Velocidad en la tubería de succión (m/s)
            elevation: Altura del nivel del líquido sobre el eje de la bomba (m)
            density: Densidad del fluido (kg/m³)
            gravity: Aceleración de la gravedad (m/s²)
            
        Returns:
            NPSH disponible (m)
        """
        pressure_head = pressure_suction / (density * gravity)
        vapor_head = vapor_pressure / (density * gravity)
        velocity_head = velocity_suction**2 / (2 * gravity)
        
        npsh_a = pressure_head - vapor_head + velocity_head + elevation
        return npsh_a
    
    @staticmethod
    def npsh_required_estimate(flow_rate: float, speed: float, 
                              suction_specific_speed: float = 11000) -> float:
        """
        Estimación del NPSH requerido usando velocidad específica de succión
        Según Hydraulic Institute Standards
        
        Args:
            flow_rate: Caudal (m³/s)
            speed: Velocidad de rotación (rpm)
            suction_specific_speed: S (típico 8000-13000 para bombas centrífugas)
            
        Returns:
            NPSH requerido estimado (m)
        """
        # Convertir caudal a GPM para fórmula empírica
        flow_gpm = flow_rate * 15850.32
        
        # Fórmula empírica NPSH_R
        npsh_r = ((speed * np.sqrt(flow_gpm)) / suction_specific_speed) ** (4/3)
        
        # Convertir pies a metros
        return npsh_r * 0.3048
    
    @staticmethod
    def specific_speed(flow_rate: float, head: float, speed: float) -> float:
        """
        Velocidad específica (Ns) - clasificación del tipo de bomba
        Según ISO 9906
        
        Args:
            flow_rate: Caudal en el punto de mejor eficiencia (m³/s)
            head: Altura en el punto de mejor eficiencia (m)
            speed: Velocidad de rotación (rpm)
            
        Returns:
            Velocidad específica (adimensional, unidades métricas)
        """
        # Fórmula europea (unidades métricas)
        flow_m3h = flow_rate * 3600  # m³/h
        n_s = speed * np.sqrt(flow_m3h) / (head ** 0.75)
        return n_s
    
    @staticmethod
    def classify_pump_type(specific_speed: float) -> str:
        """
        Clasifica el tipo de bomba según velocidad específica
        
        Args:
            specific_speed: Velocidad específica (métrica)
            
        Returns:
            Tipo de bomba
        """
        if specific_speed < 20:
            return "Centrífuga radial de baja velocidad específica"
        elif specific_speed < 40:
            return "Centrífuga radial"
        elif specific_speed < 80:
            return "Centrífuga radial-mixta"
        elif specific_speed < 150:
            return "Centrífuga de flujo mixto"
        elif specific_speed < 300:
            return "Centrífuga de flujo axial"
        else:
            return "Bomba de flujo axial (hélice)"
    
    @staticmethod
    def affinity_laws_flow(flow1: float, speed1: float, speed2: float) -> float:
        """
        Ley de afinidad para caudal (primera ley)
        Q2/Q1 = N2/N1
        
        Args:
            flow1: Caudal a velocidad original (m³/s)
            speed1: Velocidad original (rpm)
            speed2: Nueva velocidad (rpm)
            
        Returns:
            Nuevo caudal (m³/s)
        """
        return flow1 * (speed2 / speed1)
    
    @staticmethod
    def affinity_laws_head(head1: float, speed1: float, speed2: float) -> float:
        """
        Ley de afinidad para altura (segunda ley)
        H2/H1 = (N2/N1)²
        
        Args:
            head1: Altura a velocidad original (m)
            speed1: Velocidad original (rpm)
            speed2: Nueva velocidad (rpm)
            
        Returns:
            Nueva altura (m)
        """
        return head1 * (speed2 / speed1)**2
    
    @staticmethod
    def affinity_laws_power(power1: float, speed1: float, speed2: float) -> float:
        """
        Ley de afinidad para potencia (tercera ley)
        P2/P1 = (N2/N1)³
        
        Args:
            power1: Potencia a velocidad original (W)
            speed1: Velocidad original (rpm)
            speed2: Nueva velocidad (rpm)
            
        Returns:
            Nueva potencia (W)
        """
        return power1 * (speed2 / speed1)**3
    
    def generate_pump_curve(self, q_bep: float, h_bep: float, 
                           power_bep: float, efficiency_bep: float = 0.80,
                           num_points: int = 50) -> Dict[str, np.ndarray]:
        """
        Genera curva característica de la bomba usando modelo parabólico
        Basado en características típicas de bombas centrífugas
        
        Args:
            q_bep: Caudal en el punto de mejor eficiencia (m³/s)
            h_bep: Altura en el punto de mejor eficiencia (m)
            power_bep: Potencia en el punto de mejor eficiencia (W)
            efficiency_bep: Eficiencia en el BEP (0-1)
            num_points: Número de puntos de la curva
            
        Returns:
            Diccionario con arrays de Q, H, P, η
        """
        # Rango de caudales (0% a 150% del BEP)
        q_range = np.linspace(0, 1.5 * q_bep, num_points)
        
        # Curva H-Q (parabólica típica)
        # H = H0 - a*Q² donde H0 es altura a caudal cero
        h_shutoff = h_bep * 1.15  # Típicamente 115% del BEP
        a = (h_shutoff - h_bep) / q_bep**2
        h_range = h_shutoff - a * q_range**2
        h_range = np.maximum(h_range, 0)  # No valores negativos
        
        # Curva de eficiencia (parábola con máximo en BEP)
        # Eficiencia baja a caudal cero y alto
        q_normalized = q_range / q_bep
        efficiency_range = efficiency_bep * np.exp(-0.5 * ((q_normalized - 1) / 0.4)**2)
        efficiency_range = np.clip(efficiency_range, 0.01, 1.0)
        
        # Curva de potencia
        density = 998.2  # kg/m³ (agua a 20°C)
        hydraulic_power = density * self.GRAVITY * q_range * h_range
        power_range = hydraulic_power / efficiency_range
        
        self.curve_data = {
            'flow': q_range,
            'head': h_range,
            'power': power_range,
            'efficiency': efficiency_range,
            'q_bep': q_bep,
            'h_bep': h_bep,
        }
        
        return self.curve_data
    
    def operating_point(self, system_curve_params: Dict, 
                       pump_curve_params: Dict) -> Dict:
        """
        Encuentra el punto de operación (intersección de curvas)
        Curva del sistema: H = H_static + K*Q²
        
        Args:
            system_curve_params: {h_static, k_coefficient}
            pump_curve_params: {q_bep, h_bep, power_bep, efficiency_bep}
            
        Returns:
            Diccionario con punto de operación {q_op, h_op, p_op, eff_op}
        """
        # Generar curva de la bomba
        pump_curve = self.generate_pump_curve(**pump_curve_params)
        
        # Calcular curva del sistema
        h_static = system_curve_params['h_static']
        k = system_curve_params['k_coefficient']
        
        q_range = pump_curve['flow']
        h_system = h_static + k * q_range**2
        h_pump = pump_curve['head']
        
        # Encontrar intersección
        diff = np.abs(h_pump - h_system)
        idx_op = np.argmin(diff)
        
        q_op = q_range[idx_op]
        h_op = h_pump[idx_op]
        p_op = pump_curve['power'][idx_op]
        eff_op = pump_curve['efficiency'][idx_op]
        
        return {
            'flow_operating': q_op,
            'head_operating': h_op,
            'power_operating': p_op,
            'efficiency_operating': eff_op,
            'system_curve': h_system,
            'pump_curve': h_pump,
            'flow_range': q_range,
        }
    
    @staticmethod
    def cavitation_check(npsh_available: float, npsh_required: float, 
                        safety_margin: float = 0.5) -> Dict:
        """
        Verifica condiciones de cavitación según ANSI/HI 9.6.1
        
        Args:
            npsh_available: NPSH disponible (m)
            npsh_required: NPSH requerido por la bomba (m)
            safety_margin: Margen de seguridad adicional (m)
            
        Returns:
            Diccionario con resultado de la verificación
        """
        margin = npsh_available - npsh_required
        safe = margin >= safety_margin
        
        if not safe:
            status = "RIESGO DE CAVITACIÓN"
            recommendation = "Aumentar NPSH disponible o seleccionar bomba con menor NPSH requerido"
        elif margin < 1.0:
            status = "ADVERTENCIA: Margen bajo"
            recommendation = "Considerar aumentar el NPSH disponible"
        else:
            status = "SEGURO"
            recommendation = "Condiciones de succión adecuadas"
        
        return {
            'safe': safe,
            'margin': margin,
            'status': status,
            'recommendation': recommendation,
            'npsh_available': npsh_available,
            'npsh_required': npsh_required,
        }
    
    @staticmethod
    def minimum_flow(bep_flow: float, safety_factor: float = 0.3) -> float:
        """
        Caudal mínimo continuo seguro según API 610
        Típicamente 30-50% del BEP para evitar recirculación y sobrecalentamiento
        
        Args:
            bep_flow: Caudal en el BEP (m³/s)
            safety_factor: Factor (típico 0.3-0.5)
            
        Returns:
            Caudal mínimo (m³/s)
        """
        return bep_flow * safety_factor
    
    @staticmethod
    def maximum_flow(bep_flow: float, safety_factor: float = 1.2) -> float:
        """
        Caudal máximo recomendado según API 610
        Típicamente 120% del BEP para evitar sobrecarga
        
        Args:
            bep_flow: Caudal en el BEP (m³/s)
            safety_factor: Factor (típico 1.1-1.2)
            
        Returns:
            Caudal máximo (m³/s)
        """
        return bep_flow * safety_factor
    
    def complete_pump_analysis(self, flow_rate: float, total_head: float,
                               suction_conditions: Dict, pump_specs: Dict,
                               density: float = 998.2) -> Dict:
        """
        Análisis completo de la bomba
        
        Args:
            flow_rate: Caudal de diseño (m³/s)
            total_head: Altura manométrica total (m)
            suction_conditions: Condiciones de succión
            pump_specs: Especificaciones de la bomba
            density: Densidad del fluido (kg/m³)
            
        Returns:
            Diccionario completo con todos los resultados
        """
        # Potencias
        efficiency = pump_specs.get('efficiency', 0.75)
        hydraulic_pow = self.hydraulic_power(flow_rate, total_head, density)
        shaft_pow = self.shaft_power(hydraulic_pow, efficiency)
        motor_pow = self.motor_power(shaft_pow)
        
        # NPSH
        npsh_a = self.npsh_available(**suction_conditions, density=density)
        speed = pump_specs.get('speed', 1750)
        npsh_r = self.npsh_required_estimate(flow_rate, speed)
        cavitation = self.cavitation_check(npsh_a, npsh_r)
        
        # Velocidad específica
        ns = self.specific_speed(flow_rate, total_head, speed)
        pump_type = self.classify_pump_type(ns)
        
        # Rangos operativos
        min_flow = self.minimum_flow(flow_rate)
        max_flow = self.maximum_flow(flow_rate)
        
        return {
            'hydraulic_power_kw': hydraulic_pow / 1000,
            'shaft_power_kw': shaft_pow / 1000,
            'motor_power_kw': motor_pow / 1000,
            'motor_power_hp': motor_pow / 745.7,
            'efficiency': efficiency,
            'npsh_available': npsh_a,
            'npsh_required': npsh_r,
            'cavitation_check': cavitation,
            'specific_speed': ns,
            'pump_type': pump_type,
            'minimum_flow': min_flow,
            'maximum_flow': max_flow,
            'operating_range': f"{min_flow*3600:.1f} - {max_flow*3600:.1f} m³/h",
        }
