# Agentic Cognitive Router Demo (CT208E)

Dự án kết hợp 2 công trình nghiên cứu:
1. **[Awesome-Agentic-Reasoning](./Awesome-Agentic-Reasoning)**: Tổng quan lý thuyết, phân loại nhận thức (Taxonomy), các cơ chế Self-Evolution, Feedback và Benchmarks của LLM Agent.
2. **[CogRouter](./CogRouter)**: Cơ chế thích ứng độ sâu nhận thức đa cấp (ACT-R: L1 Reflex -> L2 Situational -> L3 Reflection -> L4 Strategic) và thuật toán CoPo (Cognition-aware Policy Optimization).

---

## 🚀 Hướng dẫn chạy trên Kaggle (GPU Runtime)

### Bước 1: Mở Notebook mới trên Kaggle
1. Đăng nhập vào [Kaggle](https://www.kaggle.com/).
2. Chọn **Create** -> **New Notebook**.
3. Tại menu bên phải mục **Notebook Settings**:
   - **Accelerator**: Chọn **GPU T4 x2** (hoặc GPU P100).
   - **Internet**: Bật sang **On**.

### Bước 2: Clone repository và cài đặt thư viện
Chạy cell sau trong Kaggle Notebook:
```bash
!git clone https://github.com/NguyenMinhTri24072005/CT208E-agentic-cogrouter-demo.git
%cd CT208E-agentic-cogrouter-demo
!pip install -q -r requirements.txt
```

### Bước 3: Chạy Agentic Cognitive Router Demo
```bash
!python demo_agent.py
```

---

## 📁 Cấu trúc thư mục

* `demo_agent.py`: Vòng lặp Agentic Loop (nhận thức L1-L4) tích hợp Qwen2.5-Coder-7B-Instruct.
* `sandbox.py`: Môi trường thực thi code Python cách ly và bắt phản hồi từ môi trường.
* `requirements.txt`: Các thư viện cơ bản cho demo.
* `CogRouter/`: Mã nguồn gốc của phương pháp CoPo & Cognitive Depth Router.
* `Awesome-Agentic-Reasoning/`: Tài liệu khảo sát toàn diện và danh mục Benchmark về Agentic Reasoning.
