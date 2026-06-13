from typing import List, Any

def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """Divide una lista en chunks de tamaño chunk_size"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def format_bytes(bytes: int) -> str:
    """Formatea bytes a KB, MB, GB"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024
    return f"{bytes:.2f} TB"

def safe_divide(a: float, b: float, default: float = 0.0) -> float:
    return a / b if b != 0 else default