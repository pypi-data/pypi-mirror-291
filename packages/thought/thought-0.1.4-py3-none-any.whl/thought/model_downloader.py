import os
import json
from gguf_modeldb import ModelDB

def _load_file(filename):
    file = open(filename, "r")
    return json.load(file)

def _save_file(filename, json_data):
    file = open(filename, "w")
    file.write(json.dumps(json_data))

def _fix_model_json_to_relative(model_path="./model_db"):
    for filename in os.listdir(model_path):
        if filename.endswith(".json"):
            json_data = _load_file(model_path+os.sep+filename)
            json_data["save_dir"] = model_path
            json_data["gguf_file_path"] = model_path+"/"+json_data["model_name"]+".gguf"
            _save_file(model_path+os.sep+filename, json_data)

def get_models(model_path="./model_db", use_verified=False):
    model_db = ModelDB(model_db_dir=model_path,copy_verified_models=use_verified)
    model_db.show_db_info()
    _fix_model_json_to_relative(model_path)

def find_model(search="", model_path="./model_db", use_verified=False):
    model_db = ModelDB(model_db_dir=model_path, copy_verified_models=use_verified)
    _fix_model_json_to_relative(model_path)
    return model_db.find_model(search)

def add_model(url, model_path="./model_db"):
    if not "https://" in url:
        url = "https://huggingface.co/"+url

    model_db = ModelDB(model_db_dir=model_path, copy_verified_models=False)
    model_db.add_model_by_url(url)
    _fix_model_json_to_relative(model_path)

def download_model(model_name, quantization_query="", model_path="./model_db", force_download=False):
    model_db = ModelDB(model_db_dir=model_path, copy_verified_models=False)
    mdt = model_db.find_model(model_name, quantization_query=quantization_query)
    mdt.download_gguf(force_redownload=force_download)
    return mdt
