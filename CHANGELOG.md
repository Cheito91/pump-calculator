# Changelog

All notable changes to the Industrial Pipe and Pump Calculator project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned for 0.2.0
- Complete English translation of all Python files
- Extended test coverage (target: 80%)
- Performance optimization
- Multi-fluid support preparation

## [0.1.0-alpha] - 2026-02-02

### Added
- Initial pre-release version
- Core hydraulic calculations module (Darcy-Weisbach, Colebrook-White)
- Pump selection and analysis algorithms
- Standards compliance checks (ISO, ASME, API, DIN)
- Interactive Streamlit web interface
- PDF report generation capability
- Technical visualizations with Plotly
- Unit test suite for core functions
- README.md with comprehensive project documentation
- INSTALL.md with detailed installation instructions
- LICENSE (MIT) with engineering disclaimer
- CONTRIBUTING.md with contribution guidelines
- STATUS.md documenting current project state
- Comprehensive .gitignore for Python projects

### Changed
- Converted hydraulic_calcs.py to English with complete docstrings
- Updated documentation structure for GitHub
- Replaced emojis with text indicators in test suite
- Updated Streamlit deprecated parameters (use_container_width → width)
- Fixed Plotly gridcolor configuration issue

### Security
- Removed any personal or sensitive information
- Added .gitignore patterns for sensitive data
- Implemented backup file exclusion patterns
- Generic placeholder text for user inputs

### Known Issues
- Remaining Python files (app.py, pump_calcs.py, standards.py, etc.) contain Spanish text
- Mixed language interface (partially English, partially Spanish)
- Test coverage below 80%
- Limited validation against published data
- Documentation incomplete for some modules

### Notes
- **This is a pre-release version**
- Requires further development and validation
- Not recommended for production use without independent verification
- Professional engineering review pending

## Release Definitions

### Pre-Release Versions (0.x.x-alpha/beta)
- Under active development
- Breaking changes may occur
- Incomplete features
- Limited testing
- Not for production use

### Stable Releases (1.x.x+)
- Production-ready code
- Comprehensive testing
- Professional validation
- Complete documentation
- Semantic versioning followed

## Version History

### Version Numbering

Given a version number MAJOR.MINOR.PATCH-LABEL:

- **MAJOR**: Incompatible API changes
- **MINOR**: Added functionality (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)
- **LABEL**: Pre-release identifier (alpha, beta, rc)

### Future Roadmap

#### 0.2.0 (Target: Q2 2026)
- Complete translation to English
- 80% test coverage
- Performance improvements
- Extended validation suite

#### 0.3.0 (Target: Q3 2026)
- Multi-fluid support
- Network analysis features
- Commercial pump database
- Optimization algorithms

#### 1.0.0 (Target: Q4 2026)
- Professional engineering validation
- Production-ready release
- Complete documentation
- Security audit
- Performance benchmarks

---

**Maintained by:** Industrial Calculator Project Contributors  
**License:** MIT  
**Status:** Active Development
