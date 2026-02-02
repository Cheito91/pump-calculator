"""
Script de ejemplo para usar los módulos sin la interfaz Streamlit
"""

from utils.hydraulic_calcs import HydraulicCalculator
from utils.pump_calcs import PumpCalculator
from utils.standards import Standards

def ejemplo_calculo_tuberia():
    """Ejemplo de cálculo de un sistema de tuberías"""
    
    print("=" * 60)
    print("EJEMPLO: CALCULO DE SISTEMA DE TUBERIAS")
    print("=" * 60)
    
    # Inicializar calculadora
    calc = HydraulicCalculator()
    std = Standards()
    
    # Datos de entrada
    pipe_data = {
        'diameter': 0.100,  # 100 mm = 0.1 m
        'length': 100.0,     # 100 metros
        'roughness': 0.045,  # Acero comercial nuevo (mm)
        'material': 'Acero comercial nuevo'
    }
    
    fluid_properties = {
        'flow_rate': 50.0 / 3600,  # 50 m³/h = 0.0139 m³/s
        'temperature': 20.0         # 20°C
    }
    
    fittings = [
        {'type': 'Codo 90° radio largo', 'quantity': 4},
        {'type': 'Válvula compuerta abierta', 'quantity': 1},
        {'type': 'Entrada brusca', 'quantity': 1},
        {'type': 'Salida brusca', 'quantity': 1}
    ]
    
    # Realizar cálculo
    results = calc.calculate_system(pipe_data, fluid_properties, fittings)
    
    # Mostrar resultados
    print(f"\nRESULTADOS DEL CALCULO\n")
    print(f"Velocidad:              {results['velocity']:.3f} m/s")
    print(f"Número de Reynolds:     {results['reynolds']:.0f}")
    print(f"Tipo de flujo:          {results['flow_type']}")
    print(f"Factor de fricción:     {results['friction_factor']:.5f}")
    print(f"Pérdida por fricción:   {results['head_loss_friction']:.3f} m")
    print(f"Pérdidas menores:       {results['head_loss_minor']:.3f} m")
    print(f"Pérdida total:          {results['total_head_loss']:.3f} m")
    print(f"Presión equivalente:    {results['pressure_loss']/1000:.2f} kPa")
    
    # Verificaciones
    print(f"\nVERIFICACIONES\n")
    
    velocity_check = std.check_velocity(results['velocity'], 'Tubería general')
    print(f"Estado de velocidad:    {velocity_check['status']}")
    print(f"Rango permitido:        {velocity_check['limits']['min']:.1f} - {velocity_check['limits']['max']:.1f} m/s")
    
    erosion_check = std.erosion_velocity_check(results['velocity'], results['density'])
    print(f"Velocidad de erosión:   {erosion_check['status']}")
    print(f"Riesgo:                 {erosion_check['risk']}")
    
    print("\n" + "=" * 60)


def ejemplo_calculo_bomba():
    """Ejemplo de cálculo de bomba"""
    
    print("\n" + "=" * 60)
    print("EJEMPLO: CALCULO DE BOMBA CENTRIFUGA")
    print("=" * 60)
    
    # Inicializar calculadora
    calc = PumpCalculator()
    
    # Datos de entrada
    flow_rate = 50.0 / 3600  # 50 m³/h en m³/s
    total_head = 30.0         # 30 metros
    
    suction_conditions = {
        'pressure_suction': 101300,    # 1.013 bar en Pa (presión atmosférica)
        'vapor_pressure': 2300,        # 0.023 bar en Pa (agua a 20°C)
        'velocity_suction': 1.0,       # 1 m/s
        'elevation': 2.0               # 2 metros sobre la bomba
    }
    
    pump_specs = {
        'efficiency': 0.75,      # 75%
        'speed': 1750            # rpm
    }
    
    density = 998.2  # kg/m³ (agua a 20°C)
    
    # Realizar análisis completo
    results = calc.complete_pump_analysis(
        flow_rate, total_head, suction_conditions, pump_specs, density
    )
    
    # Mostrar resultados
    print(f"\nRESULTADOS DEL CALCULO\n")
    print(f"Potencia hidráulica:    {results['hydraulic_power_kw']:.2f} kW")
    print(f"Potencia al eje:        {results['shaft_power_kw']:.2f} kW")
    print(f"Potencia del motor:     {results['motor_power_kw']:.2f} kW ({results['motor_power_hp']:.1f} HP)")
    print(f"Eficiencia:             {results['efficiency']*100:.1f} %")
    
    print(f"\nANALISIS DE NPSH\n")
    print(f"NPSH disponible:        {results['npsh_available']:.2f} m")
    print(f"NPSH requerido:         {results['npsh_required']:.2f} m")
    print(f"Margen:                 {results['cavitation_check']['margin']:.2f} m")
    print(f"Estado:                 {results['cavitation_check']['status']}")
    
    print(f"\nCARACTERISTICAS\n")
    print(f"Velocidad específica:   {results['specific_speed']:.1f}")
    print(f"Tipo de bomba:          {results['pump_type']}")
    print(f"Rango operativo:        {results['operating_range']}")
    
    print("\n" + "=" * 60)


