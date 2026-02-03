# Contributing to Badge Generator

Thank you for your interest in contributing to the Badge Generator project! This document provides guidelines and instructions for contributing.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Code Standards](#code-standards)
5. [Testing](#testing)
6. [Documentation](#documentation)
7. [Submitting Changes](#submitting-changes)

## Code of Conduct

Please be respectful and constructive in all interactions within this project.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Setting Up Development Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vicdang/badge-generator.git
   cd badgenerator
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Verify installation:**
   ```bash
   pytest tests/
   ```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Use descriptive branch names:
- `feature/add-export-support`
- `bugfix/fix-qr-generation`
- `docs/update-api-guide`

### 2. Make Changes

- Write clean, well-documented code
- Follow the [Code Standards](#code-standards)
- Commit frequently with meaningful messages

### 3. Test Your Changes

```bash
pytest tests/ -v
```

### 4. Update Documentation

- Update relevant markdown files in `docs/`
- Add docstrings to new functions/classes
- Include examples for new features

### 5. Submit Changes

See [Submitting Changes](#submitting-changes) section below

## Code Standards

### Style Guide

We follow **PEP 8** with these specifications:

- **Line length:** 100 characters maximum
- **Indentation:** 4 spaces
- **String quotes:** Double quotes preferred for docstrings, single for regular strings
- **Imports:** Grouped in order (stdlib, third-party, local)

### Type Hints

Add type hints to all new functions:

```python
def process_image(image_path: str, scale: float = 1.0) -> PIL.Image.Image:
    """
    Process an image file.
    
    Args:
        image_path: Path to the image file
        scale: Scale factor for resizing
        
    Returns:
        Processed PIL Image object
    """
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def generate_badge(user_info: Dict[str, str], output_path: str) -> bool:
    """
    Generate a badge from user information.
    
    This function creates a badge image with the provided user information,
    including face detection and QR code generation.
    
    Args:
        user_info: Dictionary containing user details (name, id, etc.)
        output_path: Path where the badge should be saved
        
    Returns:
        True if badge generation succeeded, False otherwise
        
    Raises:
        ValueError: If user_info is missing required fields
        IOError: If output file cannot be written
        
    Example:
        >>> user = {'name': 'John Doe', 'id': '12345'}
        >>> generate_badge(user, 'output/badge.png')
        True
    """
    pass
```

### Naming Conventions

- **Functions/variables:** `snake_case`
- **Classes:** `PascalCase`
- **Constants:** `UPPER_SNAKE_CASE`
- **Private members:** Prefix with underscore (`_private_method`)

### Code Organization

Project structure:
```
src/                    # Main application code
├── badgenerator.py  # CLI entry point
├── badge_gui.py        # GUI entry point
├── config.py          # Configuration management
└── core/              # Core functionality

tools/                 # Utility modules
├── image_manager.py
├── image_crawler.py
└── ...

tests/                 # Test files
config/                # Configuration files
resources/             # Static resources
docs/                  # Documentation
```

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_image_manager.py -v

# Run with coverage
pytest tests/ --cov=src --cov=tools

# Run specific test marker
pytest -m unit
pytest -m integration
pytest -m e2e
```

### Writing Tests

1. **Test location:** `tests/` directory
2. **Test naming:** `test_*.py` or `*_test.py`
3. **Test function naming:** `test_*` in test classes

Example test structure:

```python
import pytest
from src.badgenerator import BadgeGenerator

class TestBadgeGenerator:
    """Tests for BadgeGenerator class."""
    
    @pytest.fixture
    def generator(self):
        """Fixture providing a BadgeGenerator instance."""
        return BadgeGenerator()
    
    def test_generate_badge_with_valid_input(self, generator):
        """Test generating a badge with valid input."""
        user_info = {'name': 'John Doe', 'id': '12345'}
        result = generator.generate_badge(user_info, 'output/badge.png')
        assert result is True
    
    @pytest.mark.unit
    def test_validate_user_info(self, generator):
        """Test user info validation."""
        invalid_info = {'name': 'John Doe'}  # Missing 'id'
        with pytest.raises(ValueError):
            generator._validate_user_info(invalid_info)
```

### Test Markers

- `@pytest.mark.unit` - Unit tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.e2e` - End-to-end tests
- `@pytest.mark.gui` - GUI tests
- `@pytest.mark.slow` - Slow running tests
- `@pytest.mark.skip_on_ci` - Skip in CI environments

## Documentation

### Updating Documentation

Documentation files are in the `docs/` directory:

- **README.md** - Project overview
- **QUICKSTART.md** - Getting started guide
- **ARCHITECTURE.md** - Technical architecture
- **API.md** - API reference (if applicable)
- **CONTRIBUTING.md** - This file

### Documentation Style

- Use Markdown formatting
- Include code examples where appropriate
- Keep language clear and concise
- Update table of contents if adding new sections

### Code Examples in Documentation

```markdown
## Example Usage

\`\`\`python
from src.badgenerator import generate_badge

user_info = {
    'name': 'John Doe',
    'id': '12345',
    'department': 'Engineering'
}

generate_badge(user_info, 'output/badge.png')
\`\`\`
```

## Submitting Changes

### Before Submission

1. **Update tests:**
   ```bash
   pytest tests/ -v
   ```

2. **Check code style:**
   ```bash
   black src/ tools/ tests/
   flake8 src/ tools/ tests/
   isort src/ tools/ tests/
   ```

3. **Type checking:**
   ```bash
   mypy src/ tools/
   ```

4. **Update documentation:**
   - Add docstrings to new functions
   - Update relevant markdown files
   - Include examples for new features

### Commit Messages

Write clear, concise commit messages:

```
type(scope): brief description

Longer explanation if needed. Explain why this change is needed
and what problems it solves.

Fixes #issue_number (if applicable)
```

Types:
- `feat:` New feature
- `bugfix:` Bug fix
- `docs:` Documentation update
- `refactor:` Code refactoring
- `test:` Test additions/updates
- `chore:` Build, dependencies, etc.

Examples:
```
feat(badge): Add badge export to PDF format

Implement PDF export functionality to BadgeGenerator class.
Users can now export generated badges in PDF format.

Fixes #123
```

### Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes following the guidelines
4. Push to your fork
5. Submit a pull request with:
   - Clear description of changes
   - Reference to related issues
   - Screenshots/examples if applicable

## Questions or Issues?

- **Bugs:** Create an issue with detailed reproduction steps
- **Features:** Discuss in an issue before implementing
- **Questions:** Open a discussion or issue

Thank you for contributing to Badge Generator! 🎉
