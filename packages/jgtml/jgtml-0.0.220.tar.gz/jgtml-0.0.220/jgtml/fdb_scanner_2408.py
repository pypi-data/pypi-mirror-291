# %%

import os
import json
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import pandas as pd
from datetime import datetime,timedelta
import tlid

from jgtutils.coltypehelper import DTYPE_DEFINITIONS

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

# Validity of cache
def is_timeframe_cached_valid(df, timeframe:str,use_utc=True,quiet=True):
  """
  Checks if the cached data is still valid for the given timeframe.

  Args:
    df: The cached DataFrame.
    timeframe: The timeframe to check.

  Returns:
    True if the cache is valid, False otherwise.
  """

  # Get the last bar's timestamp.
  if "Date" in df.columns:
    last_bar_timestamp = df.iloc[-1]["Date"]
  else:
    last_bar_timestamp = df.index[-1]
  
  # Ensure the timestamp is in UTC if required
    if use_utc:
      last_bar_timestamp = pd.to_datetime(last_bar_timestamp, utc=True)
      now = datetime.utcnow().replace(tzinfo=pd.Timestamp.utcnow().tzinfo)
    else:
      last_bar_timestamp = pd.to_datetime(last_bar_timestamp)
      now = datetime.now()
  if not quiet:
    print(f"DEBUG::UTC::last_bar_timestamp:{last_bar_timestamp} now:{now}")
  # Calculate the valid range for the timeframe.
  if timeframe == "m1":
    valid_range = pd.Timedelta(minutes=1)
  elif timeframe == "m5":
    valid_range = pd.Timedelta(minutes=5)
  elif timeframe == "m15":
    valid_range = pd.Timedelta(minutes=15)
  elif timeframe == "m30":
    valid_range = pd.Timedelta(minutes=30)
  elif timeframe == "H1":
    valid_range = pd.Timedelta(hours=1)
  elif timeframe == "H2":
    # Calculate the next expiration time for H2 timeframe
    next_expiration = last_bar_timestamp.replace(minute=0, second=0, microsecond=0)
    while next_expiration <= now:
      next_expiration += timedelta(hours=2)
    is_within_expiration = now < next_expiration
    return is_within_expiration
  elif timeframe == "H3":
    next_expiration = last_bar_timestamp.replace(minute=0, second=0, microsecond=0)
    while next_expiration <= now:
      next_expiration += timedelta(hours=3)
    is_within_expiration = now < next_expiration
    return is_within_expiration
  elif timeframe == "H4":
    # Calculate the next expiration time for H4 timeframe
    next_expiration = last_bar_timestamp.replace(minute=0, second=0, microsecond=0)
    while next_expiration <= now:
      next_expiration += timedelta(hours=4)
    is_within_expiration = now < next_expiration
    return is_within_expiration
  elif timeframe == "H6":
    next_expiration = last_bar_timestamp.replace(minute=0, second=0, microsecond=0)
    while next_expiration <= now:
      next_expiration += timedelta(hours=6)
    is_within_expiration = now < next_expiration
    return is_within_expiration
  elif timeframe == "H8":
    next_expiration = last_bar_timestamp.replace(minute=0, second=0, microsecond=0)
    while next_expiration <= now:
      next_expiration += timedelta(hours=8)
    is_within_expiration = now < next_expiration
    return is_within_expiration
  elif timeframe == "D1":
    valid_range = pd.Timedelta(days=1)
  elif timeframe == "W1":
    valid_range = pd.Timedelta(days=7)
  elif timeframe == "M1":
    valid_range = pd.Timedelta(days=30)
  else:
    raise ValueError("Invalid timeframe.")
  if not quiet:
    print("DEBUG::valid_range:",valid_range)
  # Check if the last bar's timestamp is within the valid range.
  return last_bar_timestamp + valid_range > now


# %% [markdown]
# # --@STCGoal Proto Scan FDB Signal Analysis
# 

# %%
from jgtpy import JGTCDSSvc as svc

from jgtutils.jgtconstants import LOW,HIGH,FDB

import JGTBalanceAnalyzer as ba
import pandas as pd

# %% [markdown]

# # CDS Data gets added ctx bar Ctx gator
use_cache=True
cds_cache_file_suffix = "_cds_cache"
cache_root_dir="/var/lib/jgt/cache"
#look if writable, able to create otherwise use $HOME/.cache/jgt/cache
if not os.access(cache_root_dir, os.W_OK):
    cache_root_dir=os.path.join(os.getenv("HOME","~"),".cache/jgt/cache")
    try:
      os.makedirs(cache_root_dir,exist_ok=True)
    except:
      raise Exception("Unable to create cache dir")
    print("Using HOME cache dir")
    if not os.access(cache_root_dir, os.W_OK):
        print("Cache dir not writable")
        raise Exception("Cache dir not writable")
# 
# 

