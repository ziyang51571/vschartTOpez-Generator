import json
import re
import os
import shutil
import zipfile
from fractions import Fraction
from datetime import datetime
from mutagen.oggvorbis import OggVorbis
from mutagen.wave import WAVE
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VSB_JSON_DIR = os.path.join(BASE_DIR, "vsbjson")
AUDIO_DIR = os.path.join(BASE_DIR, "audiogroup_default")
SPRITE_DIR = os.path.join(BASE_DIR, "Sprites")
OUTPUT_DIR = os.path.join(BASE_DIR, "pezOutput")
SONG_INFO_PATH = os.path.join(BASE_DIR, "song_information.json")
BLACK_PNG_PATH = os.path.join(BASE_DIR, "black.png")

DIFFICULTY_MAP = {
    "OPENING.json": {"abbr": "OP", "level": 1},
    "MIDDLE.json": {"abbr": "MD", "level": 2},
    "FINALE.json": {"abbr": "FN", "level": 3},
    "ENCORE.json": {"abbr": "EC", "level": 4},
}

TMPL = r'''{
   "BPMList" : [
      {
         "bpm" : 60.0,
         "startTime" : [ 0, 0, 1 ]
      }
   ],
   "META" : {
      "RPEVersion" : 170,
      "background" : "black.png",
      "charter" : "vsb2pez",
      "composer" : "vsb2pez",
      "duration" : 392.90701293945312,
      "id" : "6708198698448521",
      "illustration" : "",
      "level" : "0",
      "name" : "vsb2pez",
      "offset" : -1028,
      "song" : "6708198698448521.ogg"
   },
   "chartTime" : 439081.0,
   "judgeLineGroup" : [ "Default" ],
   "judgeLineList" : [
      {
         "Group" : 0,
         "Name" : "Untitled",
         "Texture" : "line.png",
         "alphaControl" : [
            {
               "alpha" : 1.0,
               "easing" : 1,
               "x" : 0.0
            },
            {
               "alpha" : 1.0,
               "easing" : 1,
               "x" : 9999999.0
            }
         ],
         "anchor" : [ 0.5, 0.5 ],
         "bpmfactor" : 1.0,
         "eventLayers" : [
            {
               "alphaEvents" : [
                  {
                     "bezier" : 255,
                     "bezierPoints" : [ 0.0, 0.0, 0.0, 0.0 ],
                     "easingLeft" : 0.0,
                     "easingRight" : 1.0,
                     "easingType" : 1,
                     "end" : 255,
                     "endTime" : [ 1, 0, 1 ],
                     "linkgroup" : 0,
                     "start" : 0,
                     "startTime" : [ 0, 0, 1 ]
                  }
               ],
               "moveXEvents" : [
                  {
                     "bezier" : 0,
                     "bezierPoints" : [ 0.0, 0.0, 0.0, 0.0 ],
                     "easingLeft" : 0.0,
                     "easingRight" : 1.0,
                     "easingType" : 1,
                     "end" : 0.0,
                     "endTime" : [ 1, 0, 1 ],
                     "linkgroup" : 0,
                     "start" : 0.0,
                     "startTime" : [ 0, 0, 1 ]
                  }
               ],
               "moveYEvents" : [
                  {
                     "bezier" : 0,
                     "bezierPoints" : [ 0.0, 0.0, 0.0, 0.0 ],
                     "easingLeft" : 0.0,
                     "easingRight" : 1.0,
                     "easingType" : 1,
                     "end" : -300.0,
                     "endTime" : [ 1, 0, 1 ],
                     "linkgroup" : 0,
                     "start" : -300.0,
                     "startTime" : [ 0, 0, 1 ]
                  }
               ],
               "rotateEvents" : [
                  {
                     "bezier" : 0,
                     "bezierPoints" : [ 0.0, 0.0, 0.0, 0.0 ],
                     "easingLeft" : 0.0,
                     "easingRight" : 1.0,
                     "easingType" : 1,
                     "end" : 0.0,
                     "endTime" : [ 1, 0, 1 ],
                     "linkgroup" : 0,
                     "start" : 0.0,
                     "startTime" : [ 0, 0, 1 ]
                  }
               ],
               "speedEvents" : [
                  {
                     "easingLeft" : 0.0,
                     "easingRight" : 1.0,
                     "easingType" : 1,
                     "end" : 12,
                     "endTime" : [ 1, 0, 1 ],
                     "linkgroup" : 0,
                     "start" : 0,
                     "startTime" : [ 0, 0, 1 ]
                  }
               ]
            },
            {
               "alphaEvents" : [
                  {
                     "bezier" : 0,
                     "bezierPoints" : [ 0.0, 0.0, 0.0, 0.0 ],
                     "easingLeft" : 0.0,
                     "easingRight" : 1.0,
                     "easingType" : 1,
                     "end" : 0,
                     "endTime" : [ 1, 0, 1 ],
                     "linkgroup" : 0,
                     "start" : 0,
                     "startTime" : [ 0, 0, 1 ]
                  }
               ],
               "moveXEvents" : [
                  {
                     "bezier" : 0,
                     "bezierPoints" : [ 0.0, 0.0, 0.0, 0.0 ],
                     "easingLeft" : 0.0,
                     "easingRight" : 1.0,
                     "easingType" : 1,
                     "end" : 0.0,
                     "endTime" : [ 1, 0, 1 ],
                     "linkgroup" : 0,
                     "start" : 0.0,
                     "startTime" : [ 0, 0, 1 ]
                  }
               ],
               "moveYEvents" : [
                  {
                     "bezier" : 0,
                     "bezierPoints" : [ 0.0, 0.0, 0.0, 0.0 ],
                     "easingLeft" : 0.0,
                     "easingRight" : 1.0,
                     "easingType" : 1,
                     "end" : 0.0,
                     "endTime" : [ 1, 0, 1 ],
                     "linkgroup" : 0,
                     "start" : 0.0,
                     "startTime" : [ 0, 0, 1 ]
                  }
               ],
               "rotateEvents" : [
                  {
                     "bezier" : 0,
                     "bezierPoints" : [ 0.0, 0.0, 0.0, 0.0 ],
                     "easingLeft" : 0.0,
                     "easingRight" : 1.0,
                     "easingType" : 1,
                     "end" : 0.0,
                     "endTime" : [ 1, 0, 1 ],
                     "linkgroup" : 0,
                     "start" : 0.0,
                     "startTime" : [ 0, 0, 1 ]
                  }
               ]
            },
            {
               "alphaEvents" : [
                  {
                     "bezier" : 0,
                     "bezierPoints" : [ 0.0, 0.0, 0.0, 0.0 ],
                     "easingLeft" : 0.0,
                     "easingRight" : 1.0,
                     "easingType" : 1,
                     "end" : 0,
                     "endTime" : [ 1, 0, 1 ],
                     "linkgroup" : 0,
                     "start" : 0,
                     "startTime" : [ 0, 0, 1 ]
                  }
               ],
               "moveXEvents" : [
                  {
                     "bezier" : 0,
                     "bezierPoints" : [ 0.0, 0.0, 0.0, 0.0 ],
                     "easingLeft" : 0.0,
                     "easingRight" : 1.0,
                     "easingType" : 1,
                     "end" : 0.0,
                     "endTime" : [ 1, 0, 1 ],
                     "linkgroup" : 0,
                     "start" : 0.0,
                     "startTime" : [ 0, 0, 1 ]
                  }
               ],
               "moveYEvents" : [
                  {
                     "bezier" : 0,
                     "bezierPoints" : [ 0.0, 0.0, 0.0, 0.0 ],
                     "easingLeft" : 0.0,
                     "easingRight" : 1.0,
                     "easingType" : 1,
                     "end" : 0.0,
                     "endTime" : [ 1, 0, 1 ],
                     "linkgroup" : 0,
                     "start" : 0.0,
                     "startTime" : [ 0, 0, 1 ]
                  }
               ],
               "rotateEvents" : [
                  {
                     "bezier" : 0,
                     "bezierPoints" : [ 0.0, 0.0, 0.0, 0.0 ],
                     "easingLeft" : 0.0,
                     "easingRight" : 1.0,
                     "easingType" : 1,
                     "end" : 0.0,
                     "endTime" : [ 1, 0, 1 ],
                     "linkgroup" : 0,
                     "start" : 0.0,
                     "startTime" : [ 0, 0, 1 ]
                  }
               ]
            }
         ],
         "extended" : {
            "inclineEvents" : [
               {
                  "bezier" : 0,
                  "bezierPoints" : [ 0.0, 0.0, 0.0, 0.0 ],
                  "easingLeft" : 0.0,
                  "easingRight" : 1.0,
                  "easingType" : 0,
                  "end" : 0.0,
                  "endTime" : [ 1, 0, 1 ],
                  "linkgroup" : 0,
                  "start" : 0.0,
                  "startTime" : [ 0, 0, 1 ]
               }
            ]
         },
         "father" : -1,
         "isCover" : 1,
         "isGif" : false,
         "notes" : [],
         "numOfNotes" : 0,
         "posControl" : [
            {
               "easing" : 1,
               "pos" : 1.0,
               "x" : 0.0
            },
            {
               "easing" : 1,
               "pos" : 1.0,
               "x" : 9999999.0
            }
         ],
         "rotateWithFather" : true,
         "sizeControl" : [
            {
               "easing" : 1,
               "size" : 1.0,
               "x" : 0.0
            },
            {
               "easing" : 1,
               "size" : 1.0,
               "x" : 9999999.0
            }
         ],
         "skewControl" : [
            {
               "easing" : 1,
               "skew" : 0.0,
               "x" : 0.0
            },
            {
               "easing" : 1,
               "skew" : 0.0,
               "x" : 9999999.0
            }
         ],
         "yControl" : [
            {
               "easing" : 1,
               "x" : 0.0,
               "y" : 1.0
            },
            {
               "easing" : 1,
               "x" : 9999999.0,
               "y" : 1.0
            }
         ],
         "zOrder" : 0
      }
   ],
   "multiLineString" : "0:10",
   "multiScale" : 1.0,
   "xybind" : false
}'''


