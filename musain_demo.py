from fastapi import FastAPI, Request, Depends, WebSocket
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse, StreamingResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from Schema import MusainReqForm
from fastapi.staticfiles import StaticFiles

import music_util
import uvicorn
import shutil
import time
import json
import requests
import asyncio
import os
import musain
import base64

app = FastAPI()
app.mount('/static', StaticFiles(directory='./static'), name='static')
#templates = Jinja2Templates(directory="templates")

baseFolder = './static'

CONFIG = {"temperature": 1.0, "model_size": 4, "tempo": 100, "percent": 100, "bars_per_step": 2, "tracks_per_step": 1, "shuffle" : 1, "instrument_N" : "[0 3 5 7 9]", "canGenerate" : "[0 1 1 1 1]", "n_tracks" : 5}

class MyCustomException(Exception):
    def __init__(self, name: str):
        self.name = name
        
@app.exception_handler(MyCustomException)
async def MyCustomExceptionHandler(request: Request, exception: MyCustomException):
    app.restart()
    return JSONResponse (status_code = 500, content = {"message": "Something critical happened"})

@app.on_event("startup") # 초기 파일 지움.
async def on_app_start():
    try:
        await os.remove(f'{baseFolder}/input.mid')
    except Exception as e:
        pass
    #await fastapi_plugins.redis_plugin.init()


@app.post("/musain_demo_upload")
async def create_file(request: Request,
                      form_data: MusainReqForm = Depends(MusainReqForm.as_form)):
    # print(request)
    #print(form_data)
    CONFIG['temperature'] = form_data.temperature
    CONFIG['model_size'] = form_data.model_size
    CONFIG['tempo'] = form_data.tempo
    CONFIG['percent'] = form_data.percentage  # ...
    CONFIG['bars_per_step'] = form_data.bars_per_step  # ...
    CONFIG['shuffle'] = form_data.shuffle
    CONFIG['instrument_N'] = form_data.instrument
    CONFIG['canGenerate'] = form_data.canGenerate
    CONFIG['n_tracks'] = form_data.n_tracks
    CONFIG['task_name'] = form_data.arrangementID
    CONFIG['addr'] = form_data.url

    tmp_file = form_data.file
    with open(f"{baseFolder}/input.mid", "wb") as buffer:
        shutil.copyfileobj(tmp_file.file, buffer)
    jsondata_result = jsonable_encoder(form_data)
    return JSONResponse(content=jsondata_result)


@app.middleware("http")
async def after_response(request: Request, call_next):
    loop = asyncio.get_event_loop()
    #print(f'1: {request.client.host}')
    #print(f'2: {request.url.scheme}')
    #print(f'3: {request.url.path}')
    response = await call_next(request)
    if request.url.path == '/musain_demo_upload':
        # loop.create_task(doing_something(response))
        return StreamingResponse(arrange_resp())
    # else:
        # return response


async def doing_something(response):
    if response:
        print('Action after response ... ')
        return StreamingResponse(arrange_resp())
        #os.system('curl -L 0.0.0.0:7000/musain_ai')


def read_track_map():
    with open("track_map.json", "r") as f:
        return json.load(f)


def write_track_map(x):
    with open("track_map.json", "w") as f:
        json.dump(x, f)


def get_current_midi():
    with open("current_midi.json", "r") as f:
        return json.load(f)


def save_current_midi(midi_json):
    with open("current_midi.json", "w") as f:
        json.dump(midi_json, f)


def save_status(status):
    with open("current_status.json", "w") as f:
        json.dump(status, f)


def update_gui_midi(midi_json):
    assert isinstance(midi_json, dict)
    # execute_js('''build_from_midi(JSON.parse('{}'))'''.format(json.dumps(midi_json)))
    music_util.build_from_midi(json.dumps(midi_json))


def show_track(piece, i):
    print("=" * 30)
    for bar in piece["tracks"][i]["bars"]:
        for event in bar.get("events", []):
            print(piece["events"][event])
    print("=" * 30)


