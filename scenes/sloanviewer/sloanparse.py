from csv import DictReader, DictWriter

# open sloandata.csv, grab headers from first row
import astropy
import astropy.cosmology
import astropy.coordinates
import astropy.units as u
import numpy as np


def main():
    path = "sloandata2.csv"
    path_out = "sloandata2_out_clean.csv"
    writer = None
    skipped = 0
    with open(path, "r") as file:
        reader = DictReader(file)

        with open(path_out, "w") as file_out:

            for i, row in enumerate(reader):

                ra = row["ra"]
                dec = row["dec"]
                z = row["z"]

                if float(z) == 0:
                    skipped += 1
                    # print("Skipping row with redshift (z)=0")
                    continue

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
                    "distance (mPc)": distance,
                    "distance (ly)": distance * 3.262e6,
                }

                if writer is None:
                    writer = DictWriter(file_out, fieldnames=row_out.keys())
                    writer.writeheader()

                writer.writerow(row_out)

    # write to new file
    print(f"Skipped {skipped} rows")


if __name__ == "__main__":
    main()
