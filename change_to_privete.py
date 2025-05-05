import requests
import json
import os
import dotenv

# .envファイルから環境変数を読み込む
dotenv.load_dotenv()

def change_repository_to_private(username, token, repo_name):
    """
    GitHubのリポジトリをプライベートに変更する関数
    
    Args:
        username (str): GitHubのユーザー名
        token (str): GitHubのパーソナルアクセストークン
        repo_name (str): 変更するリポジトリ名
    
    Returns:
        bool: 変更が成功したかどうか
    """
    # APIのエンドポイントURL
    url = f"https://api.github.com/repos/{username}/{repo_name}"
    
    # ヘッダー設定（認証情報を含む）
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # リポジトリをプライベートに設定するリクエストボディ
    data = {
        "private": True
    }
    
    # PATCHリクエストの実行
    response = requests.patch(url, headers=headers, json=data)
    
    # ステータスコードの確認
    if response.status_code == 200:
        print(f"✅ リポジトリ '{repo_name}' をプライベートに変更しました")
        return True
    else:
        print(f"❌ リポジトリ '{repo_name}' の変更に失敗しました: HTTPステータスコード {response.status_code}")
        print(response.text)
        return False

def read_repositories_from_file(filename="repositories.txt"):
    """
    ファイルからリポジトリ名のリストを読み込む関数
    
    Args:
        filename (str): 読み込むファイル名
    
    Returns:
        list: リポジトリ名のリスト
    """
    repo_names = []
    try:
        with open(filename, "r") as f:
            for line in f:
                repo_name = line.strip()
                if repo_name:  # 空行をスキップ
                    repo_names.append(repo_name)
        print(f"{filename}から{len(repo_names)}個のリポジトリ名を読み込みました")
        return repo_names
    except FileNotFoundError:
        print(f"エラー: {filename}が見つかりません")
        return []

def change_repositories_to_private_from_file(username, token, filename="repositories.txt"):
    """
    ファイルから読み込んだリポジトリをプライベートに変更する関数
    
    Args:
        username (str): GitHubのユーザー名
        token (str): GitHubのパーソナルアクセストークン
        filename (str): リポジトリ名が書かれたファイル名
    """
    # ファイルからリポジトリ名を読み込む
    repo_names = read_repositories_from_file(filename)
    
    if not repo_names:
        print("変更するリポジトリがありません")
        return
    
    # 変更確認
    print(f"以下の{len(repo_names)}個のリポジトリをプライベートに変更しますか？")
    for i, repo in enumerate(repo_names, 1):
        print(f"{i}. {repo}")
    
    confirmation = input("変更を実行するには 'yes' と入力してください: ")
    if confirmation.lower() != "yes":
        print("変更がキャンセルされました")
        return
    
    # リポジトリの変更
    success_count = 0
    fail_count = 0
    
    for repo_name in repo_names:
        if change_repository_to_private(username, token, repo_name):
            success_count += 1
        else:
            fail_count += 1
    
    # 結果の表示
    print("\n変更処理の結果:")
    print(f"成功: {success_count}件")
    print(f"失敗: {fail_count}件")

if __name__ == "__main__":
    # GitHubのユーザー名とトークンを環境変数から取得
    username = os.getenv("GITHUB_USERNAME")
    token = os.getenv("GITHUB_TOKEN")
    
    if not username or not token:
        print("エラー: 環境変数GITHUB_USERNAMEとGITHUB_TOKENが設定されていません")
        print("'.env'ファイルを作成し、以下の内容を記述してください:")
        print("GITHUB_USERNAME=あなたのGitHubユーザー名")
        print("GITHUB_TOKEN=あなたのGitHubパーソナルアクセストークン")
        exit(1)
    
    # repositories.txtからリポジトリを読み込んでプライベートに変更
    change_repositories_to_private_from_file(username, token)
