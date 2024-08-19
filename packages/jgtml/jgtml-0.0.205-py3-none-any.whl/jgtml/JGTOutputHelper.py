import json
import os

def generate_markdown_from_json_file(json_filepath):
    with open(json_filepath, 'r') as file:
        data = json.load(file)
    
    signalbar = data['signalbar']
    currentbar = data['currentbar']
    
    markdown_output = f"""
# Trade Signal Details

## Trade Information
- **Entry Price:** {data['entry']}
- **Stop Loss:** {data['stop']}
- **Buy/Sell:** {data['bs']}
- **Lots:** {data['lots']}
- **Tlid ID:** {data['tlid_id']}
- **Instrument:** {data['i']}
- **Timeframe:** {data['t']}

![](signal.png)

[../charts](../charts)
[M1](../charts/M1.png)-[W1](../charts/W1.png)-[D1](../charts/D1.png)-[H4](../charts/H4.png)-[H1](../charts/H1.png)-[m15](../charts/m15.png)-[m5](../charts/m5.png)

"""



    markdown_output += """

----

## Utilities

* [entry.sh](../.jgt/entry.sh)
* [stop.sh](../.jgt/stop.sh)
* [watch.sh](../.jgt/watch.sh)
* [status.sh](../.jgt/status.sh)
* [update.sh](../.jgt/update.sh)
* [env.sh](../.jgt/env.sh)

### --@STCIssue Future Enhancements

* CLI Commands to run, not hard coded scripts
* Example : _fxtrupdate, _jgtsession_mksg, _jgtsession_vswsopen, _jgtsession_mkads_ctx_timeframe, _jgtsession_mkads_all_timeframes

"""



    markdown_output += f"""

## Signal Bar Data
| Metric           | Value         |
|------------------|---------------|
"""
    for key, value in signalbar.items():
        markdown_output += f"| {key} | {value} |\n"

    markdown_output += """
## Current Bar Data
| Metric           | Value         |
|------------------|---------------|
"""
    for key, value in currentbar.items():
        markdown_output += f"| {key} | {value} |\n"


    return markdown_output

def serialize_signal_to_markdown_file_from_json_file(json_filepath,quiet=True):
    markdown_output = generate_markdown_from_json_file(json_filepath)
    markdown_filepath = json_filepath.replace('.json', '.md')
    try:  
      with open(markdown_filepath, 'w') as file:
          file.write(markdown_output)
          if not quiet:print(f">Markdown file saved to: {markdown_filepath}")
      return markdown_filepath
    except Exception as e:
      print(f"Error saving markdown file to {markdown_filepath} {e}")
      return None
  
def serialize_signal_to_json_file(i,t,o,signal_bar,current_bar,quiet=True,signal_dir="data/signals",ext="json",indent=2):
      
      tlid_id=o["tlid_id"]
      o["i"]=i
      o["t"]=t
      o["signalbar"]=signal_bar.to_dict()
      o["currentbar"]=current_bar.to_dict()
      
      signal_fn = create_signal_filename(i,t, tlid_id, ext)
      signal_savepath =os.path.join(signal_dir,signal_fn)
      try:      
        os.makedirs(signal_dir,exist_ok=True)
        json.dump(o,open(signal_savepath,"w"),indent=indent)
        if not quiet:print(f">Signal saved to :{signal_savepath}")
        return signal_savepath
      except Exception as e:
        print(f"Error saving signal to {signal_savepath} {e}")
        return None

def create_signal_savepath(i,t, tlid_id, ext, signal_dir="data/signals"):
    signal_fn = create_signal_filename(i,t, tlid_id, ext)
    signal_savepath =os.path.join(signal_dir,signal_fn)
    return signal_savepath

def create_signal_filename(i,t, tlid_id, ext):
    ifn=i.replace("/","-")
    filename = f"{ifn}_{t}_{tlid_id}.{ext}"
    return filename