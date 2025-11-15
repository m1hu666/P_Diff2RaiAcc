# -*- coding: utf-8 -*-
import argparse
import json
import os
from datasets import load_dataset
import tkinter as tk
from tkinter import scrolledtext, ttk, filedialog, messagebox
import platform

def get_result_path(model: str, round_num: int):
    return os.path.join('data', 'data', 'verified', model.replace('/', '_'), f'round{round_num}.json')

def get_swebench_data():
    ds = load_dataset("princeton-nlp/SWE-bench_Verified", split="test")
    return {item['instance_id']: item for item in ds}

def show_patch_window(gold_patch, model_patch, is_correct, instance_id):
    # Create main window with modern style
    root = tk.Tk()
    root.title(f'Patch Comparison - {instance_id}')
    root.geometry('1400x900')  # Larger initial window size
    root.minsize(1200, 800)    # Minimum window size
    
    # Modern color scheme
    bg_color = '#f8f9fa'
    header_bg = '#2d3436'
    panel_bg = '#ffffff'
    gold_color = '#dfe6e9'
    model_color = '#ffeaa7'
    accent_color = '#0984e3'
    correct_color = '#00b894'
    incorrect_color = '#d63031'
    
    root.configure(bg=bg_color)
    
    # Configure grid weights for responsive layout
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    
    # Header section
    header_frame = tk.Frame(root, bg=header_bg, height=80)
    header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=15)
    header_frame.grid_columnconfigure(0, weight=1)
    
    # Status label with larger font
    status_text = "Patch Correct" if is_correct else "Patch Incorrect"
    status_label = tk.Label(
        header_frame, 
        text=status_text, 
        font=('Segoe UI', 20, 'bold'), 
        bg=header_bg,
        fg=correct_color if is_correct else incorrect_color
    )
    status_label.grid(row=0, column=0, sticky="w", padx=20, pady=10)
    
    # Instance ID display
    id_label = tk.Label(
        header_frame, 
        text=f"Instance ID: {instance_id}", 
        font=('Segoe UI', 14), 
        bg=header_bg,
        fg='#ffffff'
    )
    id_label.grid(row=0, column=1, sticky="e", padx=20, pady=10)
    
    # Main content frame (includes toolbar and patch panels)
    main_frame = tk.Frame(root, bg=bg_color)
    main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_rowconfigure(0, weight=0)  # toolbar
    main_frame.grid_rowconfigure(1, weight=1)  # main panels
    
    # Toolbar (copy/save functions)
    def copy_to_clipboard(text):
        try:
            root.clipboard_clear()
            root.clipboard_append(text)
            messagebox.showinfo("Copied", "Content copied to clipboard")
        except Exception as e:
            messagebox.showerror("Error", f"Copy failed: {e}")

    def save_patch(text, default_name):
        path = filedialog.asksaveasfilename(defaultextension='.patch', initialfile=default_name)
        if path:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(text)
                messagebox.showinfo("Saved", f"Saved to: {path}")
            except Exception as e:
                messagebox.showerror("Error", f"Saving failed: {e}")

    toolbar = tk.Frame(main_frame, bg=bg_color)
    toolbar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))
    toolbar.grid_columnconfigure(0, weight=1)

    ttk.Button(toolbar, text="Copy Gold", command=lambda: copy_to_clipboard(gold_patch)).pack(side="left", padx=6)
    ttk.Button(toolbar, text="Copy Model", command=lambda: copy_to_clipboard(model_patch)).pack(side="left", padx=6)
    ttk.Button(toolbar, text="Save Gold", command=lambda: save_patch(gold_patch, f"{instance_id}_gold.patch")).pack(side="left", padx=6)
    ttk.Button(toolbar, text="Save Model", command=lambda: save_patch(model_patch, f"{instance_id}_model.patch")).pack(side="left", padx=6)

    # Gold Patch Panel
    gold_frame = tk.Frame(main_frame, bg=panel_bg, relief=tk.RAISED, bd=1)
    gold_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
    gold_frame.grid_columnconfigure(0, weight=1)
    gold_frame.grid_rowconfigure(1, weight=1)
    
    # Gold Patch Header
    gold_header = tk.Frame(gold_frame, bg=accent_color, height=50)
    gold_header.grid(row=0, column=0, sticky="ew")
    gold_header.grid_columnconfigure(0, weight=1)
    gold_header.pack_propagate(False)
    
    tk.Label(
        gold_header, 
        text="Gold Patch", 
        font=('Segoe UI', 16, 'bold'), 
        bg=accent_color,
        fg='white',
        pady=10,
        padx=15,
        anchor="w"
    ).grid(row=0, column=0, sticky="w")
    
    # Gold Patch Text Area with larger font
    gold_text = scrolledtext.ScrolledText(
        gold_frame, 
        wrap=tk.NONE,
        font=('Consolas', 12) if platform.system() != 'Windows' else ('Courier New', 12),
        bg=gold_color,
        relief=tk.FLAT,
        bd=0,
        padx=15,
        pady=15
    )
    gold_text.insert('1.0', gold_patch if gold_patch.strip() else "<No patch content>")
    gold_text.configure(state='disabled')
    gold_text.grid(row=1, column=0, sticky="nsew")
    
    # Horizontal scrollbar for gold patch
    gold_hscroll = ttk.Scrollbar(gold_frame, orient=tk.HORIZONTAL, command=gold_text.xview)
    gold_hscroll.grid(row=2, column=0, sticky="ew")
    gold_text.configure(xscrollcommand=gold_hscroll.set)
    
    # Model Patch Panel
    model_frame = tk.Frame(main_frame, bg=panel_bg, relief=tk.RAISED, bd=1)
    model_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
    model_frame.grid_columnconfigure(0, weight=1)
    model_frame.grid_rowconfigure(1, weight=1)
    
    # Model Patch Header
    model_header = tk.Frame(model_frame, bg=accent_color, height=50)
    model_header.grid(row=0, column=0, sticky="ew")
    model_header.grid_columnconfigure(0, weight=1)
    model_header.pack_propagate(False)
    
    tk.Label(
        model_header, 
        text="Model Patch", 
        font=('Segoe UI', 16, 'bold'), 
        bg=accent_color,
        fg='white',
        pady=10,
        padx=15,
        anchor="w"
    ).grid(row=0, column=0, sticky="w")
    
    # Model Patch Text Area with larger font
    model_text = scrolledtext.ScrolledText(
        model_frame, 
        wrap=tk.NONE,
        font=('Consolas', 12) if platform.system() != 'Windows' else ('Courier New', 12),
        bg=model_color,
        relief=tk.FLAT,
        bd=0,
        padx=15,
        pady=15
    )
    model_text.insert('1.0', model_patch if model_patch.strip() else "<No patch content>")
    model_text.configure(state='disabled')
    model_text.grid(row=1, column=0, sticky="nsew")
    
    # Horizontal scrollbar for model patch
    model_hscroll = ttk.Scrollbar(model_frame, orient=tk.HORIZONTAL, command=model_text.xview)
    model_hscroll.grid(row=2, column=0, sticky="ew")
    model_text.configure(xscrollcommand=model_hscroll.set)
    
    # Footer with close button
    footer_frame = tk.Frame(root, bg=bg_color, height=60)
    footer_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
    footer_frame.grid_columnconfigure(0, weight=1)
    
    close_btn = ttk.Button(
        footer_frame,
        text="Close Window",
        command=root.destroy,
        style="Modern.TButton"
    )
    close_btn.grid(row=0, column=1, sticky="e")
    
    # Configure modern button style
    style = ttk.Style()
    style.configure("Modern.TButton", 
                   font=('Segoe UI', 12),
                   padding=10)

    root.mainloop()

