from musain_demo import *
from pprint import pprint

INST_MAP = { 'acoustic_grand_piano': 0, 'bright_acoustic_piano': 1, 'electric_grand_piano': 2, 'honky_tonk_piano': 3, 'electric_piano_1': 4, 'electric_piano_2': 5, 'harpsichord': 6, 'clavi': 7, 'celesta': 8, 'glockenspiel': 9, 'music_box': 10, 'vibraphone': 11, 'marimba': 12, 'xylophone': 13, 'tubular_bells': 14, 'dulcimer': 15, 'drawbar_organ': 16, 'percussive_organ': 17, 'rock_organ': 18, 'church_organ': 19, 'reed_organ': 20, 'accordion': 21, 'harmonica': 22, 'tango_accordion': 23, 'acoustic_guitar_nylon': 24, 'acoustic_guitar_steel': 25, 'electric_guitar_jazz': 26, 'electric_guitar_clean': 27, 'electric_guitar_muted': 28, 'overdriven_guitar': 29, 'distortion_guitar': 30, 'guitar_harmonics': 31, 'acoustic_bass': 32, 'electric_bass_finger': 33, 'electric_bass_pick': 34, 'fretless_bass': 35, 'slap_bass_1': 36, 'slap_bass_2': 37, 'synth_bass_1': 38, 'synth_bass_2': 39, 'violin': 40, 'viola': 41, 'cello': 42, 'contrabass': 43, 'tremolo_strings': 44, 'pizzicato_strings': 45, 'orchestral_harp': 46, 'timpani': 47, 'string_ensemble_1': 48, 'string_ensemble_2': 49, 'synth_strings_1': 50, 'synth_strings_2': 51, 'choir_aahs': 52, 'voice_oohs': 53, 'synth_voice': 54, 'orchestra_hit': 55, 'trumpet': 56, 'trombone': 57, 'tuba': 58, 'muted_trumpet': 59, 'french_horn': 60, 'brass_section': 61, 'synth_brass_1': 62, 'synth_brass_2': 63, 'soprano_sax': 64, 'alto_sax': 65, 'tenor_sax': 66, 'baritone_sax': 67, 'oboe': 68, 'english_horn': 69, 'bassoon': 70, 'clarinet': 71, 'piccolo': 72, 'flute': 73, 'recorder': 74, 'pan_flute': 75, 'blown_bottle': 76, 'shakuhachi': 77, 'whistle': 78, 'ocarina': 79, 'lead_1_square': 80, 'lead_2_sawtooth': 81, 'lead_3_calliope': 82, 'lead_4_chiff': 83, 'lead_5_charang': 84, 'lead_6_voice': 85, 'lead_7_fifths': 86, 'lead_8_bass__lead': 87, 'pad_1_new_age': 88, 'pad_2_warm': 89, 'pad_3_polysynth': 90, 'pad_4_choir': 91, 'pad_5_bowed': 92, 'pad_6_metallic': 93, 'pad_7_halo': 94, 'pad_8_sweep': 95, 'fx_1_rain': 96, 'fx_2_soundtrack': 97, 'fx_3_crystal': 98, 'fx_4_atmosphere': 99, 'fx_5_brightness': 100, 'fx_6_goblins': 101, 'fx_7_echoes': 102, 'fx_8_sci_fi': 103, 'sitar': 104, 'banjo': 105, 'shamisen': 106, 'koto': 107, 'kalimba': 108, 'bag_pipe': 109, 'fiddle': 110, 'shanai': 111, 'tinkle_bell': 112, 'agogo': 113, 'steel_drums': 114, 'woodblock': 115, 'taiko_drum': 116, 'melodic_tom': 117, 'synth_drum': 118, 'reverse_cymbal': 119, 'guitar_fret_noise': 120, 'breath_noise': 121, 'seashore': 122, 'bird_tweet': 123, 'telephone_ring': 124, 'helicopter': 125, 'applause': 126, 'gunshot': 127, 'drum_0': 0, 'drum_1': 1, 'drum_2': 2, 'drum_3': 3, 'drum_4': 4, 'drum_5': 5, 'drum_6': 6, 'drum_7': 7, 'drum_8': 8, 'drum_9': 9, 'drum_10': 10, 'drum_11': 11, 'drum_12': 12, 'drum_13': 13, 'drum_14': 14, 'drum_15': 15, 'drum_16': 16, 'drum_17': 17, 'drum_18': 18, 'drum_19': 19, 'drum_20': 20, 'drum_21': 21, 'drum_22': 22, 'drum_23': 23, 'drum_24': 24, 'drum_25': 25, 'drum_26': 26, 'drum_27': 27, 'drum_28': 28, 'drum_29': 29, 'drum_30': 30, 'drum_31': 31, 'drum_32': 32, 'drum_33': 33, 'drum_34': 34, 'drum_35': 35, 'drum_36': 36, 'drum_37': 37, 'drum_38': 38, 'drum_39': 39, 'drum_40': 40, 'drum_41': 41, 'drum_42': 42, 'drum_43': 43, 'drum_44': 44, 'drum_45': 45, 'drum_46': 46, 'drum_47': 47, 'drum_48': 48, 'drum_49': 49, 'drum_50': 50, 'drum_51': 51, 'drum_52': 52, 'drum_53': 53, 'drum_54': 54, 'drum_55': 55, 'drum_56': 56, 'drum_57': 57, 'drum_58': 58, 'drum_59': 59, 'drum_60': 60, 'drum_61': 61, 'drum_62': 62, 'drum_63': 63, 'drum_64': 64, 'drum_65': 65, 'drum_66': 66, 'drum_67': 67, 'drum_68': 68, 'drum_69': 69, 'drum_70': 70, 'drum_71': 71, 'drum_72': 72, 'drum_73': 73, 'drum_74': 74, 'drum_75': 75, 'drum_76': 76, 'drum_77': 77, 'drum_78': 78, 'drum_79': 79, 'drum_80': 80, 'drum_81': 81, 'drum_82': 82, 'drum_83': 83, 'drum_84': 84, 'drum_85': 85, 'drum_86': 86, 'drum_87': 87, 'drum_88': 88, 'drum_89': 89, 'drum_90': 90, 'drum_91': 91, 'drum_92': 92, 'drum_93': 93, 'drum_94': 94, 'drum_95': 95, 'drum_96': 96, 'drum_97': 97, 'drum_98': 98, 'drum_99': 99, 'drum_100': 100, 'drum_101': 101, 'drum_102': 102, 'drum_103': 103, 'drum_104': 104, 'drum_105': 105, 'drum_106': 106, 'drum_107': 107, 'drum_108': 108, 'drum_109': 109, 'drum_110': 110, 'drum_111': 111, 'drum_112': 112, 'drum_113': 113, 'drum_114': 114, 'drum_115': 115, 'drum_116': 116, 'drum_117': 117, 'drum_118': 118, 'drum_119': 119, 'drum_120': 120, 'drum_121': 121, 'drum_122': 122, 'drum_123': 123, 'drum_124': 124, 'drum_125': 125, 'drum_126': 126, 'drum_127': 127 };

