import requests
import json
import os
import dotenv

# .envファイルから環境変数を読み込む
dotenv.load_dotenv()

def delete_github_repository(username, token, repo_name):
    """
    GitHubのリポジトリを削除する関数
    
    Args:
        username (str): GitHubのユーザー名
        token (str): GitHubのパーソナルアクセストークン
        repo_name (str): 削除するリポジトリ名
    
    Returns:
        bool: 削除が成功したかどうか
    """
    # APIのエンドポイントURL
    url = f"https://api.github.com/repos/{username}/{repo_name}"
    
    # ヘッダー設定（認証情報を含む）
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # DELETEリクエストの実行
    response = requests.delete(url, headers=headers)
    
    # ステータスコードの確認
    if response.status_code == 204:
        print(f"✅ リポジトリ '{repo_name}' の削除に成功しました")
        return True
    else:
        print(f"❌ リポジトリ '{repo_name}' の削除に失敗しました: HTTPステータスコード {response.status_code}")
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

def delete_repositories_from_file(username, token, filename="repositories.txt"):
    """
    ファイルから読み込んだリポジトリを削除する関数
    
    Args:
        username (str): GitHubのユーザー名
        token (str): GitHubのパーソナルアクセストークン
        filename (str): リポジトリ名が書かれたファイル名
    """
    # ファイルからリポジトリ名を読み込む
    repo_names = read_repositories_from_file(filename)
    
    if not repo_names:
        print("削除するリポジトリがありません")
        return
    
    # 削除確認
    print(f"以下の{len(repo_names)}個のリポジトリを削除しますか？")
    for i, repo in enumerate(repo_names, 1):
        print(f"{i}. {repo}")
    
    confirmation = input("削除を実行するには 'yes' と入力してください: ")
    if confirmation.lower() != "yes":
        print("削除がキャンセルされました")
        return
    
    # リポジトリの削除
    success_count = 0
    fail_count = 0
    
    for repo_name in repo_names:
        if delete_github_repository(username, token, repo_name):
            success_count += 1
        else:
            fail_count += 1
    
    # 結果の表示
    print("\n削除処理の結果:")
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
    
    # repositories.txtからリポジトリを読み込んで削除
    delete_repositories_from_file(username, token)