def ejemplo_curvas_bomba():
    """Ejemplo de generación de curvas de bomba"""
    
    print("\n" + "=" * 60)
    print("EJEMPLO: GENERACION DE CURVAS DE BOMBA")
    print("=" * 60)
    
    calc = PumpCalculator()
    
    # Datos del BEP (Best Efficiency Point)
    q_bep = 50.0 / 3600  # 50 m³/h
    h_bep = 30.0         # 30 m
    eff_bep = 0.80       # 80%
    
    # Calcular potencia en BEP
    density = 998.2
    p_bep = calc.hydraulic_power(q_bep, h_bep, density) / eff_bep
    
    # Generar curvas
    curves = calc.generate_pump_curve(q_bep, h_bep, p_bep, eff_bep, num_points=10)
    
    print(f"\nCURVAS GENERADAS (10 puntos)\n")
    print(f"{'Caudal (m³/h)':<15} {'Altura (m)':<12} {'Potencia (kW)':<15} {'Eficiencia (%)':<15}")
    print("-" * 60)
    
    for i in range(0, 10, 2):  # Mostrar cada 2 puntos
        q = curves['flow'][i] * 3600
        h = curves['head'][i]
        p = curves['power'][i] / 1000
        eff = curves['efficiency'][i] * 100
        print(f"{q:<15.1f} {h:<12.2f} {p:<15.2f} {eff:<15.1f}")
    
    print("\n" + "=" * 60)


def ejemplo_punto_operacion():
    """Ejemplo de cálculo del punto de operación"""
    
    print("\n" + "=" * 60)
    print("EJEMPLO: PUNTO DE OPERACION")
    print("=" * 60)
    
    calc = PumpCalculator()
    
    # Curva de la bomba
    pump_params = {
        'q_bep': 50.0 / 3600,
        'h_bep': 30.0,
        'power_bep': 5000.0,
        'efficiency_bep': 0.78
    }
    
    # Curva del sistema
    system_params = {
        'h_static': 10.0,      # Altura estática
        'k_coefficient': 5000.0  # Coeficiente de pérdidas
    }
    
    # Calcular punto de operación
    op_point = calc.operating_point(system_params, pump_params)
    
    print(f"\nPUNTO DE OPERACION\n")
    print(f"Caudal de operación:    {op_point['flow_operating']*3600:.2f} m³/h")
    print(f"Altura de operación:    {op_point['head_operating']:.2f} m")
    print(f"Potencia de operación:  {op_point['power_operating']/1000:.2f} kW")
    print(f"Eficiencia:             {op_point['efficiency_operating']*100:.1f} %")
    
    print("\n" + "=" * 60)


def ejemplo_leyes_afinidad():
    """Ejemplo de aplicación de leyes de afinidad"""
    
    print("\n" + "=" * 60)
    print("EJEMPLO: LEYES DE AFINIDAD")
    print("=" * 60)
    
    calc = PumpCalculator()
    
    # Condiciones originales
    q1 = 50.0 / 3600  # m³/s
    h1 = 30.0         # m
    p1 = 5000.0       # W
    n1 = 1750         # rpm
    
    # Nueva velocidad
    n2 = 1450         # rpm
    
    # Aplicar leyes de afinidad
    q2 = calc.affinity_laws_flow(q1, n1, n2)
    h2 = calc.affinity_laws_head(h1, n1, n2)
    p2 = calc.affinity_laws_power(p1, n1, n2)
    
    print(f"\nCAMBIO DE VELOCIDAD: {n1} rpm -> {n2} rpm\n")
    print(f"{'Parámetro':<20} {'Original':<15} {'Nuevo':<15} {'Cambio (%)':<15}")
    print("-" * 65)
    print(f"{'Caudal (m³/h)':<20} {q1*3600:<15.2f} {q2*3600:<15.2f} {(q2/q1-1)*100:+.1f}")
    print(f"{'Altura (m)':<20} {h1:<15.2f} {h2:<15.2f} {(h2/h1-1)*100:+.1f}")
    print(f"{'Potencia (kW)':<20} {p1/1000:<15.2f} {p2/1000:<15.2f} {(p2/p1-1)*100:+.1f}")
    
    print("\n" + "=" * 60)


def ejemplo_seleccion_tuberia():
    """Ejemplo de selección de tamaño de tubería"""
    
    print("\n" + "=" * 60)
    print("EJEMPLO: SELECCION DE DIAMETRO DE TUBERIA")
    print("=" * 60)
    
    std = Standards()
    
    # Caudal deseado
    flow_m3h = 50.0
    flow_m3s = flow_m3h / 3600
    
    # Velocidad máxima permitida
    max_velocity = 2.5  # m/s
    
    # Seleccionar tamaño
    result = std.select_pipe_size(flow_m3s, max_velocity)
    
    print(f"\nSELECCION DE TUBERIA\n")
    print(f"Caudal:                 {flow_m3h:.1f} m³/h")
    print(f"Velocidad máxima:       {max_velocity:.1f} m/s")
    print(f"Diámetro requerido:     {result['required_diameter_mm']:.1f} mm")
    print(f"DN recomendado:         DN {result['recommended_dn']:.0f}")
    print(f"Velocidad real:         {result['actual_velocity']:.2f} m/s")
    
    if len(result['next_sizes']) > 1:
        print(f"\nOpciones alternativas:")
        for dn in result['next_sizes'][1:3]:
            area = 3.14159 * (dn/1000 / 2)**2
            v = flow_m3s / area
            print(f"  DN {dn}: velocidad = {v:.2f} m/s")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    print("\n")
    print("+" + "=" * 58 + "+")
    print("|" + " " * 8 + "EJEMPLOS DE USO - CALCULADORA DE TUBERIAS Y BOMBAS" + " " * 8 + "|")
    print("+" + "=" * 58 + "+")
    
    ejemplo_calculo_tuberia()
    ejemplo_calculo_bomba()
    ejemplo_curvas_bomba()
    ejemplo_punto_operacion()
    ejemplo_leyes_afinidad()
    ejemplo_seleccion_tuberia()
    
    print("\n[OK] Todos los ejemplos ejecutados exitosamente!\n")
