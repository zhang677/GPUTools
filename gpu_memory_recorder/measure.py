from utils.memory_recorder import gpu_memory_recorder
import torch
import os
import argparse

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--gpuid", type=int, default=0)
  parser.add_argument("--process", type=int, default=0)
  parser.add_argument("--interval", type=float, default=0.2)
  args = parser.parse_args()

  # the directory where the memory data will be saved
  log_dir = 'logs'

  if (not os.path.exists(log_dir)):
      os.makedirs(log_dir)

  # the name of the file where the data will be saved, if None, a name will
  # be generated automatically
  mem_usage_filename = str(args.process)+'.txt'

  # interval for probing the gpu (in seconds)
  interval = args.interval

  # gpu id
  gpu_id = args.gpuid

  # create the mem recorder object
  mem_recorder = gpu_memory_recorder(gpu_id=gpu_id,
                                    log_dir=log_dir,
                                    process_id=args.process,
                                    log_filename=mem_usage_filename,
                                    recording_interval=interval)  

  # start recording
  mem_recorder.start_recording()

  # User control when to stop
  stop_sig = input("Measuring... Type anything to stop: \n")

  # stop recording
  mem_recorder.stop_recording()

  # save chart in log folder
  mem_recorder.generate_chart()