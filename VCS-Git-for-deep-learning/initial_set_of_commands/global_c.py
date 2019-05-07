import os

DLV_DIR = ".dlv"

CONFIG_FILE = "config"
HEAD_FILE = "HEAD"
STAGE_FILE = "stage"

REFS_DIR = "refs"
CACHE_DIR = "cache"
MASTER_BRANCH = "master"

root_dir, dlv_dir, dlv_config_file, dlv_head_file, dlv_stage_file, dlv_refs_dir, dlv_cache_dir, dlv_master_file = ('',)*8

def set_defaults( repository = os.curdir ):
    global root_dir, dlv_dir, dlv_config_file, dlv_head_file, dlv_stage_file, dlv_refs_dir, dlv_cache_dir, dlv_master_file

    root_dir = os.path.abspath(repository)

    if not os.path.isdir(root_dir):
        os.mkdir(root_dir)
        
    dlv_dir = os.path.join(root_dir, DLV_DIR)

    dlv_config_file = os.path.join(dlv_dir, CONFIG_FILE)
    dlv_head_file = os.path.join(dlv_dir, HEAD_FILE)
    dlv_stage_file = os.path.join(dlv_dir, STAGE_FILE)

    dlv_refs_dir = os.path.join(dlv_dir, REFS_DIR)
    dlv_cache_dir = os.path.join(dlv_dir, CACHE_DIR)

    dlv_master_file = os.path.join(dlv_refs_dir, MASTER_BRANCH)
