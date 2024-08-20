


import tlid
from jgtutils import iprops
from jgtutils.jgtconstants import \
  HIGH,LOW,FDB,ASKHIGH,ASKLOW,BIDHIGH,BIDLOW,JAW,TEETH,LIPS,BJAW,BTEETH,BLIPS,DATE

#@STCGoal Standardize the Signal Columns
from mlconstants import (
  NORMAL_MOUTH_IS_OPEN_COLNAME,
  CURRENT_BAR_IS_OUT_OF_NORMAL_MOUTH_COLNAME,
  CURRENT_BAR_IS_IN_BIG_TEETH_COLNAME,
  BIG_MOUTH_IS_OPEN_AND_CURRENT_BAR_IS_IN_BIG_LIPS_COLNAME,
  MOUTH_IS_OPEN_AND_CURRENT_BAR_IS_IN_BIG_TEETH_COLNAME,
  CURRENT_BAR_IS_IN_TIDE_TEETH_COLNAME,
  TIDE_MOUTH_IS_OPEN_AND_CURRENT_BAR_IS_IN_TIDE_LIPS_COLNAME,
  MOUTH_IS_OPEN_AND_CURRENT_BAR_IS_IN_TIDE_TEETH_COLNAME
)

from jgtutils.iprops import \
  get_pips

def get_entry_stop_rate_ticked(i,bs,entry_rate,stop_rate,tick_shift=1,rouding_add = 2,t=None):
  pips=get_pips(i)
  tick_size=pips/10
  
  decimal_places = len(str(pips).split('.')[1]) + rouding_add if '.' in str(pips) else 1
  if bs=="B":
    entry_rate+=tick_size*tick_shift
    stop_rate-=tick_size*tick_shift
  else:
    if bs=="S":
      entry_rate-=tick_size*tick_shift
      stop_rate+=tick_size*tick_shift
  entry_rate = round(entry_rate, decimal_places)
  stop_rate = round(stop_rate, decimal_places)
  return entry_rate,stop_rate
  

def valid_gator(last_bar_completed,current_bar,bs):
  last_bar_mouth_is_open_and_price_is_out = is_mouth_open_and_bar_out_of_it(last_bar_completed,bs)
  cur_bar_mouth_is_open_and_price_is_out = is_mouth_open_and_bar_out_of_it(current_bar,bs)
  return \
    last_bar_mouth_is_open_and_price_is_out \
      and \
        cur_bar_mouth_is_open_and_price_is_out



def is_mouth_open_and_bar_out_of_it(bar,bs)->bool:
  return is_bar_out_of_mouth(bar,bs) and is_mouth_open(bar,bs)


def is_bar_out_of_mouth(bar,bs)->bool:
  mouth_open_reverse = is_mouth_open(bar,"B") if bs=="S" else is_mouth_open(bar,"S")
  if bs=="B":
    return bar[HIGH] < bar[LIPS] \
      and \
        not mouth_open_reverse
  if bs=="S":
    return bar[LOW] > bar[LIPS] \
      and \
        not mouth_open_reverse
  
def is_mouth_open(bar,bs)->bool:
  if bs=="B":
    return  bar[LIPS] < bar[TEETH] and bar[TEETH] < bar[JAW] and  bar[LIPS] < bar[JAW]
  if bs=="S":
    return  bar[LIPS] > bar[TEETH] and bar[TEETH] > bar[JAW]and  bar[LIPS] > bar[JAW]
  
def is_big_mouth_open(bar,bs)->bool:
  if bs=="B":
    return  bar[BLIPS] < bar[BTEETH] and bar[BTEETH] < bar[BJAW] and  bar[BLIPS] < bar[BJAW]
  if bs=="S":
    return  bar[BLIPS] > bar[BTEETH] and bar[BTEETH] > bar[BJAW]and  bar[BLIPS] > bar[BJAW]

def is_fdbsignal_crossed_t(bar,bs,tcol):
  if bs=="B":
    return bar[HIGH] < bar[tcol]
  if bs=="S":
    return bar[LOW] > bar[tcol]

def is_fdbsignal_in_big_mouth(bar,bs):
  return is_fdbsignal_crossed_t(bar,bs,BLIPS)
  
def is_fdbsignal_in_big_mouth_teeth(bar,bs):
  return is_fdbsignal_crossed_t(bar,bs,BLIPS)

