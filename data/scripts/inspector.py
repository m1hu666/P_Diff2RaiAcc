#!/usr/bin/env python3
# -*- coding: gbk -*-
"""
Simple terminal trajectory inspector.

- inspector.py --m ... --r ... --i ...
"""

import json
from pathlib import Path
from typing import List, Dict, Any

import typer
from colorama import Fore, Style, init as colorama_init

app = typer.Typer(rich_markup_mode="rich", add_completion=False)

# 初始化颜色（在 Windows / 其他终端都能正常显示）
colorama_init(autoreset=True)


def load_messages_from_traj(traj_path: Path) -> List[Dict[str, Any]]:
    data = json.loads(traj_path.read_text())
    if isinstance(data, list):
        messages = data
    elif isinstance(data, dict) and "messages" in data:
        messages = data["messages"]
    else:
        raise ValueError("Unrecognized trajectory format")
    return messages


def build_traj_path(path: str, m: str | None, r: int | None, i: str | None) -> Path:
    if m is not None or r is not None or i is not None:
        if not (m and r and i):
            raise typer.BadParameter("When using --m/--r/--i, all three must be provided")

        base = Path(__file__).resolve().parents[1]  # .../P_Diff2RaiAcc/data
        repo_root = base.parent                     # .../P_Diff2RaiAcc

        traj_path = (
            repo_root
            / "data"
            / "traj"
            / m
            / f"round{r}"
            / i
            / f"{i}.traj.json"
        )

        if not traj_path.is_file():
            raise typer.BadParameter(f"Trajectory file does not exist: '{traj_path}'")
        return traj_path

    # 兼容原来的 path 行为
    path_obj = Path(path)
    if path_obj.is_file():
        return path_obj
    elif path_obj.is_dir():
        files = sorted(path_obj.rglob("*.traj.json"))
        if not files:
            raise typer.BadParameter(f"No trajectory files found in '{path}'")
        return files[0]
    else:
        raise typer.BadParameter(f"Error: Path '{path}' does not exist")


def role_style(role: str) -> str:
    """根据 role 返回不同颜色样式前缀。"""
    if role == "system":
        return Fore.CYAN + Style.BRIGHT
    if role == "user":
        return Fore.BLUE + Style.BRIGHT
    # assistant / others
    return Fore.GREEN + Style.BRIGHT


def print_step(step_idx: int, steps: List[Dict[str, Any]], traj_name: str | None = None) -> None:
    """在终端打印当前 step 的所有 message。"""
    step_no = step_idx + 1
    total = len(steps)

    header_line = f" Step {step_no}/{total} "
    if traj_name:
        header_line += f"- {traj_name} "

    bar = "=" * max(80, len(header_line) + 4)
    print(Fore.MAGENTA + bar)
    print(Fore.MAGENTA + Style.BRIGHT + header_line)
    print(Fore.MAGENTA + bar)

    messages = steps[step_idx]
    for m in messages:
        role_raw = m.get("role", "")
        role = role_raw.replace("assistant", "mini-swe-agent")
        content = m.get("content", "")
        if isinstance(content, list):
            content_str = "\n".join(str(item.get("text", "")) for item in content)
        else:
            content_str = str(content)

        rs = role_style(role_raw)
        print(rs + f"[{role.upper()}]" + Style.RESET_ALL)
        print(content_str)
        print(Fore.YELLOW + "-" * 80)

    print(Style.RESET_ALL, end="")


@app.command(help="Simple terminal inspector for trajectory files (no GUI).")
def main(
    path: str = typer.Argument(
        ".",
        help="Directory to search for trajectory files or specific trajectory file (when --m/--r/--i not used)",
    ),
    m: str = typer.Option(
        None,
        "--m",
        help="Model name, e.g. 'gpt-5-2025-08-07(medium reasoning)'",
    ),
    r: int = typer.Option(
        None,
        "--r",
        help="Round number, starting from 1",
    ),
    i: str = typer.Option(
        None,
        "--i",
        help="Example name (file prefix), e.g. 'astropy__astropy-7671'",
    ),
) -> None:
    """Decide which trajectory file to load based on parameters and inspect in terminal."""
    traj_path = build_traj_path(path, m, r, i)

    try:
        messages = load_messages_from_traj(traj_path)
    except Exception as e:
        raise typer.BadParameter(f"Failed to load trajectory '{traj_path}': {e}") from e

    # 简化版：每条 message 当作一个 step
    steps: List[List[Dict[str, Any]]] = [[m] for m in messages]
    if not steps:
        typer.echo("Empty trajectory.")
        raise typer.Exit(code=0)

    idx = 0
    traj_name = traj_path.name
    while True:
        print_step(idx, steps, traj_name=traj_name)
        typer.echo(
            Fore.CYAN
            + "Commands: "
            + Fore.GREEN
            + "[l] next"
            + Fore.RESET
            + "  "
            + Fore.GREEN
            + "[h] prev"
            + Fore.RESET
            + "  "
            + Fore.GREEN
            + "[q] quit"
            + Fore.RESET
            + "  "
            + Fore.GREEN
            + "[number] jump"
        )
        cmd = input(Fore.YELLOW + "> " + Style.RESET_ALL).strip().lower()

        if cmd in ("q", "quit", "exit"):
            break
        elif cmd in ("l", ""):
            # 默认回车等同 next
            idx = min(len(steps) - 1, idx + 1)
        elif cmd == "h":
            idx = max(0, idx - 1)
        else:
            # 尝试把输入当作 step 编号
            try:
                num = int(cmd)
                if 1 <= num <= len(steps):
                    idx = num - 1
                else:
                    print(Fore.RED + f"Invalid step number: {num}")
            except ValueError:
                print(Fore.RED + f"Unknown command: {cmd}")


if __name__ == "__main__":
    app()