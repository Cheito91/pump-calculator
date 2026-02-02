# Industrial Pipe and Pump Calculator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status: Alpha](https://img.shields.io/badge/status-alpha-orange.svg)](https://github.com)

> **⚠️ PRE-RELEASE VERSION** 
> 
> This is an early alpha release (v0.1.0) intended for review and further development.
> The calculations and methodologies require thorough validation before use in production environments.
> **DO NOT USE FOR CRITICAL ENGINEERING DECISIONS WITHOUT INDEPENDENT VERIFICATION.**

## Overview

Professional calculation tool for hydraulic piping systems and centrifugal pump selection. Built with Python and Streamlit, this application provides comprehensive analysis based on international engineering standards.

### Key Features

- **Hydraulic Calculations**
  - Reynolds number and flow regime determination
  - Friction factor calculation (Colebrook-White, Swamee-Jain)
  - Head loss analysis (Darcy-Weisbach, Hazen-Williams)
  - Minor losses from fittings and valves
  - Complete system pressure drop analysis

- **Pump Selection & Analysis**
  - Hydraulic and shaft power calculations
  - NPSH available and required analysis
  - Specific speed calculation and pump classification
  - Affinity laws for speed variations
  - Operating point determination
  - Pump curve generation and visualization

- **Standards Compliance**
  - ISO 9906: Rotodynamic pumps
  - ISO 15649: Petroleum and natural gas industries - Piping
  - ASME B31.3: Process Piping
  - API 610: Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries
  - ANSI/HI 9.6.3: NPSH for Rotodynamic Pumps
  - DIN 1988: Codes of practice for drinking water installations
  - API RP 14E: Recommended Practice for Design and Installation of Offshore Production Platform Piping Systems

- **Technical Visualizations**
  - Interactive pump characteristic curves (H-Q, P-Q, η-Q)
  - Hydraulic profile graphs
  - NPSH analysis charts
  - Loss distribution diagrams
  - Reynolds number analysis

- **PDF Report Generation**
  - Professional calculation memorandums
  - Complete input data documentation
  - Detailed calculation steps
  - Normative compliance verification
  - Graphs and charts integration

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/your-username/pump-calculator.git
cd pump-calculator

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Alternative: Using run scripts

```bash
# Linux/Mac
./run.sh

# Windows
run.bat
```

## Project Structure

```
pump_calculator/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── INSTALL.md                  # Detailed installation instructions
├── LICENSE                     # MIT License
├── .gitignore                  # Git ignore patterns
├── utils/                      # Calculation modules
│   ├── __init__.py
│   ├── hydraulic_calcs.py     # Hydraulic calculations
│   ├── pump_calcs.py          # Pump calculations
│   ├── standards.py           # Engineering standards
│   ├── visualizations.py      # Technical plots
│   └── report_generator.py    # PDF report generation
├── examples.py                 # Usage examples
├── test_suite.py              # Unit tests
└── .streamlit/                 # Streamlit configuration
    └── config.toml             # App theme and settings
```

## Usage

### Basic Pipe Calculation

```python
from utils.hydraulic_calcs import HydraulicCalculator

calc = HydraulicCalculator()

# Calculate system parameters
results = calc.calculate_system(
    flow_rate=0.01,          # m³/s
    diameter=0.1,            # m
    length=100,              # m
    roughness=0.00005,       # m (commercial steel)
    minor_losses_k=[0.5, 0.9, 0.9, 1.0],  # Fittings
    temperature=20           # °C
)

print(f"Velocity: {results['velocity']:.2f} m/s")
print(f"Reynolds: {results['reynolds']:.0f}")
print(f"Total head loss: {results['total_head_loss']:.2f} m")
```

### Pump Calculation

```python
from utils.pump_calcs import PumpCalculator

pump = PumpCalculator()

# Calculate required power
power = pump.hydraulic_power(
    flow_rate=0.01,    # m³/s
    head=30,           # m
    density=1000       # kg/m³
)

# Check NPSH
npsh_avail = pump.npsh_available(
    pressure_suction=101300,  # Pa
    vapor_pressure=2300,      # Pa
    velocity_suction=1.0,     # m/s
    elevation=2.0,            # m
    density=1000              # kg/m³
)

print(f"Hydraulic power: {power/1000:.2f} kW")
print(f"NPSH available: {npsh_avail:.2f} m")
```