def create_fdb_entry_order(i,signal_bar,current_bar,lots=1,tick_shift=2,quiet=True,valid_gator_mouth_open_in_mouth=False,valid_sig_out_mouth=True,t=None,validation_timestamp=None):
  had_valid_signal=False
  current_bar_broke_signal=True
  
  tlid_id = tlid.get_seconds()
  
  if signal_bar[FDB]==1:
    
    askhigh = signal_bar[ASKHIGH]
    bidlow = signal_bar[BIDLOW]
    
    entry_rate,stop_rate=get_entry_stop_rate_ticked(i,"B",askhigh,bidlow,tick_shift=tick_shift,t=t)

    buysell="B"
    had_valid_signal=True
    #check of the current_bar make the signal invalid by being out of range (means the entry_rate is already hit or it passed the stop_rate (making it invalid))
    cur_askhigh = current_bar[ASKHIGH]
    cur_bidlow = current_bar[BIDLOW]
    
    if cur_askhigh<=entry_rate and cur_bidlow>=stop_rate :
      current_bar_broke_signal=False
    if not quiet:print(f"cur_askhigh:{cur_askhigh} entry_rate:{entry_rate} cur_bidlow:{cur_bidlow} stop_rate:{stop_rate}")
  if signal_bar[FDB]==-1:
    #print(f"# Sell Signal on {i}")
    
    bidlow = signal_bar[BIDLOW]
    askhigh = signal_bar[ASKHIGH]
    
    entry_rate,stop_rate=get_entry_stop_rate_ticked(i,"S",bidlow,askhigh,tick_shift=tick_shift,t=t)

    buysell="S"
    had_valid_signal=True
    
    cur_bidlow = current_bar[BIDLOW]
    cur_askhigh = current_bar[ASKHIGH]
    
    if cur_bidlow>=entry_rate and cur_askhigh<=stop_rate:
      current_bar_broke_signal=False
    
    if not quiet:print(f"cur_bidlow:{cur_bidlow} entry_rate:{entry_rate} cur_askhigh:{cur_askhigh} stop_rate:{stop_rate}")
  
  if  current_bar_broke_signal and had_valid_signal:
    print(f"## Current Bar Broke the Signal {i}")
    return None
  
  if not had_valid_signal:
    return None
  
  if valid_gator_mouth_open_in_mouth \
    and \
      not valid_gator(signal_bar,current_bar,buysell):
    print(f"## Invalid Gator {i} valid_gator_mouth_open_in_mouth")
    return None
  
  if valid_sig_out_mouth \
    and \
      not is_bar_out_of_mouth(current_bar,buysell):
    print(f"## Invalid Gator {i} not valid_sig_out_mouth")
    return None
  #Get 'Date' or index of the signal bar
  
  validation_timestamp_str=validation_timestamp.strftime("%Y-%m-%d %H:%M") if validation_timestamp is not None else ""
  
  output_script = generate_entry_order_script(lots, entry_rate, stop_rate, i, buysell,tlid_id=tlid_id,t=t,validation_timestamp_str=validation_timestamp_str)
  
  o = build_order_result_object(lots, entry_rate, stop_rate, buysell, tlid_id, output_script,i,t)
  
  return o

def build_order_result_object(lots, entry_rate, stop_rate, buysell, tlid_id, output_script,i,t):
    o={}
    o["sh"]=output_script
    o["entry"]=entry_rate
    o["stop"]=stop_rate
    o["bs"]=buysell
    o["lots"]=lots
    o["tlid_id"]=tlid_id
    o["i"]=i
    o["t"]=t
    return o


def generate_entry_order_script(lots, entry_rate, stop_rate, instrument, buysell,tlid_id=None,t=None,validation_timestamp_str=""):
    timeframe=t if t is not None else "_"
    if tlid_id is None:
      tlid_id = tlid.get_seconds()
    output_script=f"""
```sh
### --- COPY FROM HERE --- ts:{validation_timestamp_str}
# Entry Order for {instrument} {timeframe} {buysell} 
demo_arg=" --demo"
tlid_id={tlid_id}
jgtnewsession $tlid_id {instrument} {timeframe} {entry_rate} {stop_rate} {buysell} {lots} $demo_arg
### ---- COPY TO HERE ---
```
"""
    
    return output_script

def generate_entry_order_script_pto1(lots, entry_rate, stop_rate, instrument, buysell):
    output_script=f"""
```sh
entry_rate={entry_rate};stop_rate={stop_rate};instrument={instrument};buysell={buysell};lots={lots}
s=CreateEntryOrderPtoAddStop.py
python $s $real_fx_cli_base_args -lots $lots -r $entry_rate -d $buysell -i $instrument -stop $stop_rate  | tee __output.txt  && \
OrderID=$(cat __output.txt| grep -o 'OrderID=[0-9]*' | cut -d '=' -f2) && \
echo "OrderID: $OrderID"
```
"""
    
    return output_script


def get_iprop(i):
  return iprops.get_iprop(i)