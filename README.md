# 信州みらい病院 重点投資シナリオ

Streamlit Community Cloud / ローカル共通版です。

## Streamlit Community Cloud
1. このフォルダの中身をGitHubリポジトリへ配置します。
2. Streamlit Community Cloudでリポジトリを指定します。
3. Main file path に `app.py` を指定します。

## ローカル起動
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 操作
- 「はじめる」「次へ」「場面を見る」をマウスクリックして進行します。
- 選択分岐はありません。
- 話者は明るく、非話者は暗く表示されます。
- 背景はシナリオに沿って確実に切り替わります。
- BGMは場面に応じて自動的に切り替わります。最初の「はじめる」クリック後に再生開始します。
