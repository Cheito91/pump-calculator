"""
Tests unitarios básicos para los módulos de cálculo
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from utils.hydraulic_calcs import HydraulicCalculator
from utils.pump_calcs import PumpCalculator
from utils.standards import Standards


def test_hydraulic_calculator():
    """Test del calculador hidráulico"""
    print("\n[TEST] Testing HydraulicCalculator...")
    
    calc = HydraulicCalculator()
    
    # Test Reynolds
    reynolds = calc.reynolds_number(velocity=2.0, diameter=0.1, viscosity=1e-6)
    assert abs(reynolds - 200000) < 1, f"Reynolds test failed: {reynolds}"
    print("  [OK] Reynolds number calculation OK")
    
    # Test velocidad
    velocity = calc.velocity_from_flow(flow_rate=0.01, diameter=0.1)
    assert abs(velocity - 1.273) < 0.01, f"Velocity test failed: {velocity}"
    print("  [OK] Velocity calculation OK")
    
    # Test fricción Swamee-Jain
    f = calc.friction_factor_swamee_jain(reynolds=100000, roughness=0.00005, diameter=0.1)
    assert 0.01 < f < 0.05, f"Friction factor test failed: {f}"
    print("  [OK] Friction factor calculation OK")
    
    # Test pérdida de carga
    hf = calc.head_loss_darcy_weisbach(
        friction_factor=0.02, 
        length=100, 
        diameter=0.1, 
        velocity=2.0
    )
    assert hf > 0, f"Head loss test failed: {hf}"
    print("  [OK] Head loss calculation OK")
    
    # Test conversiones
    head = calc.pressure_to_head(pressure=100000, density=1000)
    pressure = calc.head_to_pressure(head=head, density=1000)
    assert abs(pressure - 100000) < 1, "Pressure conversion test failed"
    print("  [OK] Pressure conversions OK")
    
    print("[OK] HydraulicCalculator: All tests passed!")


def test_pump_calculator():
    """Test del calculador de bombas"""
    print("\n[TEST] Testing PumpCalculator...")
    
    calc = PumpCalculator()
    
    # Test potencia hidráulica
    p_hyd = calc.hydraulic_power(flow_rate=0.01, head=30, density=1000)
    assert p_hyd > 0, f"Hydraulic power test failed: {p_hyd}"
    print("  [OK] Hydraulic power calculation OK")
    
    # Test potencia al eje
    p_shaft = calc.shaft_power(hydraulic_power=3000, efficiency=0.75)
    assert p_shaft == 4000, f"Shaft power test failed: {p_shaft}"
    print("  [OK] Shaft power calculation OK")
    
    # Test NPSH
    npsh_a = calc.npsh_available(
        pressure_suction=101300,
        vapor_pressure=2300,
        velocity_suction=1.0,
        elevation=2.0,
        density=1000
    )
    assert npsh_a > 0, f"NPSH test failed: {npsh_a}"
    print("  [OK] NPSH calculation OK")
    
    # Test velocidad específica
    ns = calc.specific_speed(flow_rate=0.01, head=30, speed=1750)
    assert ns > 0, f"Specific speed test failed: {ns}"
    print("  [OK] Specific speed calculation OK")
    
    # Test leyes de afinidad
    q2 = calc.affinity_laws_flow(flow1=0.01, speed1=1750, speed2=1450)
    assert q2 < 0.01, f"Affinity law test failed: {q2}"
    print("  [OK] Affinity laws OK")
    
    # Test clasificación de bomba
    pump_type = calc.classify_pump_type(specific_speed=30)
    assert "radial" in pump_type.lower(), f"Pump classification test failed: {pump_type}"
    print("  [OK] Pump classification OK")
    
    print("[OK] PumpCalculator: All tests passed!")


def test_standards():
    """Test de normativas y estándares"""
    print("\n[TEST] Testing Standards...")
    
    std = Standards()
    
    # Test verificación de velocidad
    check = std.check_velocity(velocity=2.0, service_type='Tubería general')
    assert 'status' in check, "Velocity check test failed"
    print("  [OK] Velocity check OK")
    
    # Test verificación de Reynolds
    check = std.check_reynolds(reynolds=50000)
    assert check['flow_type'] == 'TURBULENTO', f"Reynolds check test failed: {check}"
    print("  [OK] Reynolds check OK")
    
    # Test selección de clase de presión
    result = std.select_pressure_class(operating_pressure=10, temperature=50, standard='PN')
    assert result['status'] == 'OK', f"Pressure class test failed: {result}"
    print("  [OK] Pressure class selection OK")
    
    # Test selección de tamaño de tubería
    result = std.select_pipe_size(flow_rate=0.01, max_velocity=2.5)
    assert 'recommended_dn' in result, f"Pipe size test failed: {result}"
    print("  [OK] Pipe size selection OK")
    
    # Test verificación de erosión
    check = std.erosion_velocity_check(velocity=2.0, density=1000)
    assert 'status' in check, "Erosion check test failed"
    print("  [OK] Erosion check OK")
    
    # Test normativas aplicables
    standards_list = std.get_applicable_standards('Industrial general')
    assert len(standards_list) > 0, "Standards list test failed"
    print("  [OK] Standards list OK")
    
    print("[OK] Standards: All tests passed!")


def test_integration():
    """Test de integración del sistema completo"""
    print("\n[TEST] Testing System Integration...")
    
    calc = HydraulicCalculator()
    
    # Test data - complete system calculation with new signature
    results = calc.calculate_system(
        flow_rate=0.01,          # m³/s
        diameter=0.1,            # m
        length=100,              # m
        roughness=0.00005,       # m (commercial steel)
        minor_losses_k=[0.5, 0.9, 0.9, 1.0],  # Entrance, 2 elbows, exit
        temperature=20,          # °C
        elevation_change=0       # m
    )
    
    # Verificaciones
    assert 'velocity' in results, "Integration test: velocity missing"
    assert 'reynolds' in results, "Integration test: reynolds missing"
    assert 'total_head_loss' in results, "Integration test: head loss missing"
    assert results['velocity'] > 0, "Integration test: invalid velocity"
    assert results['total_head_loss'] > 0, "Integration test: invalid head loss"
    
    print("  [OK] System integration OK")
    print(f"    Velocity: {results['velocity']:.3f} m/s")
    print(f"    Reynolds: {results['reynolds']:.0f}")
    print(f"    Head loss: {results['total_head_loss']:.3f} m")
    
    print("[OK] System Integration: All tests passed!")


def run_all_tests():
    """Ejecutar todos los tests"""
    print("\n" + "="*60)
    print("  EJECUTANDO SUITE DE TESTS")
    print("="*60)
    
    try:
        test_hydraulic_calculator()
        test_pump_calculator()
        test_standards()
        test_integration()
        
        print("\n" + "="*60)
        print("  [OK] TODOS LOS TESTS PASARON EXITOSAMENTE!")
        print("="*60 + "\n")
        return True
        
    except AssertionError as e:
        print(f"\n[X] TEST FAILED: {e}\n")
        return False
    except Exception as e:
        print(f"\n[X] ERROR: {e}\n")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
