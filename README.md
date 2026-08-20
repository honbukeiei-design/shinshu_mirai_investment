# 信州みらい病院 重点投資シナリオ

Streamlit Community Cloud / ローカル共通版（素材埋め込み版）です。

## Streamlit Community Cloud
1. このフォルダの**中身をすべて**GitHubリポジトリへ配置します。
2. Streamlit Community Cloudでリポジトリを指定します。
3. Main file path に `app.py` を指定します。

画像・背景・BGMは `embedded_assets.py` に埋め込まれているため、`static` フォルダは不要です。

## 必須ファイル
- `app.py`
- `scenario.json`
- `embedded_assets.py`
- `requirements.txt`
- `.streamlit/config.toml`

## ローカル起動
```bash
pip install -r requirements.txt
streamlit run app.py
```
