# File: logic/mi.py
from .base_logic import BaseLogic
import numpy as np
from brainflow.data_filter import DataFilter, FilterTypes
import pickle
import constants

class MI(BaseLogic):
    """
    運動想起(MI)解析モジュール (CSP + LDA 統合版)
    """
    def __init__(self, board, fs=None, window_seconds=None):
        super().__init__(board)
        self.fs = fs or constants.SAMPLING_RATE
        self.window_seconds = window_seconds or constants.MI_WINDOW_SECONDS
        self.n_samples = int(self.window_seconds * self.fs)
        # 統合済みモデル読み込み
        self.csp_filters = self._load_pickle(constants.MI_CSP_MODEL_PATH)
        self.lda_model = self._load_pickle(constants.MI_LDA_MODEL_PATH)

    def _load_pickle(self, path):
        with open(path, 'rb') as f:
            return pickle.load(f)

    def _apply_csp(self, filters, data):
        # CSPフィルタ行列を適用し、各成分の分散を特徴量とする
        projected = filters.dot(data)
        var = np.var(projected, axis=1)
        return var / np.sum(var)

    def get_data_dict(self):
        # EEGチャネルデータ取得
        data = self.board.get_current_board_data(self.n_samples)[constants.EEG_CHANNELS]
        # バンドパスフィルタ 8-30Hz
        DataFilter.perform_bandpass(
            data, self.fs, *constants.MI_BAND, 4, FilterTypes.BUTTERWORTH.value, 0
        )
        # 特徴量抽出と分類
        features = self._apply_csp(self.csp_filters, data)
        label = self.lda_model.predict(features.reshape(1, -1))[0]
        return { 'Intent_MI': float(label) }z