def generate_callback(status):
    try:
        with open('status.txt', 'w') as f:
            f.write(str(status))
    except Exception as e:
        print(e)
    #status = json.load(status)
    midi_json = get_current_midi()
    midi_json["resolution"] = midi_json.get("resolution", 12)
    midi_json["tempo"] = status['tempo']
    status["temperature"] = float(status["temperature"])
    
    ordered_midi_json_tracks = []
    track_gui_map = {}
    num_bars = len(status["tracks"][0]["selected_bars"])
    

    #print(status["tracks"][0]["instrument_num"])
    #print(status["tracks"][0]["instrument_N"])

    num_tracks = len(midi_json.get("tracks", []))
    # print(len(status["tracks"]), num_tracks)
    
    for i, track in enumerate(status["tracks"]):

        if track["track_id"] < num_tracks:
            midi_track = midi_json["tracks"][track["track_id"]]
            
        else:
            midi_track = {}
            midi_track["trackType"] = track["track_type"]
            midi_track["bars"] = [{"events": [], "internalBeatLength": 4, "tsNumerator": 4, "tsDenominator": 4, } for _ in range(num_bars)]
        
        # override instrument via status
        #print('??', track['instrument_num'])
        midi_track["instrument"] = track["instrument_num"] #
        midi_track["trackType"] = track["track_type"]
        
        ordered_midi_json_tracks.append(midi_track)

        track_gui_map[i] = track["track_id"]
        track["track_id"] = i
    midi_json["tracks"] = ordered_midi_json_tracks

    # format param
    param = {
        "tracks_per_step": int(status.pop("tracks_per_step")),
        "bars_per_step": int(status.pop("bars_per_step")),
        "model_dim": int(status.pop("model_dim")),
        "percentage": int(status.pop("percentage")),
        "batch_size": int(1),
        "temperature": float(status.pop("temperature")),
        "max_steps": int(0),
        "polyphony_hard_limit": int(6),
        "shuffle": (status.pop("shuffle")==1),
        "verbose": False,
        "ckpt": "model.pt"
    }

    # format status
    valid_status = {"tracks": []}
    for track in status.get("tracks", []):
        track.pop("mute")
        track.pop("solo")
        track.pop("instrument_num")
        track["autoregressive"] = track.pop("resample")
        valid_status["tracks"].append(track)

    # run generate
    #show_track(midi_json, 0)
    piece = json.dumps(midi_json)
    status = json.dumps(valid_status)
    param = json.dumps(param)
    
    # print(param)
    #print(musain.default_sample_param())
    
    #print(type(param))
    
    
    #print('stat? ', len(valid_status['tracks']))
    #print('param?', param)
    #print('tracks', len(midi_json['tracks']))
    
    #for i in range(len(valid_status['tracks'])):
    #    print(i)
    #    show_track(midi_json, i)
    #    print('===' * 20)
    
    midi_str = musain.sample_multi_step(piece, status, param)  # ???????
    #self.show_track(json.loads(midi_str), 0)

    # get density for tracks
    midi_str = musain.update_note_density(midi_str)
    midi_str = musain.update_av_polyphony_and_note_duration(midi_str)
    midi_json = json.loads(midi_str)

    # make sure each bar has events
    for track in midi_json["tracks"]:
        for bar in track["bars"]:
            bar["events"] = bar.get("events", [])
    midi_json["events"] = midi_json.get("events", [])

    # normalize volume (works in place)
    mix_tracks_in_json(midi_json)

    # update the midi
    update_gui_midi(midi_json)

    # save the midi
    save_current_midi(midi_json)


# this should work now basically
def mix_tracks_in_json(midi_json, levels=None):
    AUDIO_LEVELS = [12, 24, 36, 48, 60, 72, 84, 96, 108, 120]
    for track_num, track in enumerate(midi_json.get("tracks", [])):
        for bar in track.get("bars", []):
            for event_index in bar.get("events", []):
                event = midi_json["events"][event_index]
                if event["velocity"] > 0:
                    audio_level = AUDIO_LEVELS[8]
                    if levels is not None:
                        audio_level = AUDIO_LEVELS[levels[track_num]]
                    event["velocity"] = audio_level


def play_callback(status):
    midi_json = get_current_midi()
    tracks = []
    for track in status["tracks"]:
        tid = int(track["track_id"])
        if track["solo"]:
            tracks = [tid]
            break
        elif not track["mute"]:
            tracks.append(tid)

    encoder = musain.TrackDensityEncoder()

    midi_json["tempo"] = status["tempo"]
    # mix_tracks_in_json(midi_json)
    raw = json.dumps(midi_json)
    bars_to_keep = list(range(status["nbars"]))
    raw = musain.prune_tracks(raw, tracks, bars_to_keep)
    encoder.json_to_midi(raw, "current.mid")


