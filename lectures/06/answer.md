# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前：glossary_search_glossary
- STEP 2 の [tool call]：glossary_search_glossary({'query': '3レベル'})
- STEP 3 の [tool call]：fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
- STEP 4 の [tool call]：
  - aws_aws___search_documentation({'search_phrase': 'Amazon S3 バージョニング 概要', 'topics': ['general']})
  - aws_aws___search_documentation({'topics': ['general'], 'search_phrase': 'Using versioning Amazon S3'})
- 気づき・疑問：
  - モデルに渡るのは、どの方式でも「名前・説明文・引数」の同じ形だった。`app.agent`の`search_materials`と`app.mcp_agent`の`glossary_search_glossary`を並べても、ツールがMCPサーバーの中で動いているかは、モデルからは見分けられない。
  - 設定の`"command"`は自分のCodespacesでサーバーを起動し、`"url"`は外部で動くサーバーに接続する。`uv`（glossary）はプロジェクトの`.venv`で自分のコードを動かし、`uvx`（fetch）は公開パッケージを取得して、プロジェクトとは別の使い捨ての環境で動かす。初回だけ`Installed 46 packages`と出たのは、この環境を作ったため。
  - fetchの説明文には「本来はインターネットにアクセスできないと言われていたが、このツールでアクセスできる」という趣旨の文があり、説明文がモデルの振る舞いを変える指示にもなっていた。出所の分からないサーバーを足すと、その文章もそのままモデルに渡る。
  - fetchは、ページを取る前に`robots.txt`を確認していた（既定の動作）。
  - awsを足すとツールは7個に増え、入力はSTEP 2の715トークンから11,152トークンになった。AWSの検索結果が長いことに加え、使わないツールも含めた7個の定義が、3回のモデル応答のたびに渡るためだと考えられる。
  - STEP 4では、日本語の検索語で別の資料が1位になり、モデルが英語で検索し直した（モデル応答3回）。
  - 外に送られる情報は相手ごとに違う。Geminiには、指示文・質問・7個のツール定義・ツールの結果（AWSの検索結果を含む）が送られる。AWSには、モデルが作った検索語（`search_phrase`と`topics`）だけが送られ、質問の全文やGeminiの回答は送られない。
  - 疑問：設定に書いたサーバーには起動時にすべて接続してツール一覧を受け取るため、awsを書いた状態では、用語集の質問でもAWSに接続していると考えられる。サーバーを質問ごとに選んで有効にする仕組みは作れるか。

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：発展
- やったこと：
  - 調べたソフトウェア：VS Code（GitHub Copilotのエージェント機能からMCPサーバーを使う場合）。特に使っているエージェントのソフトウェアがないため、資料の指定どおりVS Codeを選んだ。
  - 調べた日付：2026年11月23日（参照したページの更新日はいずれも2026年11月18日）
  - 参照した公式ドキュメント：
    - MCP configuration reference：https://code.visualstudio.com/docs/agents/reference/mcp-configuration
    - Add and use MCP servers in VS Code：https://code.visualstudio.com/docs/copilot/customization/mcp-servers
  - MCP configuration referenceを自分で開き、次の3か所を確かめた：「Configuration file」の表（`$COPILOT_HOME/mcp-config.json`、`COPILOT_HOME`がなければ`~/.copilot/mcp-config.json`）、「Portable configuration」の例（`"type": "stdio"`、`"command": "npx"`、`"tools": ["*"]`）、「Important」の囲み（新しい設定には`.vscode/mcp.json`やプロファイルの`mcp.json`を使わない。これらは非推奨のLocal harnessの`servers`形式）。
  - 4つの観点（設定を書く場所、コマンドで起動する書き方、URLで接続する書き方、有効になる範囲）で、演習の`app/mcp_servers.json`と比べた。演習の設定を、VS Codeの形式に書き直した例も作った。
