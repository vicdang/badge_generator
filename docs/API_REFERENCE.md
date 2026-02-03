# API Reference

Complete API documentation for Badge Generator modules.

## Table of Contents

1. [badgenerator Module](#badgenerator-module)
2. [badge_gui Module](#badge_gui-module)
3. [config Module](#config-module)
4. [tools.image_manager](#tools-image_manager)
5. [tools.image_crawler](#tools-image_crawler)
6. [tools.util](#tools-util)

---

## badgenerator Module

Main CLI application for badge generation with multi-threaded image downloading.

**Location:** `src/badgenerator.py`

### BadgeGenerator Class

```python
class BadgeGenerator:
    """Generate badges with employee information and face detection."""
    
    def __init__(self, config: Optional[Dict] = None) -> None:
        """
        Initialize BadgeGenerator.
        
        Args:
            config: Optional configuration dictionary. If None, loads from config.ini
            
        Raises:
            FileNotFoundError: If config file not found
            ValueError: If config is invalid
        """
    
    def generate_badge(
        self,
        user_info: Dict[str, str],
        output_path: Optional[str] = None
    ) -> bool:
        """
        Generate a badge for a single user.
        
        Args:
            user_info: Dictionary with keys:
                - 'name': Full name (str)
                - 'id': Employee ID (str)
                - 'department': Department name (str)
                - 'image_path': Path to employee photo (str)
            output_path: Where to save badge. If None, uses config default.
        
        Returns:
            True if badge generated successfully, False otherwise
            
        Raises:
            KeyError: If user_info missing required keys
            FileNotFoundError: If image_path doesn't exist
            IOError: If unable to write output file
        """
    
    def generate_batch(
        self,
        user_list: List[Dict[str, str]],
        output_dir: Optional[str] = None
    ) -> Dict[str, bool]:
        """
        Generate badges for multiple users.
        
        Args:
            user_list: List of user info dictionaries
            output_dir: Directory to save badges. If None, uses config default.
        
        Returns:
            Dictionary mapping user IDs to success status
            
        Example:
            >>> users = [
            ...     {'name': 'John Doe', 'id': '001', 'department': 'HR', 'image_path': 'john.jpg'},
            ...     {'name': 'Jane Smith', 'id': '002', 'department': 'IT', 'image_path': 'jane.jpg'}
            ... ]
            >>> gen = BadgeGenerator()
            >>> results = gen.generate_batch(users)
            >>> print(results)
            {'001': True, '002': True}
        """
    
    def download_images(
        self,
        employee_ids: List[str],
        output_dir: Optional[str] = None
    ) -> Dict[str, bool]:
        """
        Download employee images from configured source.
        
        Args:
            employee_ids: List of employee IDs to download
            output_dir: Where to save downloaded images. If None, uses images/source
        
        Returns:
            Dictionary mapping employee IDs to success status
            
        Note:
            Uses multi-threaded downloading with configured worker count.
            Failed downloads are logged but don't raise exceptions.
        """
```

### Functions

```python
def execute() -> None:
    """Main entry point for CLI application."""

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""

def _parse_user_info(row: List[str]) -> Dict[str, str]:
    """Parse user info from spreadsheet row."""

def _render_text(
    img: PIL.Image.Image,
    text: str,
    position: Tuple[int, int],
    font_size: int = 20
) -> PIL.Image.Image:
    """Render text on image at position."""

def parse_qr_code(employee_id: str) -> PIL.Image.Image:
    """Generate QR code image from employee ID."""
```

---

## badge_gui Module

GUI application for configuring and running badge generation.

**Location:** `src/badge_gui.py`

### ConfigEditor Class

```python
class ConfigEditor:
    """GUI editor for configuration and badge generation."""
    
    def __init__(self, root: tk.Tk) -> None:
        """
        Initialize GUI.
        
        Args:
            root: Tkinter root window
        """
    
    def load_config(self) -> Dict:
        """Load configuration from file."""
    
    def save_config(self) -> bool:
        """Save configuration to file."""
    
    def generate_badges(self) -> bool:
        """Generate badges using current configuration."""
    
    def select_input_file(self) -> str:
        """Open file dialog to select input file."""
    
    def select_output_dir(self) -> str:
        """Open directory dialog to select output directory."""
```

### Main Functions

```python
def main() -> None:
    """Main GUI application entry point."""

def create_main_window() -> tk.Tk:
    """Create and configure main window."""
```

---

## config Module

Configuration management and position definitions.

**Location:** `src/config.py`

### Config Class

```python
class Config:
    """Configuration management."""
    
    def __init__(self, config_file: Optional[str] = None) -> None:
        """
        Initialize configuration.
        
        Args:
            config_file: Path to config.ini file. If None, uses default location.
        """
    
    def get(self, section: str, key: str) -> str:
        """
        Get configuration value.
        
        Args:
            section: Configuration section (e.g., 'crawler', 'generation')
            key: Configuration key
        
        Returns:
            Configuration value
            
        Raises:
            KeyError: If section or key not found
        """
    
    def set(self, section: str, key: str, value: str) -> None:
        """Set configuration value."""
    
    def save(self) -> None:
        """Save configuration to file."""
```

### Functions

```python
def get_position_dict() -> Dict[str, Tuple[int, int]]:
    """
    Get text position mappings for badge template.
    
    Returns:
        Dictionary mapping position names to (x, y) coordinates
    """

def get_file_extensions() -> Dict[str, List[str]]:
    """
    Get supported file extensions by category.
    
    Returns:
        Dictionary like:
        {
            'image': ['.png', '.jpg', '.webp'],
            'data': ['.xlsx', '.xls', '.csv']
        }
    """
```

---

## tools.image_manager

Image lifecycle management with downloading and processing.

**Location:** `tools/image_manager.py`

### ImageManager Class

```python
class ImageManager:
    """Manage image downloading, validation, and processing."""
    
    def __init__(
        self,
        source_url: str,
        output_dir: str,
        max_workers: int = 5
    ) -> None:
        """
        Initialize ImageManager.
        
        Args:
            source_url: Base URL for image downloads
            output_dir: Directory to save images
            max_workers: Number of concurrent download threads
        """
    
    def download(
        self,
        employee_id: str,
        format: str = ".webp"
    ) -> Optional[str]:
        """
        Download single image.
        
        Args:
            employee_id: Employee ID to download
            format: Image format extension (e.g., '.webp', '.jpg')
        
        Returns:
            Path to downloaded image, or None if failed
        """
    
    def download_batch(
        self,
        employee_ids: List[str],
        format: str = ".webp"
    ) -> Dict[str, Optional[str]]:
        """
        Download multiple images concurrently.
        
        Args:
            employee_ids: List of employee IDs
            format: Image format extension
        
        Returns:
            Dictionary mapping employee IDs to file paths (None if failed)
        """
    
    def process_image(
        self,
        image_path: str,
        size: Optional[Tuple[int, int]] = None,
        format: str = "RGB"
    ) -> Optional[PIL.Image.Image]:
        """
        Process downloaded image.
        
        Args:
            image_path: Path to image file
            size: Resize to this size. If None, keeps original.
            format: Convert to this format (RGB, RGBA, etc.)
        
        Returns:
            Processed PIL Image, or None if failed
        """
    
    def detect_faces(
        self,
        image_path: str
    ) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in image.
        
        Args:
            image_path: Path to image file
        
        Returns:
            List of face rectangles as (x, y, width, height)
        """
    
    def validate_image(
        self,
        image_path: str
    ) -> bool:
        """
        Validate downloaded image.
        
        Args:
            image_path: Path to image file
        
        Returns:
            True if image is valid (readable, not corrupted), False otherwise
        """
```

---

## tools.image_crawler

Multi-threaded image downloading from TMA intranet.

**Location:** `tools/image_crawler.py`

### ImageCrawler Class

```python
class ImageCrawler:
    """Download images from TMA intranet with multi-threading."""
    
    def __init__(
        self,
        base_url: str,
        workers: int = 5,
        timeout: int = 30
    ) -> None:
        """
        Initialize crawler.
        
        Args:
            base_url: Base URL for image downloads
            workers: Number of concurrent worker threads
            timeout: Request timeout in seconds
        """
    
    def download_single(
        self,
        employee_id: str,
        format: str = ".webp"
    ) -> Tuple[bool, Optional[str]]:
        """
        Download single image.
        
        Args:
            employee_id: Employee ID
            format: Image format extension
        
        Returns:
            (success: bool, file_path: Optional[str])
        """
    
    def download_batch(
        self,
        employee_ids: List[str],
        format: str = ".webp"
    ) -> Dict[str, Tuple[bool, Optional[str]]]:
        """
        Download multiple images with multi-threading.
        
        Args:
            employee_ids: List of employee IDs
            format: Image format
        
        Returns:
            Dictionary mapping employee IDs to (success, path) tuples
        """
    
    def verify_url(self, employee_id: str) -> bool:
        """
        Verify image URL exists.
        
        Args:
            employee_id: Employee ID
        
        Returns:
            True if URL accessible, False otherwise
        """
```

### Functions

```python
def build_image_url(base_url: str, employee_id: str, format: str = ".webp") -> str:
    """Build complete image URL from components."""

def download_file(
    url: str,
    output_path: str,
    timeout: int = 30
) -> bool:
    """
    Download file from URL.
    
    Args:
        url: URL to download
        output_path: Where to save file
        timeout: Request timeout in seconds
    
    Returns:
        True if successful, False otherwise
    """
```

---

## tools.util

Utility functions used across modules.

**Location:** `tools/util.py`

### Functions

```python
def log_message(
    level: str,
    message: str,
    file_path: Optional[str] = None
) -> None:
    """
    Log message to file and console.
    
    Args:
        level: Log level ('DEBUG', 'INFO', 'WARNING', 'ERROR')
        message: Message to log
        file_path: Optional file path for file-based logging
    """

def ensure_directory(path: str) -> bool:
    """
    Create directory if it doesn't exist.
    
    Args:
        path: Directory path
    
    Returns:
        True if directory exists or was created, False if error
    """

def validate_file_path(path: str) -> bool:
    """Validate file path is readable."""

def validate_image_file(path: str) -> bool:
    """Validate file is a valid image."""

def get_file_size(path: str) -> int:
    """Get file size in bytes."""

def format_size(size_bytes: int) -> str:
    """Format bytes as human-readable size (KB, MB, etc.)."""

def retry_on_error(
    func,
    max_retries: int = 3,
    delay: float = 1.0
) -> Any:
    """
    Retry function with exponential backoff.
    
    Args:
        func: Function to retry
        max_retries: Maximum retry attempts
        delay: Initial delay between retries
    
    Returns:
        Function result
    """
```

---

## Configuration Files

### config.ini

```ini
[general]
input_file = data/employee_list.xlsx
output_dir = images/output
log_file = logs/generation.log

[generation]
badge_width = 200
badge_height = 250
template_path = resources/templates/badge_template.png
font_path = resources/fonts/Arial.ttf
font_size = 20

[crawler]
enable_crawler = false
base_url = https://intranet.tma.com.vn/images/emp_images/big_new
workers = 5
timeout = 30
format = .webp

[image_processing]
face_cascade = resources/haar_cascade/haarcascade_frontalface_default.xml
min_image_size = 50
```

---

## Data Structures

### User Info Dictionary

```python
{
    'name': str,           # Full employee name
    'id': str,             # Employee ID
    'department': str,     # Department name
    'image_path': str,     # Path to employee photo
    'position': str,       # Optional: job position
    'email': str,          # Optional: email address
}
```

### Badge Info Dictionary

```python
{
    'user_id': str,
    'user_name': str,
    'department': str,
    'qr_code': bytes,      # QR code image data
    'faces_detected': int, # Number of faces found
    'output_path': str,    # Badge file path
    'timestamp': str,      # Generation time
    'status': str,         # 'success' or 'failed'
}
```

---

## Error Codes

| Code | Error | Description |
|------|-------|-------------|
| 1001 | ConfigError | Configuration file not found or invalid |
| 1002 | FileError | Input/output file error |
| 1003 | ImageError | Image processing error |
| 1004 | DownloadError | Image download failed |
| 1005 | FaceError | Face detection failed |
| 1006 | ValidationError | Data validation error |
| 1007 | TemplateError | Badge template error |

---

**Last Updated:** 2024
**Version:** 2.0