def load_song_info():
    if not os.path.exists(SONG_INFO_PATH):
        raise FileNotFoundError(f"找不到{SONG_INFO_PATH}")
    with open(SONG_INFO_PATH, 'r', encoding='utf-8') as f:
        song_list = json.load(f)
    return {item["chart_id"]: item for item in song_list}


def get_audio_duration(chart_id):
    cache_key = f"duration_{chart_id}"
    if not hasattr(get_audio_duration, "_cache"):
        get_audio_duration._cache = {}
    if cache_key in get_audio_duration._cache:
        return get_audio_duration._cache[cache_key]

    for ext in ['.ogg', '.wav']:
        audio_path = os.path.join(AUDIO_DIR, f"music_chart_{chart_id}{ext}")
        if os.path.exists(audio_path):
            try:
                audio = WAVE(audio_path) if ext == '.wav' else OggVorbis(audio_path)
                duration = audio.info.length
                get_audio_duration._cache[cache_key] = duration
                return duration + 1
            except Exception as e:
                print(f"警告: 读取音频失败 {audio_path}: {e}")

    get_audio_duration._cache[cache_key] = 0.0
    return 1.0


def calculate_id(song_id):
    return str(int(song_id) * 51571)


def get_current_edit_time():
    return datetime.now().strftime("%Y_%m_%d_%H_%M_%S_")


