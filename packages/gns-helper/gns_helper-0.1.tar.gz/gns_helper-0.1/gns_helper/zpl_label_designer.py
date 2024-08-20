from datetime import date
from flask import request, jsonify
from PIL import Image
import shutil
import subprocess
import os
from .table_operations import (
    DBTableOperations
)
from .config import logger
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ZPLLabelDesigner:
    def __init__(self, dir_path, printer_name):
        self.dir_path = dir_path
        self.printer_name = printer_name

    def generate_zpl(self):
        logger.info("generate zpl called")
        data = request.get_json()
        logger.info("Received data for ZPL generation: %s", data)

        start = "^XA"
        end = "^XZ"
        label_pos = "^FT"
        label_text_tag = "^FD"
        change_font = "^CFA,30"
        start_of_field = "^FO"
        end_of_field = "^FS"

        input_labels = data['input_labels']
        text_values_co_ords = data['text_values_co_ords']
        input_qr_code = data['input_qr_code']
        input_barcode = data['input_barcode']
        barcode_cords = data['barcode_cords']
        qr_code_cords = data['qr_code_cords']
        line_co_ordinates = data['line_co_ordinates']
        rect_co_ordinates = data['rect_co_ordinates']
        font_size = data['font_size']
        font_weight = data['fontweight_array']
        image_data = data['image_data']

        code = [start]

        font_style = ['^CF0' if weight == 'bold' else '^AN' for weight in font_weight]
        for num, label in enumerate(input_labels):
            text_cords = text_values_co_ords[num]
            total_var = f"{font_style[num]},{font_size[num]}{start_of_field}{text_cords['x1']},{text_cords['y1']}{label_text_tag}{label}{end_of_field}"
            code.append(total_var)

        for line in line_co_ordinates:
            if line:
                if 0 < line['angle'] < 175 or 263 < line['angle'] < 280:
                    line_cmd = f"^FO{line['x1']},{line['y1']}^GB1,{line['x2']}^FS"
                else:
                    line_cmd = f"^FO{line['x1']},{line['y1']}^GB{line['x2']},1^FS"
                code.append(line_cmd)

        for rect in rect_co_ordinates:
            if rect:
                rect_cmd = f"^FO{rect['x1']},{rect['y1']}^GB{rect['x2']},{rect['y2']}^FS"
                code.append(rect_cmd)

        if input_barcode and barcode_cords:
            barcode_cmd = f"^FO{barcode_cords[0]['x1']},{barcode_cords[0]['y1']}^BY3^BCN,{barcode_cords[0]['width']},N,N,N^FD{input_barcode}^FS"
            code.append(barcode_cmd)
        elif input_qr_code and qr_code_cords:
            qr_code_cmd = f"^FO{qr_code_cords[0]['x1']},{qr_code_cords[0]['y1']}^BQN,2,3^FD00{input_qr_code}^FS"
            code.append(qr_code_cmd)

        if data.get('logo_flag'):
            image = Image.open(data['file_path'])
            width, height = 200, 200
            image = image.resize((width, height), Image.ANTIALIAS).convert('L').point(lambda x: 0 if x >= 128 else 1, '1')

            zpl_command = f"^FO{image_data[0]['x1']},{image_data[0]['y1']}^GFA,{width},{height * 25},{width // 8},"
            for y in range(height):
                for x in range(width // 8):
                    byte = 0
                    for i in range(8):
                        pixel = image.getpixel((x * 8 + i, y))
                        byte |= (pixel & 1) << (7 - i)
                    zpl_command += f"{byte:02X}"
            zpl_command += "^FS"
            code.append(zpl_command)

        code.append(end)
        result_string = ','.join(code)
        logger.info("Generated ZPL command: %s", result_string)

        label1_path = os.path.join(self.dir_path, "label1.zpl")
        with open(label1_path, "w") as f:
            f.write(result_string)

        return jsonify({"success": True})

    def print_thermal_label(self):
        replacement_dict = request.get_json()

        label1_path = os.path.join(self.dir_path, "label1.zpl")
        label_path = os.path.join(self.dir_path, "label.zpl")

        try:
            shutil.copy(label1_path, label_path)
            logger.info(f"File copied successfully from {label1_path} to {label_path}")
        except Exception as e:
            logger.error(f"An error occurred: {e}")

        operation = DBTableOperations()
        query = "SELECT name FROM LabelVars"
        response = operation.fetch(query)
        search_list = [row['name'] for row in response]

        self.replace_items_in_file(label_path, search_list, replacement_dict)

        subprocess.call(["lp", "-d", self.printer_name, "-o", "raw", label_path])

        return jsonify({"success": True, "message": "success"})

    @staticmethod
    def replace_items_in_file(file_path, search_list, replacement_dict):
        with open(file_path, 'r') as file:
            content = file.read()

        for item in search_list:
            if item in replacement_dict:
                content = content.replace(item, replacement_dict[item])

        with open(file_path, 'w') as file:
            file.write(content)