def main():
    parser = argparse.ArgumentParser(description='Visualize patch results and compare with gold standard')
    parser.add_argument('--m', type=str, required=True, help='Model name')
    parser.add_argument('--r', type=int, required=True, help='Round number')
    parser.add_argument('--i', type=str, required=True, help='Instance ID')
    parser.add_argument('--key', type=str, nargs='*', help='Attributes to output')
    parser.add_argument('--v', action='store_true', help='Visualize diff')
    args = parser.parse_args()
    
    result_path = get_result_path(args.m, args.r)
    if not os.path.exists(result_path):
        print(f"Result file not found: {result_path}")
        return
    with open(result_path, 'r', encoding='utf-8') as f:
        result_data = json.load(f)
    
    instance_obj = result_data.get(args.i)
    if not instance_obj:
        print(f"Instance '{args.i}' not found in result file.")
        return
    
    print("Loading SWE-bench-verified from HuggingFace...")
    sb_data = get_swebench_data()
    sb_obj = sb_data.get(args.i)
    if not sb_obj:
        print(f"Instance '{args.i}' not found in swe-bench-verified dataset.")

    if args.key:
        print("== From result ==")
        for k in args.key:
            print(f"{k}: {instance_obj.get(k, '<No such data>')}")
        if sb_obj:
            print("== From swe-bench-verified ==")
            for k in args.key:
                print(f"{k}: {sb_obj.get(k, '<No such data>')}")

    if args.v:
        gold_patch = sb_obj.get('patch', '') if sb_obj else ''
        model_patch = instance_obj.get('model_patch', '')
        is_correct = (model_patch.strip() == gold_patch.strip())
        print(f"\nPatch Correct: {is_correct}")

        # Removed unified diff printing part
        show_patch_window(gold_patch, model_patch, is_correct, args.i)

if __name__ == '__main__':
    main()