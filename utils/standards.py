"""
Módulo de normativas y estándares técnicos
ISO, ASME, DIN, API, ANSI/HI
"""

from typing import Dict, List, Tuple
import warnings


class Standards:
    """
    Normativas y estándares técnicos para diseño de tuberías y bombas
    """
    
    # Velocidades recomendadas según tipo de servicio (m/s)
    # Basado en ISO 15649 y buenas prácticas de ingeniería
    VELOCITY_LIMITS = {
        'Succión de bomba': {'min': 0.6, 'max': 1.5, 'recommended': 1.0},
        'Descarga de bomba': {'min': 1.5, 'max': 3.0, 'recommended': 2.0},
        'Tubería general': {'min': 1.0, 'max': 3.0, 'recommended': 2.0},
        'Drenaje por gravedad': {'min': 0.5, 'max': 2.0, 'recommended': 1.0},
        'Agua potable': {'min': 0.5, 'max': 2.5, 'recommended': 1.5},
        'Vapor saturado': {'min': 15.0, 'max': 30.0, 'recommended': 20.0},
        'Vapor sobrecalentado': {'min': 20.0, 'max': 50.0, 'recommended': 30.0},
        'Gas': {'min': 5.0, 'max': 30.0, 'recommended': 15.0},
    }
    
    # Presiones de diseño según ASME B31.3
    PRESSURE_CLASSES_ANSI = {
        '150': {'max_pressure_bar': 19.6, 'max_temp_c': 260},
        '300': {'max_pressure_bar': 51.0, 'max_temp_c': 370},
        '600': {'max_pressure_bar': 102.0, 'max_temp_c': 400},
        '900': {'max_pressure_bar': 153.0, 'max_temp_c': 427},
        '1500': {'max_pressure_bar': 255.0, 'max_temp_c': 450},
        '2500': {'max_pressure_bar': 425.0, 'max_temp_c': 482},
    }
    
    # Presiones nominales según DIN/ISO
    PRESSURE_CLASSES_PN = {
        'PN6': {'max_pressure_bar': 6, 'applications': 'Baja presión, drenaje'},
        'PN10': {'max_pressure_bar': 10, 'applications': 'Agua fría, baja presión'},
        'PN16': {'max_pressure_bar': 16, 'applications': 'Agua, servicios generales'},
        'PN25': {'max_pressure_bar': 25, 'applications': 'Media presión, industrial'},
        'PN40': {'max_pressure_bar': 40, 'applications': 'Alta presión, procesos'},
        'PN63': {'max_pressure_bar': 63, 'applications': 'Muy alta presión'},
        'PN100': {'max_pressure_bar': 100, 'applications': 'Presión extrema'},
    }
    
    # Diámetros nominales estándar según ISO/DIN (mm)
    STANDARD_PIPE_SIZES = [
        6, 8, 10, 15, 20, 25, 32, 40, 50, 65, 80, 100, 125, 150, 200, 
        250, 300, 350, 400, 450, 500, 600, 700, 800, 900, 1000, 1200
    ]
    
    # Schedule de tuberías según ASME B36.10
    PIPE_SCHEDULES = {
        'SCH 5S': {'description': 'Muy delgada, acero inoxidable'},
        'SCH 10S': {'description': 'Delgada, acero inoxidable'},
        'SCH 10': {'description': 'Delgada, baja presión'},
        'SCH 20': {'description': 'Media, aplicaciones especiales'},
        'SCH 30': {'description': 'Media, servicios ligeros'},
        'SCH 40': {'description': 'Estándar, más común'},
        'SCH 60': {'description': 'Extra fuerte, XS'},
        'SCH 80': {'description': 'Extra fuerte, alta presión'},
        'SCH 100': {'description': 'Muy fuerte, XXS'},
        'SCH 120': {'description': 'Muy fuerte, alta presión'},
        'SCH 140': {'description': 'Extra pesada'},
        'SCH 160': {'description': 'Extra pesada, máxima presión'},
    }
    
    # Materiales y sus propiedades según ASME/ISO
    MATERIALS = {
        'Acero al carbono': {
            'code': 'ASTM A106 Gr.B',
            'max_temp': 400,
            'tensile_strength': 415,  # MPa
            'applications': 'Servicios generales alta temperatura',
            'corrosion_allowance': 3.0,  # mm
        },
        'Acero inoxidable 304': {
            'code': 'ASTM A312 TP304',
            'max_temp': 650,
            'tensile_strength': 515,
            'applications': 'Servicios corrosivos, alimentos',
            'corrosion_allowance': 0.0,
        },
        'Acero inoxidable 316': {
            'code': 'ASTM A312 TP316',
            'max_temp': 650,
            'tensile_strength': 515,
            'applications': 'Alta corrosión, marinos',
            'corrosion_allowance': 0.0,
        },
        'PVC': {
            'code': 'ASTM D1785 SCH 40',
            'max_temp': 60,
            'tensile_strength': 52,
            'applications': 'Agua fría, drenaje',
            'corrosion_allowance': 0.0,
        },
        'HDPE': {
            'code': 'ASTM D3350 PE100',
            'max_temp': 60,
            'tensile_strength': 24,
            'applications': 'Agua, gas, enterrado',
            'corrosion_allowance': 0.0,
        },
        'Cobre tipo K': {
            'code': 'ASTM B88',
            'max_temp': 200,
            'tensile_strength': 210,
            'applications': 'Agua potable, HVAC',
            'corrosion_allowance': 0.0,
        },
        'Hierro fundido dúctil': {
            'code': 'ISO 2531',
            'max_temp': 50,
            'tensile_strength': 420,
            'applications': 'Agua, enterrado',
            'corrosion_allowance': 2.0,
        },
    }
    
    # Factores de seguridad según normativa
    SAFETY_FACTORS = {
        'Presión estática': {
            'ASME_B31.3': 1.5,
            'ISO_15649': 1.5,
            'API_610': 1.25,
            'description': 'Para presión de diseño vs operación'
        },
        'Golpe de ariete': {
            'factor': 2.0,
            'description': 'Incremento por transitorios hidráulicos'
        },
        'Potencia de motor': {
            'factor': 1.15,
            'description': 'Margen para motor eléctrico'
        },
        'NPSH': {
            'margin': 0.5,  # metros
            'description': 'Margen de seguridad sobre NPSH requerido'
        },
    }
    
    # Coeficiente C de Hazen-Williams según material y edad
    HAZEN_WILLIAMS_C = {
        'PVC nuevo': 150,
        'PVC usado': 140,
        'HDPE': 150,
        'Cobre': 140,
        'Acero nuevo': 140,
        'Acero 5 años': 130,
        'Acero 10 años': 120,
        'Acero 20 años': 100,
        'Hierro fundido nuevo': 130,
        'Hierro fundido 10 años': 110,
        'Hierro fundido 20 años': 90,
        'Concreto liso': 130,
        'Concreto rugoso': 110,
    }
    
    @staticmethod
    def check_velocity(velocity: float, service_type: str = 'Tubería general') -> Dict:
        """
        Verifica si la velocidad está dentro de rangos recomendados
        
        Args:
            velocity: Velocidad del fluido (m/s)
            service_type: Tipo de servicio
            
        Returns:
            Diccionario con resultado de verificación
        """
        limits = Standards.VELOCITY_LIMITS.get(service_type, 
                                               Standards.VELOCITY_LIMITS['Tubería general'])
        
        status = "OK"
        warnings_list = []
        
        if velocity < limits['min']:
            status = "ADVERTENCIA"
            warnings_list.append(f"Velocidad baja ({velocity:.2f} m/s < {limits['min']} m/s)")
            warnings_list.append("Riesgo de sedimentación y estratificación")
        
        if velocity > limits['max']:
            status = "ADVERTENCIA"
            warnings_list.append(f"Velocidad alta ({velocity:.2f} m/s > {limits['max']} m/s)")
            warnings_list.append("Riesgo de erosión, ruido y vibración")
        
        if limits['min'] <= velocity <= limits['max']:
            if abs(velocity - limits['recommended']) > 0.5:
                status = "ACEPTABLE"
            else:
                status = "ÓPTIMO"
        
        return {
            'status': status,
            'velocity': velocity,
            'limits': limits,
            'warnings': warnings_list,
            'in_range': limits['min'] <= velocity <= limits['max'],
        }
    
    @staticmethod
    def check_reynolds(reynolds: float) -> Dict:
        """
        Verifica el número de Reynolds y tipo de flujo
        
        Args:
            reynolds: Número de Reynolds
            
        Returns:
            Diccionario con análisis del flujo
        """
        if reynolds < 2300:
            flow_type = "LAMINAR"
            description = "Flujo ordenado en capas paralelas"
            concerns = ["Velocidad muy baja", "Posible sedimentación"]
        elif reynolds < 4000:
            flow_type = "TRANSICIÓN"
            description = "Flujo inestable entre laminar y turbulento"
            concerns = ["Comportamiento impredecible", "Evitar operar en esta zona"]
        else:
            flow_type = "TURBULENTO"
            description = "Flujo con mezcla completa, régimen normal"
            concerns = []
        
        return {
            'reynolds': reynolds,
            'flow_type': flow_type,
            'description': description,
            'concerns': concerns,
        }
    
    @staticmethod
    def select_pressure_class(operating_pressure: float, temperature: float,
                            standard: str = 'ANSI') -> Dict:
        """
        Selecciona clase de presión apropiada
        
        Args:
            operating_pressure: Presión de operación (bar)
            temperature: Temperatura (°C)
            standard: 'ANSI' o 'PN'
            
        Returns:
            Clase de presión recomendada
        """
        design_pressure = operating_pressure * Standards.SAFETY_FACTORS['Presión estática']['ASME_B31.3']
        
        if standard == 'ANSI':
            classes = Standards.PRESSURE_CLASSES_ANSI
        else:
            classes = Standards.PRESSURE_CLASSES_PN
        
        suitable_classes = []
        for class_name, specs in classes.items():
            if standard == 'ANSI':
                if design_pressure <= specs['max_pressure_bar'] and temperature <= specs['max_temp_c']:
                    suitable_classes.append(class_name)
            else:
                if design_pressure <= specs['max_pressure_bar']:
                    suitable_classes.append(class_name)
        
        if not suitable_classes:
            return {
                'status': 'ERROR',
                'message': 'No hay clase de presión adecuada para estas condiciones',
                'design_pressure': design_pressure,
            }
        
        recommended_class = suitable_classes[0]
        
        return {
            'status': 'OK',
            'operating_pressure': operating_pressure,
            'design_pressure': design_pressure,
            'recommended_class': recommended_class,
            'all_suitable_classes': suitable_classes,
            'standard': standard,
        }
    
    @staticmethod
    def select_pipe_size(flow_rate: float, max_velocity: float = 2.0) -> Dict:
        """
        Selecciona diámetro nominal de tubería basado en velocidad
        
        Args:
            flow_rate: Caudal (m³/s)
            max_velocity: Velocidad máxima permitida (m/s)
            
        Returns:
            Tamaño de tubería recomendado
        """
        import numpy as np
        
        # Calcular diámetro mínimo requerido
        area_required = flow_rate / max_velocity
        diameter_required = np.sqrt(4 * area_required / np.pi) * 1000  # mm
        
        # Encontrar el DN estándar más cercano mayor
        suitable_sizes = [dn for dn in Standards.STANDARD_PIPE_SIZES 
                         if dn >= diameter_required]
        
        if not suitable_sizes:
            return {
                'status': 'ERROR',
                'message': f'Diámetro requerido ({diameter_required:.0f} mm) excede tamaños estándar',
            }
        
        recommended_dn = suitable_sizes[0]
        
        # Calcular velocidad real con el DN seleccionado
        diameter_m = recommended_dn / 1000
        area = np.pi * (diameter_m / 2)**2
        actual_velocity = flow_rate / area
        
        return {
            'status': 'OK',
            'required_diameter_mm': diameter_required,
            'recommended_dn': recommended_dn,
            'actual_velocity': actual_velocity,
            'flow_rate_m3h': flow_rate * 3600,
            'next_sizes': suitable_sizes[:3] if len(suitable_sizes) > 1 else suitable_sizes,
        }
    
    @staticmethod
    def erosion_velocity_check(velocity: float, density: float) -> Dict:
        """
        Verifica velocidad de erosión según API RP 14E
        V_erosion = C / sqrt(ρ)
        donde C típicamente = 100 para servicio continuo
        
        Args:
            velocity: Velocidad actual (m/s)
            density: Densidad del fluido (kg/m³)
            
        Returns:
            Análisis de erosión
        """
        import numpy as np
        
        c_factor = 100  # Factor conservador para servicio continuo
        v_erosion = c_factor / np.sqrt(density)
        
        ratio = velocity / v_erosion
        
        if ratio < 0.5:
            status = "SEGURO"
            risk = "Riesgo de erosión muy bajo"
        elif ratio < 0.8:
            status = "ACEPTABLE"
            risk = "Riesgo de erosión bajo"
        elif ratio < 1.0:
            status = "PRECAUCIÓN"
            risk = "Cerca del límite de erosión"
        else:
            status = "PELIGRO"
            risk = "VELOCIDAD EXCEDE LÍMITE DE EROSIÓN"
        
        return {
            'status': status,
            'velocity': velocity,
            'erosion_velocity': v_erosion,
            'ratio': ratio,
            'risk': risk,
        }
    
    @staticmethod
    def get_applicable_standards(application: str) -> List[str]:
        """
        Lista de normativas aplicables según aplicación
        
        Args:
            application: Tipo de aplicación
            
        Returns:
            Lista de normativas aplicables
        """
        standards_map = {
            'Agua potable': [
                'ISO 9906 - Bombas centrífugas',
                'ISO 15649 - Sistemas de tuberías',
                'EN 1092 - Bridas',
                'NSF/ANSI 61 - Componentes para agua potable',
            ],
            'Industrial general': [
                'ISO 9906 - Bombas centrífugas',
                'ASME B31.3 - Tuberías de proceso',
                'API 610 - Bombas centrífugas para refinería',
                'ANSI/HI 9.6.3 - NPSH',
                'ISO 5167 - Medición de caudal',
            ],
            'Petróleo y gas': [
                'API 610 - Bombas centrífugas',
                'API 614 - Sellos mecánicos',
                'ASME B31.3 - Tuberías de proceso',
                'API RP 14E - Velocidad de erosión',
                'NACE MR0175 - Materiales para H2S',
            ],
            'Química': [
                'ASME B31.3 - Tuberías de proceso',
                'ISO 9906 - Bombas',
                'ISO 5199 - Bombas químicas',
                'DIN 24255 - Bombas químicas',
            ],
        }
        
        return standards_map.get(application, standards_map['Industrial general'])
