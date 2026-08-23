import subprocess 
import tempfile
import os
import sys

def execute_python_code(code: str, timeout: int = 5) -> str: 
    """công cụ thực thi code và bắt phản hồi từ môi trường"""
    # tạo một file python tạm thời để chạy code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as temp_file:
        temp_file.write(code)
        temp_path = temp_file.name
    try: 
        # chạy code python trong môi trường subprocess cách ly và với timeout
        result = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode == 0:
            return f"[Môi trường phản hồi THÀNH CÔNG]:\n{result.stdout}"
        else:
            return f"[Môi trường phản hồi THẤT BẠI]:\n{result.stderr}"
    except subprocess.TimeoutExpired:
        return "[Môi trường phản hồi THẤT BẠI]:\nThời gian thực thi code vượt quá giới hạn cho phép."
    finally:
        # xóa file tạm thời sau khi thực thi
        if os.path.exists(temp_path):
            os.remove(temp_path)