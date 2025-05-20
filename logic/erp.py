# File: logic/erp.py
from .base_logic import BaseLogic
import numpy as np
import constants

class ERP(BaseLogic):
    """
    事象関連電位(ERP)解析モジュール (P300検出)
    """
    def __init__(self, board, fs=None):
        super().__init__(board)
        self.fs = fs or constants.SAMPLING_RATE
        self.window_ms = constants.ERP_WINDOW_MS
        self.n_samples = int(self.window_ms * self.fs / 1000)
        self.epoch_buffer = []
        self.max_epochs = constants.ERP_MAX_EPOCHS

    def add_epoch(self, marker_time):
        # マーカー時刻からエポックを切り出し保存
        raw = self.board.get_board_data(constants.EEG_CHANNELS)
        idx = int((marker_time - self.board.get_board_timestamp()) * self.fs)
        if idx >= 0 and idx + self.n_samples <= raw.shape[1]:
            epoch = raw[:, idx:idx + self.n_samples]
            self.epoch_buffer.append(epoch)
            if len(self.epoch_buffer) > self.max_epochs:
                self.epoch_buffer.pop(0)

    def get_data_dict(self):
        if not self.epoch_buffer:
            return { 'Intent_ERP': 0.0 }
        # エポック平均
        mean_epoch = np.mean(np.stack(self.epoch_buffer), axis=0)
        # P300振幅 (300ms付近)
        p_idx = int(0.3 * self.fs)
        p_amplitude = np.max(mean_epoch[:, p_idx])
        detected = 1.0 if p_amplitude > constants.ERP_THRESHOLD else 0.0
        return { 'Intent_ERP': detected }