### Running Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run test suite
python test_suite.py
```

### Running Examples

```bash
# Execute example calculations
python examples.py
```

## Engineering Standards & References

This application implements calculations according to:

1. **ISO 9906:2012** - Rotodynamic pumps - Hydraulic performance acceptance tests - Grades 1, 2 and 3
2. **ISO 15649** - Petroleum and natural gas industries - Piping
3. **ASME B31.3** - Process Piping - Design, fabrication, and erection
4. **API 610** - Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries
5. **ANSI/HI 9.6.3** - Rotodynamic (Centrifugal and Vertical) Pumps - Guideline for NPSH Margin
6. **DIN 1988** - Technical rules for drinking water installations (TRWI)
7. **API RP 14E** - Design and Installation of Offshore Production Platform Piping Systems

## Calculation Methodologies

### Hydraulic Calculations

- **Darcy-Weisbach Equation**: Primary method for head loss calculation
- **Colebrook-White Equation**: Iterative friction factor calculation for turbulent flow
- **Swamee-Jain Approximation**: Explicit friction factor formula (error < 1%)
- **Hazen-Williams**: Alternative empirical method for water flow
- **Minor Loss Coefficients**: K-factor method for fittings and valves

### Pump Analysis

- **Affinity Laws**: Scaling for speed and diameter changes
- **Specific Speed**: Pump type classification (radial, mixed-flow, axial)
- **NPSH Calculation**: Cavitation risk assessment
- **Pump Curves**: H-Q, P-Q, and efficiency curves
- **Operating Point**: System curve intersection method

## Dependencies

Main packages (see `requirements.txt` for complete list):

- **streamlit** >= 1.31.0 - Web application framework
- **numpy** >= 1.24.0 - Numerical computations
- **pandas** >= 2.0.0 - Data manipulation
- **plotly** >= 5.18.0 - Interactive visualizations
- **scipy** >= 1.11.0 - Scientific computing
- **reportlab** >= 4.0.0 - PDF generation

## Development Status

### Current Version: 0.1.0-alpha

**Implemented:**
- [x] Core hydraulic calculations
- [x] Pump selection algorithms
- [x] Standards compliance checks
- [x] Interactive visualizations
- [x] PDF report generation
- [x] Web interface (Streamlit)
- [x] Unit tests for core functions

**Pending/Under Review:**
- [ ] Extended validation of all calculation methods
- [ ] Peer review by professional engineers
- [ ] Additional test cases and edge case handling
- [ ] Multi-fluid support (currently water-focused)
- [ ] Database of commercial pumps
- [ ] Network analysis for complex piping systems
- [ ] Transient flow analysis
- [ ] API for integration with other tools

**Known Limitations:**
- Calculations are currently validated for water only
- Pump database not included (user must input curves)
- Single-path systems only (no network analysis)
- Steady-state flow only (no transient/surge analysis)
- Requires manual validation for critical applications

## Contributing

This project is in early alpha stage and we welcome contributions! Please read `CONTRIBUTING.md` for:

- Code of conduct
- Development guidelines
- How to submit issues
- Pull request process

**Priority areas for contribution:**
1. Validation of calculation methods
2. Additional unit tests
3. Bug reports and fixes
4. Documentation improvements
5. International standards updates

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

### Third-Party Components

This software uses the following open-source packages:
- Streamlit (Apache 2.0)
- NumPy (BSD)
- Pandas (BSD)
- Plotly (MIT)
- SciPy (BSD)
- ReportLab (BSD)

## Disclaimer

⚠️ **IMPORTANT ENGINEERING DISCLAIMER** ⚠️

This software is provided "as is" for educational and preliminary design purposes only.

**YOU MUST:**
- Independently verify all calculations
- Have designs reviewed by licensed professional engineers
- Follow local codes and regulations
- Perform proper system commissioning and testing
- Use manufacturer's certified pump curves and data

**THIS SOFTWARE IS NOT:**
- A substitute for professional engineering judgment
- Certified for safety-critical applications
- Validated for all operating conditions
- A replacement for detailed engineering analysis

The authors and contributors assume no liability for:
- Errors in calculations
- Equipment failures
- Property damage
- Personal injury
- Financial losses

**For production systems, always consult with qualified engineers and follow applicable codes and standards.**

## Authors & Acknowledgments

**Project Lead:** Industrial Calculator Project Contributors

**Special Thanks:**
- Contributors to the scientific Python ecosystem
- Open-source engineering software community
- Standards organizations (ISO, ASME, API, ANSI, DIN)

## Support

- **Issues**: Please report bugs via GitHub Issues
- **Questions**: Use GitHub Discussions for technical questions
- **Security**: Report security issues privately to [security contact]

## Roadmap

### Version 0.2.0 (Planned)
- Extended validation suite
- Multi-fluid support
- Commercial pump database integration
- Enhanced error handling

### Version 0.3.0 (Future)
- Network analysis capabilities
- Optimization algorithms
- Cost estimation module
- API documentation

### Version 1.0.0 (Future)
- Production-ready release
- Professional engineer validation
- Comprehensive test coverage
- Performance optimization

## Citation

If you use this software in your work, please cite:

```
Industrial Pipe and Pump Calculator (v0.1.0-alpha)
https://github.com/your-username/pump-calculator
```

---

**Version:** 0.1.0-alpha  
**Last Updated:** February 2026  
**Status:** Pre-release - Requires validation and further development  
**Maintenance:** Active development

For more information, visit the [project documentation](https://github.com/your-username/pump-calculator/wiki).
