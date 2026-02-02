# Contributing to Industrial Pipe and Pump Calculator

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [How to Contribute](#how-to-contribute)
4. [Development Guidelines](#development-guidelines)
5. [Testing](#testing)
6. [Submission Guidelines](#submission-guidelines)

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and respectful environment for all contributors, regardless of experience level, background, or identity.

### Our Standards

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the project and community
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment, trolling, or insulting comments
- Public or private harassment
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of hydraulic engineering or willingness to learn
- Familiarity with Python and scientific computing

### Setting Up Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/YOUR-USERNAME/pump-calculator.git
cd pump-calculator

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy

# Run tests to verify setup
python test_suite.py
```

## How to Contribute

### Reporting Bugs

Before creating a bug report, please check existing issues to avoid duplicates.

**Good Bug Report Includes:**
- Clear, descriptive title
- Steps to reproduce the issue
- Expected vs. actual behavior
- Screenshots or code snippets (if applicable)
- System information (OS, Python version)
- Relevant log outputs

**Template:**
```markdown
**Description:** Brief description of the bug

**To Reproduce:**
1. Go to '...'
2. Click on '....'
3. See error

**Expected Behavior:** What should happen

**Actual Behavior:** What actually happens

**Environment:**
- OS: [e.g., Ubuntu 22.04]
- Python: [e.g., 3.10.0]
- Version: [e.g., 0.1.0]

**Additional Context:** Any other relevant information
```

### Suggesting Enhancements

Enhancement suggestions are welcome! Please provide:

- Clear, descriptive title
- Detailed description of the proposed feature
- Use cases and benefits
- Possible implementation approach (if you have ideas)
- References to standards or methodologies (if applicable)

### Pull Requests

1. **Fork the Repository**
2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Make Your Changes**
   - Follow the development guidelines below
   - Write or update tests
   - Update documentation

4. **Test Your Changes**
   ```bash
   python test_suite.py
   ```

5. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

6. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Submit Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template

## Development Guidelines

### Code Style

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Maximum line length: 100 characters
- Use type hints for function signatures

**Example:**
```python
def calculate_reynolds(velocity: float, diameter: float, 
                      viscosity: float) -> float:
    """
    Calculate Reynolds number for pipe flow.
    
    Args:
        velocity: Flow velocity in m/s
        diameter: Pipe diameter in m
        viscosity: Kinematic viscosity in m²/s
        
    Returns:
        Reynolds number (dimensionless)
    """
    return (velocity * diameter) / viscosity
```

### Documentation Standards

**All functions must include:**
- Brief description
- Args section with types and units
- Returns section with type and units
- Example usage (for complex functions)
- References to standards (if applicable)

**Docstring Format:**
```python
def function_name(param1: type, param2: type) -> return_type:
    """
    Brief one-line description.
    
    More detailed description if needed. Explain the purpose,
    methodology, and any important considerations.
    
    Standards:
        - ISO XXXX: Description
        - ASME XXXX: Description
    
    Args:
        param1 (type): Description with units
        param2 (type): Description with units
        
    Returns:
        return_type: Description with units
        
    Raises:
        ValueError: When and why
        
    Example:
        >>> result = function_name(value1, value2)
        >>> print(result)
        expected_output
        
    Note:
        Any important notes or limitations
    """
```

### Engineering Standards

When implementing calculations:

1. **Reference Standards**: Always cite the standard (ISO, ASME, API, etc.)
2. **Document Assumptions**: List any simplifications or assumptions
3. **Include Units**: Always specify units in comments and docstrings
4. **Validation Range**: Document valid input ranges
5. **Accuracy**: Note expected accuracy or error margins

**Example:**
```python
def friction_factor_colebrook(reynolds: float, roughness: float, 
                             diameter: float) -> float:
    """
    Calculate friction factor using Colebrook-White equation.
    
    Standards:
        - ISO 5167-2: Measurement of fluid flow
        - ASME B31.3: Process Piping
    
    Valid for:
        - Turbulent flow (Re > 4000)
        - 10^-6 < ε/D < 10^-2
    
    Accuracy:
        - Converges to within 10^-6
        - Matches experimental data within ±2%
    
    Args:
        reynolds: Reynolds number (dimensionless)
        roughness: Absolute roughness in m
        diameter: Pipe internal diameter in m
        
    Returns:
        Darcy friction factor (dimensionless)
    """
```

### Commit Messages

Use clear, descriptive commit messages:

**Format:**
```
Type: Brief description (50 chars or less)

More detailed explanation if needed (wrap at 72 characters).
Explain the problem this commit solves and why you chose
this particular solution.

References:
- Issue #123
- Standard: ISO 9906
```

**Types:**
- `Add:` New feature or functionality
- `Fix:` Bug fix
- `Update:` Changes to existing functionality
- `Docs:` Documentation only
- `Test:` Adding or updating tests
- `Refactor:` Code restructuring without changing functionality
- `Style:` Formatting, missing semicolons, etc.
- `Chore:` Maintenance tasks

## Testing

### Running Tests

```bash
# Run all tests
python test_suite.py

# Run with verbose output
python test_suite.py -v
```

### Writing Tests

All new functions should include unit tests:

```python
def test_new_function():
    """Test description"""
    # Arrange
    input_value = 10.0
    expected_output = 20.0
    
    # Act
    result = new_function(input_value)
    
    # Assert
    assert abs(result - expected_output) < 0.01, \
        f"Expected {expected_output}, got {result}"
```

### Test Coverage

- Aim for >80% code coverage
- Test edge cases and error conditions
- Include integration tests for complex workflows
- Validate against known solutions or standards

## Submission Guidelines

### Before Submitting

**Checklist:**
- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] No personal or sensitive data in commits
- [ ] Commit messages are clear
- [ ] Branch is up to date with main

### Pull Request Process

1. **Title**: Clear, descriptive title
2. **Description**: What changes and why
3. **Testing**: How you tested the changes
4. **Screenshots**: If applicable
5. **Breaking Changes**: Note any breaking changes
6. **Documentation**: Link to updated docs

**PR Template:**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe how you tested

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Follows code style guidelines
```

### Review Process

1. At least one maintainer review required
2. All automated checks must pass
3. Discussion and iteration on feedback
4. Final approval and merge

### After Merge

- Your contribution will be listed in CONTRIBUTORS.md
- Major contributions may be acknowledged in release notes
- You become part of the project community!

## Priority Contribution Areas

### High Priority

1. **Validation**: Verify calculations against published standards
2. **Testing**: Add unit tests and integration tests
3. **Documentation**: Improve inline and external documentation
4. **Bug Fixes**: Address known issues

### Medium Priority

1. **Features**: Implement planned features from roadmap
2. **Performance**: Optimize calculation speed
3. **UI/UX**: Improve Streamlit interface
4. **Standards**: Update to latest standard revisions

### Low Priority

1. **Refactoring**: Code cleanup and organization
2. **Tooling**: Development workflow improvements
3. **Examples**: Additional usage examples

## Questions?

- **Technical Questions**: Use GitHub Discussions
- **Bug Reports**: Create an Issue
- **Feature Ideas**: Create an Issue with enhancement label
- **General Chat**: Join our community (link TBD)

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Project documentation
- Release notes (for significant contributions)

Thank you for contributing to making this project better!

---

**Last Updated:** February 2026  
**Version:** 1.0
