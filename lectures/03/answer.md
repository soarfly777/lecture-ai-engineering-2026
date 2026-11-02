# 第3回 解答

## 演習

- 第1回（素のLLM）とエージェントの回答の違い：
- `--trace` で見えたツール呼び出し（ツール名と引数）：
- 1つの質問での LLM 呼び出し回数（`requests`）：

@soarfly777 ➜ /workspaces/lecture-ai-engineering-2026 (main) $ git pull --no-rebase
remote: Enumerating objects: 15, done.
remote: Counting objects: 100% (3/3), done.
remote: Total 15 (delta 3), reused 3 (delta 3), pack-reused 12 (from 1)
Unpacking objects: 100% (15/15), 7.53 KiB | 856.00 KiB/s, done.
From https://github.com/soarfly777/lecture-ai-engineering-2026
   d9184de..b64976d  main       -> origin/main
Updating d9184de..b64976d
Fast-forward
 .devcontainer/devcontainer.json | 28 ++++++++++++++++++++++++++++
 .gitignore                      | 14 ++++++++++++++
 lectures/02/answer.md           | 73 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++----------
 lectures/02/problem.md          |  2 +-
 4 files changed, 106 insertions(+), 11 deletions(-)
 create mode 100644 .devcontainer/devcontainer.json
 create mode 100644 .gitignore

@soarfly777 ➜ /workspaces/lecture-ai-engineering-2026 (main) $ git switch -c lec03
Switched to a new branch 'lec03'

@soarfly777 ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ uv run python -m app.agent "AIE2026の講座の宿題にある「3レベル」とは何ですか？"
[model] gemini-3.5-flash-lite
                 pydantic-ai v2.57.0 • Python 3.14.2
      / \
     /   \       agent: target • model: google:gemini-3.5-flash-lite • tools: 2 • capabilities: 0
   /___.___\
  /    |    \    observability: off — see every model and tool call live, with cost
/      |      \    set it up free with Logfire and a GitHub login: https://pydantic.dev/ai-setup.md
`---.._|_..---'    or use any OpenTelemetry backend: https://pydantic.dev/docs/ai/logfire/#otel

                 goes away once observability is on — or PYDANTIC_AI_NO_BANNER=1
AIE2026の宿題における「3レベル」とは、宿題の難易度や取り組み方の構成のことです。

具体的には以下の3つの段階に分かれており、受講生は自分のレベルや目的に応じてどれか1つを選んで取り組みます（どれか1つに取り組めばその回の宿題は完了となり、原則として採点は行われません）。

1. **基礎**：講義内容の確認
2. **実装**：自分でコードを書く
3. **発展**：調査や試行

（関係する回：第1回）
@soarfly777 ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ uv run python -m app.agent --trace "LoRA とQLoRAの違い は？"
[model] gemini-3.5-flash-lite
                 pydantic-ai v2.57.0 • Python 3.14.2
      / \
     /   \       agent: target • model: google:gemini-3.5-flash-lite • tools: 2 • capabilities: 0
   /___.___\
  /    |    \    observability: off — see every model and tool call live, with cost
/      |      \    set it up free with Logfire and a GitHub login: https://pydantic.dev/ai-setup.md
`---.._|_..---'    or use any OpenTelemetry backend: https://pydantic.dev/docs/ai/logfire/#otel

                 goes away once observability is on — or PYDANTIC_AI_NO_BANNER=1
LoRAとQLoRAの違いは、ベースモデルの重みの扱い方にあります。

* **LoRA（Low-Rank Adaptation）**
  事前学習済みの重みをそのまま（通常の精度で）固定し、重みの更新分を表す小さな低ランク行列だけを追加して学習するPEFT手法です。学習するパラメータ数が非常に少なくて済みます。

* **QLoRA（Quantized LoRA）**
  LoRAの仕組みをベースにしつつ、**ベースモデルの重みを4ビットなどの低ビットに量子化（Quantize）してメモリ使用量を大幅に削減**したうえでLoRAの学習を行います。これにより、より大きなモデルを限られたGPUメモリでも効率よく扱えるようになります。

関係する回：第2回

