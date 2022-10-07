[InsightFace による顔検出](https://www.kkaneko.jp/cc/deepim/insightface.html) を参考にしながらInsight Faceによる人物画像の分類を行うためのプログラム  
[【Python】OpenCVを超えたInsightFaceによる顔認識](https://self-development.info/%E3%80%90python%E3%80%91opencv%E3%82%92%E8%B6%85%E3%81%88%E3%81%9Finsightface%E3%81%AB%E3%82%88%E3%82%8B%E9%A1%94%E8%AA%8D%E8%AD%98/) にある通り、精度が非常によい

## 事前準備
* [InsightFace による顔検出](https://www.kkaneko.jp/cc/deepim/insightface.html) からpythonライブラリ群をインストールしておく
  * GPUを積んでいるならCUDA, cuDNNの利用により高速化できる
    * onnxruntime-gpuのバージョンによってはエラーが発生
      * 問題
      ```
      ValueError: This ORT build has ['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider'] enabled. Since ORT 1.9, you are required to explicitly set the providers parameter when instantiating InferenceSession. Fo
      r example, onnxruntime.InferenceSession(..., providers=['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider'], ...)
      ```
      * 対応策
      ```
      # 当該ソースの以下で、以下のようにCUDAExecutionProviderを指定
      model = router.get_model(providers=kwargs.get('providers', ["CUDAExecutionProvider"]), provider_options=kwargs.get('provider_options'))
      # 下記URLの手順に従い、zlibwapi.dllを指定の場所に配置
      https://stackoverflow.com/questions/72356588/could-not-locate-zlibwapi-dll-please-make-sure-it-is-in-your-library-path#answer-72458201
      ```

* .envに格納フォルダ、出力フォルダを設定
    * 顔認識：画像内に人物の顔があるかどうか
    * 顔認証：同一人物と判定できるかどうか
* sortedフォルダに人物が１人で映っている画像を1枚以上入れておく
  * ./sorted/BarackObama/***.jpg
  * ./sorted/JoeBiden/***.jpg
```text
TARGET_EXT=.jpg|.jpeg|.png（対象となる画像の拡張子）

UNKNOWN_FOLDER=（判定対象となる画像を格納するフォルダパス）
SORTED_FOLDER=（分類された画像を格納するフォルダパス。実行後、顔認証された画像が追加されていく）

UNIDENTIFIED_FOLDER=（顔認識自体ができたい画像の移動先）
THRESHOLD_FOLDER=（下記で顔認証ができなかった画像の移動先）

THRESHOLD=0.5(顔判別をどれだけ厳しくするか。大きいほど厳しくなる。-1.0~1.0まで)
```
### 起動
```
python main.py
```
### 実行結果
```
対象フォルダ格納ファイル数: 58
移動前ファイル数: 0
ok BarackObama[0.6647154688835144]: D:\Python\images\BarackObama-1523325020059090945-20220509_003241-img1.jpg
out of threshold[0.1273338943719864]: D:\Python\images\BarackObama-1523377561975214080-20220509_040128-img1.jpg
out of threshold[0.11327635496854782]: D:\Python\images\BarackObama-1531259328346333184-20220530_220047-img1.jpg
ok BarackObama[0.7003363966941833]: D:\Python\images\BarackObama-1534611402278699015-20220609_040044-img1.jpg
ok BarackObama[0.5798514485359192]: D:\Python\images\BarackObama-1535245743530954759-20220610_220123-img1.jpg
ok JoeBiden[0.7613946199417114]: D:\Python\images\POTUS-1567586398504370179-20220908_035136-img2.jpg
ok JoeBiden[0.696438193321228]: D:\Python\images\POTUS-1567640240533168130-20220908_072533-img1.jpg
cannot find faces in: D:\Python\images\POTUS-1567952734623596548-20220909_040717-img1.jpg
cannot find faces in: D:\Python\images\POTUS-1567952734623596548-20220909_040717-img2.jpg
cannot find faces in: D:\Python\images\POTUS-1568306634228912128-20220910_033333-img1.jpg
out of threshold[0.40434694290161133]: D:\Python\images\POTUS-1568343500298797057-20220910_060003-img1.jpg
ok JoeBiden[0.5533902049064636]: D:\Python\images\POTUS-1568631646932312064-20220911_010503-img1.jpg
...(略)
移動後ファイル数: 58
残り対象フォルダ格納ファイル数: 0
```

## 所感
* 顔認識については非常に精度がよい。ほぼ見逃さない
  * 顔がマスクや手で覆われていたり、90度を軽く超えた横顔、小さい映り方、一部だけの映り方だったとしても認識する
    * 多少の手振れは問題ないが、コップや水たまりに反射している等のぼやっとした映り方をしている顔は認識できない
* 顔認証については、閾値を0.5にすると精度がよい。正答率は9割程度
  * 顔全体が映っていればほぼ間違えない。人間でも見間違えるほど似ていれば間違えるといった感じ
  * 当然だが、上記のように顔の一部が隠れているほど精度は落ちる。ただ、マスクをしていてもsortedにマスクをしている画像があれば精度を上げることができる
  * sortedに格納されている画像の枚数に偏りがあっても、少ないサンプルの人物を分類できている
* GPUの利用により速度は早くなる（但し、利用せず実行した場合の動作は行っていないため比較はできない）
  * タスクマネージャーのパフォーマンスからGPUの使用量を確認して動作を確認する
