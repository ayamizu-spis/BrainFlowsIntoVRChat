# BFiVRC: BrainFlowsIntoVRChat

これは私の[bci-workshop fork](https://github.com/ChilloutCharles/bci-workshop)のBrainFlow実装で、あなたの脳のリラクゼーションと集中のメトリクス、そしてEEG測定で一般的に使用される周波数帯に基づいた左右両方の頭のパワー値を送信します。機械学習を使用して脳波からアクションを読み取るロジックです。詳細については、`model/intent`ディレクトリのREADME.mdをお読みください。ハードウェアが対応している場合は、心拍数と呼吸の追加サポートが利用可能です。

## なぜBrainFlowなのか？

[BrainFlow](https://BrainFlow.org)ライブラリは、デバイスに依存しない統一されたAPIを提供し、私のワークショップフォークのこの実装がすべての[サポートされているバイオセンサー](https://BrainFlow.readthedocs.io/en/stable/SupportedBoards.html)（Museヘッドバンドを含む）で動作することを可能にします。追加のソフトウェアは必要ありません！

## デモ
- [Rantis's Brain Controlled Ears](https://twitter.com/RantiMess/status/1746704510972580061)
- [Brain Controlled Ears: Five Months Later [VRChat]](https://www.youtube.com/watch?v=kPPTT3ogEgg)
- [VRCHAT OSC MAGIC! (Last 30 seconds)](https://twitter.com/kentrl_z/status/1497020472046800897)
- [Old version of Brain Controlled Ears](https://www.youtube.com/watch?v=WjWc51xNgKg)

## 手順

1. このプロジェクトをフォルダにダウンロードし、そのフォルダパスを覚えておいてください
2. [Python 3.11.5](https://www.python.org/downloads/release/python-3115/)をインストールします
3. スタートメニューでcmdを検索してコマンドプロンプトを開きます
4. コマンドプロンプト内でプロジェクトのパスに移動します。
   - 例: `cd "C:\Users\<ここにユーザー名>\Documents\GitHub\BrainFlowsIntoVRChat"`
5. 次のコマンドを実行して、必要な依存関係をインストールします: `python -m pip install -r requirements.txt`
6. お使いのデバイスの名前またはボードIDを調べます: [Board IDs Page](https://brainflow.readthedocs.io/en/stable/UserAPI.html?highlight=MUSE_2016_BOARD#brainflow-board-shim)
7. ヘッドバンドの電源を入れます
8. デバイス名またはIDを指定してスクリプト`main.py`を実行します。たとえば、[Muse 2ヘッドバンド](https://choosemuse.com/muse-2/)で実行する場合のコマンドは次のようになります: `python .\main.py --board-id muse_2_board`

## OSCアバターパラメータスキーマ

VRChatに送信されるさまざまなアバターパラメータを次に示します。ニューロフィードバックスコアの範囲は、符号付きfloatの場合は-1から1、符号なしの場合は0から1で、値が高いほどリラックス/フォーカススコアが高くなり、低いほど低くなります。使用しているボードによっては、心拍数、呼吸、バッテリー情報が利用できる場合があります。パワーバンド番号も場所ごとに送信され、0から1の範囲で平均0.2です。

これらのパラメータをVRChat内で使用するには、パラメータ名をパスとして記述します。たとえば、左側のアルファ値を取得する場合、パラメータ名は次のようになります。
- `BFI/PwrBands/Left/Alpha`

```yaml
BFI:
  Info:
    - VersionMajor [int]
    - VersionMinor [int]
    - SecondsSinceLastUpdate [float]
    - DeviceConnected [bool]
    - BatterySupported [bool]
    - BatteryLevel [float]
  NeuroFB:
    - FocusLeft [float]
    - FocusLeftPos [float]
    - FocusRight [float]
    - FocusRightPos [float]
    - FocusAvg [float]
    - FocusAvgPos [float]
    - RelaxLeft [float]
    - RelaxLeftPos [float]
    - RelaxRight [float]
    - RelaxRightPos [float]
    - RelaxAvg [float]
    - RelaxAvgPos [float]
  PwrBands:
    Left:
      - Gamma [float]
      - Beta [float]
      - Alpha [float]
      - Theta [float]
      - Delta [float]
    Right:
      - Gamma [float]
      - Beta [float]
      - Alpha [float]
      - Theta [float]
      - Delta [float]
    Avg:
      - Gamma [float]
      - Beta [float]
      - Alpha [float]
      - Theta [float]
      - Delta [float]
  Addons:
    - HueShift [float 0-1]
  Biometrics:
    - Supported [bool]
    - HeartBeatsPerSecond [float]
    - HeartBeatsPerMinute [int]
    - OxygenPercent [float]
    - BreathsPerSecond [float]
    - BreathsPerMinute [int]
```

## 古いパラメータスキーマからの移行

既存のプレハブを移行する必要がありますか？このwikiを使用してパラメータ名を変換してください：[Migration of Old Parameters](https://github.com/ChilloutCharles/BrainFlowsIntoVRChat/wiki/Deprecation-of-Old-Parameters)

## パラメータの説明
### ユーティリティ
これらのユーティリティパラメータは、デバイスとBFiVRCに関する基本情報を提供します。
| パラメータ | 説明 | タイプ |
| ------ | ----- | ----- |
| BFI/Info/VersionMajor | 現在のパラメータスキーマのメジャーバージョン番号 | Int |
| BFI/Info/VersionMinor | 現在のパラメータスキーマのマイナーバージョン番号 | Int |
| BFI/Info/SecondsSinceLastUpdate | BFiVRCのデータストリームの更新レート | Float |
| BFI/Info/DeviceConnected | デバイスのBFiVRCへの接続ステータス | Bool |
| BFI/Info/BatterySupported | デバイスがBFiVRCへのバッテリーステータスの送信をサポートしているかどうか | Bool |
| BFI/Info/BatteryLevel | デバイスのバッテリーの現在の充電ステータス | Float |

### ニューロフィードバック
これらのパラメータは現在の精神状態に基づいて計算され、符号付きの正負両方のfloat範囲全体を利用します。
| パラメータ | 説明 | タイプ | 範囲 |
| ------ | ----- | ----- | ----- |
| BFI/NeuroFB/FocusLeft | 左 非集中から集中へ | Float | [-1.0, 1.0] |
| BFI/NeuroFB/FocusRight | 右 非集中から集中へ | Float | [-1.0, 1.0] |
| BFI/NeuroFB/FocusAvg | 非集中から集中へ | Float | [-1.0, 1.0] |
| BFI/NeuroFB/RelaxLeft | 左 興奮からリラックスへ | Float | [-1.0, 1.0] |
| BFI/NeuroFB/RelaxRight | 右 興奮からリラックスへ | Float | [-1.0, 1.0] |
| BFI/NeuroFB/RelaxAvg | 興奮からリラックスへ | Float | [-1.0, 1.0] |

これらは同じニューロフィードバックスコアで、必要に応じて正の0から1の範囲に再マッピングされます。
| パラメータ | 説明 | タイプ | 範囲 |
| ------ | ----- | ----- | ----- |
| BFI/NeuroFB/FocusLeftPos | 左 非集中から集中へ | Float | [0.0, 1.0] |
| BFI/NeuroFB/FocusRightPos | 右 非集中から集中へ | Float | [0.0, 1.0] |
| BFI/NeuroFB/FocusAvgPos | 非集中から集中へ | Float | [0.0, 1.0] |
| BFI/NeuroFB/RelaxLeftPos | 左 興奮からリラックスへ | Float | [0.0, 1.0] |
| BFI/NeuroFB/RelaxRightPos | 右 興奮からリラックスへ | Float | [0.0, 1.0] |
| BFI/NeuroFB/RelaxAvgPos | 興奮からリラックスへ | Float | [0.0, 1.0] |

### パワーバンド
これらのパラメータは、EEG測定で使用される一般的な周波数帯のパワー値を場所ごとに示します。各パワーバンドの意味の詳細については、こちらをお読みください：[What are Brainwaves](https://www.sciencedirect.com/topics/agricultural-and-biological-sciences/brain-waves)
| パラメータ | 説明 | タイプ | 範囲 |
| ------ | ----- | ----- | ----- |
| BFI/PwrBands/Left/Alpha | 左脳波アルファ帯 | Float | [0.0, 1.0] |
| BFI/PwrBands/Right/Alpha | 右脳波アルファ帯 | Float | [0.0, 1.0] |
| BFI/PwrBands/Avg/Alpha | 脳波アルファ帯 | Float | [0.0, 1.0] |
| BFI/PwrBands/Left/Beta | 左脳波ベータ帯 | Float | [0.0, 1.0] |
| BFI/PwrBands/Right/Beta | 右脳波ベータ帯 | Float | [0.0, 1.0] |
| BFI/PwrBands/Avg/Beta | 脳波ベータ帯 | Float | [0.0, 1.0] |
| BFI/PwrBands/Left/Theta | 左脳波シータ帯 | Float | [0.0, 1.0] |
| BFI/PwrBands/Right/Theta | 右脳波シータ帯 | Float | [0.0, 1.0] |
| BFI/PwrBands/Avg/Theta | 脳波シータ帯 | Float | [0.0, 1.0] |
| BFI/PwrBands/Left/Delta | 左脳波デルタ帯 | Float | [0.0, 1.0] |
| BFI/PwrBands/Right/Delta | 右脳波デルタ帯 | Float | [0.0, 1.0] |
| BFI/PwrBands/Avg/Delta | 脳波デルタ帯 | Float | [0.0, 1.0] |
| BFI/PwrBands/Left/Gamma | 左脳波ガンマ帯 | Float | [0.0, 1.0] |
| BFI/PwrBands/Right/Gamma | 右脳波ガンマ帯 | Float | [0.0, 1.0] |
| BFI/PwrBands/Avg/Gamma | 脳波ガンマ帯 | Float | [0.0, 1.0] |

### アドオン
これらのパラメータはBFiVRCの追加機能です
| パラメータ | 説明 | タイプ | 範囲 |
| ------ | ----- | ----- | ----- |
| BFI/Addons/HueShift | このパラメータは、リラックス/フォーカスの組み合わせを使用して、マテリアルFX用の単一のfloatパラメータを駆動します | Float | [0.0, 1.0] |

### バイオメトリクス
これらのパラメータは、ハードウェアでサポートされている場合、デバイスから他の生体データを読み取ります
| パラメータ | 説明 | タイプ | 範囲 |
| ------ | ----- | ----- | ----- |
| BFI/Biometrics/Supported | ハードウェアが心拍数と呼吸数の読み取りをサポートしている場合 | Bool | True/False |
| BFI/Biometrics/HeartBeatsPerSecond | 1秒あたりの心拍数 | Float | [0.0, inf) |
| BFI/Biometrics/HeartBeatsPerMinute | 1分あたりの心拍数 | Int | [0, 255] |
| BFI/Biometrics/OxygenPercent | 血中酸素飽和度 | Float | [0.0, 1.0] |
| BFI/Biometrics/BreathsPerSecond | 1秒あたりの推定呼吸数 | Float | [0.0, inf) |
| BFI/Biometrics/BreathsPerMinute | 1分あたりの推定呼吸数 | Int | [0, 255] |

## デバッグとロギング
- デバッグを容易にするために、`--debug`起動引数を追加します。これにより、送信されたすべてのOSCメッセージのデバッグメッセージがコンソールに表示され、VRChatのOSCデバッグパネルやその他のOSCディスプレイで読み取れるようにパラメータ名が短くなります。
- 毎秒値を記録するには、`--enable-logs`起動引数を追加します。これにより、`logs`フォルダの下にタイムスタンプ付きのログが作成され、アニメーションなどの調整に役立つ値の視覚化に役立ちます。

## 古いパラメータスキームの使用
このスキーマに更新することをお勧めします。ただし、アセットがまだ古いパラメータスキームを使用している場合は、`--use-old-reporter`起動引数を追加することでそれらに切り替えることができます。

## 追加: 実行コマンドの変更
### Muse2
- `python main.py --board-id MUSE_2_BOARD --mode normal`
- `python main.py --board-id MUSE_2_BOARD --mode ssvep`
- `python main.py --board-id MUSE_2_BOARD --mode erp`
- `python main.py --board-id MUSE_2_BOARD --mode mi`

### OpenBCI
- `python main.py --board-id CYTON_BOARD --serial-port <COMポート名>`

### Trial-Feature Branch Memo
OpenBCI Cytonや各測定法が動作するかの試験的な機能の実装

## 謝辞

感謝します
- PPG信号の作業を手伝ってくれた[@Mitzi_DelverVRC](https://twitter.com/Mitzi_DelverVRC)と[AartHark](https://github.com/AartHauk)
- 初期のユーザーテストを行ってくれた[@wordweaver1001](https://twitter.com/wordweaver1001)
- パラメータスキーマの作成を手伝ってくれた[AtriusX](https://github.com/AtriusX)
- 再接続再試行ロジックを強化してくれた[sync1211](https://github.com/sync1211)
- アクション分類モデルと統合の開発とテストを行ってくれた[Hosomi](https://twitter.com/FakeHosomi)、[Eni](https://github.com/eni-808)、[AtriusX](https://github.com/AtriusX)、[Rantis](https://github.com/RantiMess)、[DeliciousSalad](https://github.com/DeliciousSalad)
- 自己教師ありモデルの開発を行ってくれた[Summer](https://x.com/TheGoodAI1)とProgrammerboi
- 複数の記録されたセッションをトレーニングデータ収集に使用できるようにしてくれた[Scapsters](https://github.com/Scapsters)

## トラブルシューティング
- PCに内蔵されているBluetoothアダプタが壊れていて、代わりにドングルを使用したいのですが、ヘッドバンドをそのドングルに接続するにはどうすればよいですか？
  1. 使用したいBluetoothドングルを取り外します
  2. スタートメニューで「デバイスマネージャー」を検索します
  3. Bluetooth無線のエントリを見つけて右クリックし、無効にします
  4. 新しいBluetoothドングルを再度接続します

- Museヘッドバンドは正常に接続されますが、数秒後にタイムアウトします。解決策：ヘッドバンドをリセットします
  1. ヘッドバンドの電源を切ります
  2. 電源ボタンを長押しして電源を入れます。ライトが変わるまで押し続けます。
  3. 再接続します。

- すべてを設定し、新しいアバターを作成しましたが、まだ反応しません
  - 理由：VRChatはアバターのキャッシュされたOSCパラメータを保存しており、アバターが新しいパラメータで更新されても更新されません
  - 解決策：`C:\Users\<ここにユーザー名>\AppData\LocalLow\VRChat\VRChat\OSC`に移動し、その下のすべてのフォルダを削除してから、アバターをリロードします

- Pythonが認識されないように見える場合、これはWindows 10/11の問題です
  - 解決策：手順5と8で、`python`を`py`に置き換えます

## コミュニティ
[コミュニティ](https://discord.com/invite/W2R7zA84ay)に自由に参加して、追加のヘルプを得たり、BCI技術について話し合ったり、VRChatでのミートアップについて情報を得たりしてください！

## ライセンス
[MIT](http://opensource.org/licenses/MIT).
http://googleusercontent.com/youtube_content/0 http://googleusercontent.com/youtube_content/1
