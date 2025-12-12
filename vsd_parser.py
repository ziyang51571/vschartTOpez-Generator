import struct
import json
from pathlib import Path
from typing import List, Dict, Any


class VSDParser:

    FIELD_ID_MAP = {
        1: "name", 2: "formatted_name", 3: "artist", 4: "chart_id",
        5: "bpm_display", 6: "version", 7: "has_encore", 8: "is_original",
        9: "jacket_artist", 10: "is_published", 11: "genre",
        12: "unlock_id", 13: "preview_start_time", 14: "preview_end_time",
    }

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.buf = None
        self.position = 0
        self.unknown_field_ids = set()
        self.difficulties = []  # [(display, constant, designer)]

    def read_bytes(self, n: int) -> bytes:
        data = self.buf.read(n)
        if len(data) < n:
            raise EOFError(f"位置 {self.position} 需要 {n} 字节")
        self.position += n
        return data

    def read_u8(self) -> int:
        return self.read_bytes(1)[0]

    def read_u32_le(self) -> int:
        return struct.unpack("<I", self.read_bytes(4))[0]

    def read_f32_le(self) -> float:
        return struct.unpack("<f", self.read_bytes(4))[0]

    def read_null_terminated_string(self) -> str:
        result = bytearray()
        while True:
            byte = self.read_bytes(1)
            if byte[0] == 0:
                break
            result.extend(byte)
        return result.decode('utf-8', errors='replace')

    def parse_record(self) -> Dict[str, Any]:
        # 单条记录
        marker = self.read_bytes(3)
        if marker != b'\xA0\xA2\xB2':
            raise ValueError(f"无效标记: {marker.hex()}")

        record_id = self.read_u32_le()
        record = {"_record_id": record_id, "song_id": record_id}
        self.difficulties.clear()

        while True:
            peek = self.buf.read(1)
            if not peek:
                break
            self.buf.seek(-1, 1)

            if peek[0] == 0xA1:
                self.read_bytes(1)
                break

            # 类型标记
            type_byte = self.read_u8()

            if type_byte == 0xC0:
                # C0 [显示名:字符串]00 [常数:4字节浮点] [谱师:字符串]00
                display_name = self.read_null_terminated_string()
                constant = round(self.read_f32_le(), 1)
                designer = self.read_null_terminated_string()
                self.difficulties.append((display_name, constant, designer))

            elif type_byte == 0xA2:
                # A2 [子类型:1字节] [字段ID:1字节] [字符串/布尔]
                sub_type = self.read_u8()
                field_id = self.read_u8()
                field_name = self.FIELD_ID_MAP.get(field_id)

                if sub_type == 0xB8:  # string
                    value = self.read_null_terminated_string()
                    if field_name:
                        record[field_name] = value
                    else:
                        self.unknown_field_ids.add(field_id)
                        record[f"unknown_{field_id}"] = value

                elif sub_type == 0xB7:  # bool
                    value = self.read_u8()
                    if field_name:
                        record[field_name] = bool(value)
                    else:
                        record[f"unknown_bool_{field_id}"] = bool(value)

                else:
                    self.read_null_terminated_string()

            else:
                self.read_null_terminated_string()

        for i, (display, constant, designer) in enumerate(self.difficulties, 1):
            record[f"difficulty_display_{i}"] = display
            record[f"difficulty_constant_{i}"] = constant
            record[f"note_designer_{i}"] = designer

        return record

    def parse_file(self) -> List[Dict[str, Any]]:
        with open(self.filepath, "rb") as f:
            self.buf = f

            header = self.read_bytes(5)
            if header[:3] != b"VSD" or header[3] != 1:
                raise ValueError("无效VSD文件头")

            print(f"VSD文件头: VSD v1.{header[4]}")

            records = []
            while True:
                pos = self.buf.tell()
                peek = self.buf.read(1)
                if not peek or peek[0] != 0xA0:
                    break
                self.buf.seek(pos)

                try:
                    record = self.parse_record()
                    records.append(record)
                except Exception as e:
                    print(f"解析失败 (位置: {pos}): {e}")
                    break

            return records


def process_song_information(
        input_file: str = "song_information.bin",
):
    input_path = Path(input_file)
    output_path = Path() / "song_information.json"

    if not input_path.exists():
        print(f"错误: 文件不存在 {input_file}")
        return

    print(f"正在解析: {input_path}")
    print(f"文件大小: {input_path.stat().st_size} 字节")

    try:
        parser = VSDParser(input_path)
        songs = parser.parse_file()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(songs, f, indent=2, ensure_ascii=False)

        print(f"\n>◹ < 解析成功!")
        print(f"  - 歌曲数量: {len(songs)}")
        print(f"  - 输出文件: {output_path}")

        if parser.unknown_field_ids:
            print(f"\n未知字段ID: {sorted(parser.unknown_field_ids)}")

        return songs

    except Exception as e:
        print(f"\n> ╮< 解析失败: {e}")
        import traceback
        traceback.print_exc()
        return []


if __name__ == "__main__":
    process_song_information()