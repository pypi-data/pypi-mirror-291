# **R**otation of **3**-dimensional **F**rames

Functions
---------
This library includes four sets of functions: general array checks,
attitude-representation conversions, reference-frame conversions, and rotation
matrix (direction cosine matrix) utilities.

All twenty possible conversions among the following five attitude
representations are provided: rotation vector, rotation axis and angle, roll and
pitch and yaw (RPY) Euler angles, direction cosine matrix (DCM), and quaternion.
However, some of the conversions are built using other conversions. In the
following table, the low-level conversions are marked with an `x` and the
conversions build using the other conversions are marked with an `o`:

|         | vector  | ax, ang |   RPY   |   DCM   |  quat   |
| ------- | ------- | ------- | ------- | ------- | ------- |
| vector  |    -    |    x    |    o    |    o    |    o    |
| ax, ang |    x    |    -    |    o    |    x    |    x    |
|   RPY   |    o    |    x    |    -    |    x    |    x    |
|   DCM   |    o    |    x    |    x    |    -    |    x    |
|  quat   |    o    |    x    |    x    |    x    |    -    |

The roll, pitch, and yaw angles are applied in a zyx sequence of passive
rotations. The quaternions follow a Hamilton convention. Here is an example:

```python
roll = 20*np.pi/180
pitch = 45*np.pi/180
yaw = 10*np.pi/180
C = r3f.rpy_to_dcm([roll, pitch, yaw])
>> C = [[ 0.69636424  0.1227878  -0.70710678]
    [ 0.07499469  0.96741248  0.24184476]
    [ 0.71375951 -0.2214413   0.66446302]]
```

In addition to the conversion from the z, y, x sequence of Euler angles to a
DCM, the function `rot` is also provided for creating a DCM from a generic set
of Euler angles in any desired sequence of axes. Although this `rot` function
could be used, two additional functions are provided for generating rotation
matrices: `dcm_inertial_to_ecef` and `dcm_ecef_to_navigation`. By default, all
angles are treated as being in radians, but if the `degs` parameter is set to
True, then they are treated as being in degrees.

This library includes all twelve possible conversions among the following four
frames: ECEF (Earth-centered, Earth-fixed), geodetic (latitude, longitude, and
height above ellipsoid), local-level tangent, and local-level curvilinear. By
default, all local-level coordinates are interpreted as having a North, East,
Down (NED) orientation, but if the `ned` parameter is set to False, the
coordinates are interpreted as having an East, North, Up (ENU) orientation. Here
is an example:

```python
lat = 45*np.pi/180
lon = 0.0
hae = 1000.0
[xe, ye, ze] = r3f.geodetic_to_ecef([lat, lon, hae])
>> xe = 4518297.985630118
>> ye = 0.0
>> ze = 4488055.515647106
```

The rotation matrix utility functions are an `orthonormalize_dcm` function, a
`rodrigues_rotation` function, and an `inverse_rodrigues_rotation` function. The
`orthonormalize_dcm` function will work to make a rotation matrix normalized and
orthogonal, a proper rotation matrix. The two Rodrigues's rotation functions are
meant for converting a vector to the matrix exponential of the skew-symmetric
matrix of that vector and back again.

Passive Rotations
-----------------
Unless specifically otherwise stated, all rotations are interpreted as passive.
This means they represent rotations of reference frames, not of vectors.

Vectorization
-------------
When possible, the functions are vectorized in order to handle processing
batches of values. A set of scalars is a 1D array. A set of vectors is a 2D
array, with each vector in a column. So, a (3, 7) array is a set of seven
vectors, each with 3 elements. If the `axis` parameter is set to 0, the
transpose is true. A set of matrices is a 3D array with each matrix in a stack.
The first index is the stack number. So, a (5, 3, 3) array is a stack of five
3x3 matrices. Roll, pitch, and yaw are not treated as a vector but as three
separate quantities. The same is true for latitude, longitude, and height above
ellipsoid. A quaternion is passed around as an array.

Robustness
----------
In general, the functions in this library check that the inputs are of the
correct type and shape. They do not generally handle converting inputs which do
not conform to the ideal type and shape. Generally, the allowed types are int,
float, list, and np.ndarray.
