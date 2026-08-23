import torch
import re
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from sandbox import execute_python_code


SYSTEM_PROMPT = """Bạn là một Tác tử Lập trình. Trước khi viết code, hãy chọn Cấp độ nhận thức (Cognitive Level):
- [L1]: Phản xạ nhanh (Chỉ viết code ngay, không cần suy luận).
- [L2]: Quy tắc mẫu (Suy luận ngắn gọn 1 câu).
- [L3]: Lập luận điều kiện (Phân tích lỗi từ môi trường để sửa).
- [L4]: Chiến lược (Suy luận từng bước chi tiết trước khi giải quyết bài toán phức tạp).

Định dạng xuất bắt buộc
Level: [L1][L2][L3][L4]
Thought: [Suy nghĩ của bạn dựa trên Level đã chọn]
Action: [chỉ chứa mã nguồn Python, đặt trong block ```python ...```]
"""


# hàm chạy agent lập (agentic loop)
def run_agent_loop(task: str, max_steps: int = 3):
    model_id = "Qwen/Qwen2.5-Coder-7B-Instruct"
    print('đang nạp mô hình')
    
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16
    )
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=bnb_config, device_map="auto")
    
    message = [
        {"role": "system", "content":SYSTEM_PROMPT},
        {"role": "user", "content": task}
    ]
    
    for step in range(max_steps):
        print(f"\n{'='*10} bước {step+1} {'='*10}")
        # sinh câu trả lời từ LLM 
        text_input = tokenizer.apply_chat_template(message, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer([text_input], return_tensors="pt").to(model.device)
        outputs = model.generate(**inputs, max_new_tokens=512, temperature=0.2)
        response = tokenizer.decode(outputs[0][len(inputs.input_ids[0]):], skip_special_tokens=True)
        
        print(f"\n[Mô hình phản hồi]:\n{response}")
        message.append({"role": "assistant", "content": response})
        
        # trích xuất code từ action
        match = re.search(r"```python(.*?)```", response, re.DOTALL)
        if match:
            code = match.group(1).strip()
            print(f"\n[Đang chạy công cụ (sandbox)...]:\n{code}")
            observation = execute_python_code(code)
            print(observation)
            
            if "THÀNH CÔNG" in observation:
                print("\n[Môi trường phản hồi]:\nCode chạy thành công, kết thúc vòng lặp.")
                break
            else:
                message.append({"role": "user", "content": f"Code của bạn sinh ra lỗi khi chạy trong môi trường:\n{observation}\nHãy chuyển sang Level 3 (Lập luận điều kiện) hoặc Level 4 (Chiến lược) để phân tích lỗi và viết lại code khắc phục hoàn chỉnh."})
        else:
            print("Không tìm thấy khối mã Python ```python ... ``` hợp lệ. Dừng.")
            break
        
if __name__ == "__main__":
    task = """Hãy viết một đoạn code Python sử dụng thư viện 're' để tìm tất cả các địa chỉ email hợp lệ trong chuỗi văn bản sau:
    'Liên hệ hỗ trợ qua email admin@texteditor.com hoặc support@regex.vn. Đừng gửi vào test@ fail.'
    Sau đó in danh sách email ra màn hình."""
    run_agent_loop(task)