REV_INST_MAP = { 0: 'acoustic_grand_piano', 1: 'bright_acoustic_piano', 2: 'electric_grand_piano', 3: 'honky_tonk_piano', 4: 'electric_piano_1', 5: 'electric_piano_2', 6: 'harpsichord', 7: 'clavi', 8: 'celesta', 9: 'glockenspiel', 10: 'music_box', 11: 'vibraphone', 12: 'marimba', 13: 'xylophone', 14: 'tubular_bells', 15: 'dulcimer', 16: 'drawbar_organ', 17: 'percussive_organ', 18: 'rock_organ', 19: 'church_organ', 20: 'reed_organ', 21: 'accordion', 22: 'harmonica', 23: 'tango_accordion', 24: 'acoustic_guitar_nylon', 25: 'acoustic_guitar_steel', 26: 'electric_guitar_jazz', 27: 'electric_guitar_clean', 28: 'electric_guitar_muted', 29: 'overdriven_guitar', 30: 'distortion_guitar', 31: 'guitar_harmonics', 32: 'acoustic_bass', 33: 'electric_bass_finger', 34: 'electric_bass_pick', 35: 'fretless_bass', 36: 'slap_bass_1', 37: 'slap_bass_2', 38: 'synth_bass_1', 39: 'synth_bass_2', 40: 'violin', 41: 'viola', 42: 'cello', 43: 'contrabass', 44: 'tremolo_strings', 45: 'pizzicato_strings', 46: 'orchestral_harp', 47: 'timpani', 48: 'string_ensemble_1', 49: 'string_ensemble_2', 50: 'synth_strings_1', 51: 'synth_strings_2', 52: 'choir_aahs', 53: 'voice_oohs', 54: 'synth_voice', 55: 'orchestra_hit', 56: 'trumpet', 57: 'trombone', 58: 'tuba', 59: 'muted_trumpet', 60: 'french_horn', 61: 'brass_section', 62: 'synth_brass_1', 63: 'synth_brass_2', 64: 'soprano_sax', 65: 'alto_sax', 66: 'tenor_sax', 67: 'baritone_sax', 68: 'oboe', 69: 'english_horn', 70: 'bassoon', 71: 'clarinet', 72: 'piccolo', 73: 'flute', 74: 'recorder', 75: 'pan_flute', 76: 'blown_bottle', 77: 'shakuhachi', 78: 'whistle', 79: 'ocarina', 80: 'lead_1_square', 81: 'lead_2_sawtooth', 82: 'lead_3_calliope', 83: 'lead_4_chiff', 84: 'lead_5_charang', 85: 'lead_6_voice', 86: 'lead_7_fifths', 87: 'lead_8_bass__lead', 88: 'pad_1_new_age', 89: 'pad_2_warm', 90: 'pad_3_polysynth', 91: 'pad_4_choir', 92: 'pad_5_bowed', 93: 'pad_6_metallic', 94: 'pad_7_halo', 95: 'pad_8_sweep', 96: 'fx_1_rain', 97: 'fx_2_soundtrack', 98: 'fx_3_crystal', 99: 'fx_4_atmosphere', 100: 'fx_5_brightness', 101: 'fx_6_goblins', 102: 'fx_7_echoes', 103: 'fx_8_sci_fi', 104: 'sitar', 105: 'banjo', 106: 'shamisen', 107: 'koto', 108: 'kalimba', 109: 'bag_pipe', 110: 'fiddle', 111: 'shanai', 112: 'tinkle_bell', 113: 'agogo', 114: 'steel_drums', 115: 'woodblock', 116: 'taiko_drum', 117: 'melodic_tom', 118: 'synth_drum', 119: 'reverse_cymbal', 120: 'guitar_fret_noise', 121: 'breath_noise', 122: 'seashore', 123: 'bird_tweet', 124: 'telephone_ring', 125: 'helicopter', 126: 'applause', 127: 'gunshot', 128: 'drum_0', 129: 'drum_1', 130: 'drum_2', 131: 'drum_3', 132: 'drum_4', 133: 'drum_5', 134: 'drum_6', 135: 'drum_7', 136: 'drum_8', 137: 'drum_9', 138: 'drum_10', 139: 'drum_11', 140: 'drum_12', 141: 'drum_13', 142: 'drum_14', 143: 'drum_15', 144: 'drum_16', 145: 'drum_17', 146: 'drum_18', 147: 'drum_19', 148: 'drum_20', 149: 'drum_21', 150: 'drum_22', 151: 'drum_23', 152: 'drum_24', 153: 'drum_25', 154: 'drum_26', 155: 'drum_27', 156: 'drum_28', 157: 'drum_29', 158: 'drum_30', 159: 'drum_31', 160: 'drum_32', 161: 'drum_33', 162: 'drum_34', 163: 'drum_35', 164: 'drum_36', 165: 'drum_37', 166: 'drum_38', 167: 'drum_39', 168: 'drum_40', 169: 'drum_41', 170: 'drum_42', 171: 'drum_43', 172: 'drum_44', 173: 'drum_45', 174: 'drum_46', 175: 'drum_47', 176: 'drum_48', 177: 'drum_49', 178: 'drum_50', 179: 'drum_51', 180: 'drum_52', 181: 'drum_53', 182: 'drum_54', 183: 'drum_55', 184: 'drum_56', 185: 'drum_57', 186: 'drum_58', 187: 'drum_59', 188: 'drum_60', 189: 'drum_61', 190: 'drum_62', 191: 'drum_63', 192: 'drum_64', 193: 'drum_65', 194: 'drum_66', 195: 'drum_67', 196: 'drum_68', 197: 'drum_69', 198: 'drum_70', 199: 'drum_71', 200: 'drum_72', 201: 'drum_73', 202: 'drum_74', 203: 'drum_75', 204: 'drum_76', 205: 'drum_77', 206: 'drum_78', 207: 'drum_79', 208: 'drum_80', 209: 'drum_81', 210: 'drum_82', 211: 'drum_83', 212: 'drum_84', 213: 'drum_85', 214: 'drum_86', 215: 'drum_87', 216: 'drum_88', 217: 'drum_89', 218: 'drum_90', 219: 'drum_91', 220: 'drum_92', 221: 'drum_93', 222: 'drum_94', 223: 'drum_95', 224: 'drum_96', 225: 'drum_97', 226: 'drum_98', 227: 'drum_99', 228: 'drum_100', 229: 'drum_101', 230: 'drum_102', 231: 'drum_103', 232: 'drum_104', 233: 'drum_105', 234: 'drum_106', 235: 'drum_107', 236: 'drum_108', 237: 'drum_109', 238: 'drum_110', 239: 'drum_111', 240: 'drum_112', 241: 'drum_113', 242: 'drum_114', 243: 'drum_115', 244: 'drum_116', 245: 'drum_117', 246: 'drum_118', 247: 'drum_119', 248: 'drum_120', 249: 'drum_121', 250: 'drum_122', 251: 'drum_123', 252: 'drum_124', 253: 'drum_125', 254: 'drum_126', 255: 'drum_127' };

