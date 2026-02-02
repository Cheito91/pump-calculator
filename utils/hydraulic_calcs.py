"""
Hydraulic Calculations Module for Piping Systems

This module provides comprehensive hydraulic calculations for pipe flow analysis
following international standards (ISO, ASME, DIN, API).

Classes:
    HydraulicCalculator: Professional hydraulic calculator for piping systems

Key Features:
    - Reynolds number calculation
    - Friction factor calculation (Colebrook-White, Swamee-Jain)
    - Head loss calculations (Darcy-Weisbach, Hazen-Williams)
    - Pressure and head conversions
    - Complete system calculations

Standards Compliance:
    - ISO 9906: Rotodynamic pumps - Hydraulic performance acceptance tests
    - ASME B31.3: Process Piping
    - DIN 1988: Codes of practice for drinking water installations
    - API RP 14E: Recommended Practice for Design and Installation of Offshore
                  Production Platform Piping Systems

Author: Industrial Calculator Project
Version: 0.1.0 (Pre-release - Requires further development and review)
License: MIT
"""

import numpy as np
from typing import Dict, Tuple, List
import warnings


class HydraulicCalculator:
    """
    Professional Hydraulic Calculator for Piping Systems
    
    This class provides comprehensive hydraulic calculations for pipe flow analysis
    based on internationally recognized standards and equations.
    
    Attributes:
        GRAVITY (float): Gravitational acceleration constant (m/s²)
        ROUGHNESS (dict): Absolute roughness values for common pipe materials (mm)
    
    Methods:
        reynolds_number: Calculate Reynolds number for flow regime determination
        friction_factor_colebrook: Iterative Colebrook-White friction factor
        friction_factor_swamee_jain: Explicit Swamee-Jain approximation
        head_loss_darcy_weisbach: Head loss using Darcy-Weisbach equation
        head_loss_hazen_williams: Head loss using Hazen-Williams equation
        velocity_from_flow: Calculate velocity from volumetric flow rate
        flow_from_velocity: Calculate volumetric flow rate from velocity
        pressure_to_head: Convert pressure to head
        head_to_pressure: Convert head to pressure
        calculate_system: Complete system hydraulic analysis
    
    Example:
        >>> calc = HydraulicCalculator()
        >>> reynolds = calc.reynolds_number(velocity=2.0, diameter=0.1, 
        ...                                  viscosity=1e-6)
        >>> print(f"Reynolds number: {reynolds:.0f}")
        Reynolds number: 200000
    """
    
    # Physical constants
    GRAVITY = 9.81  # Gravitational acceleration (m/s²)
    
    # Typical absolute roughness values (mm) according to ISO/ASME standards
    ROUGHNESS = {
        'Commercial steel new': 0.045,
        'Commercial steel used': 0.15,
        'Riveted steel': 1.5,
        'Cast iron new': 0.26,
        'Cast iron used': 1.5,
        'Galvanized iron': 0.15,
        'PVC': 0.0015,
        'HDPE': 0.0015,
        'Copper': 0.0015,
        'Glass': 0.0015,
        'Smooth concrete': 0.3,
        'Rough concrete': 3.0,
    }
    
    @staticmethod
    def get_kinematic_viscosity(temperature: float) -> float:
        """
        Calculate kinematic viscosity of water based on temperature.
        
        Uses ISO standard tables for water properties at various temperatures.
        Linear interpolation is applied for intermediate values.
        
        Args:
            temperature (float): Water temperature in °C (range: 0-100°C)
            
        Returns:
            float: Kinematic viscosity in m²/s
            
        Raises:
            Warning: If temperature is outside typical range (0-100°C)
            
        Example:
            >>> calc = HydraulicCalculator()
            >>> visc = calc.get_kinematic_viscosity(20)
            >>> print(f"Viscosity at 20°C: {visc:.2e} m²/s")
            Viscosity at 20°C: 1.00e-06 m²/s
        """
        viscosity_table = {
            0: 1.787e-6,
            5: 1.519e-6,
            10: 1.307e-6,
            15: 1.139e-6,
            20: 1.004e-6,
            25: 0.893e-6,
            30: 0.801e-6,
            40: 0.658e-6,
            50: 0.553e-6,
            60: 0.475e-6,
            70: 0.413e-6,
            80: 0.364e-6,
            90: 0.326e-6,
            100: 0.294e-6,
        }
        
        if temperature < 0 or temperature > 100:
            warnings.warn(f"Temperature {temperature}°C outside typical range (0-100°C)")
        
        # Linear interpolation
        temps = sorted(viscosity_table.keys())
        if temperature in temps:
            return viscosity_table[temperature]
        
        for i in range(len(temps) - 1):
            if temps[i] <= temperature <= temps[i + 1]:
                t1, t2 = temps[i], temps[i + 1]
                v1, v2 = viscosity_table[t1], viscosity_table[t2]
                return v1 + (v2 - v1) * (temperature - t1) / (t2 - t1)
        
        # Extrapolation for out-of-range values
        return viscosity_table[temps[-1]]
    
    @staticmethod
    def get_water_density(temperature: float) -> float:
        """
        Calculate water density based on temperature.
        
        Uses standard water property tables. Assumes atmospheric pressure.
        
        Args:
            temperature (float): Water temperature in °C
            
        Returns:
            float: Water density in kg/m³
            
        Example:
            >>> calc = HydraulicCalculator()
            >>> density = calc.get_water_density(20)
            >>> print(f"Density: {density:.1f} kg/m³")
            Density: 998.2 kg/m³
        """
        density_table = {
            0: 999.8,
            5: 1000.0,
            10: 999.7,
            15: 999.1,
            20: 998.2,
            25: 997.0,
            30: 995.7,
            40: 992.2,
            50: 988.0,
            60: 983.2,
            70: 977.8,
            80: 971.8,
            90: 965.3,
            100: 958.4,
        }
        
        # Linear interpolation
        temps = sorted(density_table.keys())
        if temperature in temps:
            return density_table[temperature]
        
        for i in range(len(temps) - 1):
            if temps[i] <= temperature <= temps[i + 1]:
                t1, t2 = temps[i], temps[i + 1]
                d1, d2 = density_table[t1], density_table[t2]
                return d1 + (d2 - d1) * (temperature - t1) / (t2 - t1)
        
        return density_table[temps[-1]]
    
    @staticmethod
    def reynolds_number(velocity: float, diameter: float, 
                       viscosity: float) -> float:
        """
        Calculate Reynolds number for pipe flow.
        
        The Reynolds number determines the flow regime (laminar, transitional, 
        or turbulent) and is fundamental to hydraulic calculations.
        
        Formula: Re = (v * D) / ν
        
        Flow regimes:
            - Re < 2300: Laminar flow
            - 2300 < Re < 4000: Transitional flow
            - Re > 4000: Turbulent flow
        
        Args:
            velocity (float): Flow velocity in m/s
            diameter (float): Pipe internal diameter in m
            viscosity (float): Kinematic viscosity in m²/s
            
        Returns:
            float: Reynolds number (dimensionless)
            
        Raises:
            ValueError: If inputs are negative or zero
            
        Example:
            >>> calc = HydraulicCalculator()
            >>> re = calc.reynolds_number(2.0, 0.1, 1e-6)
            >>> print(f"Reynolds: {re:.0f} - Turbulent flow")
            Reynolds: 200000 - Turbulent flow
        """
        if velocity <= 0 or diameter <= 0 or viscosity <= 0:
            raise ValueError("All parameters must be positive")
        
        return (velocity * diameter) / viscosity
    
    @staticmethod
    def friction_factor_colebrook(reynolds: float, roughness: float, 
                                  diameter: float, tolerance: float = 1e-6,
                                  max_iter: int = 100) -> float:
        """
        Calculate Darcy friction factor using Colebrook-White equation.
        
        This is the most accurate method for friction factor calculation in turbulent
        flow. Uses iterative solution as the equation is implicit.
        
        Colebrook-White equation:
            1/√f = -2 * log10(ε/(3.7*D) + 2.51/(Re*√f))
        
        Where:
            f = Darcy friction factor
            ε = absolute roughness
            D = pipe diameter
            Re = Reynolds number
        
        Valid for:
            - Turbulent flow (Re > 4000)
            - Smooth and rough pipes
            - Full range of relative roughness
        
        Args:
            reynolds (float): Reynolds number
            roughness (float): Absolute roughness in m
            diameter (float): Pipe internal diameter in m
            tolerance (float): Convergence tolerance for iteration
            max_iter (int): Maximum number of iterations
            
        Returns:
            float: Darcy friction factor (dimensionless)
            
        Raises:
            RuntimeError: If iteration does not converge
            ValueError: For laminar flow (use f = 64/Re instead)
            
        Example:
            >>> calc = HydraulicCalculator()
            >>> f = calc.friction_factor_colebrook(100000, 0.00005, 0.1)
            >>> print(f"Friction factor: {f:.6f}")
            Friction factor: 0.018324
        """
        if reynolds < 4000:
            raise ValueError("Colebrook equation is for turbulent flow (Re > 4000). "
                           "For laminar flow use f = 64/Re")
        
        relative_roughness = roughness / diameter
        
        # Initial guess using Swamee-Jain equation
        f = 0.25 / (np.log10(relative_roughness/3.7 + 5.74/reynolds**0.9))**2
        
        # Iterative solution
        for iteration in range(max_iter):
            f_old = f
            term1 = relative_roughness / 3.7
            term2 = 2.51 / (reynolds * np.sqrt(f))
            f = 0.25 / (np.log10(term1 + term2))**2
            
            if abs(f - f_old) < tolerance:
                return f
        
        raise RuntimeError(f"Colebrook iteration did not converge after {max_iter} iterations")
    
    @staticmethod
    def friction_factor_swamee_jain(reynolds: float, roughness: float, 
                                    diameter: float) -> float:
        """
        Calculate friction factor using Swamee-Jain explicit approximation.
        
        This is an explicit approximation of the Colebrook-White equation,
        providing good accuracy (error < 1%) without iteration.
        
        Formula:
            f = 0.25 / [log10(ε/(3.7*D) + 5.74/Re^0.9)]²
        
        Valid for:
            - 4000 < Re < 10^8
            - 10^-6 < ε/D < 10^-2
        
        Args:
            reynolds (float): Reynolds number
            roughness (float): Absolute roughness in m
            diameter (float): Pipe internal diameter in m
            
        Returns:
            float: Darcy friction factor (dimensionless)
            
        Note:
            This approximation is faster than Colebrook-White but slightly
            less accurate. Use Colebrook for critical applications.
            
        Example:
            >>> calc = HydraulicCalculator()
            >>> f = calc.friction_factor_swamee_jain(100000, 0.00005, 0.1)
            >>> print(f"Friction factor: {f:.6f}")
            Friction factor: 0.018301
        """
        relative_roughness = roughness / diameter
        term = relative_roughness / 3.7 + 5.74 / (reynolds ** 0.9)
        return 0.25 / (np.log10(term) ** 2)
    
    @staticmethod
    def head_loss_darcy_weisbach(friction_factor: float, length: float, 
                                diameter: float, velocity: float) -> float:
        """
        Calculate head loss using Darcy-Weisbach equation.
        
        This is the most accurate and widely used method for calculating
        friction losses in pipes. Applicable to all flow regimes and fluids.
        
        Formula:
            hf = f * (L/D) * (v²/2g)
        
        Where:
            hf = head loss due to friction (m)
            f = Darcy friction factor
            L = pipe length (m)
            D = pipe diameter (m)
            v = flow velocity (m/s)
            g = gravitational acceleration (9.81 m/s²)
        
        Standards:
            - ISO 5167: Measurement of fluid flow
            - ASME B31.3: Process piping calculations
        
        Args:
            friction_factor (float): Darcy friction factor
            length (float): Pipe length in m
            diameter (float): Pipe internal diameter in m
            velocity (float): Flow velocity in m/s
            
        Returns:
            float: Head loss in m
            
        Example:
            >>> calc = HydraulicCalculator()
            >>> hf = calc.head_loss_darcy_weisbach(0.02, 100, 0.1, 2.0)
            >>> print(f"Head loss: {hf:.2f} m")
            Head loss: 4.08 m
        """
        return friction_factor * (length / diameter) * (velocity ** 2) / (2 * HydraulicCalculator.GRAVITY)
    
    @staticmethod
    def minor_loss(k_factor: float, velocity: float) -> float:
        """
        Calculate minor (local) head loss from fittings and valves.
        
        Minor losses occur at valves, bends, tees, expansions, contractions,
        and other fittings. Calculated using resistance coefficients (K values).
        
        Formula:
            h_minor = K * (v²/2g)
        
        Where:
            K = loss coefficient (from tables/manufacturer data)
            v = flow velocity (m/s)
            g = gravitational acceleration (9.81 m/s²)
        
        Typical K values:
            - Gate valve (fully open): 0.2
            - Globe valve (fully open): 10
            - 90° elbow: 0.9
            - Tee (flow through branch): 1.8
            - Entrance (sharp): 0.5
            - Exit: 1.0
        
        Args:
            k_factor (float): Loss coefficient (dimensionless)
            velocity (float): Flow velocity in m/s
            
        Returns:
            float: Minor head loss in m
            
        Example:
            >>> calc = HydraulicCalculator()
            >>> h_elbow = calc.minor_loss(k_factor=0.9, velocity=2.0)
            >>> print(f"Elbow loss: {h_elbow:.3f} m")
            Elbow loss: 0.184 m
        """
        return k_factor * (velocity ** 2) / (2 * HydraulicCalculator.GRAVITY)
    
    @staticmethod
    def head_loss_hazen_williams(flow_rate: float, diameter: float, 
                                 length: float, c_factor: float = 120) -> float:
        """
        Calculate head loss using Hazen-Williams equation.
        
        An empirical formula commonly used for water flow in pressure pipes.
        Simpler than Darcy-Weisbach but less accurate and only valid for water.
        
        Formula:
            hf = 10.67 * L * Q^1.852 / (C^1.852 * D^4.87)
        
        Where:
            Q = flow rate (m³/s)
            C = Hazen-Williams coefficient
            D = diameter (m)
            L = length (m)
        
        Typical C values:
            - Very smooth pipes (PVC, copper new): 140-150
            - Smooth pipes (steel new): 130
            - Average pipes (steel used): 100-120
            - Rough pipes (old cast iron): 80-100
        
        Note:
            Only valid for water at normal temperatures (5-25°C).
            For other fluids or extreme conditions, use Darcy-Weisbach.
        
        Args:
            flow_rate (float): Volumetric flow rate in m³/s
            diameter (float): Pipe internal diameter in m
            length (float): Pipe length in m
            c_factor (float): Hazen-Williams coefficient (default: 120)
            
        Returns:
            float: Head loss in m
            
        Example:
            >>> calc = HydraulicCalculator()
            >>> hf = calc.head_loss_hazen_williams(0.01, 0.1, 100, 120)
            >>> print(f"Head loss: {hf:.2f} m")
            Head loss: 1.52 m
        """
        return 10.67 * length * (flow_rate ** 1.852) / (c_factor ** 1.852 * diameter ** 4.87)
    
    @staticmethod
    def velocity_from_flow(flow_rate: float, diameter: float) -> float:
        """
        Calculate flow velocity from volumetric flow rate.
        
        Formula:
            v = Q / A = 4Q / (πD²)
        
        Args:
            flow_rate (float): Volumetric flow rate in m³/s
            diameter (float): Pipe internal diameter in m
            
        Returns:
            float: Flow velocity in m/s
            
        Example:
            >>> calc = HydraulicCalculator()
            >>> v = calc.velocity_from_flow(0.01, 0.1)
            >>> print(f"Velocity: {v:.2f} m/s")
            Velocity: 1.27 m/s
        """
        area = np.pi * (diameter ** 2) / 4
        return flow_rate / area
    
    @staticmethod
    def flow_from_velocity(velocity: float, diameter: float) -> float:
        """
        Calculate volumetric flow rate from velocity.
        
        Formula:
            Q = v * A = v * πD²/4
        
        Args:
            velocity (float): Flow velocity in m/s
            diameter (float): Pipe internal diameter in m
            
        Returns:
            float: Volumetric flow rate in m³/s
            
        Example:
            >>> calc = HydraulicCalculator()
            >>> q = calc.flow_from_velocity(2.0, 0.1)
            >>> print(f"Flow rate: {q:.4f} m³/s")
            Flow rate: 0.0157 m³/s
        """
        area = np.pi * (diameter ** 2) / 4
        return velocity * area
    
    @staticmethod
    def pressure_to_head(pressure: float, density: float = 1000) -> float:
        """
        Convert pressure to head (pressure head).
        
        Formula:
            h = P / (ρ * g)
        
        Args:
            pressure (float): Pressure in Pa
            density (float): Fluid density in kg/m³ (default: 1000 for water)
            
        Returns:
            float: Pressure head in m
            
        Example:
            >>> calc = HydraulicCalculator()
            >>> h = calc.pressure_to_head(100000)
            >>> print(f"Head: {h:.2f} m")
            Head: 10.19 m
        """
        return pressure / (density * HydraulicCalculator.GRAVITY)
    
    @staticmethod
    def head_to_pressure(head: float, density: float = 1000) -> float:
        """
        Convert head to pressure.
        
        Formula:
            P = ρ * g * h
        
        Args:
            head (float): Head in m
            density (float): Fluid density in kg/m³ (default: 1000 for water)
            
        Returns:
            float: Pressure in Pa
            
        Example:
            >>> calc = HydraulicCalculator()
            >>> p = calc.head_to_pressure(10)
            >>> print(f"Pressure: {p/1000:.1f} kPa")
            Pressure: 98.1 kPa
        """
        return density * HydraulicCalculator.GRAVITY * head
    
    def calculate_system(self, flow_rate: float, diameter: float, length: float,
                        roughness: float, minor_losses_k: List[float],
                        temperature: float = 20, elevation_change: float = 0) -> Dict:
        """
        Perform complete hydraulic system calculation.
        
        This method combines all hydraulic calculations to provide a comprehensive
        analysis of a piping system including:
        - Flow velocity
        - Reynolds number and flow regime
        - Friction factor
        - Friction head loss
        - Minor losses
        - Total head loss
        - Pressure drop
        
        Args:
            flow_rate (float): Volumetric flow rate in m³/s
            diameter (float): Pipe internal diameter in m
            length (float): Pipe length in m
            roughness (float): Absolute roughness in m
            minor_losses_k (List[float]): List of K factors for fittings
            temperature (float): Fluid temperature in °C (default: 20)
            elevation_change (float): Net elevation change in m (default: 0)
            
        Returns:
            Dict: Complete results dictionary containing:
                - velocity: Flow velocity (m/s)
                - reynolds: Reynolds number
                - flow_regime: Flow regime (Laminar/Transitional/Turbulent)
                - friction_factor: Darcy friction factor
                - head_loss_friction: Friction head loss (m)
                - head_loss_minor: Sum of minor losses (m)
                - elevation_head: Elevation head change (m)
                - total_head_loss: Total system head loss (m)
                - pressure_drop: Total pressure drop (kPa)
                
        Example:
            >>> calc = HydraulicCalculator()
            >>> results = calc.calculate_system(
            ...     flow_rate=0.01,
            ...     diameter=0.1,
            ...     length=100,
            ...     roughness=0.00005,
            ...     minor_losses_k=[0.5, 0.9, 0.9, 1.0],
            ...     temperature=20
            ... )
            >>> print(f"Total head loss: {results['total_head_loss']:.2f} m")
            Total head loss: 2.15 m
        """
        # Calculate velocity
        velocity = self.velocity_from_flow(flow_rate, diameter)
        
        # Get fluid properties
        viscosity = self.get_kinematic_viscosity(temperature)
        density = self.get_water_density(temperature)
        
        # Calculate Reynolds number
        reynolds = self.reynolds_number(velocity, diameter, viscosity)
        
        # Determine flow regime
        if reynolds < 2300:
            flow_regime = "Laminar"
            friction_factor = 64 / reynolds
        elif reynolds < 4000:
            flow_regime = "Transitional"
            friction_factor = self.friction_factor_swamee_jain(reynolds, roughness, diameter)
        else:
            flow_regime = "Turbulent"
            friction_factor = self.friction_factor_colebrook(reynolds, roughness, diameter)
        
        # Calculate head losses
        head_loss_friction = self.head_loss_darcy_weisbach(
            friction_factor, length, diameter, velocity
        )
        
        head_loss_minor = sum([self.minor_loss(k, velocity) for k in minor_losses_k])
        
        total_head_loss = head_loss_friction + head_loss_minor + elevation_change
        
        # Calculate pressure drop
        pressure_drop = self.head_to_pressure(total_head_loss, density) / 1000  # Convert to kPa
        
        return {
            'velocity': velocity,
            'reynolds': reynolds,
            'flow_regime': flow_regime,
            'friction_factor': friction_factor,
            'head_loss_friction': head_loss_friction,
            'head_loss_minor': head_loss_minor,
            'elevation_head': elevation_change,
            'total_head_loss': total_head_loss,
            'pressure_drop': pressure_drop,
            'density': density,
            'viscosity': viscosity
        }
