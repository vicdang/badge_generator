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

    def __init__(self, folder_path, log_file):
        """Initialize ImageNameVerifier instance.

        :param folder_path: Path to the folder for mock data.
        :type folder_path: str
        :param log_file: Path to the log file.
        :type log_file: str
        """
        self.folder_path = folder_path
        self.log_file = log_file
        self.logger = self.setup_logger()

    def setup_logger(self):
        """Set up logger for ImageNameVerifier.

        :return: Logger instance
        :rtype: logging.Logger
        """
        logger = logging.getLogger('image_name_verification')
        logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        return logger
    
    def cleanup_folder(self):
        """Clean up mock images folder."""
        mock_folder = os.path.join(self.folder_path, 'mock_images')
        if os.path.exists(mock_folder):
            for filename in os.listdir(mock_folder):
                file_path = os.path.join(mock_folder, filename)
                os.remove(file_path)

    def generate_mock_data(self, num_images):
        """Generate mock data for image names.

        :param num_images: Number of mock images to generate.
        :type num_images: int
        """
        # Sample data for mock generation
        first_name = ['Huy', 'Linh', 'Minh', 'An', 'Tú', 'Phương', 'Nam', 'Hạnh', 'Dũng', 'Thảo', 'Quân', 'Hoàng', 'Thị', 'Hồng', 'Tuấn', 'Lan', 'Thắng', 'Thu', 'Đức', 'Mai', 'Cường', 'Thành', 'Ngọc', 'Vân', 'Sơn', 'Nguyệt', 'Hải', 'Trang', 'Phúc', 'Lệ', 'Đạt', 'Thuận', 'Thơ', 'Tâm', 'Hoa', 'Đông', 'Tùng', 'Hằng', 'Quang', 'Trâm', 'Danh', 'Linh', 'Nhân', 'Bình', 'Thư', 'Tân', 'Yến', 'Dương', 'Việt', 'Thảnh', 'Giang', 'Tâm', 'Thùy', 'Thắm', 'Hùng', 'Diễm', 'Thơm', 'Tín', 'Như', 'Đan', 'Phong', 'Thịnh', 'Nhật', 'Hạ', 'Thanh', 'Thảo', 'Phú', 'Hiền', 'Nhàn', 'Tâm', 'Khoa', 'Quỳnh', 'Lâm', 'Nguyên', 'Hà', 'Hải', 'Thủy', 'Tân', 'Cát', 'Chí', 'Trúc', 'Vinh', 'Phương', 'Nga', 'Ninh', 'Châu', 'Hiệp', 'Thuý', 'Lan', 'Khánh', 'Tuấn', 'Thanh', 'Thảo', 'Hương', 'Nga', 'Nhị', 'Thắm', 'Lợi', 'Bảo', 'Phương', 'Châu', 'Tài', 'Lễ', 'Lý', 'Ngọc', 'Thanh', 'Trúc', 'Tâm', 'Đức', 'Phượng', 'Thanh', 'Hà', 'Thư', 'Thi', 'Khuê', 'Hiếu', 'Thiện', 'Trúc', 'Nhi', 'Duy', 'Trinh', 'Nguyên', 'Vinh', 'Nhật', 'Thiện', 'Tài', 'Lợi', 'Huyền', 'Nga', 'Tùng', 'Hà', 'Văn', 'Hương', 'Nhiên', 'Nhật', 'Tín', 'Ngọc', 'Trang', 'Nhân', 'Dương', 'Thu', 'Thanh', 'Tú', 'Thịnh', 'Nhã', 'Anh', 'Định', 'Nhật', 'Thịnh', 'Thắng', 'Thành', 'Đức', 'Tín', 'Bảo', 'Đạt', 'Hoa', 'Vân', 'An', 'Tuấn', 'Trường', 'Nga', 'Hạnh', 'Thi', 'Hiền', 'Tâm', 'Thúy', 'Nhân', 'Tùng', 'Ngọc', 'Tú', 'Thiện', 'Hoài', 'Châu', 'Quỳnh', 'Quốc', 'Trúc', 'Thanh', 'Hồng', 'Nga', 'Vân', 'Nhật', 'Hải', 'Nhi', 'Nhã', 'Trúc', 'Bích', 'Thu', 'Thảo', 'Bình', 'Hà', 'Quân', 'Dung', 'Nhàn', 'Dũng', 'Nhật', 'Tâm', 'Đình', 'Thiện', 'Huyền', 'Hiếu', 'Hồng', 'Thắm', 'Hương', 'Trang', 'Hạnh', 'Ninh', 'Hoa', 'Hậu', 'Trang', 'Thảo', 'Nhã', 'Hà', 'Minh', 'Quang', 'Nhật', 'Trúc', 'Thanh', 'Hoài', 'Vân', 'Hiền', 'Thị', 'Nga', 'Thắng', 'Tuấn', 'Thi', 'Anh', 'Hạnh', 'Thảo', 'An', 'Thu', 'Tâm', 'Hiếu', 'Nhật', 'Phương', 'Thuận', 'Hương', 'Thiện', 'Nhã', 'Nhi', 'Trúc', 'Đức', 'Nhật', 'Vinh', 'Lan', 'Thành', 'Nhiên', 'Thúy', 'Như', 'Đức', 'Nhân', 'Huyền', 'Vân', 'Phúc', 'Hải', 'Ngọc', 'Như', 'Hoa', 'Nhật', 'Trúc', 'Nhi', 'Thi', 'Hiền', 'Dung', 'Thiện', 'Hạnh', 'Nhi', 'Linh', 'Hiếu', 'Thảo', 'Hồng', 'Nhật', 'Thúy', 'Thi', 'Đình', 'Hoài', 'Hiếu', 'Nhật', 'Thi', 'Vân', 'Thắm', 'Nhật', 'Vân', 'Đức', 'Anh', 'Phúc', 'Nhật', 'Hạnh', 'Minh', 'Vân', 'Duy', 'Thành', 'Vinh', 'Hiếu', 'Thảo', 'Quang', 'Hà', 'An', 'Hạnh', 'Bình', 'Hồng', 'Đức', 'Linh', 'Lam', 'Thi', 'Thắm', 'Duy', 'Tâm', 'Đình', 'Như', 'Hạnh', 'Thi', 'Hương', 'Nhi', 'Đức', 'Huyền', 'Nhi', 'Trang', 'Minh', 'Tâm', 'Đức', 'Thiện', 'Vân', 'Phương', 'Nga', 'Thiện', 'Hiếu', 'Tâm', 'Thủy', 'Đức', 'Hải', 'Nhật', 'Hiếu', 'Như', 'Trang', 'Hiếu', 'Tâm', 'Nhi', 'Như', 'Hải', 'Tùng', 'Vân', 'An', 'Hương', 'Nhân', 'Đức', 'Hiếu']
        mid_name = ['Thị', 'Văn', 'Như', 'Ngọc', 'Minh', 'Hữu', 'Tuấn', 'Thành', 'Kim', 'Quốc', 'Hồng', 'Đức', 'Công', 'Thái', 'Anh', 'Thế', 'Hải', 'Quang', 'Đình', 'Hạnh', 'Trung', 'Thiện', 'Hoàng', 'Tâm', 'Nhật', 'Thư', 'Vinh', 'Trần', 'Lâm', 'Phương', 'Hoài', 'Lệ', 'Hoa', 'Huy', 'Trí', 'Nga', 'Hương', 'Linh', 'Phúc', 'Duy', 'Tuyết', 'Nhi', 'Sơn', 'Hà', 'Lan', 'Bình', 'Mai', 'Tú', 'Gia', 'Thắng', 'Tùng', 'Phong', 'Thảo', 'Nhàn', 'Dung', 'Nhân', 'Đông', 'Tình', 'Đức', 'Tài', 'Thái', 'Đức', 'Bảo', 'Nguyên', 'Đan', 'Thuận', 'Thành', 'Thắng', 'Bích', 'Thảnh', 'Vinh', 'Phước', 'Cường', 'Việt', 'Thủy', 'Quân', 'Như', 'Hân', 'Lương', 'Khánh', 'Nghĩa', 'Hòa', 'Phát', 'Vân', 'Ninh', 'Thu', 'Phụng', 'Hải', 'Dương', 'Nhã', 'Hoàng', 'Khoa', 'Lan', 'Tài', 'Chí', 'Nguyệt', 'Nhật', 'Tín', 'Tấn', 'Hiếu', 'Thắng', 'Đức', 'Thuỳ', 'Nhung', 'Thịnh', 'Nhãn', 'Hữu', 'Thành', 'Giang', 'Tân', 'Nhung', 'Hà', 'Trang', 'Hải', 'An', 'Trọng', 'Hòa', 'Nhật', 'Lam', 'Hậu', 'Như', 'Nghĩa', 'Hải', 'Đăng', 'Hiệp', 'Thành', 'Nhàn', 'Hà', 'Phong', 'Đông', 'Thùy', 'Thu', 'Hải', 'Như', 'Nghĩa', 'Hiếu', 'Như', 'Hạnh', 'Thanh', 'Hòa', 'Hoàng', 'Nhật', 'Nghĩa', 'Lâm', 'Nhàn', 'Hồng', 'Trung', 'Đan', 'Bảo', 'Thành', 'Hải', 'Thiên', 'Quang', 'Như', 'Hoa', 'Hồng', 'Thu', 'Nghiêm', 'Nhân', 'Phụng', 'Nhãn', 'Hải', 'Hiền', 'Đức', 'Nhã', 'Hà', 'Nhất', 'Quỳnh', 'Đức', 'Lưu', 'Duy', 'Dung', 'Hồng', 'Thi', 'Hải', 'Hân', 'Nhã', 'Hòa', 'Thiện', 'Lưu', 'Hoàng', 'Bảo', 'Hải', 'Chính', 'Hoa', 'Quân', 'Thế', 'Nhi', 'Nhàn', 'Trang', 'Hải', 'Nhật', 'Trọng', 'Như', 'Phúc', 'Thái', 'Hương', 'Vũ', 'Thịnh', 'Hiếu', 'Linh', 'Nhã', 'Hương', 'Nga', 'Hạnh', 'Phong', 'Hải', 'Đức', 'Phước', 'Nhã', 'Thanh', 'Nhật', 'Hà', 'Như', 'Hải', 'Huyền', 'Thi', 'Thanh', 'Trang', 'Như', 'Hạnh', 'Thanh', 'Hương', 'Hoàng', 'Tùng', 'Như', 'Trang', 'Hoa', 'Như', 'Thiện', 'Hải', 'Trang', 'Hải', 'Nhã', 'Tâm', 'Thanh', 'Hương', 'Bảo', 'Phúc', 'Thiện', 'Nhi', 'Đức', 'Nghĩa', 'Nhãn', 'Bích', 'Như', 'Hòa', 'Nhã', 'Nghĩa', 'Hải', 'Thái', 'Như', 'Tân', 'Hồng', 'Nhã', 'Hồng', 'Thu', 'Hà', 'Hiếu', 'Nghĩa', 'Quang', 'Dương', 'Nhật', 'Văn', 'Như', 'Nhẫn', 'Nhật', 'Nhi', 'Nhật', 'Hải', 'Hoàng', 'Như', 'Nghĩa', 'Hòa', 'Hải', 'Hải', 'Như', 'Nhất', 'Nhã', 'Phúc', 'Thanh', 'Hòa', 'Hà', 'Hoa', 'Nghiêm', 'Thịnh', 'Tâm', 'Nhật', 'Tâm', 'Linh', 'Hoàng', 'Nhã', 'Trang', 'Nhật', 'Hồng', 'Hà', 'Hải', 'Hiền', 'Nhi', 'Hà', 'Hiền', 'Nghiêm', 'Huyền', 'Thanh', 'Thịnh', 'Nhật', 'Nghiêm', 'Thanh', 'Trang', 'Như', 'Hạnh', 'Nhã', 'Hoàng', 'Huyền', 'Thịnh', 'Hồng', 'Phúc', 'Nhã', 'Như', 'Hải', 'Nhã', 'Nghiêm', 'Hồng', 'Quang', 'Thành', 'Hoài', 'Nhã', 'Huyền', 'Phương', 'Thái', 'Như', 'Hải', 'Trang', 'Như', 'Nghiêm', 'Thịnh', 'Hồng', 'Hải', 'Nhật', 'Hồng']
        last_name = ['Nguyễn', 'Trần', 'Lê', 'Phạm', 'Hoàng', 'Huỳnh', 'Phan', 'Vũ', 'Võ', 'Đặng', 'Bùi', 'Đỗ', 'Hồ', 'Ngô', 'Dương', 'Lý', 'Trịnh', 'Đinh', 'Phùng', 'Đoàn', 'Bạch', 'Hà', 'Tạ', 'Tô', 'Lương', 'Kiều', 'Mai', 'Tăng', 'Sơn', 'Giang', 'Chu', 'Âu', 'Thái', 'Từ', 'Tiêu', 'Nghiêm', 'Lục', 'Tôn', 'Mạc', 'Lỗ', 'Triệu', 'Điền', 'Nghị', 'Đồng', 'Nữ', 'Thi', 'Lục', 'Cao', 'Viên', 'Chung', 'Đường', 'Tiết', 'Thủy', 'Lưu', 'Tưởng', 'Kha', 'Châu', 'Đoàn', 'Trang', 'Diệp', 'Hứa', 'Trương', 'Doãn', 'Lư', 'Tòng', 'Lục', 'Lâm', 'Lư', 'Kiều', 'Lục', 'Ngưu', 'Chu', 'Quách', 'Phó', 'Vương', 'Dương']
        positions = ['E', 'SE', 'TL', 'PM', 'SM', 'ASM', 'SME', 'A', 'SA', 'D', 'SD', 'VP']
        formats = ['png', 'jpg', 'bmp', 'jpeg']
        prefixes = ['', 'T', 'B']

        # Generate mock image names
        for _ in range(num_images):
            vietnamese_name = ' '.join([random.choice(last_name),
                                       random.choice(mid_name),
                                       random.choice(first_name)])
            ID = random.choice(prefixes) + ''.join([str(random.randint(0, 9)) for _ in range(6)])
            position = random.choice(positions)
            number = random.randint(1, 3)
            image_format = random.choice(formats)

            image_name = f"{vietnamese_name}_{ID}_{position}_{number}.{image_format}"
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
    parser = argparse.ArgumentParser(description='Generate mock data for ImageNameVerifier testing.')
    parser.add_argument('-f', '--folder-path', type=str, default="./", nargs='?', help='Path to the folder to create mock data')
    parser.add_argument('-l', '--log-file', type=str, default="./log.log", nargs='?', help='Path to the log file')
    parser.add_argument('-n', '--num-images', type=int, default=10, nargs='?', help='Number of mock images to generate')
    parser.add_argument('-c', '--cleanup', action='store_false', default=True, help='Do not cleanup the "mock_images" folder before generating new data')
    return parser.parse_args()

def main():
    """Execute the script to generate mock data."""
    args = parse_arguments()
    verifier = ImageNameVerifier(args.folder_path, args.log_file)
    verifier.cleanup = args.cleanup

    num_images = args.num_images
    if num_images < 0:
        num_images = 0

    verifier.create_mock_images(num_images)

if __name__ == "__main__":
    main()
