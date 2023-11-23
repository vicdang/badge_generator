# -*- coding: utf-8 -*-
# vim:ts=3:sw=3:expandtab
"""
---------------------------
Copyright (C) 2021
@Authors: Vic Dang
@Skype: traxanh_dl
@Date: 16-Dec-21
@Version: 1.0
---------------------------
 Usage example:
   +  python mock_data_generator.py -f ./ -l log.log -n 5 -c
"""

import os
import random
import argparse
import logging


class ImageNameVerifier:
    """Class to verify and generate mock data for image names."""

    def __init__(self, args):
        """Initialize ImageNameVerifier instance.

        :param folder_path: Path to the folder for mock data.
        :type folder_path: str
        :param log_file: Path to the log file.
        :type log_file: str
        """
        self.folder_path = args.folder_path
        self.log_file = args.log_file
        self.logger = self.setup_logger()

    def setup_logger(self):
        """
        Sets up logging configuration.

        Returns
        -------
        logging.Logger
            Configured logger instance.
        """
        logger = logging.getLogger('image_name_verification')
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')

        # File handler
        file_handler = logging.FileHandler(
            self.log_file, encoding='utf-8')  # Specify encoding
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Stream handler for terminal logging
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        return logger

    def cleanup_folder(self):
        """Clean up mock images folder."""
        mock_folder = os.path.join(self.folder_path, 'mock_images')
        self.logger.info(f"Mock folder: {mock_folder}")
        if os.path.exists(mock_folder):
            for filename in os.listdir(mock_folder):
                file_path = os.path.join(mock_folder, filename)
                self.logger.info(f"Removed file: {filename}")
                os.remove(file_path)

    def get_fullname(self, gender=True):
        if gender:
            first_name = ["Hồng", "Đức", "Quốc", "Hoàng", "Hải", "Công", "Minh", "Thành", "Thuận", "Đông", "Tuấn", "Nhân", "Trung", "Sơn",
                           "Duy", "Hùng", "Long", "Tiến", "Vũ", "Bình", "Loan", "Huy", "Phúc", "Đạt", "Trọng", "Gia", "Linh", "An", "Vinh", "Đại", "Khánh"]
            mid_name = ["Văn", "Hữu", "Đức", "Minh", "Thành", "Nhật", "Đình", "An", "Gia", "Trọng", "Quang", "Hồng", "Nhân",
                         "Sơn", "Hải", "Hoàng", "Duy", "Quốc", "Trung", "Tuấn", "Nhật", "Hưng", "Tiến", "Bảo", "Đại", "Ngọc", "Phúc", "Nam"]
        else:
            first_name = ["Mai", "Thị", "Như", "Thủy", "Phương", "Quỳnh", "Trang", "Ngọc", "Thanh", "Hạnh", "Nga", "Lan",
                             "Thu", "Hoa", "Nguyệt", "Nhật", "Hằng", "Thuỳ", "Tâm", "Anh", "Hương", "Vân", "Trà", "Dung", "Tú", "Loan", "Ngân", "Ánh"]
            mid_name = ["Thị", "Ngọc", "Hồng", "Thu", "Hạnh", "Mai", "Loan", "Linh", "Phương", "Quỳnh", "Trang",
                           "Vân", "Hương", "Tú", "Ánh", "Diễm", "Yến", "Ly", "Kiều", "Trâm", "Nga", "Thúy", "Thủy", "Thảo", "Dung", "Tâm"]
        last_name = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý", "Đào", "Mai", "Tạ", "Trương", "Đinh", "Phùng", "Lâm", "Tô", "Tăng", "Bành",
                     "Đoàn", "Ân", "Thái", "Thiều", "Hoa", "Tôn", "Nghiêm", "Quách", "Đổng", "Lục", "Bạch", "Ninh", "Du", "Sử", "Phi", "La", "Viên", "Vương", "Khuất", "Lương", "Đoàn", "Từ", "Tiêu", "Tiết", "Thi", "Đồng", "Chu", "Từ"]
        return ' '.join([random.choice(last_name), ' '.join([(random.choice(mid_name)) for _ in range(random.randint(1, 2))]),
                    random.choice(first_name)])

    def generate_mock_data(self, num_images):
        """Generate mock data for image names.

        :param num_images: Number of mock images to generate.
        :type num_images: int
        """
        # Sample data for mock generation
        positions = ['E', 'SE', 'TL', 'PM', 'SM',
                     'ASM', 'SME', 'A', 'SA', 'D', 'SD', 'VP']
        formats = ['png', 'jpg', 'bmp', 'jpeg']
        prefixes = ['', 'T', 'B']

        # Generate mock image names
        for _ in range(num_images):
            vietnamese_name = self.get_fullname(random.choice([True, False]))
            ID = random.choice(
                prefixes) + ''.join([str(random.randint(0, 9)) for _ in range(6)])
            position = random.choice(positions)
            number = random.randint(1, 3)
            image_format = random.choice(formats)

            image_name = f"{vietnamese_name}_{ID}_{position}_{number}.{image_format}"
            self.logger.info(f"Image: {image_name}")
            yield image_name

    def create_mock_images(self, num_images):
        """Create mock images based on generated mock data.

        :param num_images: Number of mock images to generate.
        :type num_images: int
        """
        mock_folder = os.path.join(self.folder_path, 'mock_images')
        os.makedirs(mock_folder, exist_ok=True)

        for idx, image_name in enumerate(self.generate_mock_data(num_images), start=1):
            with open(os.path.join(mock_folder, f"{image_name}"), 'w') as file:
                file.write("Mock image content.")


def parse_arguments():
    """Parse command line arguments using argparse.

    :return: Parsed arguments.
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(
        description='Generate mock data for ImageNameVerifier testing.')
    parser.add_argument('-f', '--folder-path', type=str, default="./",
                        nargs='?', help='Path to the folder to create mock data')
    parser.add_argument('-l', '--log-file', type=str,
                        default="./log.log", nargs='?', help='Path to the log file')
    parser.add_argument('-n', '--num-images', type=int, default=10,
                        nargs='?', help='Number of mock images to generate')
    parser.add_argument('-c', '--cleanup', action='store_true', default=True,
                        help='Do not cleanup the "mock_images" folder before generating new data')
    return parser.parse_args()


def main():
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
