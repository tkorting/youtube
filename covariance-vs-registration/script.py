#######################################
# create scatterplots for correlation #
#######################################
import rasterio as rio
import matplotlib.pyplot as plt

raster_path = 'AMAZONIA_1_WFI_20241111_035_020_L4_bgrnir_crop.tif'

with rio.open(raster_path) as raster:
    matrix_band1 = raster.read(1)
    matrix_band2 = raster.read(2)
    matrix_band3 = raster.read(3)    
    matrix_band4 = raster.read(4)

rows, columns = matrix_band1.shape

L = 10
plt.figure(figsize=(20, 7))
plt.subplot(2, 4, 1)
plt.imshow(matrix_band1, cmap='gray', vmin=0, vmax=2**L);
plt.title(f'Crop from band 1, blue');
plt.colorbar()

plt.subplot(2, 4, 2)
plt.imshow(matrix_band2, cmap='gray', vmin=0, vmax=2**L);
plt.title(f'Crop from band 2, green');
plt.colorbar()

plt.subplot(2, 4, 3)
plt.imshow(matrix_band3, cmap='gray', vmin=0, vmax=2**L);
plt.title(f'Crop from band 3, red');
plt.colorbar()

plt.subplot(2, 4, 4)
plt.imshow(matrix_band4, cmap='gray', vmin=0, vmax=2**L);
plt.title(f'Crop from band 4, nir');
plt.colorbar()

# computing scatterplots for pairs
scatterplot_b1b2 = np.zeros((2**L, 2**L))
for b1, b2 in zip(matrix_band1.flatten(), matrix_band2.flatten()):
    scatterplot_b1b2[b1, b2] = scatterplot_b1b2[b1, b2] + 1

scatterplot_b1b3 = np.zeros((2**L, 2**L))
for b1, b3 in zip(matrix_band1.flatten(), matrix_band3.flatten()):
    scatterplot_b1b3[b1, b3] = scatterplot_b1b3[b1, b3] + 1

scatterplot_b2b4 = np.zeros((2**L, 2**L))
for b2, b4 in zip(matrix_band2.flatten(), matrix_band4.flatten()):
    scatterplot_b2b4[b2, b4] = scatterplot_b2b4[b2, b4] + 1

scatterplot_b3b4 = np.zeros((2**L, 2**L))
for b3, b4 in zip(matrix_band3.flatten(), matrix_band4.flatten()):
    scatterplot_b3b4[b3, b4] = scatterplot_b3b4[b3, b4] + 1

plt.subplot(2, 4, 5)
plt.imshow(scatterplot_b1b2, cmap='gray_r', origin='lower', norm='symlog');
plt.title(f'blue x green'); plt.colorbar()

plt.subplot(2, 4, 6)
plt.imshow(scatterplot_b1b3, cmap='gray_r', origin='lower', norm='symlog');
plt.title(f'blue x red'); plt.colorbar()

plt.subplot(2, 4, 7)
plt.imshow(scatterplot_b2b4, cmap='gray_r', origin='lower', norm='symlog');
plt.title(f'green x nir'); plt.colorbar()

plt.subplot(2, 4, 8)
plt.imshow(scatterplot_b3b4, cmap='gray_r', origin='lower', norm='symlog');
plt.title(f'red x nir'); plt.colorbar()

plt.tight_layout(); plt.show()

#############
# animation #
#############

import numpy as np
import rasterio as rio
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.ndimage import shift
from IPython.display import display, clear_output
from mpl_toolkits.axes_grid1 import make_axes_locatable

filename_in_animation = "animation/"

def get_covariance(x, y):
    xbar, ybar = x.mean(), y.mean()
    return np.sum((x - xbar) * (y - ybar)) / (len(x))

row_start, row_end = 100, 600
col_start, col_end = 100, 600
offset = 50
L = 8
pan_raster_path = 'CBERS_4_PAN10M_20260513_153_126_L2_BAND1_clip.tif'
nir_raster_path = 'CBERS_4_PAN10M_20260513_153_126_L2_BAND4_clip.tif'
red_channel = mpatches.Patch(color='red', label='Panchromatic band')
green_channel = mpatches.Patch(color='green', label='NIR band')
blue_channel = mpatches.Patch(color='blue', label='None')
with rio.open(pan_raster_path) as src:
    pan_matrix = src.read(1)[row_start:row_end, col_start:col_end] + offset
