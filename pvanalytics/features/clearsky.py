"""Functions for identifying periods of clear sky conditions."""
import pvlib


def reno(ghi, ghi_clearsky):
    """Identify times when GHI is consistent with clearsky conditions.

    Uses the function :py:func:`pvlib.clearsky.detect_clearsky`.

    .. note::

       Must be given irradiance data with regular (constant) time intervals
       of 1 to 30 minutes.

    Parameters
    ----------
    ghi : Series
        Global horizontal irradiance in :math:`W/m^2`. Must have an
        index with time intervals of 1 to 30 minutes. Plane-of-array
        irradiance can also be used, see Notes.
    ghi_clearsky : Series
        Global horizontal irradiance in :math:`W/m^2` under clearsky
        conditions. Must be on the same plane as `ghi`.

    Returns
    -------
    Series
        True when clear sky conditions are indicated.

    Raises
    ------
    ValueError
        if the time intervals are less than 1 minute or greater than
        30 minutes.

    Notes
    -----
    Clear-sky conditions are inferred when each of six criteria are
    met; see :py:func:`pvlib.clearsky.detect_clearsky` for references
    and details. Threshold values for each criterion were originally
    developed for ten minute windows containing one-minute data
    [1]_. Here, the window length and threshold values are inferred
    from the time interval of the data, as described in [2]_
    (``infer_limits=True`` in :py:func:`pvlib.clearsky.detect_clearsky`).
    [2]_ also shows that the method applies to time-averaged data at
    intervals of up to 30 minutes, and to plane-of-array irradiance.

    Copyright (c) 2019 SolarArbiter. See the file
    LICENSES/SOLARFORECASTARBITER_LICENSE at the top level directory
    of this distribution and at `<https://github.com/pvlib/
    pvanalytics/blob/master/LICENSES/SOLARFORECASTARBITER_LICENSE>`_
    for more information.

    References
    ----------
    .. [1] Reno, M.J. and C.W. Hansen, "Identification of periods of
       clear sky irradiance in time series of GHI measurements"
       Renewable Energy, v90, p. 520-531, 2016.

    .. [2] Jordan, D.C. and C. Hansen, "Clear-sky detection for PV
       degradation analysis using multiple regression", Renewable
       Energy, v209, p. 393-400, 2023.

    """
    delta = ghi.index.to_series().diff()
    delta_minutes = delta.iloc[1].total_seconds() / 60
    if delta_minutes < 1 or delta_minutes > 30:
        raise ValueError('clearsky requires regular time intervals '
                         'of 1m to 30m')
    flags = pvlib.clearsky.detect_clearsky(
        ghi,
        ghi_clearsky,
        ghi.index,
        infer_limits=True
    )
    return flags