CURRENT_NUM_BARS = 16
TRACK_COUNT = 0

POLY_LEVELS = ["any", "one", "two", "three", "four", "five", "six"]
DUR_LEVELS = ["any", "thirty_second", "sixteenth", "eighth", "quarter", "half", "whole"]

inst_arr = []
inst_arr_int = []
density_arr = []
density_disabled_arr = []
min_poly_arr = []
max_poly_arr = []
min_dur_arr = []
max_dur_arr = []
resample_arr = []
mute_arr = []
solo_arr = []
midi_track_len = 0

APP = app #App()

def build_from_midi(midi_json):
    clear_tracks(False)
    midi_json = json.loads(midi_json)
    midi_track_len = len(midi_json["tracks"])
    CURRENT_NUM_BARS = len(midi_json["tracks"][0]["bars"])
    
    for i in range(len(midi_json["tracks"])):
        build_track(midi_json)

def clear_tracks(is_reset):
    global TRACK_COUNT
    TRACK_COUNT=0
    
    if is_reset:
        reset_midi()
        
def build_track(midi_json):
    
    global TRACK_COUNT
    global inst_arr
    global density_arr
    global density_disabled_arr
    global min_poly_arr
    global max_poly_arr
    global min_dur_arr
    global max_dur_arr
    global resample_arr
    
    build_pianoroll(midi_json, TRACK_COUNT)
	
    inst = "acoustic_grand_piano"
    density = 5
    min_poly = "any"
    max_poly = "any"
    min_dur = "any"
    max_dur = "any"

    if midi_json:
        #CURRENT_NUM_BARS = len(midi_json["tracks"][TRACK_COUNT]["bars"])
        #print(CURRENT_NUM_BARS)
        
        isDrum = ((midi_json["tracks"][TRACK_COUNT]["trackType"] == 11) or (midi_json["tracks"][TRACK_COUNT]["trackType"] == "STANDARD_DRUM_TRACK"))
        
        #print(TRACK_COUNT)
        inst_number = midi_json["tracks"][TRACK_COUNT]["instrument"]
        inst = REV_INST_MAP[inst_number + 128 * isDrum]

        features = midi_json["tracks"][TRACK_COUNT]["internalFeatures"][0]
        density = features["noteDensityV2"]
        min_poly = POLY_LEVELS[features["minPolyphonyQ"] + 1]
        max_poly = POLY_LEVELS[features["maxPolyphonyQ"] + 1]
        min_dur = DUR_LEVELS[features["minNoteDurationQ"] + 1]
        max_dur = DUR_LEVELS[features["maxNoteDurationQ"] + 1]
        
    #elif midi_json == {}:
    #    resample_arr.append(True)
    
    
    inst_arr.append(inst)
    density_arr.append(density)
    density_disabled_arr.append(False)
    min_poly_arr.append(min_poly)
    max_poly_arr.append(max_poly)
    min_dur_arr.append(min_dur)
    max_dur_arr.append(max_dur)
    mute_arr.append(False)
    solo_arr.append(False)
    #print(TRACK_COUNT)
    TRACK_COUNT += 1

