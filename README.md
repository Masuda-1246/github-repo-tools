# github-repo-tools

GitHub リポジトリを管理するための Python ツールセット

## 機能

- リポジトリ一覧の取得と保存（`get_repo_list.py`）
- リポジトリをプライベートに変更（`change_to_privete.py`）
- リポジトリの削除（`delete_repo.py`）

## 使い方

### 準備

1. GitHub Personal Access Token を取得してください
2. 以下のいずれかの方法で環境設定ファイルを作成してください:
   - `.env.example`ファイルをコピーして`.env`を作成:
     ```
     cp .env.example .env
     ```
   - または、`.env` ファイルをプロジェクトルートに手動で作成し、以下の内容を記述:
     ```
     GITHUB_USERNAME=あなたのGitHubユーザー名
     GITHUB_TOKEN=あなたのGitHubパーソナルアクセストークン
     ```
3. 作成した`.env`ファイルを編集して、あなたのGitHubユーザー名とトークンを設定してください

4. 必要なライブラリをインストール:
   ```
   pip install requests python-dotenv
   ```

### リポジトリ一覧の取得

基本的な使用方法:
```
python get_repo_list.py
```

コマンドライン引数オプション:
```
python get_repo_list.py [--private] [--per_page=数値] [--output=ファイル名]
```

- `--private`: プライベートリポジトリも含めて取得する（デフォルトはすべてのリポジトリ）
- `--per_page=数値`: 1回のAPI呼び出しで取得するリポジトリ数（デフォルトは100）
- `--output=ファイル名`: 結果を保存するファイル名（デフォルトは`repositories.txt`）

例:
```
python get_repo_list.py --private --per_page=50 --output=my_repos.txt
```

このコマンドは自分のGitHubアカウントのリポジトリ一覧を取得し、指定したファイルに保存します。

### リポジトリをプライベートに変更

```
python change_to_privete.py
```

`repositories.txt`に記載されたリポジトリをプライベートに変更します。実行前に確認が表示されます。

### リポジトリの削除

```
python delete_repo.py
```

`repositories.txt`に記載されたリポジトリを削除します。実行前に確認が表示されます。

## 注意事項

- リポジトリの削除は元に戻せません。実行前に十分確認してください。
- 大量のリポジトリを操作する場合、GitHub API のレート制限に注意してください。