def generate_meta_str(song_info, difficulty, duration, id_str, audio_ext):
    level_num = DIFFICULTY_MAP[difficulty]["level"]
    display_key = f"difficulty_display_{level_num}"
    designer_key = f"note_designer_{level_num}"
    difficulty_display = song_info.get(display_key, "0")
    charter = song_info.get(designer_key, "Unknown")
    jacket_artist = song_info.get("jacket_artist", "") + " (51571 modified)"
    meta_lines = [
        '   "META" : {',
        '      "RPEVersion" : 170,',
        f'      "background" : "{id_str}.png",',
        f'      "charter" : "{charter}",',
        f'      "composer" : "{song_info.get("artist", "Unknown Artist")}",',
        f'      "duration" : {duration:.12f},',
        f'      "id" : "{id_str}",',
        f'      "illustration" : "{jacket_artist}",',
        f'      "level" : "{DIFFICULTY_MAP[difficulty]["abbr"]} Lv.{difficulty_display}",',
        f'      "name" : "{song_info.get("formatted_name", "Unknown Song")}",',
        '      "offset" : -1028,',
        f'      "song" : "{id_str}{audio_ext}"',
        '   },'
    ]
    return '\n'.join(meta_lines)


def generate_info_txt(song_info, difficulty, id_str, duration, audio_ext):
    level_num = DIFFICULTY_MAP[difficulty]["level"]
    designer_key = f"note_designer_{level_num}"
    display_key = f"difficulty_display_{level_num}"
    difficulty_display = song_info.get(display_key, "0")

    return f"""#
Name: {song_info.get("formatted_name", "Unknown Song")}
Path: {id_str}
Song: {id_str}{audio_ext}
Picture: {id_str}.png
Chart: {id_str}.json
Level: {DIFFICULTY_MAP[difficulty]["abbr"]} Lv.{difficulty_display}
Composer: {song_info.get("artist", "Unknown Artist")}
Charter: {song_info.get(designer_key, "Unknown")}
LastEditTime: {get_current_edit_time()}
Length: {duration:.3f}
EditTime: 439081.0
Group: VIVIDSTASISTOPHIGROS
"""


