import astropy.cosmology
from scipy.stats.kde import gaussian_kde
import astropy.coordinates
import astropy.units as u
import numpy as np

data = np.genfromtxt('your_csv_file'), delimiter=',')
sdss_low_redshift = np.array([np.array([i[1], i[2], i[3]]) for i in data])
comoving_dist = astropy.cosmology.WMAP9.comoving_distance(sdss_low_redshift[:, 2])
c = astropy.coordinates.SkyCoord(ra=sdss_low_redshift[:, 0]*u.degree, dec=sdss_low_redshift[:, 1]*u.degree, distance=comoving_dist*u.mpc)
sdss_pos = np.stack([np.array([i.x.value, i.y.value, i.z.value]) for i in c.cartesian])
# Removing nans
mask = np.all(np.isnan(sdss_pos) | np.equal(sdss_pos, 0), axis=1)
sdss_pos = sdss_pos[~mask]


x, y = sdss_pos[:, 2], sdss_pos[:, 1]
heatmap, xedges, yedges = np.histogram2d(x, y, bins=50)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

plt.clf()
plt.figure(figsize=(8, 6))
plt.gca().set_aspect('equal')
plt.imshow(heatmap.T, extent=extent, origin='lower', cmap=plt.get_cmap('nipy_spectral'))
