"""Shims de compatibilidad para correr el pipeline en Python 3.9.

pyxelate 2.1.1 (HEAD) hace `from skimage.morphology import footprint_rectangle`,
que existe recien en scikit-image >= 0.25; esa version pide Python >= 3.10. En 3.9
la ultima scikit-image disponible es 0.24, que todavia expone la API vieja
(`square` / `rectangle`).

`footprint_rectangle(shape)` devuelve simplemente un array de unos con esa forma,
asi que el shim es exacto para el uso que hace pyxelate (elemento estructurante
rectangular para operaciones morfologicas).

Importar este modulo ANTES de importar pyxelate:

    import _compat  # noqa: F401
    from pyxelate import Pyx, Pal
"""
import numpy as np
import skimage.morphology as _morph

if not hasattr(_morph, "footprint_rectangle"):
    def footprint_rectangle(shape, *, dtype=np.uint8, decomposition=None):
        """Reimplementacion minima de skimage>=0.25 footprint_rectangle."""
        return np.ones(tuple(int(s) for s in shape), dtype=dtype)

    _morph.footprint_rectangle = footprint_rectangle