def copy_resource_files(target_dir, chart_id, id_str, audio_ext):
    # 音频
    src_audio = os.path.join(AUDIO_DIR, f"music_chart_{chart_id}{audio_ext}")
    dst_audio = os.path.join(target_dir, f"{id_str}{audio_ext}")
    if not os.path.exists(src_audio):
        raise FileNotFoundError(f"音频文件不存在: {src_audio}")
    shutil.copy2(src_audio, dst_audio)

    # 图
    output_png_path = os.path.join(target_dir, f"{id_str}.png")
    sprite_path = os.path.join(SPRITE_DIR, f"song_{chart_id}_0.png")

    if os.path.exists(BLACK_PNG_PATH):
        try:
            base = Image.open(BLACK_PNG_PATH).convert("RGBA")
        except:
            base = Image.new("RGBA", (300, 300), (0, 0, 0, 255))
    else:
        base = Image.new("RGBA", (300, 300), (0, 0, 0, 255))

    if os.path.exists(sprite_path):
        try:
            cover = Image.open(sprite_path).convert("RGBA").resize((300, 300), Image.NEAREST)
            base_w, base_h = base.size
            offset_x = (base_w - 300) // 15
            offset_y = (base_h - 300) // 2
            base.paste(cover, (offset_x, offset_y), cover)
        except Exception as e:
            print(f"警告: 封面处理失败 {sprite_path}: {e}")

    base.save(output_png_path, "PNG")

def compress_folder_to_pez(folder_path, pez_path):
    zip_path = pez_path.replace('.pez', '.zip')
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
    os.rename(zip_path, pez_path)
    shutil.rmtree(folder_path)