# %%
def _make_cached_filepath(i, t,subdir="fdb_scanners",ext="csv",suffix=""):
  ifn=i.replace("/","-")
  fn = f"{ifn}_{t}{suffix}.{ext}"
  #make sure the subdir exists
  cache_dir_fullpath=os.path.join(cache_root_dir,subdir)
  os.makedirs(cache_dir_fullpath,exist_ok=True)
  fpath=os.path.join(cache_dir_fullpath,fn)
  return fpath.replace("..",".")

def generate_fresh_and_cache(_i,_t,_quotescount=300,cache_filepath=None):
    if cache_filepath is None:
      cache_filepath = _make_cached_filepath(_i, _t,suffix=cds_cache_file_suffix)
    dfsrc:pd.DataFrame=svc.get(_i,_t,quotescount=_quotescount)
    dfsrc.to_csv(cache_filepath)
    return dfsrc

def main():

  # %%
  # i="SPX500"
  # i="NZD/CAD"
  # t="D1"
  quotescount=333
  lots=2

  md_df_tail_amount = 50
  outdir="output"
    
  contexes_all = {
      "tide": {"title": "Tide Alligator"},
      "big": {"title": "Big Alligator", "name": "big"},
      "normal": {"title": "Normal Alligator", "name": "normal"}
  }
  contexes = {
      "tide": {"title": "Tide Alligator"},
      "big": {"title": "Big Alligator", "name": "big"}
  }

  save_bars=False

  instruments = "AUD/NZD,NZD/CAD,AUD/CAD,SPX500,EUR/USD,GBP/USD,XAU/USD,USD/CAD"
  instruments = "AUD/NZD,NZD/CAD,AUD/CAD"
  instruments = "SPX500,EUR/USD,GBP/USD,AUD/USD,XAU/USD,USD/CAD,AUS200,USD/JPY,EUR/CAD,AUD/CAD,NZD/CAD,AUD/NZD"
  instruments="SPX500"
  instruments = "SPX500,EUR/USD,GBP/USD,AUD/USD,XAU/USD,USD/CAD,USD/JPY,EUR/CAD,AUD/CAD,NZD/CAD,AUD/NZD,CAD/JPY"

  instruments=os.getenv("INSTRUMENTS",instruments)
  if os.getenv("INSTRUMENTS") is not None:
      print("INSTRUMENTS loaded from environment")
  lots = int(os.getenv("LOTS",lots))
  if os.getenv("LOTS") is not None:
      print("LOTS loaded from environment")
      
  timeframes = "H1,m15,m5,m1"
  timeframes = "D1,H4,H1,m15,m5,m1"
  timeframes = "D1,H4,H2,H1,m15,m5,m1"
  timeframes = "H8,H6,H4,H3,H2,H1,m15,m5"
  timeframes = "H8,H4,H1,m15,m5"
  timeframes = "m15,m5,m1"
  timeframes = "H4,H1,m15,m5"
  timeframes = "M1,W1,D1,H4,H1,m15,m5"
  timeframes = "D1,H4,H1,m15,m5"
  timeframes = "m15,m5,m1"
  timeframes = "H1,m15,m5"
  timeframes = "D1,H4,H1,m15,m5"
  timeframes = os.getenv("TIMEFRAMES",timeframes)
  if os.getenv("TIMEFRAMES") is not None:
    print("TIMEFRAMES loaded from environment")

  previous_tlid_id = tlid.get_seconds()

      
  for i in instruments.split(","):

    for t in timeframes.split(","):
      if t == " " or t == "":
        continue
      output_string = f"# Scanning: {i} {t} "
      
      cache_filepath = _make_cached_filepath(i, t,suffix=cds_cache_file_suffix)

      try:
        dfsrc=pd.read_csv(cache_filepath,index_col=0,parse_dates=True,dtype=DTYPE_DEFINITIONS)
      except:
        dfsrc:pd.DataFrame=generate_fresh_and_cache(i,t,quotescount,cache_filepath)
    
      if not is_timeframe_cached_valid(dfsrc, t):
        dfsrc=generate_fresh_and_cache(i,t,quotescount)
      
      validation_timestamp = dfsrc.index[-1]
      from jgtutils.jgtos import tlid_dt_to_string
      output_string += f" {tlid_dt_to_string(validation_timestamp)}"
    
      current_bar = dfsrc.iloc[-1]
      signal_bar = dfsrc.iloc[-2]
      if save_bars:
          current_bar_fn=_make_cached_filepath(i,t,suffix="_currentbar")
          last_bar_completed_fn=_make_cached_filepath(i,t,suffix="_signalbar")
          current_bar.to_csv(current_bar_fn,index=True) 
          signal_bar.to_csv(last_bar_completed_fn,index=True) 


      
      # %%
      tlid_id = tlid.get_seconds()
      while tlid_id == previous_tlid_id:
        tlid_id = tlid.get_seconds()
        #print(".",end="")
      
      from SignalOrderingHelper import create_fdb_entry_order
      valid_gator_mouth_open_in_mouth=False
      valid_sig_out_mouth=True
      o=create_fdb_entry_order(i,signal_bar,current_bar,lots=lots,t=t,
                                          valid_gator_mouth_open_in_mouth=valid_gator_mouth_open_in_mouth,
                                          valid_sig_out_mouth=valid_sig_out_mouth,validation_timestamp=validation_timestamp)
      if o is not None:
        sh=o["sh"]
        #output_string+="\n"
        #output_string+="\n----\n"
        _found_signal_string = f" - Signal Found"
        output_string+=_found_signal_string
        output_string+=sh
        print(output_string)
        from JGTOutputHelper import serialize_signal_to_json_file,serialize_signal_to_markdown_file_from_json_file
        signal_savepath=serialize_signal_to_json_file(i,t,o,signal_bar,current_bar)
        md_filepath=serialize_signal_to_markdown_file_from_json_file(signal_savepath)
      else:
        print(output_string)

      
      previous_tlid_id = tlid_id
      
      
      process_balancing=False


      if process_balancing:

        # %%

        # #refresh the import
        # import importlib
        # importlib.reload(ba)

        r={}
        _df=None
        for bs in ["B","S"]:
          obs={}
          print("bs:",bs)
          for ctx_name,v in contexes.items():
            o={}
            #_df=dfsrc if o["df"] is None else o["df"] # Reused the new df
            if _df is None:
              _df=dfsrc
            #_df=dfsrc if _df is None else _df
            ocols=ba.generate_column_names_for_direction(ctx_name,bs)
            ctx_evaltitle =v["title"]
            o["ctx_evaltitle"]=ctx_evaltitle
            o["name"]=ctx_name
            print("k:",ctx_name," v:",ctx_evaltitle)
            #sig_ctx_mouth_is_open_and_in_ctx_lips
            df_filter=ba.filter_sig_ctx_mouth_is_open_and_in_ctx_lips(_df,bs,ctx_name)
            new_col="sig_ctx_mouth_is_open_and_in_ctx_lips"
            _df=ba.add_sig_ctx_mouth_is_open_and_in_ctx_lips(_df,bs,ctx_name,None)
            #add_sig_ctx_mouth_is_open_and_in_ctx_lips_sell
            #print(df.tail(2))
            o["df"]=_df
            o["df_filter"]=df_filter
            obs[ctx_name]=o
          r[bs]=obs
          
          #df_sig_is_in_ctx_teeth = filter_sig_is_in_ctx_teeth_sell(df_sig_is_out_of_normal_mouth, cteeth_colname, teval_colname) if bs=="S" else filter_sig_is_in_ctx_teeth_buy(df_sig_is_out_of_normal_mouth, cteeth_colname, teval_colname)
          # df_sig_is_in_ctx_teeth = filter_sig_is_in_ctx_teeth_sell(df_sig_is_out_of_normal_mouth, cteeth_colname, teval_colname) if bs=="S" else filter_sig_is_in_ctx_teeth_buy(df_sig_is_out_of_normal_mouth, cteeth_colname, teval_colname)
          
          
            

        # %%

        os.makedirs(outdir,exist_ok=True)

        rb=r["B"]
        rs=r["S"]
        content=f"""

        """

        for ctx_name,v in contexes.items():
          ctx_evaltitle =v["title"]
          rb_ctx=rb[ctx_name]
          rs_ctx=rs[ctx_name]
          print("ctx_name:",ctx_name)
          rb_ctx_df=rb_ctx["df"]
          rs_ctx_df=rs_ctx["df"]
          #save
          df_outputfile = _make_cached_filepath(i,t,subdir=outdir,suffix=f"_bs")
          _df.to_csv(df_outputfile)
          
          #make some markdown output
          content=content+f"""

  # Total number of rows:
  {len(rb_ctx_df)}
        
  # {ctx_evaltitle} Buy
  {rb_ctx_df.tail(md_df_tail_amount).to_markdown()}

  ## Columns
  {rb_ctx_df.columns.to_list()}

  # {ctx_evaltitle} Sell
  {rs_ctx_df.tail(md_df_tail_amount).to_markdown()}

  ## Columns
  {rs_ctx_df.columns.to_list()}

          """

        #save
        md_output_filepath = _make_cached_filepath(i,t,subdir=outdir,suffix=f"_ctx",ext="md")
        with open(md_output_filepath,"w") as f:
            f.write(content)
          
          
      # # %%

      # rb_tide=rb["tide"]
      # rs_tide=rs["tide"]

      # # %%

      # rb_tide_df=rb_tide["df"]
      # rs_tide_df=rs_tide["df"]

      # # %%

      # rb_tide_df.to_csv(f"{outdir}/rb_tide_df.csv")
      # rs_tide_df.to_csv(f"{outdir}/rs_tide_df.csv")



if __name__ == "__main__":
    main()