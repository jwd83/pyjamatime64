from csv import DictReader, DictWriter

# open sloandata.csv, grab headers from first row
import astropy
import astropy.cosmology
import astropy.coordinates
import astropy.units as u
import numpy as np


def main():
    path = "sloandata.csv"
    path_out = "sloandata_out.csv"
    writer = None
    with open(path, "r") as file:
        reader = DictReader(file)

        with open(path_out, "w") as file_out:

            # display the first 10 rows

            for i, row in enumerate(reader):

                # if i == 10:
                #     break

                ra = row["ra"]
                dec = row["dec"]
                z = row["z"]

                # convert to cartesian coordinates
                # comoving distance
                comoving_dist = astropy.cosmology.WMAP9.comoving_distance(float(z))
                c = astropy.coordinates.SkyCoord(
                    ra=float(ra) * u.degree,
                    dec=float(dec) * u.degree,
                    distance=comoving_dist * u.mpc,
                )

                cx = c.cartesian.x.value
                cy = c.cartesian.y.value
                cz = c.cartesian.z.value

                # distance from origin
                distance = np.sqrt(cx**2 + cy**2 + cz**2)

                row_out = {
                    "ra": ra,
                    "dec": dec,
                    "z": z,
                    "cx": c.cartesian.x.value,
                    "cy": c.cartesian.y.value,
                    "cz": c.cartesian.z.value,
                    "distance": distance,
                }

                if writer is None:
                    writer = DictWriter(file_out, fieldnames=row_out.keys())
                    writer.writeheader()

                writer.writerow(row_out)

            # write to new file


if __name__ == "__main__":
    main()