def convert_vsb_to_notes(vsb_data):
    lane_map_type0_2 = {0: -405, 1: -135, 2: 135, 3: 405}
    lane_map_type1 = {0: -270, 2: 270}
    fixed_note_template = {
        "above": 1, "alpha": 255, "color": [255, 255, 255],
        "endTime": [0, 0, 1], "isFake": 0, "judgeArea": 1.0,
        "positionX": 0.0, "size": 1.0, "speed": 1.0,
        "startTime": [0, 0, 1], "type": 1, "visibleTime": 1.0, "yOffset": 0.0
    }

    notes_list = []
    raw_notes = []  # (时间, 类型, 轨道, 原始索引, 结束时间, 半区)

    # 预处理
    for idx, note in enumerate(vsb_data):
        if note['type'] not in [0, 1, 2, 6, 7, 8]:
            continue

        t_start = Fraction(int(note['time']), 1000) + 1
        t_end = t_start

        if note['type'] == 0:  # chip
            half = 0 if note['lane'] in [0, 1] else 2
            raw_notes.append((t_start, 0, note['lane'], idx, t_end, half))
        elif note['type'] == 2:  # hold
            half = 0 if note['lane'] in [0, 1] else 2
            raw_notes.append((t_start, 2, note['lane'], idx, Fraction(int(note['extra']['1']), 1000) + 1, half))
        elif note['type'] in [1, 8]:  # bumper
            half = note['lane']
            raw_notes.append((t_start, 1, note['lane'], idx, t_end, half))
        elif note['type'] == 6:  # mine
            half = 0 if note['lane'] in [0, 1] else 2
            raw_notes.append((t_start, 6, note['lane'], idx, t_end, half))
        elif note['type'] == 7:  # bumper mine
            half = note['lane']
            raw_notes.append((t_start, 7, note['lane'], idx, t_end, half))

    raw_notes.sort(key=lambda x: x[0])

    # 半区处理
    for target_half in [0, 2]:
        half_notes = [n for n in raw_notes if n[5] == target_half]
        i = 0

        while i < len(half_notes):
            time, typ, lane, orig_idx, end_time, _ = half_notes[i]

            # not bumper
            if typ != 1 and typ != 8:
                new_note = fixed_note_template.copy()
                new_note['startTime'] = [int(time), time.numerator % time.denominator, time.denominator]
                new_note['endTime'] = [int(end_time), end_time.numerator % end_time.denominator, end_time.denominator]

                if typ == 0:  # Chip
                    new_note['positionX'] = lane_map_type0_2[lane]
                elif typ == 2:  # Hold
                    new_note['type'] = 2
                    new_note['positionX'] = lane_map_type0_2[lane]
                elif typ == 6:  # 普通地雷
                    new_note['type'] = 3
                    new_note['isFake'] = 1
                    new_note['alpha'] = 127
                    new_note['positionX'] = lane_map_type0_2.get(lane, 0.0)
                elif typ == 7:  # bumper地雷
                    new_note['type'] = 3
                    new_note['isFake'] = 1
                    new_note['alpha'] = 127
                    new_note['positionX'] = lane_map_type1.get(lane, 0.0)
                    new_note['size'] = 2.6

                notes_list.append(new_note)
                i += 1
                continue

            # bumper chain detection
            chain_start = i
            chain_end = i

            # extend chain as far as p
            while chain_end + 1 < len(half_notes) and half_notes[chain_end + 1][1] == 1:
                chain_end += 1

            chain = half_notes[chain_start:chain_end + 1]

            # 如果有hold盖着直接确定
            filtered_chain = []
            for bumper in chain:
                b_time = bumper[0]
                cover_info = None

                # 確定是否被覆蓋以及檢測是否有同側雙押hold覆蓋(非法配置)
                for lane in [target_half, target_half + 1]:
                    idx = chain_start - 1
                    while idx >= 0:
                        t, tp, ln, _, et, _ = half_notes[idx]
                        if ln == lane and tp == 2 and et >= b_time:
                            if cover_info is not None:
                                raise ValueError(f"轨道{target_half}/{target_half + 1}上同时有Hold覆盖Bumper，bro你这怎么打")
                            cover_info = (True, ln)
                            break
                        idx -= 1

                if cover_info:
                    new_note = fixed_note_template.copy()
                    b_time = bumper[0]
                    new_note['startTime'] = [int(b_time), b_time.numerator % b_time.denominator, b_time.denominator]
                    new_note['endTime'] = new_note['startTime'].copy()
                    new_note['type'] = 1
                    base_pos = -270 if target_half == 0 else 270
                    cover_lane = cover_info[1]
                    offset = 85 if cover_lane in [0, 2] else -85
                    new_note['positionX'] = base_pos + offset
                    notes_list.append(new_note)
                else:
                    filtered_chain.append(bumper)

            if not filtered_chain:
                i = chain_end + 1
                continue

            # (虚拟)头音符, 返回time和lane
            def get_virtual_head_note():
                candidates = []

                for lane in [target_half, target_half + 1]:
                    idx = chain_start - 1
                    while idx >= 0:
                        if half_notes[idx][2] == lane:
                            t, tp, ln, _, et, _ = half_notes[idx]
                            is_chip = (tp == 0)
                            effective_time = et if (tp == 2) else t
                            candidates.append((effective_time, ln, is_chip))
                            break
                        idx -= 1

                if not candidates:
                    return None, None

                if len(candidates) == 2 and candidates[0][0] == candidates[1][0]:
                    # 双押情况下Chip优先
                    chip_candidates = [c for c in candidates if c[2]]
                    if len(chip_candidates) == 1:
                        return chip_candidates[0][0], chip_candidates[0][1]
                    elif len(chip_candidates) == 2:
                        return None, None

                best = max(candidates, key=lambda x: x[0])
                return best[0], best[1]

            # 尾音符 BREAKPOINT 為什麼此處沒有雙軌判斷?
            def get_tail_note():
                idx = chain_end + 1

                if idx >= len(half_notes):
                    return None, None

                while idx < len(half_notes) and half_notes[idx][1] == 1:
                    idx += 1

                t, tp, ln, _, et, _ = half_notes[idx]
                return (t, ln)

            head_time, head_lane = get_virtual_head_note()
            tail_time, tail_lane = get_tail_note()

            # 倾向
            def get_tendency(lane, half):
                if lane == half:
                    return half + 1
                elif lane == half + 1:
                    return half
                return None

            head_tendency = get_tendency(head_lane, target_half) if head_lane is not None else None
            tail_tendency = get_tendency(tail_lane, target_half) if tail_lane is not None else None

            # 双押处理
            if head_tendency is None and tail_tendency is not None:
                head_tendency = tail_tendency
            elif tail_tendency is None and head_tendency is not None:
                tail_tendency = head_tendency
            elif head_tendency is None and tail_tendency is None:
                head_tendency = target_half + 1 if target_half == 0 else target_half

            # 初始交替分配
            assigned_lanes = []
            cur = head_tendency
            for _ in filtered_chain:
                assigned_lanes.append(cur)
                cur = target_half + 1 if cur == target_half else target_half

            # 对齐验证
            if assigned_lanes and tail_tendency is not None:
                if assigned_lanes[-1] != tail_tendency:
                    intervals = []

                    # 头->首
                    if head_time is not None:
                        gap = filtered_chain[0][0] - head_time
                        intervals.append((gap, -1))

                    # 中间
                    for j in range(len(filtered_chain) - 1):
                        gap = filtered_chain[j + 1][0] - filtered_chain[j][0]
                        intervals.append((gap, j))

                    # 尾->末
                    if tail_time is not None:
                        last_end = filtered_chain[-1][0]
                        gap = tail_time - last_end
                        intervals.append((gap, len(filtered_chain) - 1))

                    intervals.sort(key=lambda x: (-float(x[0]), -x[1]))
                    max_gap_idx = intervals[0][1]

                    for k in range(max_gap_idx + 1, len(assigned_lanes)):
                        assigned_lanes[k] = target_half + 1 if assigned_lanes[k] == target_half else target_half

            # 输出bumper
            for (time, _, _, _, _, _), out_lane in zip(filtered_chain, assigned_lanes):
                new_note = fixed_note_template.copy()
                new_note['startTime'] = [int(time), time.numerator % time.denominator, time.denominator]
                new_note['endTime'] = new_note['startTime'].copy()
                new_note['type'] = 1

                base_pos = -270 if target_half == 0 else 270
                offset = -85 if out_lane in [0, 2] else 85
                new_note['positionX'] = base_pos + offset

                notes_list.append(new_note)

            i = chain_end + 1

    return notes_list

