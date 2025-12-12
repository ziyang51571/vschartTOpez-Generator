import os
import struct
import json

MAGIC = [0x56, 0x53, 0x43, 0x01, 0x00]

class VSBRawConverter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.offset = 0
        self.notes = []
        with open(file_path, 'rb') as f:
            self.buffer = f.read()

    def u8(self):
        val = self.buffer[self.offset]
        self.offset += 1
        return val

    def read_float(self):
        val = struct.unpack('<f', self.buffer[self.offset:self.offset + 4])[0]
        self.offset += 4
        return val

    def read_int32(self):
        val = struct.unpack('<i', self.buffer[self.offset:self.offset + 4])[0]
        self.offset += 4
        return val

    def verify(self, expected, msg):
        got = self.u8()
        if got != expected:
            raise ValueError(f'Mismatched {msg}: got 0x{got:02x}, expected 0x{expected:02x}')

    def read_note(self):
        note = {'type': 0, 'lane': 0, 'time': 0.0, 'extra': {}}

        while True:
            flag = self.u8()
            if flag == 0xA1:
                break
            if flag == 0xA2:
                note['type'] = self.u8()
            elif flag == 0xA3:
                note['lane'] = self.u8()
            elif flag == 0xA4:
                note['time'] = self.read_float()
            elif flag == 0xA6:
                extra = {}
                while True:
                    t = self.u8()
                    if t == 0xA7:
                        break
                    id_ = self.u8()
                    if note['type'] == 2:
                        # 这太诡谲了，，
                        extra[id_] = self.read_int32()
                    else:
                        extra[id_] = self.read_float()
                note['extra'] = extra
            else:
                raise ValueError(f'Unknown flag in note: 0x{flag:02x}')

        self.notes.append(note)

    def read(self):
        # 验证文件头魔数
        for i, magic_byte in enumerate(MAGIC):
            self.verify(magic_byte, f'file magic[{i}]')

        self.verify(0xC0, 'notes section start')

        while True:
            flag = self.u8()
            if flag == 0xC1:
                break
            if flag == 0xA0:
                self.read_note()
            else:
                raise ValueError(f'Unknown flag in notes section: 0x{flag:02x}')

        if self.u8() not in (0xFF, 0xE0):
            raise ValueError('Unexpected end-of-chart marker')

    @staticmethod
    def convert_all_vsb_files():
        current_dir = os.path.dirname(os.path.abspath(__file__))

        input_dir = os.path.join(current_dir, 'Charts')
        output_dir = os.path.join(current_dir, 'vsbjson')

        if not os.path.isdir(input_dir):
            print(f"错误：找不到输入文件夹 '{input_dir}'")
            return

        os.makedirs(output_dir, exist_ok=True)

        target_files = ['OPENING.vsb', 'MIDDLE.vsb', 'FINALE.vsb', 'ENCORE.vsb']

        total_converted = 0
        total_errors = 0
        total_notes = 0

        print(f"开始扫描 '{input_dir}' 中的谱面文件...\n")

        for root, dirs, files in os.walk(input_dir):
            rel_path = os.path.relpath(root, input_dir)

            if rel_path == '.':
                continue

            found_files = [f for f in target_files if f in files]
            if not found_files:
                continue

            output_subdir = os.path.join(output_dir, rel_path)
            os.makedirs(output_subdir, exist_ok=True)

            print(f"处理曲目 '{rel_path}':")

            for target_file in found_files:
                input_path = os.path.join(root, target_file)
                output_filename = os.path.splitext(target_file)[0] + '.json'
                output_path = os.path.join(output_subdir, output_filename)

                try:
                    converter = VSBRawConverter(input_path)
                    converter.read()

                    with open(output_path, 'w', encoding='utf-8') as f:
                        json.dump(converter.notes, f, indent=2, ensure_ascii=False)

                    print(f"  ✓ {target_file} -> {output_filename} ({len(converter.notes)} 个音符)")
                    total_converted += 1
                    total_notes += len(converter.notes)

                except Exception as e:
                    print(f"  ✗ {target_file} 转换失败: {str(e)}")
                    total_errors += 1

            print()

        print("=" * 50)
        print(f">◹ < 转换完成:")
        print(f"  成功: {total_converted} 个文件")
        print(f"  失败: {total_errors} 个文件")
        print(f"  总计解析 {total_notes} 个音符")

        if total_errors > 0:
            print(f"\n警告: {total_errors} 个文件转换失败，请检查错误信息")


if __name__ == '__main__':
    VSBRawConverter.convert_all_vsb_files()