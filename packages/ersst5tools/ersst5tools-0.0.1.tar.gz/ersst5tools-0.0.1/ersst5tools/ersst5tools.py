#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import requests
import datetime
import xarray as xr
import climperiods
from tqdm.auto import tqdm

class ERSST5():
    def __init__(self):
        """Convenience class for downloading and processing ERSSTv5 SST data.
        """

        # List available precomputed climatologies for calculating anomalies
        self.climpath = os.path.join(os.path.dirname(__file__), 'clims')
        self.clims_available = sorted([f.split('.')[0]
                                       for f in os.listdir(self.climpath)
                                       if 'zarr' in f and not f.startswith('.')])
        self.clim = None
        self.url = 'https://www1.ncdc.noaa.gov/pub/data/cmb/ersst/v5/netcdf/'
        self.this_year = datetime.datetime.now().year
        self.this_month = datetime.datetime.now().month

    def download(self, outpath, year_range=(None,None), overwrite=False, proxy={}):
        """Download ERSSTv5 data.

        Parameters
        ----------
            outpath : str
                Output path to save files.
            year_range : (int, int), optional
                Year range to download. Defaults to maximum possible range.
            overwrite : boolean, optional
                If True, don't check for existence of file before downloading.
                Defaults to False.
            proxy : dict, optional
                Proxy dictionary if needed.
        """

        year_from, year_to = year_range
        if year_from is None:
            year_from = 1854
        if year_to is None:
            year_to = self.this_year
        years = range(year_from, year_to+1)

        # Loop over years
        for year in tqdm(years):
            if year < self.this_year:
                months = range(1,13)
            else:
                months = range(1, self.this_month)
            for month in months:
                fname = f'ersst.v5.{year}{month:02}.nc'
                fpath = os.path.join(outpath, fname)
                if not overwrite and os.path.exists(fpath):
                    print(f'Skipping {fname} as it exists in directory.')
                else:
                    r = requests.get(self.url+fname, stream=True, proxies=proxy)
                    if r.ok:
                        with open(fpath, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=1024 * 8):
                                if chunk:
                                    f.write(chunk)
                                    f.flush()
                                    os.fsync(f.fileno())
                    else:  # HTTP status code 4XX/5XX
                        print(f'Download failed: '
                              f'status code {r.status_code}\n{r.text}')

    def convert(self, ds):
        """Convert structure of raw files.

        Parameters
        ----------
            ds : Dataset
                Dataset with dims
                ['lat','lev','lon','time'].

        Returns
        -------
            da : DataArray
                Converted DataArray.
        """

        # Drop unneeded dims/coords
        da = ds['sst'].squeeze('lev', drop=True)

        # Convert longitudes from 0->360 to -180->180
        da['lon'] = ((da['lon'] + 180) % 360) - 180
        da = da.sortby(['lat','lon'])

        # Assign new coords and reshape to (..., 'month', 'year')
        da = da.assign_coords(year=('time', da.time.dt.year.data),
                              month=('time', da.time.dt.month.data)
                             ).set_index(time=('year', 'month')).unstack('time')
        return da

    def proc(self, inpath, year_range=(None, None)):
        """Process multiple ERSSTv5 SST files.

        Parameters
        ----------
            inpath : str
                Path to monthly netcdf files.
            year_range : (int, int), optional
                Year range to process.

        Returns
        -------
            da : DataArray
                Processed DataArray.
        """

        # Generate all file paths - assumes monthly files
        years = range(year_range[0], year_range[1]+1)
        fnames = [fname for fname in os.listdir(inpath) if '.nc' in fname]

        # Check if all years requested are available in fnames
        years_fnames = [int(fname.split('.')[2][:4]) for fname in fnames]
        years_missing = set(years) - set(years_fnames)
        if len(years_missing) > 0:
            print(f'Warning: some years in year_range not in {inpath}:\n'
                  f'{", ".join(map(str, years_missing))}')
            return None

        fpaths = [os.path.join(inpath, fname) for fname in fnames
                  if int(fname.split('.')[2][:4]) in years]

        # Generate combined DataArray for all months for this variable
        ds = xr.merge([self.convert(xr.open_dataset(fpath, engine='netcdf4'))
                       for fpath in fpaths]).sortby(['year','month','lat','lon'])
        return ds

    def calc_clim(self, inpath, year_range):
        """Calculate a single climatology for a year range.

        Takes the average over all grid locations and months over the
        year_range passed. Assumes time dimension converted to [year, month].

        Parameters
        ----------
            inpath : str
                Input path to raw download data.
            year_range : (int, int)
                Year range to process.

        Returns
        -------
            da : Dataset
                Climatology Dataset.
        """
        da = self.proc(inpath, year_range)
        if da is not None:
            return da.mean(dim='year').assign_attrs(desc=f'SST climatology',
                                                    clim_range=year_range)['sst']
        else:
            return None

    def calc_clims(self, inpath, year_range):
        """Calculate multiple climatologies for all years in a year range.

        Calculates NOAA 30-year centred climatologies in 5-year chunks and saves
        in self.climpath. Assumes the time dimension converted to [year, month].

        Parameters
        ----------
            inpath : str
                Input path to raw download data.
            year_range : (int, int)
                Year range to process.
        """
        for year_from, year_to in climperiods.clims(*year_range).drop_duplicates().values:
            clim = self.calc_clim(inpath, (year_from, year_to))
            out_fpath = os.path.join(self.climpath, f'sst_{year_from}_{year_to}.zarr')
            if clim is not None and not os.path.exists(out_fpath):
                clim.to_zarr(out_fpath)

        # Update self.clims_available
        self.clims_available = sorted([f.split('.')[0]
                                       for f in os.listdir(self.climpath)
                                       if 'zarr' in f and not f.startswith('.')])

    def load_clim(self, year_range):
        """Load precomputed climatology.

        Parameters
        ----------
            year_range : (int, int)
                Climatology year range to load.
        """

        fname =  f'sst_{year_range[0]}_{year_range[1]}.zarr'
        self.clim = xr.open_dataset(os.path.join(self.climpath, fname),
                                    engine='zarr')['sst']
        return self.clim

    def calc_anoms(self, inpath, year_range):
        """Calculate anomalies from reanalysis and climatology.

        Generates climatologies using standard NOAA 30-year rolling
        window which changes every 5 years. Assumes raw data has been
        processed to have year and month dimensions.

        Parameters
        ----------
            inpath : str
                Input path to raw download data.
            year_range : (int, int)
                Year range of data to process.

        Returns
        -------
            anoms : xarray.Dataset
                Processed anomalies Dataset.
        """

        anoms = []
        # Generate year ranges used to calculate climatology for each year
        clims = climperiods.clims(*year_range)

        # Loop over climatology year ranges
        for year_range_clim, df in clims.groupby(['year_from','year_to']):
            clim = self.load_clim(year_range_clim)
            data = self.proc(inpath, (df.index.min(), df.index.max()))
            if data is None:
                pass
            else:
                anoms.append(data - clim)
        return xr.concat(anoms, dim='year')['sst']


# If running the module as a whole, only download a single month's forecast
if __name__ == '__main__':
    # Always assume that outpath year_from and year_to will be passed
    outpath = sys.argv[1]
    year_from = sys.argv[2]
    year_to = sys.argv[3]

    ersst5 = ERSST5()
    ersst5.download(outpath, year_range=(int(year_from), int(year_to)), overwrite=False)