- 結果：
  - 現在のVS Codeには、設定の形式が2つある。新しく設定するときは、`mcpServers`形式（Copilot harnessが直接読む）を使う。`.vscode/mcp.json`などの`servers`形式は、Local harnessとともに非推奨となり、Local harnessは2027年2月に削除される予定。

    | 観点 | 演習の`app/mcp_servers.json` | VS Code（推奨：`mcpServers`形式） | VS Code（非推奨：`servers`形式） |
    |---|---|---|---|
    | 設定を書く場所 | リポジトリの`app/mcp_servers.json`（`app/mcp_agent.py`がこのパスを決め打ちで読む） | ワークスペースの直下の`.mcp.json`、またはユーザー設定の`~/.copilot/mcp-config.json`（`COPILOT_HOME`があれば`$COPILOT_HOME/mcp-config.json`）。コマンドパレットの「MCP: Add Server」、または「Chat: Open Customizations」→「MCP Servers」からも追加できる | ワークスペースの`.vscode/mcp.json`、またはユーザープロファイルの`mcp.json`。`code --add-mcp`でも追加できる |
    | 一番外側のキー | `mcpServers` | `mcpServers`（演習と同じ） | `servers` |
    | コマンドで起動する書き方 | `"command"`と`"args"`。`"type"`は書かず、`command`があればstdioとして扱う | `"type": "stdio"`、`"command"`、`"args"`。ほかに`env`、`cwd`、`tools`を書ける | `"type": "stdio"`（必須）、`"command"`（必須）、`"args"`。ほかに`cwd`、`env`、`envFile`、`dev`、`sandboxEnabled`を書ける |
    | URLで接続する書き方 | `"url"`だけ（Streamable HTTPで接続） | `"type": "http"`と`"url"`（古いSSE方式のサーバーには`"sse"`）。ほかに`headers`、`oauthClientId`、`tools`を書ける | `"type": "http"`または`"sse"`と`"url"`。ほかに`headers`、`oauth`を書ける。HTTPでつながらなければSSEに切り替える |
    | 有効になる範囲 | このリポジトリの`app/mcp_agent.py`だけ。VS Codeやほかのエージェントは読まない | `.mcp.json`はそのワークスペースだけ（Gitで管理して、チームで共有できる）。`mcp-config.json`は同じマシン（ホスト）のすべてのワークスペースと、Copilot CLIなどで共通 | `.vscode/mcp.json`はそのワークスペースだけ。プロファイルの`mcp.json`はユーザー全体 |

  - 演習の3つのサーバーを、VS Codeの`.mcp.json`（`mcpServers`形式）に書き直すと、次のようになる。違いは、`"type"`を明示することと、使うツールを`"tools"`で選べることの2点。

    ```json
    {
      "mcpServers": {
        "glossary": {
          "type": "stdio",
          "command": "uv",
          "args": ["run", "python", "-m", "app.mcp_server"],
          "tools": ["*"]
        },
        "fetch": {
          "type": "stdio",
          "command": "uvx",
          "args": ["mcp-server-fetch==2026.11.11", "--no-readability-js"],
          "tools": ["*"]
        },
        "aws": {
          "type": "http",
          "url": "https://knowledge-mcp.global.api.aws",
          "tools": ["*"]
        }
      }
    }
    ```

  - 実際に試した結果：書き直し例をリポジトリの直下に`.mcp.json`として保存すると、CodespacesのVS Codeで「MCP: List Servers」に、glossary・fetch・awsの3つが「実行中」と表示された（ほかに、Copilotに最初から付いている`github-mcp-server`も表示された）。演習と同じ`mcpServers`形式の設定を、VS Codeがそのまま読み込めることを確かめた。
  - VS Codeのチャット（Copilot）からも、2つのサーバーのツールを呼べた。
    - glossary：引数`{"query": "LoRA"}`で呼ばれ、用語集の「LoRA」「ランク（LoRAのr）」「QLoRA」の3件が返った。演習の`app/mcp_agent.py`から呼んだときと同じサーバー、同じ用語集の内容だった。
    - aws：引数`{"search_phrase": "Amazon S3 bucket versioning how versioning works", "topics": ["general"], "limit": 4}`で1回だけ呼ばれ、1位にS3のユーザーガイド「Retaining multiple versions of objects with S3 Versioning」が返った。演習（Gemini）では日本語で検索して外れ、英語で検索し直して2回呼んでいたが、Copilotは最初から英語で検索し、演習では使わなかった`limit`も指定していた。
  - そのほかの違い：
    - 使うツールの絞り込み：VS Codeでは`"tools"`に名前を並べて、使うツールを絞れる（`["*"]`は全部）。演習の設定には絞る方法がなく、awsの5個のツールが全部モデルに渡っていた。
    - 秘密の値の扱い：VS Codeの`mcpServers`形式では、`${NAME}`の形で環境変数を参照できる。トークンやパスワードを、共有するファイルに直接書いてはいけないと明記されている。非推奨の`servers`形式には、起動時に値を入力させる`${input:...}`もあるが、Copilot harnessには引き継がれない。
    - 動く場所：Codespacesのようなリモート環境では、ユーザー設定の`~/.copilot/mcp-config.json`は、手元のPCではなく、エージェントが動く側（Codespacesのコンテナ）のホームディレクトリにあるものが読まれる。
    - 安全面：VS Codeの公式ドキュメントにも、ローカルのMCPサーバーは自分のマシンでコードを実行できるので、提供元・コマンド・接続先を確認してから足すように、と書かれている。演習の補足と同じ考え方だった。
