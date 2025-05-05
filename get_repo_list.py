import requests
import json
import os
import argparse

import dotenv

dotenv.load_dotenv()

def list_github_repositories(username, token, include_private=True, per_page=100):
    """
    GitHubのリポジトリ一覧を取得して表示する関数
    
    Args:
        username (str): GitHubのユーザー名
        token (str): GitHubのパーソナルアクセストークン
        include_private (bool): プライベートリポジトリを含めるかどうか
        per_page (int): 1回のリクエストで取得するリポジトリ数
    
    Returns:
        list: リポジトリ名のリスト
    """
    # プライベートリポジトリを含める場合は認証ユーザーのエンドポイントを使用
    if include_private:
        url = "https://api.github.com/user/repos"
    else:
        url = f"https://api.github.com/users/{username}/repos"
    
    # ヘッダー設定（認証情報を含む）
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # クエリパラメータ
    params = {
        "per_page": per_page,  # 一度に取得するリポジトリ数を増やす
        "sort": "updated",  # 更新日順に並べる
        "direction": "desc",  # 新しい順に並べる
        "affiliation": "owner"  # 所有者であるリポジトリのみ取得
    }
    
    # リクエストの実行
    response = requests.get(url, headers=headers, params=params)
    
    # ステータスコードの確認
    if response.status_code != 200:
        print(f"エラー: HTTPステータスコード {response.status_code}")
        print(response.text)
        return []
    
    # レスポンスのJSONを解析
    repos = json.loads(response.text)
    
    # リポジトリ一覧を表示
    print(f"{username}のリポジトリ一覧:")
    print("-" * 60)
    
    repo_names = []
    public_count = 0
    private_count = 0
    
    for i, repo in enumerate(repos, 1):
        repo_name = repo["name"]
        repo_owner = repo["owner"]["login"]
        
        # 自分のアカウントのリポジトリのみ処理
        if repo_owner != username:
            continue
            
        repo_names.append(repo_name)
        is_private = repo["private"]
        visibility = "🔒 プライベート" if is_private else "🌐 パブリック"
        
        if is_private:
            private_count += 1
        else:
            public_count += 1
        
        print(f"{i}. {repo_name} ({visibility})")
        print(f"   説明: {repo['description'] or '(説明なし)'}")
        print(f"   URL: {repo['html_url']}")
        print(f"   作成日: {repo['created_at']}")
        print("-" * 60)
    
    print(f"合計: {len(repo_names)}個のリポジトリ（パブリック: {public_count}、プライベート: {private_count}）")
    
    return repo_names

def save_repositories_to_file(repo_names, filename="repositories.txt"):
    """
    リポジトリ名をファイルに保存する関数
    
    Args:
        repo_names (list): リポジトリ名のリスト
        filename (str): 保存先のファイル名
    """
    with open(filename, "w") as f:
        for repo in repo_names:
            f.write(f"{repo}\n")
    print(f"リポジトリ名を {filename} に保存しました")

def parse_arguments():
    """
    コマンドライン引数をパースする関数
    
    Returns:
        argparse.Namespace: パースされた引数
    """
    parser = argparse.ArgumentParser(description="GitHubリポジトリ一覧を取得して保存するツール")
    
    parser.add_argument("--private", action="store_true", 
                        help="プライベートリポジトリを含める（デフォルト: 含める）")
    parser.add_argument("--per_page", type=int, default=100,
                        help="1回のAPIリクエストで取得するリポジトリ数（デフォルト: 100）")
    parser.add_argument("--output", type=str, default="repositories.txt",
                        help="結果を保存するファイル名（デフォルト: repositories.txt）")
    
    return parser.parse_args()

if __name__ == "__main__":
    # コマンドライン引数をパース
    args = parse_arguments()
    
    # GitHubのユーザー名とトークンを設定
    username = os.getenv("GITHUB_USERNAME")
    token = os.getenv("GITHUB_TOKEN")
    
    if not username or not token:
        print("エラー: 環境変数GITHUB_USERNAMEとGITHUB_TOKENが設定されていません")
        print("'.env'ファイルを作成し、以下の内容を記述してください:")
        print("GITHUB_USERNAME=あなたのGitHubユーザー名")
        print("GITHUB_TOKEN=あなたのGitHubパーソナルアクセストークン")
        exit(1)
    
    # リポジトリ一覧を取得して表示
    repos = list_github_repositories(username, token, include_private=args.private, per_page=args.per_page)
    
    # リポジトリ名をファイルに保存
    save_repositories_to_file(repos, filename=args.output)