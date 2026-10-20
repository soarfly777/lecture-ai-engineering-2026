"""第1回: 素のLLMに1回だけ質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask

モデルを切り替える場合:
    AIE_MODEL=gemini-3.5-flash-lite uv run python -m app.ask
    AIE_MODEL=gemini-3.8-flash uv run python -m app.ask

temperatureを指定する場合:
    AIE_TEMPERATURE=0.2 uv run python -m app.ask
"""

import argparse
import csv
import os
import time
from datetime import datetime
from pathlib import Path

from google import genai
from google.genai import errors, types

from app.config import MODEL, api_error_message, get_api_key


# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"

# 実験結果の保存先
RESULT_FILE = Path("results.csv")


def get_model() -> str:
    """AIE_MODELが設定されていれば、そのモデルを使用する。"""
    return os.getenv("AIE_MODEL", MODEL)


def get_temperature() -> float | None:
    """AIE_TEMPERATUREを取得する。未設定ならNoneを返す。"""
    value = os.getenv("AIE_TEMPERATURE")

    if value is None or value == "":
        return None

    return float(value)


def save_result(
    *,
    model: str,
    actual_model: str,
    temperature: float | None,
    question: str,
    elapsed_seconds: float,
    input_tokens: int | None,
    output_tokens: int | None,
    total_tokens: int | None,
    status: str,
    error_message: str = "",
) -> None:
    """実験結果をCSVへ追記する。"""
    file_exists = RESULT_FILE.exists()

    with RESULT_FILE.open("a", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(
                [
                    "実行日時",
                    "指定モデル",
                    "実行モデル",
                    "temperature",
                    "質問",
                    "応答時間_秒",
                    "入力トークン数",
                    "出力トークン数",
                    "合計トークン数",
                    "ステータス",
                    "エラー内容",
                ]
            )

        writer.writerow(
            [
                datetime.now().astimezone().isoformat(timespec="seconds"),
                model,
                actual_model,
                "" if temperature is None else temperature,
                question,
                f"{elapsed_seconds:.3f}",
                "" if input_tokens is None else input_tokens,
                "" if output_tokens is None else output_tokens,
                "" if total_tokens is None else total_tokens,
                status,
                error_message,
            ]
        )


def ask(
    question: str,
    model: str,
    temperature: float | None,
) -> str:
    client = genai.Client(api_key=get_api_key())

    # temperature未指定時は空の設定を使用する
    config = types.GenerateContentConfig()

    if temperature is not None:
        config.temperature = temperature

    started_at = time.perf_counter()

    try:
        response = client.models.generate_content(
            model=model,
            contents=question,
            config=config,
        )
    except errors.APIError as error:
        elapsed_seconds = time.perf_counter() - started_at

        save_result(
            model=model,
            actual_model="",
            temperature=temperature,
            question=question,
            elapsed_seconds=elapsed_seconds,
            input_tokens=None,
            output_tokens=None,
            total_tokens=None,
            status=f"ERROR_{error.code}",
            error_message=error.message,
        )

        raise

    elapsed_seconds = time.perf_counter() - started_at
    usage = response.usage_metadata

    input_tokens = (
        usage.prompt_token_count
        if usage is not None
        else None
    )
    output_tokens = (
        usage.candidates_token_count
        if usage is not None
        else None
    )
    total_tokens = (
        usage.total_token_count
        if usage is not None
        else None
    )

    # APIが返した実際のモデルバージョンを取得
    actual_model = response.model_version or model

    print(f"[指定モデル] {model}")
    print(f"[実行モデル] {actual_model}")
    print(f"[temperature] {temperature if temperature is not None else '未指定'}")
    print(f"[応答時間] {elapsed_seconds:.3f} 秒")
    print(f"[入力トークン数] {input_tokens}")
    print(f"[出力トークン数] {output_tokens}")
    print(f"[合計トークン数] {total_tokens}")

    save_result(
        model=model,
        actual_model=actual_model,
        temperature=temperature,
        question=question,
        elapsed_seconds=elapsed_seconds,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        status="SUCCESS",
    )

    return response.text or ""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="素のLLMに質問し、応答時間とトークン数を記録する"
    )
    parser.add_argument(
        "question",
        nargs="?",
        default=DEFAULT_QUESTION,
    )
    args = parser.parse_args()

    model = get_model()

    try:
        temperature = get_temperature()
    except ValueError:
        print(
            "[設定エラー] AIE_TEMPERATUREには"
            "0.2などの数値を指定してください。"
        )
        raise SystemExit(1)

    print(f"[model] {model}")
    print(f"[質問] {args.question}\n")

    try:
        answer = ask(
            question=args.question,
            model=model,
            temperature=temperature,
        )
        print("\n[回答]")
        print(answer)

    except errors.APIError as error:
        print(api_error_message(error.code, error.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
    