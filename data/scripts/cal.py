import os
import json
from pathlib import Path

def main():
    summary_file = Path("analyse/result/summary.txt")
    output_file = Path("analyse/result/token_usage_stats.txt")
    base_traj_dir = Path("data/traj")

    # 定义模型列表
    models = [
        "claude-sonnet-4-5-20250929",
        "gemini-3-pro-preview",
        "gpt-5-2025-08-07-medium-reasoning"
    ]

    # 初始化统计数据结构
    stats = {
        model: {
            "success": {"count": 0, "completion": 0, "prompt": 0, "total": 0},
            "fail": {"count": 0, "completion": 0, "prompt": 0, "total": 0}
        } for model in models
    }

    if not summary_file.exists():
        print(f"找不到汇总文件: {summary_file}")
        return

    with open(summary_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 跳过表头
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        
        parts = line.split()
        if len(parts) < 4:
            continue
            
        instance_id = parts[0]
        results = {
            models[0]: parts[1],
            models[1]: parts[2],
            models[2]: parts[3]
        }

        # 遍历每个模型及其对应的结果 (例如 "√×√")
        for model, res_str in results.items():
            if len(res_str) != 3:
                continue
                
            for round_idx, char in enumerate(res_str, 1):
                is_success = char == '√'
                state_key = "success" if is_success else "fail"
                
                # 拼接文件路径格式
                json_path = base_traj_dir / model / f"round{round_idx}" / instance_id / f"{instance_id}.traj.json"
                
                if not json_path.exists():
                    continue
                
                try:
                    with open(json_path, 'r', encoding='utf-8') as jf:
                        data = json.load(jf)
                        
                    # 遍历 messages, 提取 usage
                    traj_completion = 0
                    traj_prompt = 0
                    traj_total = 0
                    
                    for msg in data.get('messages', []):
                        if msg.get('role') == 'assistant' and 'extra' in msg:
                            extra = msg['extra']
                            if 'response' in extra and 'usage' in extra['response']:
                                usage = extra['response']['usage']
                                traj_completion += usage.get('completion_tokens', 0)
                                traj_prompt += usage.get('prompt_tokens', 0)
                                traj_total += usage.get('total_tokens', 0)
                    
                    # 记录到总计中
                    stats[model][state_key]["count"] += 1
                    stats[model][state_key]["completion"] += traj_completion
                    stats[model][state_key]["prompt"] += traj_prompt
                    stats[model][state_key]["total"] += traj_total
                    
                except Exception as e:
                    print(f"读取或解析 {json_path} 时出错: {e}")

    # 写入结果到目标文件
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write("各模型运行 Token 消耗统计\n")
        out.write("=" * 60 + "\n\n")
        
        for model in models:
            out.write(f"模型: {model}\n")
            out.write("-" * 60 + "\n")
            
            for state in ["success", "fail"]:
                state_label = "【成功】" if state == "success" else "【失败】"
                data = stats[model][state]
                count = data["count"]
                
                if count > 0:
                    avg_comp = data["completion"] / count
                    avg_prompt = data["prompt"] / count
                    avg_total = data["total"] / count
                    
                    out.write(f"  {state_label} 数据条数: {count}\n")
                    out.write(f"    Avg Completion Tokens  : {avg_comp:.2f}\n")
                    out.write(f"    Avg Prompt Tokens      : {avg_prompt:.2f}\n")
                    out.write(f"    Avg Total Tokens       : {avg_total:.2f}\n")
                else:
                    out.write(f"  {state_label} 数据条数: 0\n")
            out.write("\n")
            
    print(f"统计完成！结果已输出至: {output_file}")

if __name__ == "__main__":
    main()