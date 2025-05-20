# File: logic/ssvep.py
from .base_logic import BaseLogic
import numpy as np
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
import constants

class SSVEP(BaseLogic):
    """
    定常視覚誘発電位(SSVEP)解析モジュール
    """
    def __init__(self, board, window_seconds=2.0, target_freqs=None, fs=None):
        super().__init__(board)
        self.window_seconds = window_seconds
        self.fs = fs or constants.SAMPLING_RATE
        self.target_freqs = target_freqs or constants.SSVEP_TARGET_FREQUENCIES
        self.n_samples = int(self.window_seconds * self.fs)

    def get_data_dict(self):
        data = self.board.get_current_board_data(self.n_samples)[constants.EEG_CHANNELS]
        # ノイズ除去
        DataFilter.perform_bandpass(data, self.fs, 5.0, 50.0, 4, FilterTypes.BUTTERWORTH.value, 0)
        # FFT
        fft_vals = np.fft.rfft(data, axis=1)
        fft_freqs = np.fft.rfftfreq(self.n_samples, d=1/self.fs)
        # 周波数ピーク検出
        power = np.abs(fft_vals)**2
        scores = []
        for f in self.target_freqs:
            idx = np.argmin(np.abs(fft_freqs - f))
            scores.append(np.mean(power[:, idx]))
        best_idx = int(np.argmax(scores))
        return { 'Intent_SSVEP': float(best_idx) }
