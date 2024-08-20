import mrcfile
import numpy as np
import datetime

from bfastor import models


class Map:
    """
    An EM map.
    """

    @classmethod
    def from_file(cls, filename):
        with mrcfile.open(filename) as mrc:
            apix = np.array([mrc.voxel_size.x, mrc.voxel_size.y, mrc.voxel_size.z])
            origin = np.array(
                [mrc.header.origin.x, mrc.header.origin.y, mrc.header.origin.z]
            )
            axes_order = [
                int(mrc.header.mapc) - 1,
                int(mrc.header.mapr) - 1,
                int(mrc.header.maps) - 1,
            ]

            apix = np.array(
                (apix[axes_order[0]], apix[axes_order[1]], apix[axes_order[2]])
            )

            origin = np.array(
                (origin[axes_order[0]], origin[axes_order[1]], origin[axes_order[2]])
            )

            new_axes = [2 - axes_order[2 - a] for a in (0, 1, 2)]
            data = np.transpose(mrc.data, axes=new_axes)

            return cls(
                data.astype(float),
                apix,
                origin,
            )

    def __init__(self, data, apix, origin):
        self.data = np.array(data)
        self.apix = np.array(apix)
        self.origin = np.array(origin)

    def copy(self):
        return Map(self.data.copy(), self.apix.copy(), self.origin.copy())

    def crop(self, min_corner, max_corner):
        assert np.all(min_corner >= [0, 0, 0])
        assert np.all(max_corner <= self.data.shape)
        self.data = self.data[
            min_corner[0] : max_corner[0],
            min_corner[1] : max_corner[1],
            min_corner[2] : max_corner[2],
        ]
        self.origin += np.flip(min_corner * self.apix)

    def write_mrc(self, filename, overwrite=True):
        label = "Created by TEMPy on: " + str(datetime.date.today())
        fullMap_f32 = self.data.astype("float32")

        with mrcfile.new(filename, overwrite=overwrite) as mrc:
            mrc.set_data(fullMap_f32)

            # Write out modern MRC files which prefer origin over
            # nstart fields.
            mrc.header.nxstart = 0
            mrc.header.nystart = 0
            mrc.header.nzstart = 0

            # These are determined by density array
            mrc.header.mx = self.data.shape[2]
            mrc.header.my = self.data.shape[1]
            mrc.header.mz = self.data.shape[0]

            # TEMPy should produce maps which have x,y,z ordering
            mrc.header.mapc = 1
            mrc.header.mapr = 2
            mrc.header.maps = 3

            mrc.header.cellb.alpha = 90
            mrc.header.cellb.beta = 90
            mrc.header.cellb.gamma = 90

            mrc.header.ispg = 1
            mrc.header.origin.x = self.origin[0]
            mrc.header.origin.y = self.origin[1]
            mrc.header.origin.z = self.origin[2]

            mrc.header.label[0] = label
            mrc.voxel_size = tuple(self.apix)


def get_cropped_data_from_map(exp_map: Map, model: models.Structure, padding: int = 5):
    copied_map = exp_map.copy()
    min_corner, max_corner = get_map_bounding_box_around_xyz_coordinates(
        exp_map, model.get_column_data(["x", "y", "z"]), padding=padding
    )
    copied_map.crop(min_corner, max_corner)
    return copied_map


def normalise(exp_map: Map):
    return Map(
        (exp_map.data - np.mean(exp_map.data)) / np.std(exp_map.data),
        origin=exp_map.origin,
        apix=exp_map.apix,
    )


def get_map_bounding_box_around_xyz_coordinates(exp_map: Map, coordinates, padding=0):
    min_xyz = np.maximum(
        (np.min(coordinates, axis=0) - exp_map.origin) / np.flip(exp_map.apix)
        - padding,
        np.zeros(3),
    )
    max_xyz = np.minimum(
        (np.max(coordinates, axis=0) - exp_map.origin) / np.flip(exp_map.apix)
        + padding,
        np.flip(exp_map.data.shape),
    )

    min_zyx = np.flip(np.floor(min_xyz)).astype(int)
    max_zyx = np.flip(np.ceil(max_xyz)).astype(int)

    return min_zyx, max_zyx
