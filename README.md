# 信州みらい病院 重点投資を考える — Streamlit版 v4

## 起動
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Community Cloud
GitHubリポジトリ直下に、このZipの中身をそのまま配置し、Main file path を `app.py` にしてください。

## 重要
- `static/` フォルダを必ず丸ごとGitHubへアップロードしてください。
- 画像・BGMは個別ファイルで保存しており、巨大な `embedded_assets.py` は使用していません。
- `app.py` は自身の置かれた場所を基準に素材を参照するため、Streamlit Cloudでも作業ディレクトリ差によるパスずれを起こしません。
- `__pycache__` は不要です。
