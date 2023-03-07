import subprocess
import time
import numpy as np
from . import on_parent_exit
import re
import os
from .logger import Logger

import matplotlib.pyplot as plt


class gpu_memory_recorder(object):
    def __init__(self,
                 recording_interval=0.2,
                 gpu_id=0,
                 process_id=0,
                 log_dir='.',
                 log_filename=None):

        assert(isinstance(gpu_id, int))

        assert(isinstance(process_id, int))

        assert(isinstance(recording_interval, int) or 
               isinstance(recording_interval, float))

        self.recording_interval = recording_interval
        self.process_id = process_id
        self.gpu_id = gpu_id

        self.logger = Logger('GPU_memory_recorder',
                             note=str(self.process_id) + '@gpu' + str(self.gpu_id))

        self.log_dir = log_dir
       
        if (log_filename is None):
            self.log_filename = 'gpu_mem_log_' + time.strftime("%Y_%m_%d_%H_%M") + \
                                '_' + str(self.process_id) + '.txt'
        else:
            self.log_filename = log_filename

        try:
            # delete the recording if the file already exits
            os.remove(os.path.join(self.log_dir, self.log_filename))
        except OSError:
            pass

        self.recording = False


    def start_recording(self):
        # watch -n 0.1 nvidia-smi -q -i 1 | grep "Used GPU Memory" | grep -Eo "[0-9]{1,5}" >> gpu_memory_with_alloc_long.txt'
        #nvidia-smi -q -i 0 | grep -A 3 "1416" | grep "Memory" | grep -Eo "[0-9]{1,5}"

        #cmd = ['bash', '-c', 'while true; do nvidia-smi -q -i ' + str(self.gpu_id) + \
        #       ' | grep -A 3 "'+ str(self.process_id) +'" | grep "Memory" |' + \
        #       ' grep -Eo "[0-9]{1,5}" >> ' + os.path.join(self.log_dir, self.log_filename) + \
        #       '; sleep ' + str(self.recording_interval) + '; done;']
        # The process id is protected
        cmd = ['bash', '-c', 'while true; do nvidia-smi -q -i ' + str(self.gpu_id) + \
               ' | grep "Used GPU Memory" |' + \
               ' grep -Eo "[0-9]{1,5}" >> ' + os.path.join(self.log_dir, self.log_filename) + \
               '; sleep ' + str(self.recording_interval) + '; done;']
        
        print(cmd)

        self.p = subprocess.Popen(cmd, preexec_fn=on_parent_exit.on_parent_exit('SIGHUP'))

        self.logger.log('started logging GPU memory usage with process ID', self.p.pid)
        self.logger.log('logging process id', self.process_id, 'on gpu', self.gpu_id)

        self.recording = True


    def stop_recording(self):
        if (self.recording):
            self.logger.log('stopping the GPU logging process with ID', self.p.pid)

            self.p.terminate()
        else:
            self.logger.log('hey! GPU logging was not started!')


    def generate_chart(self, how_many=-1):
        try:
            assert(os.path.exists(os.path.join(self.log_dir, self.log_filename)))
        except AssertionError:
            self.logger.log(self.logger.red(os.path.join(self.log_dir, self.log_filename) + ' not found!'))

            return

        data = np.loadtxt(os.path.join(self.log_dir, self.log_filename))

        if (how_many != -1):
            data = data[-1 * how_many:]

        x_labels = np.array(range(data.shape[0]))

        fig, ax = plt.subplots(1)
        plt.title('GPU memory usage')

        plt.xlabel('Time')
        plt.ylabel('Memory')

        plt.plot(x_labels, data, '-r', label='memory')
        
        ax.legend(loc='lower right')

        chart_name = os.path.join(self.log_dir, self.log_filename[:-4] + '.png')

        fig.savefig(chart_name, bbox_inches='tight')
        plt.close(fig)

        self.logger.log('chart saved at', chart_name)

    @property
    def log_dir(self):
        assert(os.path.exists(self._log_dir) and os.path.isdir(self._log_dir))

        return self._log_dir

    @log_dir.setter
    def log_dir(self, value):
        try:
            assert(os.path.exists(value) and os.path.isdir(value))
        except AssertionError:
            self.logger.log(self.logger.red('directory ' + value + ' not found!'))

            raise

        self._log_dir = value

    @property
    def log_filename(self):
        assert(re.match("^[\w_-]+\.txt$", self._log_filename))

        return self._log_filename

    @log_filename.setter
    def log_filename(self, value):
        try:
            assert(re.match("^[\w_-]+\.txt$", value))
        except AssertionError:
            self.logger.log(self.logger.red('log filename should only contain letteres, numbers or underscores and end with .txt'))

            raise

        self._log_filename = value

    @property
    def process_id(self):
        assert(isinstance(self._process_id, int))

        return self._process_id

    @process_id.setter
    def process_id(self, value):
        assert(isinstance(value, int))

        self._process_id = value

    @property
    def gpu_id(self):
        assert(isinstance(self._gpu_id, int))

        return self._gpu_id

    @gpu_id.setter
    def gpu_id(self, value):
        assert(isinstance(value, int))

        self._gpu_id = value

    @property
    def recording_interval(self):
        assert(isinstance(self._gpu_id, int))

        return self._recording_interval

    @recording_interval.setter
    def recording_interval(self, value):
        assert(isinstance(value, int) or isinstance(value, float))

        self._recording_interval = value