with rio.open(nir_raster_path) as src:
    # provide more bad shifts to highlight the need for registration
    d_row, d_col = 20, -55
    nir_matrix = src.read(1)[row_start+d_col:row_end+d_col, col_start+d_row:col_end+d_row]
rows, columns = pan_matrix.shape

fig, ax = plt.subplots(1,2, figsize=(16, 8))
rgb_matrix = np.transpose([pan_matrix, nir_matrix, np.zeros_like(pan_matrix)], (2,1,0))
plot_rgb = ax[0].imshow(rgb_matrix, vmin=0, vmax=2**L);
ax[0].legend(handles=[red_channel, green_channel, blue_channel], loc='upper left')
ax[0].set_title(f'd_row {0}, d_col {0}'), ax[0].axis('off')
divider_fake = make_axes_locatable(ax[0])
cax_fake = divider_fake.append_axes('right', size='5%', pad=0.1)
cax_fake.axis('off')

max_shift = 30
step = 1
matrix_shift = np.zeros((max_shift // step, max_shift // step))
plot_shifts = ax[1].imshow(matrix_shift, vmin=0.0, vmax=1.0)
(plot_best_shift,) = ax[1].plot(0, 0, color='red', linewidth=2, marker='x')
ax[1].set_title(f'correlation {0}'), ax[1].axis('off')
divider = make_axes_locatable(ax[1])
cax = divider.append_axes('right', size='5%', pad=0.1)
cbar = fig.colorbar(plot_shifts, cax=cax)

animation_step = 0
best_correlation = 0.0
best_d_row, best_d_col = 0, 0
for d_row in range(0, max_shift, step):
    for d_col in range(0, max_shift, step):
        with rio.open(pan_raster_path) as src:
            shifted_pan_matrix = src.read(1)[row_start+d_col:row_end+d_col, col_start+d_row:col_end+d_row] + offset

        # computing variance, covariance and correlation
        variance_pan = shifted_pan_matrix.flatten().var()
        variance_nir = nir_matrix.flatten().var()
        covariance_pan_nir = get_covariance(shifted_pan_matrix.flatten(), nir_matrix.flatten())
        correlation_pan_nir = covariance_pan_nir / np.sqrt(variance_pan * variance_nir)

        matrix_shift[d_row // step, d_col // step] = correlation_pan_nir
        if correlation_pan_nir > best_correlation:
            best_correlation = correlation_pan_nir
            best_d_row, best_d_col = d_row, d_col
            
        rgb_matrix = np.transpose([shifted_pan_matrix, nir_matrix, np.zeros_like(pan_matrix)], (2,1,0))
        plot_rgb.set_data(rgb_matrix);
        ax[0].set_title(f'Actual shift between bands is (d_row, d_col) {d_row, d_col}')

        plot_shifts.set_data(matrix_shift)
        plot_best_shift.set_data(best_d_col, best_d_row)
        ax[1].set_title(f'Correlation map: current {correlation_pan_nir:.2f}, best {best_correlation:.2f} -> shift {best_d_row, best_d_col}')
        
        plt.tight_layout() 
        # fig.savefig(filename_in_animation + f'register_by_correlation_{str(animation_step).zfill(6)}.png', format='png', dpi=200)
        # to create the animation, after running the script, use the following
        # ffmpeg -f image2 -pattern_type glob -i "animation/register_by_correlation_*.png" -r 25 -b 50000000 -filter:v "setpts=1.25*PTS" -an register_by_correlation.flv
        animation_step += 1
        clear_output(wait=True)
        display(fig)
plt.close(fig)

plt.figure(figsize=(7, 7))
best_shift_pan_matrix = shift(pan_matrix, shift=(-best_d_col, -best_d_row), mode='constant', cval=np.nan)
rgb_matrix = np.transpose([best_shift_pan_matrix, nir_matrix, np.zeros_like(pan_matrix)], (2,1,0))
plt.imshow(rgb_matrix); plt.axis('off')
plt.title(f'Best registration, correlation {best_correlation:.2f} -> shift {best_d_row, best_d_col}');
