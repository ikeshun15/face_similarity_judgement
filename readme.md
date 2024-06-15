# ポート番号固定方法

### 1.設定ファイルを編集する方法
[1_🏠_hello.py]と同じディレクトリに[config.toml]を作成する。
```
[server]
port = 55505
```

### 2.コマンド実行時に指定する方法
streamlit run 1_🏠_hello.py --server.port 55005