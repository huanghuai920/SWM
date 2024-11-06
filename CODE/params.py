import numpy as np

# =============================================================================
# physical constants
# =============================================================================
g     = 9.81              # gravity accleration, m s^-2
H     = 10000
a     = 6371000           # Earth's radius
Omega = 2*np.pi/86400     # Angular velocity of Earth
lat   = 0                 # latitude

f     = 2*Omega*np.sin(np.radians(lat))  # Coriolis parameter

# =============================================================================
# grid configuration
# =============================================================================
nx = 200       # grid
ny = 200       # grid
dx = 50000     # x-direction gridsize (m)
dy = 50000     # y-direction gridsize (m)
nt = 15000     # total timesteps
dt = 90        # time interval

# setup x, y grids
x = np.linspace(-nx/2*dx, nx/2*dx, nx)
y = np.linspace(-ny/2*dy, ny/2*dy, ny)

# setup 2-D grids
xx, yy = np.meshgrid(x, y)

# constants for tendency calculation
D2x = 1/(2*dx)
D2y = 1/(2*dy)

# =============================================================================
# model configuration
# =============================================================================
nsave = 100             # time step
nplot = 100             # time step
add_coriolis = True
add_topography = False
add_heating = False


# =============================================================================
# model constants
# =============================================================================
k = 1e4                   # diffusion coefficient
r = 1e-2                  # time filter coefficient



