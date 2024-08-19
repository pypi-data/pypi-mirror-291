import os
from os.path import join
import requests

def setup_instance():
    basedir = join(os.path.expanduser("~"), ".thunder")
    if not os.path.exists(basedir):
        os.makedirs(basedir)
        
    setup = '''__tnr_setup() {
    if [[ "$(type -t tnr)" == "function" ]]; then
        return
    fi
    
    if [[ "${__TNR_RUN}" != "true" ]]; then
        # We aren't running in a thunder shell
        return
    fi

    export __TNR_BINARY_PATH=$(command -v tnr)
    export __DEFAULT_PS1=$PS1
    PS1="(⚡$($__TNR_BINARY_PATH device --raw)) $__DEFAULT_PS1"

    tnr() {
        if [ "$1" = "device" ]; then
            if [ $# -eq 1 ]; then
                # Handle the case for 'tnr device' with no additional arguments
                "$__TNR_BINARY_PATH" "$@"
            elif [ "$2" = "cpu" ]; then
                # Handle the case for 'tnr device cpu'
                "$__TNR_BINARY_PATH" "$@"
                unset LD_PRELOAD
                PS1="(⚡CPU) $__DEFAULT_PS1"
            else
                # Handle other 'tnr device' commands
                "$__TNR_BINARY_PATH" "$@"
                if [ $? -eq 0 ]; then
                    case "${2,,}" in
                        h100|t4|v100|a100|l4|p4|p100)
                            export LD_PRELOAD=`readlink -f ~/.thunder/libthunder.so`
                            PS1="(⚡$($__TNR_BINARY_PATH device --raw)) $__DEFAULT_PS1"
                            ;;
                        *)
                            ;;
                    esac
                fi

            fi
        else
            # Forward the command to the actual tnr binary for all other cases
            "$__TNR_BINARY_PATH" "$@"
        fi
    }
}

__tnr_setup'''
        
    scriptfile = join(basedir, 'setup.sh')
    if not os.path.exists(scriptfile):
        with open(scriptfile, 'w+', encoding="utf-8") as f:
            f.write(setup)
        os.chmod(scriptfile, 0o555)
        
        bashrc = join(os.path.expanduser('~'), '.bashrc')
        with open(bashrc, 'a', encoding="utf-8") as f:
            f.write(f'\n# start tnr setup\n. {scriptfile}\n# end tnr setup\n')
    else:
        with open(scriptfile, 'r', encoding="utf-8") as f:
            current_contents = f.read()
        
        if current_contents != setup:
            os.chmod(scriptfile, 0o777)
            with open(scriptfile, 'w+', encoding="utf-8") as f:
                f.write(setup)
            os.chmod(scriptfile, 0o555)
    
    device_file = join(basedir, "dev")
    if not os.path.exists(device_file):
        with open(device_file, "w+", encoding="utf-8") as f:
            f.write("t4")
            
    num_gpus_file = join(basedir, "ngpus")
    if not os.path.exists(num_gpus_file):
        with open(num_gpus_file, "w+", encoding="utf-8") as f:
            f.write("1")

def get_available_gpus():
    endpoint = 'http://api.thundercompute.com:8080/hosts'
    try:
        response = requests.get(endpoint, timeout=10)
        if response.status_code != 200:
            return None

        return response.json()
    except Exception as e:
        return None

get_available_gpus()