--- trace ---
[tool call]   search_glossary({'query': 'LoRA'})
[tool call]   search_glossary({'query': 'QLoRA'})
[tool return] search_glossary -> [{"term": "LoRA", "lecture": 2, "definition": "事前学習済みの重みは固定したまま、重みの更新分を2つの小さな行列の積（低ランク行列）で表し、その小さな行列だけを学習するPEFT手法。学習するパラ…
[tool return] search_glossary -> [{"term": "QLoRA", "lecture": 2, "definition": "ベースモデルの重みを4ビットなどに量子化してメモリを節約したうえで、LoRAで学習する手法。より大きなモデルを小さなGPUで扱える。本講座の第2…
[usage] RunUsage(cost=Decimal('0.0008563'), details={'text_prompt_tokens': 1196}, input_text_tokens=1196, input_tokens=1196, output_tokens=199, requests=2, tool_calls=2)
@soarfly777 ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ 


- 追加したツールと、docstring に書いた説明：
def make_quiz(lecture: int) -> str:
    """指定した回の用語集から1問の確認問題と答えを返す。

    ユーザーが「第2回の確認問題を出して」のように、特定回の講義内容を
    復習するための短い用語問題を求めたときに使う。
    lecture には確認したい講義回を1始まりの整数で指定する。
    """
    terms = [entry for entry in load_glossary() if entry["lecture"] == lecture]

    if not terms:
        return f"第{lecture}回の用語は用語集にありません。"

    entry = random.choice(terms)

    return json.dumps(
        {
            "question": f"「{entry['term']}」の意味は？",
            "answer": entry["definition"],
        },
        ensure_ascii=False,
    )
    

## 宿題

- 取り組んだレベル：実装 

- やったこと：
save_learning_log は learning_log/ に記録を書き込む副作用のあるツールなので、requires_approval=True で登録する。承認が必要なツール呼び出しでは、実行は DeferredToolRequests を返して停止し、承認・拒否の結果を DeferredToolResults で渡して再開する。ログを Markdown ファイルとして保存します。モデルが「何を学んだか」を渡せるよう、引数は content: str とする。

- 結果：
@soarfly777 ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ uv run python -m app.agent --list-tools
                 pydantic-ai v2.57.0 • Python 3.14.2
      / \
     /   \       agent: target • model: test:test • output: str | DeferredToolRequests • tools: 4 • capabilities: 0
   /___.___\
  /    |    \    observability: off — see every model and tool call live, with cost
/      |      \    set it up free with Logfire and a GitHub login: https://pydantic.dev/ai-setup.md
`---.._|_..---'    or use any OpenTelemetry backend: https://pydantic.dev/docs/ai/logfire/#otel

                 goes away once observability is on — or PYDANTIC_AI_NO_BANNER=1
モデルに見えているツール: 4 個

[search_glossary]
  講座の用語集から用語を検索し、定義と、どの回で扱うかを返す。
  
  AIエンジニアリングの用語や、この講座（AIE2026）に固有の言葉について
  答える前に使うこと。query には調べたい用語を1つだけ入れる（例: "LoRA"）。
  引数: {"query": {"type": "string"}}

[get_lecture_summary]
  指定した回（1始まりの整数）の講義の要点を返す。
  
  「第3回では何を学ぶ？」のように、回の内容や関係を聞かれたときに使う。
  引数: {"lecture": {"type": "integer"}}

[make_quiz]
  指定した回の用語集から1問の確認問題と答えを返す。
  
  ユーザーが「第2回の確認問題を出して」のように、特定回の講義内容を
  復習するための短い用語問題を求めたときに使う。
  lecture には確認したい講義回を1始まりの整数で指定する。
  引数: {"lecture": {"type": "integer"}}

[save_learning_log]
  学習内容を learning_log フォルダに記録として保存する。
  
  ユーザーが学んだこと、試したこと、実行結果、気づきなどを後から
  振り返れるよう保存したいときに使う。ファイルの作成は取り消しにくいため、
  保存前に必ずユーザーの承認を得る。
  content には保存する学習記録の本文を指定する。
  引数: {"content": {"type": "string"}}
@soarfly777 ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ uv run python -m app.agent --trace   "第3回でmake_quiz を追加し、tools.pyとagent.pyを変更した。テストは11 passedだった。この学習記録を保存して"
[model] gemini-3.5-flash-lite
                 pydantic-ai v2.57.0 • Python 3.14.2

      / \        agent: target • model: google:gemini-3.5-flash-lite • output: str | DeferredToolRequests • tools: 4
     /   \         capabilities: 0
   /___.___\
  /    |    \    observability: off — see every model and tool call live, with cost
/      |      \    set it up free with Logfire and a GitHub login: https://pydantic.dev/ai-setup.md
`---.._|_..---'    or use any OpenTelemetry backend: https://pydantic.dev/docs/ai/logfire/#otel

                 goes away once observability is on — or PYDANTIC_AI_NO_BANNER=1

保存の承認が必要です。

保存予定の内容: {'content': '【学習記録】\n- 第3回にて `make_quiz` 関数を追加\n- `tools.py` と `agent.py` のコードを変更\n- テスト実行結果: 11 passed\n'}

learning_log/ に保存してよいですか？ [y/N]: y
学習内容を learning_log フォルダに保存しました。

（関係する回：第3回）

--- trace ---
[tool call]   save_learning_log({'content': '【学習記録】\n- 第3回にて `make_quiz` 関数を追加\n- `tools.py` と `agent.py` のコードを変更\n- テスト実行結果: 11 passed\n'})
[tool return] save_learning_log -> 学習記録を保存しました: /workspaces/lecture-ai-engineering-2026/learning_log/learning_20261102_013152.md…
[usage] RunUsage(cost=Decimal('0.0002662'), details={'text_prompt_tokens': 704}, input_text_tokens=704, input_tokens=704, output_tokens=22, requests=1, tool_calls=1)
@soarfly777 ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ ls -lt learning_log/
total 4
-rw-rw-rw- 1 codespace codespace 201 Nov  2 01:31 learning_20261102_013152.md
@soarfly777 ➜ /workspaces/lecture-ai-engineering-2026 (lec03) $ cat learning_log/learning_*.md
# 学習記録

- 保存日時: 2026-11-02T01:31:52

【学習記録】
- 第3回にて `make_quiz` 関数を追加
- `tools.py` と `agent.py` のコードを変更
- テスト実行結果: 11 passed

- 気づき・疑問：
--list-tools の結果では、登録ツール数が 4 個となり、save_learning_log の関数名、docstring、引数 content: string がモデルに公開されていることを確認した。したがって、関数の型ヒントと docstring がツール仕様として利用されていることを確認できた。

保存ツールには requires_approval=True を設定した。その結果、モデルが保存を要求しても直ちにはファイル操作が行われず、保存対象の content を表示して利用者に承認を求める処理で停止した。この仕組みにより、ファイル作成のような副作用を持つ操作を、利用者の意思確認なしに実行しない設計にできた。

y を入力して承認した後に、save_learning_log が実行された。--trace には save_learning_log の呼び出し引数と、「学習記録を保存しました」というツールの返却値が表示された。したがって、承認後にのみツール本体が実行されることを確認できた。

learning_log/learning_20261102_013152.md が実際に作成され、保存日時、学習記録、テスト結果がファイルに記録された。ls -lt と cat により、ファイルの存在と内容の両方を確認した。

学習支援エージェントの最終応答は「学習内容を learning_log フォルダに保存しました」となり、ユーザーへの処理結果の通知もできている。trace 上でもツール呼び出しが 1 回であることを確認できた。

考察
Deferred Tool は、モデルにツールを使わせつつ、保存・削除・送信などの取り消しにくい操作を利用者の承認後に限定できる。Pydantic AI では、承認が必要なツール呼び出しがあると DeferredToolRequests を返して実行を中断し、承認結果を受け取ってから再開する。

今回の実装では、承認画面に保存本文を表示できている点が重要である。利用者は「保存するか」だけでなく、何が保存されるかを確認してから判断できるため、誤った内容や意図しない記録の保存を防ぎやすい。

また、--trace はモデルとツールの境界を検証する手段として有効だった。最終応答だけでは実際に保存関数が呼ばれたか分からないが、trace により、モデルが生成した content、ツール呼び出し、ツールの返却値を確認できた。