def add_midi_callback(status, raw):
    data = raw  # re.search(r"base64,(.*)", raw).group(1)
    with open(f"{baseFolder}/input.mid", "wb") as f:
        f.write(base64.b64decode(data))

    enc = musain.TrackDensityEncoder()
    midi_json = json.loads(enc.midi_to_json(f"{baseFolder}/input.mid"))
    
    
    bars_to_keep = list(range(len(midi_json["tracks"][0]["bars"])))
    midi_json = json.loads(
        musain.prune_empty_tracks(json.dumps(midi_json), bars_to_keep)
    )

    # add new midi to what we already have
    cur_midi_json = get_current_midi()
    if len(cur_midi_json) and len(status.get("tracks", [])):
        valid_tracks = []
        for track in status.get("tracks", []):
            valid_tracks.append(cur_midi_json["tracks"][track["track_id"]])
        cur_midi_json["tracks"] = valid_tracks
        bars_to_keep = list(range(len(cur_midi_json["tracks"][0]["bars"])))
        cur_midi_json = json.loads(
            musain.prune_empty_tracks(json.dumps(cur_midi_json), bars_to_keep)
        )

        midi_json = json.loads(
            musain.append_piece(json.dumps(cur_midi_json), json.dumps(midi_json))
        )

    if len(midi_json.get("tracks", [])) == 0:
        print( 'build_snackbar("Invalid MIDI file. Make sure each track has atleast 8 bars.")')
        return

    if "tempo" not in midi_json:
        midi_json["tempo"] = 160

    # get density for tracks
    midi_str = json.dumps(midi_json)
    midi_str = musain.update_note_density(midi_str)
    midi_str = musain.update_av_polyphony_and_note_duration(midi_str)
    midi_json = json.loads(midi_str)
    
    # normalize volume (works in place)
    mix_tracks_in_json(midi_json)

    # update the midi
    update_gui_midi(midi_json)

    # save the midi
    save_current_midi(midi_json)


def sync_file():
    if os.path.isfile(f'{baseFolder}/input.mid'):
        with open(f'{baseFolder}/input.mid', 'rb') as f:
            print(f'파일 로드, {f}')
            return base64.b64encode(f.read())


def check_midi_json(status):
    print(type(status))
    print(status)

    print('---' * 10)
    print(status['tracks'])
    

    if len(status['tracks']) == 0 or status['canGenerate'] == 'false':
        print('No midi tracks')
        print('build_snackbar("Must add tracks before you can generate.")')
    else:
        return status
        #self.generate_callback(status)


def reset_midi():
    save_current_midi({})


def make_midi_data():
    while True:
        (CONFIG, ROUTE_MUSAIN_SERVER) = (yield)
        
        with open(f'CONFIG_{CONFIG["task_name"]}.txt', 'w') as fd:
            fd.write(str(json.dumps(CONFIG)))

        CONFIG['canGenerate'] = CONFIG['canGenerate'][1:-1].split(' ')
        CONFIG['instrument_N'] = CONFIG['instrument_N'][1:-1].split(' ')
        CONFIG_1 = json.dumps(CONFIG, ensure_ascii=False)
        CONFIG_2 = json.loads(CONFIG_1)

        reset_midi()
        music_util.init_restart()
        
        if os.path.isfile(f'{baseFolder}/input.mid') and ROUTE_MUSAIN_SERVER and CONFIG_2:
            print('ai ready !!!')
            
            raw_files = sync_file()
            status = { "tracks": [] } # music_util.get_status()
            #print('init', status)
            
            add_midi_callback(status, raw_files)
            
            print(f"started at {time.strftime('%X')}")
            
            status_new = music_util.get_status(CONFIG_2)
            #print('??', status_new)
                
            generate_callback(status_new)
            print(f"running at {time.strftime('%X')}")
            midi_json = get_current_midi()
            enc = musain.TrackDensityEncoder()
            enc.json_to_midi(json.dumps(midi_json), f"{CONFIG['task_name']}.mid")
            print(f'미디파일 생성 완료 {time.strftime("%X")}')
            # ----------
            print(f"전송 상대 IP주소: at {ROUTE_MUSAIN_SERVER}")
            if ROUTE_MUSAIN_SERVER and os.path.isfile(f"{CONFIG['task_name']}.mid") and midi_json and status_new:
                print('made midi file %s ' % f"{CONFIG['task_name']}.mid")
                print(f'musain finished={time.strftime("%X")}===============================================================')
                # os.system(f'curl -F file=@"{CONFIG["task_name"]}.mid" https://www.vucoms.co.kr:8200/ai_arrangement')
                # r = requests.post(f'{dest}', files={'file': open(f'{CONFIG['task_name']}.mid', 'rb')})
                #r = requests.post('https://www.vucoms.co.kr:8200/ai_arrangement', files={'file': open(f'{CONFIG["task_name"]}.mid', 'rb')})
                #print('result: ', r)
                return 1


async def arrange_resp():
    #print('arrange??')
    if os.path.isfile(f'{baseFolder}/input.mid'):
        #print('AI init...')
        print(f'dest -> {CONFIG["addr"]}')
        #print('received conf: ', CONFIG)

        midi_make = make_midi_data()  # whiel True일때 yield from ...
        next(midi_make)
        try:
            result = midi_make.send((CONFIG, CONFIG['addr']))
        except StopIteration as exec:
            result = exec.value
        if result == 1:
            yield 'exec finished'
            print('wwww')
            midi_make.close()


if __name__ == "__main__":
    uvicorn.run(app="musain_demo:app",
                host="0.0.0.0",
                port=7000,
                reload=True,
                workers=4)