import re
import unicodedata

def build_final_json(meta_str, notes_list):
    def _flatten_lists(obj):
        if isinstance(obj, list):
            return str(obj)
        if isinstance(obj, dict):
            return {k: _flatten_lists(v) for k, v in obj.items()}
        return obj

    flat_notes = [_flatten_lists(n) for n in notes_list]
    notes_str = json.dumps(flat_notes, ensure_ascii=False, indent=3, separators=(',', ' : '))
    notes_str = re.sub(r'"\[(\d+(?:, \d+)*)\]"', r'[\1]', notes_str)
    notes_str = re.sub(r'^\[\n', '', notes_str)
    notes_str = re.sub(r'\n\]$', '', notes_str)
    out = TMPL.replace(
        '"META" : {\n      "RPEVersion" : 170,\n      "background" : "black.png",\n      "charter" : "vsb2pez",\n      "composer" : "vsb2pez",\n      "duration" : 392.90701293945312,\n      "id" : "6708198698448521",\n      "illustration" : "",\n      "level" : "0",\n      "name" : "vsb2pez",\n      "offset" : -1028,\n      "song" : "6708198698448521.ogg"\n   },',
        meta_str)
    out = out.replace('"notes" : []', f'"notes" : [{notes_str}\n         ]')
    out = out.replace('"numOfNotes" : 0', f'"numOfNotes" : {len(notes_list)}')
    return out

