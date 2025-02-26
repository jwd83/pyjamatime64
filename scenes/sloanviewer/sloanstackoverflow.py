# from stackoverflow to process sloan data as an example for a histogram
import astropy.cosmology
from scipy.stats.kde import gaussian_kde
import astropy.coordinates
import astropy.units as u
import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt("sloandata.csv", delimiter=",")
sloan_digital_sky_survey_low_redshift = np.array(
    [np.array([i[1], i[2], i[3]]) for i in data]
)
comoving_dist = astropy.cosmology.WMAP9.comoving_distance(
    sloan_digital_sky_survey_low_redshift[:, 2]
)
c = astropy.coordinates.SkyCoord(
    ra=sloan_digital_sky_survey_low_redshift[:, 0] * u.degree,
    dec=sloan_digital_sky_survey_low_redshift[:, 1] * u.degree,
    distance=comoving_dist * u.mpc,
)
sloan_digital_sky_survey_pos = np.stack(
    [np.array([i.x.value, i.y.value, i.z.value]) for i in c.cartesian]
)
# Removing nans
mask = np.all(
    np.isnan(sloan_digital_sky_survey_pos) | np.equal(sloan_digital_sky_survey_pos, 0),
    axis=1,
)
sloan_digital_sky_survey_pos = sloan_digital_sky_survey_pos[~mask]


x, y = sloan_digital_sky_survey_pos[:, 2], sloan_digital_sky_survey_pos[:, 1]
heatmap, xedges, yedges = np.histogram2d(x, y, bins=50)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

plt.clf()
plt.figure(figsize=(8, 6))
plt.gca().set_aspect("equal")
plt.imshow(heatmap.T, extent=extent, origin="lower", cmap=plt.get_cmap("nipy_spectral"))


# save image to disk
plt.savefig("sloanviewer.png")
plt.show()
