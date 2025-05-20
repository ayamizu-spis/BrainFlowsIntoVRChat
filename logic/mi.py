# File: logic/mi.py
from .base_logic import BaseLogic
import numpy as np
from brainflow.data_filter import DataFilter, FilterTypes
from model.mi_model import load_csp, load_lda, apply_csp
import constants

class MI(BaseLogic):
    """
    運動想起(MI)解析モジュール (CSP + LDA)
    """
    def __init__(self, board, fs=None):
        super().__init__(board)
        self.fs = fs or constants.SAMPLING_RATE
        self.window_seconds = constants.MI_WINDOW_SECONDS
        self.n_samples = int(self.window_seconds * self.fs)
        # モデルロード
        self.csp_filters = load_csp(constants.MI_CSP_MODEL_PATH)
        self.lda = load_lda(constants.MI_LDA_MODEL_PATH)

    def get_data_dict(self):
        data = self.board.get_current_board_data(self.n_samples)[constants.EEG_CHANNELS]
        # バンドパスフィルタ 8-30Hz
        DataFilter.perform_bandpass(data, self.fs, *constants.MI_BAND, 4, FilterTypes.BUTTERWORTH.value, 0)
        # CSP特徴抽出
        features = apply_csp(self.csp_filters, data)
        # LDA分類
        label = self.lda.predict(features.reshape(1, -1))[0]
        return { 'Intent_MI': float(label) }