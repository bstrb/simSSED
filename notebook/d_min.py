# constants
λ  = 0.019687   # Å
L  = 1.7        # m
P  = 17_857.14285714286  # pix per m

# helper (same as before)
def d_min(n_pix):
    import math, numpy as np
    R = n_pix / P
    θ = 0.5 * math.atan(R / L)
    return λ / (2 * math.sin(θ))

N = 1024           # example frame size
print(f"edge  : {d_min(N/2):.3f} Å")        # 2048 px
print(f"corner: {d_min(N/2*2**0.5):.3f} Å") # 2896 px
