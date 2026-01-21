# -*- coding: utf-8 -*-
"""
Mock data generator - create test data with Vietnamese names.

Copyright (C) 2021
Authors: Vic Dang
Date: 16-Dec-21
Version: 1.0

Usage example:
  python mock_data_generator.py -f ./ -l log.log -n 5 -c
"""

import argparse
import logging
import logging.handlers
import random
from pathlib import Path
from typing import Generator, Optional


class MockDataGenerator:
    """Generate mock image names and files for testing."""

    def __init__(self, folder_path: str, log_file: str) -> None:
        """
        Initialize MockDataGenerator.

        Args:
            folder_path: Path where mock data will be created.
            log_file: Path to log file.
        """
        self.folder_path = Path(folder_path)
        self.log_file = log_file
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """
        Setup logging configuration.

        Returns:
            Configured logger instance.
        """
        logger = logging.getLogger('mock_data_generator')
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )

        # File handler
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger

    def cleanup_folder(self) -> None:
        """Remove all files from mock_images folder."""
        mock_folder = self.folder_path / 'mock_images'
        self.logger.info(f"Cleaning up mock folder: {mock_folder}")
        
        if mock_folder.exists():
            for file_path in mock_folder.iterdir():
                if file_path.is_file():
                    file_path.unlink()
                    self.logger.info(f"Removed: {file_path.name}")

    @staticmethod
    def get_vietnamese_name(is_male: bool = True) -> str:
        """
        Generate random Vietnamese name.

        Args:
            is_male: True for male names, False for female names.

        Returns:
            Generated Vietnamese name.
        """
        if is_male:
            first_names = [
                "Hồng", "Đức", "Quốc", "Hoàng", "Hải", "Công", "Minh",
                "Thành", "Thuận", "Đông", "Tuấn", "Nhân", "Trung", "Sơn",
                "Duy", "Hùng", "Long", "Tiến", "Vũ", "Bình", "Huy",
                "Phúc", "Đạt", "Trọng", "Gia", "Linh", "An", "Vinh", "Đại"
            ]
            mid_names = [
                "Văn", "Hữu", "Đức", "Minh", "Thành", "Nhật", "Đình", "An",
                "Gia", "Trọng", "Quang", "Hồng", "Nhân", "Sơn", "Hải",
                "Hoàng", "Duy", "Quốc", "Trung", "Tuấn", "Hưng", "Tiến",
                "Bảo", "Đại", "Ngọc", "Phúc", "Nam"
            ]
        else:
            first_names = [
                "Mai", "Thị", "Như", "Thủy", "Phương", "Quỳnh", "Trang",
                "Ngọc", "Thanh", "Hạnh", "Nga", "Lan", "Thu", "Hoa",
                "Nguyệt", "Nhật", "Hằng", "Thuỳ", "Tâm", "Anh", "Hương",
                "Vân", "Trà", "Dung", "Tú", "Loan", "Ngân", "Ánh"
            ]
            mid_names = [
                "Thị", "Ngọc", "Hồng", "Thu", "Hạnh", "Mai", "Loan",
                "Linh", "Phương", "Quỳnh", "Trang", "Vân", "Hương", "Tú",
                "Ánh", "Diễm", "Yến", "Ly", "Kiều", "Trâm", "Nga", "Thúy",
                "Thủy", "Thảo", "Dung", "Tâm"
            ]

        last_names = [
            "Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan",
            "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương",
            "Lý", "Đào", "Mai", "Tạ", "Trương", "Đinh", "Phùng", "Lâm",
            "Tô", "Tăng", "Bành", "Đoàn", "Ân", "Thái"
        ]

        last_name = random.choice(last_names)
        mid_name = random.choice(mid_names)
        first_name = random.choice(first_names)

        return f"{last_name} {mid_name} {first_name}"

    @staticmethod
    def generate_mock_names(num_images: int) -> Generator[str, None, None]:
        """
        Generate mock image names.

        Args:
            num_images: Number of names to generate.

        Yields:
            Generated image names in format: name_ID_position_number.format
        """
        positions = ['E', 'SE', 'TL', 'PM', 'SM', 'ASM', 'SME', 'A', 'SA', 'D', 'SD', 'VP']
        formats = ['png', 'jpg', 'bmp', 'jpeg']
        prefixes = ['', 'T', 'B']

        for _ in range(num_images):
            name = MockDataGenerator.get_vietnamese_name(random.choice([True, False]))
            emp_id = random.choice(prefixes) + ''.join(str(random.randint(0, 9)) for _ in range(6))
            position = random.choice(positions)
            number = random.randint(1, 3)
            ext = random.choice(formats)

            yield f"{name}_{emp_id}_{position}_{number}.{ext}"

    def create_mock_images(self, num_images: int) -> None:
        """
        Create mock image files.

        Args:
            num_images: Number of mock images to create.
        """
        mock_folder = self.folder_path / 'mock_images'
        mock_folder.mkdir(parents=True, exist_ok=True)

        for image_name in self.generate_mock_names(num_images):
            file_path = mock_folder / image_name
            file_path.write_text("Mock image content.\n")
            self.logger.info(f"Created: {image_name}")


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description='Generate mock image names and test data.'
    )
    parser.add_argument(
        '-f', '--folder-path',
        type=str,
        default="./",
        help='Path to folder for mock data'
    )
    parser.add_argument(
        '-l', '--log-file',
        type=str,
        default="./log.log",
        help='Path to log file'
    )
    parser.add_argument(
        '-n', '--num-images',
        type=int,
        default=10,
        help='Number of mock images to generate'
    )
    parser.add_argument(
        '-c', '--cleanup',
        action='store_true',
        default=True,
        help='Cleanup mock_images folder before generating'
    )

    return parser.parse_args()


def main() -> None:
    """Main execution function."""
    args = parse_arguments()
    
    generator = MockDataGenerator(args.folder_path, args.log_file)
    
    num_images = max(0, args.num_images)
    
    if args.cleanup:
        generator.cleanup_folder()
    
    generator.create_mock_images(num_images)
    print(f"✓ Generated {num_images} mock images")


if __name__ == "__main__":
    main()
    """Execute the script to generate mock data."""
    args = parse_arguments()
    verifier = ImageNameVerifier(args)
    verifier.cleanup = args.cleanup

    num_images = args.num_images
    if num_images < 0:
        num_images = 0

    if args.cleanup:
        verifier.cleanup_folder()
    verifier.create_mock_images(num_images)


if __name__ == "__main__":
    main()
