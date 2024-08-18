# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/C. Benchmark.ipynb.

# %% auto 0
__all__ = []

# %% ../nbs/C. Benchmark.ipynb 2
import time
import torch
from fastcore.script import call_parse
from whisperspeech.pipeline import Pipeline
from whisperspeech.inference import get_compute_device

# %% ../nbs/C. Benchmark.ipynb 3
def measure(fun, iterations = 10):
    ts = []
    for x in range(iterations):
        start = time.time()
        fun()
        getattr(torch, get_compute_device()).synchronize()
        ts.append(time.time() - start)
    ts = torch.tensor(ts)
    return ts.mean(), ts.std()

@call_parse
def benchmark(
    t2s_ref='collabora/whisperspeech:t2s-small-en+pl.model',
    s2a_ref='collabora/whisperspeech:s2a-q4-tiny-en+pl.model',
    batch_size : int = 1,
    max_batch_size : int = None,
    no_torch_compile : bool = False,
    s2a_ctx_n : int = None,
    t2s_ctx_n : int = None,
    iterations = 10,
):
    max_batch_size = max_batch_size or batch_size

    pipe = Pipeline(t2s_ref=t2s_ref, s2a_ref=s2a_ref, optimize=False)

    if t2s_ctx_n:
        pipe.t2s.stoks_len = t2s_ctx_n
        pipe.t2s.decoder.mask = torch.empty(t2s_ctx_n, t2s_ctx_n).fill_(-torch.inf).triu_(1).to(get_compute_device())
    
    pipe.t2s.optimize(max_batch_size=max_batch_size, torch_compile=not no_torch_compile)

    if s2a_ctx_n:
        pipe.s2a.ctx_n = s2a_ctx_n
        pipe.s2a.decoder.mask = torch.empty(s2a_ctx_n, s2a_ctx_n).fill_(-torch.inf).triu_(1).to(get_compute_device())

    pipe.s2a.optimize(max_batch_size=max_batch_size, torch_compile=not no_torch_compile)

    txt = "This is the first demo of Whisper Speech, a fully open source text-to-speech model trained by Collabora and Lion on the Juwels supercomputer."
    stoks = torch.zeros(250)
    t = len(stoks)/25
    
    def t2s():
        return pipe.t2s.generate(txt, bs=batch_size, show_progress_bar=False)
    def s2a():
        return pipe.s2a.generate(stoks, pipe.default_speaker.unsqueeze(0), bs=batch_size, show_progress_bar=False)

    # warmup
    t2s()
    s2a()
    
    t2s_mean, t2s_std = measure(t2s, iterations=iterations)
    s2a_mean, s2a_std = measure(s2a, iterations=iterations)
    print(f"T2S: {t2s_mean:.3f} ± {t2s_std:.3f} s    S2A: {s2a_mean:.3f} ± {s2a_std:.3f} s    Total: {t2s_mean+s2a_mean:.3f} s")
    print(f"     {t/t2s_mean:.2f}x                  {t/s2a_mean:.2f}x                    {t/(t2s_mean+s2a_mean):.2f}x")