def sanitize(name: str, replacement: str = ' ') -> str:
    if not isinstance(name, str):
        raise TypeError('name 必须是 str 类型')

    name = unicodedata.normalize('NFC', name)

    blacklist = r'[<>:\"/\\|?*\x00-\x1f]'
    name = re.sub(blacklist, replacement, name)

    if replacement:
        name = re.sub(rf'{re.escape(replacement)}+', replacement, name)
    name = name.strip()

    if not name:
        name = 'N/A'
    return name


def process_single_chart(vsb_path, chart_id, difficulty, song_info):
    try:
        with open(vsb_path, 'r', encoding='utf-8') as f:
            vsb_data = json.load(f)

        src_audio_ogg = os.path.join(AUDIO_DIR, f"music_chart_{chart_id}.ogg")
        src_audio_wav = os.path.join(AUDIO_DIR, f"music_chart_{chart_id}.wav")
        if os.path.exists(src_audio_ogg):
            audio_ext = ".ogg"
        elif os.path.exists(src_audio_wav):
            audio_ext = ".wav"
        else:
            raise FileNotFoundError(f"音频文件不存在: {src_audio_ogg} 或 {src_audio_wav}")

        id_str = calculate_id(song_info["song_id"])
        duration = get_audio_duration(chart_id)
        meta_str = generate_meta_str(song_info, difficulty, duration, id_str, audio_ext)
        notes = convert_vsb_to_notes(vsb_data)
        final_json = build_final_json(meta_str, notes)
        output_subdir = os.path.join(OUTPUT_DIR, chart_id, difficulty.replace(".json", ""))
        os.makedirs(output_subdir, exist_ok=True)
        output_json_path = os.path.join(output_subdir, f"{id_str}.json")
        with open(output_json_path, 'w', encoding='utf-8') as f:
            f.write(final_json)
        info_content = generate_info_txt(song_info, difficulty, id_str, duration, audio_ext)
        with open(os.path.join(output_subdir, "info.txt"), 'w', encoding='utf-8') as f:
            f.write(info_content)
        copy_resource_files(output_subdir, chart_id, id_str, audio_ext)
        pez_path = os.path.join(OUTPUT_DIR, chart_id,
                                f"{sanitize(song_info['formatted_name'])} - {difficulty.replace('.json', '')}.pez")
        compress_folder_to_pez(output_subdir, pez_path)
        return True
    except Exception as e:
        print(f"  失败: {str(e)}")
        return False


def main():
    print("加载song_information.json...")
    try:
        song_info_dict = load_song_info()
        print(f"加载了 {len(song_info_dict)} 个曲目信息")
    except Exception as e:
        print(f"元数据加载失败: {e}")
        return

    if not os.path.exists(SPRITE_DIR):
        print(f"警告: Sprites目录不存在: {SPRITE_DIR}，将只能使用black.png作为封面")

    print("\n扫描谱面文件...")
    if not os.path.exists(VSB_JSON_DIR):
        print(f"错误: 找不到vsbjson目录: {VSB_JSON_DIR}")
        return

    total_files = 0
    success_files = 0
    failed_files = 0

    for chart_id in os.listdir(VSB_JSON_DIR):
        chart_path = os.path.join(VSB_JSON_DIR, chart_id)
        if not os.path.isdir(chart_path):
            continue

        if chart_id not in song_info_dict:
            print(f"\n跳过: {chart_id} (无元数据)")
            continue

        song_info = song_info_dict[chart_id]
        print(f"\n\n处理曲目: {song_info.get('formatted_name', chart_id)} (ID: {chart_id})")

        for diff_file in DIFFICULTY_MAP.keys():
            vsb_file_path = os.path.join(chart_path, diff_file)
            diff_pez = diff_file.replace(".json", ".pez")

            if diff_file == "ENCORE.json" and not os.path.exists(vsb_file_path):
                print(f"  {diff_pez} (无)", end="")
                continue

            if not os.path.exists(vsb_file_path):
                print(f"  {diff_pez} (无)", end="")
                continue

            total_files += 1
            print(f"  {diff_pez} √ ", end="")

            if process_single_chart(vsb_file_path, chart_id, diff_file, song_info):
                success_files += 1
            else:
                failed_files += 1

    print("\n" + "=" * 60)
    print(f"转换完成: 总计{total_files} | 成功{success_files} | 失败{failed_files}")
    print(f"输出目录: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == '__main__':
    main()