def build_pianoroll(midi_json, track_num):
    # build piano roll should accept an actual track from the representation
    if midi_json == {}:
        notes = []
    else:
        global CURRENT_NUM_BARS
        notes = get_notes(midi_json, track_num)
        CURRENT_NUM_BARS = len(midi_json["tracks"][track_num]["bars"])
        #print(CURRENT_NUM_BARS)
        
def fill_highlited_bars(track_id):
    
    
    highlighted_bars = [True] * CURRENT_NUM_BARS
    
    return highlighted_bars
    
def get_notes(midi_json, track_num):
    # we can assume that the midi_json is well formed here
    notes = []
    onsets = {}

    track = midi_json["tracks"][track_num]
    if "bars" in track:
        bar_start = 0
        bars = track["bars"]
        for i in range(len(bars)):
            if ("events" in bars[i]):
                events = bars[i]["events"]
                for j in range(len(events)):
                    event = midi_json["events"][events[j]]
                    if (event["velocity"] > 0):
                        onsets[event["pitch"]] = { "time": bar_start + event["time"]}
                        # onsets[event["pitch"]]["time"] += bar_start

                    elif(event["pitch"] in onsets):
                        notes.append({
                            "start": onsets[event["pitch"]]["time"],
                            "end": bar_start + event["time"],
                            "pitch": event["pitch"],
                            })
                        del onsets[event["pitch"]]
          

            bar_start += bars[i]["internalBeatLength"] * 12 # resolution
    ## handle remaining notes
    #print('onsets',onsets)
    if onsets != {}:
        try:
            for key in onsets:
                notes.append({
                "start": onsets[key]["time"],
                "end": 192,
                "pitch": onsets[key]["pitch"],
                })
        except Exception as e:
            #print(e)
            pass

    return notes



