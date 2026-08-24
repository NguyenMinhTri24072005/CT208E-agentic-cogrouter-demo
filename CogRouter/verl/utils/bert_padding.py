# Pure PyTorch fallback for flash_attn.bert_padding
import torch

try:
    from einops import rearrange
except ImportError:
    def rearrange(tensor, pattern, **kwargs):
        # Basic rearrange fallback if einops not present
        if "b s ... -> (b s) ..." in pattern:
            orig = tensor.shape
            return tensor.reshape(orig[0] * orig[1], *orig[2:])
        elif "(b s) d -> b s d" in pattern:
            b = kwargs.get("b")
            s = kwargs.get("s")
            return tensor.reshape(b, s, -1)
        return tensor

def index_first_axis(tensor: torch.Tensor, indices: torch.Tensor) -> torch.Tensor:
    orig_shape = tensor.shape
    return tensor.reshape(orig_shape[0], -1)[indices].reshape(-1, *orig_shape[1:])

def unpad_input(hidden_states: torch.Tensor, attention_mask: torch.Tensor):
    """
    Pure PyTorch implementation of unpad_input.
    """
    seqlens_in_batch = attention_mask.sum(dim=-1, dtype=torch.int32)
    indices = torch.nonzero(attention_mask.flatten(), as_tuple=False).flatten()
    max_seqlen_in_batch = int(seqlens_in_batch.max().item()) if seqlens_in_batch.numel() > 0 else 0
    cu_seqlens = torch.nn.functional.pad(torch.cumsum(seqlens_in_batch, dim=0, dtype=torch.int32), (1, 0))
    orig_shape = hidden_states.shape
    hidden_states_flat = hidden_states.reshape(orig_shape[0] * orig_shape[1], *orig_shape[2:])
    return (
        hidden_states_flat[indices],
        indices,
        cu_seqlens,
        max_seqlen_in_batch,
    )

def pad_input(hidden_states: torch.Tensor, indices: torch.Tensor, batch: int, seqlen: int):
    """
    Pure PyTorch implementation of pad_input.
    """
    dim_shapes = hidden_states.shape[1:]
    output = torch.zeros((batch * seqlen, *dim_shapes), device=hidden_states.device, dtype=hidden_states.dtype)
    output[indices] = hidden_states
    return output.reshape(batch, seqlen, *dim_shapes)