- 気づき・疑問：
  - 一番外側の`mcpServers`は演習と同じで、サーバー名の下に`command`と`args`、または`url`を書く形も同じだった。演習の設定ファイルは、VS Codeの新しい形式とほぼそのまま対応している（`app/mcp_agent.py`のコメントにも、Claude DesktopやCursorと同じ形式だと書かれている）。
  - 演習の設定は`"type"`を書かず、`command`があるか`url`があるかで接続方式を決めていた。VS Codeでは`"type"`を書いて明示する。書かない場合に同じように判定されるのかは、ドキュメントからは読み取れなかった。
  - 同じVS Codeの中でも、設定の場所と形式が2種類ある（`.mcp.json`と`.vscode/mcp.json`、`mcpServers`と`servers`）。古い記事のとおりに`.vscode/mcp.json`へ書くと、非推奨の形式になる。資料に「設定方法は変わることがあります」とあるとおりで、調べた日付とURLを残す意味が分かった。
  - 有効になる範囲は、「このプロジェクトだけ」（`.mcp.json`）と「自分のすべてのプロジェクト」（`mcp-config.json`）に分かれる。プロジェクトに必要なサーバー（用語集）はワークスペースに、どこでも使うサーバー（fetchやAWSのドキュメント検索）はユーザー設定に書く、という使い分けが考えられる。
  - 同じ用語集サーバーを、演習のエージェント（`app/mcp_agent.py`）とVS Codeのチャットという2つのクライアントから、コードを変えずに使えた。資料の「1つのMCPサーバーを、複数のエージェントから使える」を実際に確かめられた。
  - 同じサーバー・同じツールでも、呼び出すモデルによって引数の決め方が違った（検索語の言語、`limit`の有無、呼び出し回数）。ツールの説明文と引数の定義をどう読むかは、モデルごとに違う。
  - glossaryは`uv run python -m app.mcp_server`で起動するため、リポジトリの直下で実行する必要がある。ワークスペースの`.mcp.json`では`cwd`を書かなかったが、ツールを呼べたので、少なくとも今回のCodespacesでは、ワークスペースの直下から起動されていたと考えられる。
  - 疑問：`.mcp.json`を置くと、ワークスペースを開いた人のVS Codeで、`uv`や`uvx`のコマンドが実行される。チームで共有するときに、信頼の確認（Workspace Trust）だけで十分なのか。