CONF_GLOBAL = {"temperature":1.0, "tempo":120, "tracks_per_step":1, "bars_per_step":2, "shuffle":True, "percent":100, "model_size":4 }



   
def get_status(CONF=None):
    status = { "tracks": [] }
    global CONF_GLOBAL
    global density_arr
    global density_disabled_arr
    global min_poly_arr
    global max_poly_arr
    global min_dur_arr
    global max_dur_arr
    global mute_arr
    global solo_arr
    
    
    if CONF:
        density_arr = density_arr[: CONF["n_tracks"]]
        density_disabled_arr = density_disabled_arr[: CONF["n_tracks"]]
        min_poly_arr = min_poly_arr[: CONF["n_tracks"]]
        max_poly_arr = max_poly_arr[: CONF["n_tracks"]]
        min_dur_arr = min_dur_arr[: CONF["n_tracks"]]
        max_dur_arr = max_dur_arr[: CONF["n_tracks"]]
        mute_arr = mute_arr[: CONF["n_tracks"]]
        solo_arr = solo_arr[: CONF["n_tracks"]]
        
        can_generate = True;
        can_listen = True;
        
        CONF_GLOBAL.update(CONF)
        for i in range(0, CONF["n_tracks"]):
            build_track({})
            
            inst_arr_int.append(CONF["instrument_N"][i])
            resample_arr.append(CONF["canGenerate"][i] == '1')
        
        #tracks = CONF_GLOBAL["n_tracks"]
        
        
        # for i in range(tracks):
            track_id = i;
            
            inst_int = inst_arr_int[track_id]
            
            
            inst = REV_INST_MAP[ int(inst_arr_int[track_id]) ]
            density = density_arr[track_id] 
            density_disabled = density_disabled_arr[track_id]
            min_poly = min_poly_arr[track_id] 
            max_poly = max_poly_arr[track_id] 
            min_dur =  min_dur_arr[track_id]
            max_dur = max_dur_arr[track_id]
            resample = resample_arr[track_id]
            mute = mute_arr[track_id]
            solo = solo_arr[track_id]
            h_bars = fill_highlited_bars(track_id)

            density = int(density) + 1;
            if (density_disabled):
                density = 0;


            ignore = False
            track_type = 10;
            if "drum_" in inst:
                track_type = 11;
            #print("트랙번호:", track_id)
            print("악기번호: ",CONF["instrument_N"][track_id])
            
            status["tracks"].append({
                "track_id": int(track_id),
                "instrument": inst,
                "instrument_num": CONF_GLOBAL["instrument_N"][track_id], #int(inst_int) if inst_int is not None else inst_arr_int[track_id],
                "density": density,
                "track_type": track_type,
                "mute": mute,
                "solo": solo,
                "ignore": ignore,
                "resample": resample,
                "selected_bars": h_bars,
                "min_polyphony_q": "POLYPHONY_" + min_poly.upper(),
                "max_polyphony_q": "POLYPHONY_" + max_poly.upper(),
                "min_note_duration_q": "DURATION_" + min_dur.upper(),
                "max_note_duration_q": "DURATION_" + max_dur.upper()
              })
        
        status["temperature"] = CONF_GLOBAL["temperature"]
        status["canGenerate"] = can_generate
        status["canListen"] = can_listen
        status["tempo"] = CONF_GLOBAL["tempo"]
        status["nbars"] = CURRENT_NUM_BARS
        
        status["tracks_per_step"] = CONF_GLOBAL["tracks_per_step"] 
        status["bars_per_step"] = CONF_GLOBAL["bars_per_step"]
        status["shuffle"] = CONF_GLOBAL["shuffle"]
        status["percentage"] = CONF_GLOBAL["percent"]
        status["model_dim"] = CONF_GLOBAL["model_size"]
        
        
        
        
        print('settings was:: ', len(status["tracks"]))
        return status
    else:
        return { "tracks": [] }
	
def generate():
    status = get_status()
    if (status["tracks"] == 0):
        return
    
    if not status["canGenerate"]:
        print("Must highlight one or more bars (by clicking on them) before you can generate.")
        return
    
    try:
        print("....")
        APP.generate_callback(status)
    except Exception as error:
        print(error)
		
def init_start():
	build_track({})

def init_restart():
	clear_tracks(False)
	#build_track({})
	