import warnings
import numpy as np
import xarray as xr
import dask.dataframe as dd
from typing import Dict, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
from pathlib import Path
import copernicusmarine
import gsw
from .process import compute_sv, add_location, add_splitbeam_angle

class Dataset:
    """
    A class to encapsulate operations on the Sv dataset from split-beam echosounders.

    Attributes:
        echodata (Any): The EchoData object containing raw data.
        Sv (xr.Dataset): The dataset containing Sv data.
    """

    def __init__(self, echodata: Any):
        """
        Initialize the Dataset object with echodata.

        Args:
            echodata (Any): An EchoData object containing raw data.
        """
        self.echodata = echodata
        self.Sv: xr.Dataset = xr.Dataset()

    def compute_sv(self, encode_mode: str = "power", **kwargs) -> xr.Dataset:
        """
        Compute the Sv dataset from the echodata.

        Args:
            encode_mode (str): Encoding mode to use for Sv computation, either 'power' or 'complex'.
            **kwargs: Additional keyword arguments passed to the compute_sv function.

        Returns:
            xr.Dataset: The computed Sv dataset.
        """
        # Compute Sv using echodata and specified encoding mode
        self.Sv = compute_sv(self.echodata, encode_mode=encode_mode, **kwargs)
        return self.Sv

    def apply_chunks(self, chunks: Optional[Dict[str, int]]) -> xr.Dataset:
        """
        Apply chunking to the Sv dataset to handle large datasets more efficiently.

        Args:
            chunks (Optional[Dict[str, int]]): Dictionary specifying chunk sizes for each dimension.

        Returns:
            xr.Dataset: The chunked Sv dataset.
        """
        if chunks:
            for var in self.Sv.data_vars:
                var_chunk_sizes = {dim: chunks[dim] for dim in self.Sv[var].dims if dim in chunks}
                self.Sv[var] = self.Sv[var].chunk(var_chunk_sizes)
                if 'chunks' in self.Sv[var].encoding:
                    del self.Sv[var].encoding['chunks']
        return self.Sv

    def add_depth(self, depth_offset: float = 0, tilt: float = 0, downward: bool = True) -> xr.Dataset:
        """
        Add depth information to the Sv dataset.

        Args:
            depth_offset (float): Depth offset to be added to the depth values.
            tilt (float): Tilt angle of the transducer in degrees.
            downward (bool): Flag indicating whether the depth is measured downward (True) or upward (False).

        Returns:
            xr.Dataset: The Sv dataset with added depth information.
        """
        mult = 1 if downward else -1

        # Extract the first channel and ping time for calculation
        first_channel = self.Sv["channel"].values[0]
        first_ping_time = self.Sv["ping_time"].values[0]

        # Select and process the echo range
        selected_echo_range = self.Sv["echo_range"].sel(channel=first_channel, ping_time=first_ping_time)
        selected_echo_range = selected_echo_range.values.tolist()
        selected_echo_range = [mult * value * np.cos(tilt / 180 * np.pi) + depth_offset for value in selected_echo_range]

        # Assign new coordinates and slice the range
        self.Sv = self.Sv.assign_coords(range_sample=selected_echo_range)
        min_val = np.nanmin(selected_echo_range)
        max_val = np.nanmax(selected_echo_range)
        self.Sv = self.Sv.sel(range_sample=slice(min_val, max_val))

        return self.Sv

    def add_seabed_depth(self) -> xr.Dataset:
        """
        Add seabed depth information to the Sv dataset.

        Returns:
            xr.Dataset: The Sv dataset with added seabed depth information.
        """
        # Create a mask to locate seabed
        seabed_mask = ~self.Sv["mask_seabed"]
        seabed_level = seabed_mask.argmax(dim="range_sample")

        # Assign seabed level to the dataset
        self.Sv = self.Sv.assign(seabed_level=seabed_level)
        return self.Sv

    def enrich_sv_dataset(self, **kwargs) -> xr.Dataset:
        """
        Enhance the Sv dataset by adding depth, location, and split-beam angle information.

        Args:
            **kwargs: Keyword arguments specific to add_depth(), add_location(), and add_splitbeam_angle() functions.

        Returns:
            xr.Dataset: The enhanced Sv dataset.
        """
        # Extract arguments for depth, location, and split-beam angle
        depth_keys = ["depth_offset", "tilt", "downward"]
        depth_args = {k: kwargs[k] for k in depth_keys if k in kwargs}

        location_keys = ["nmea_sentence"]
        location_args = {k: kwargs[k] for k in location_keys if k in kwargs}

        splitbeam_keys = [
            "waveform_mode",
            "encode_mode",
            "pulse_compression",
            "storage_options",
            "return_dataset",
        ]
        splitbeam_args = {k: kwargs[k] for k in splitbeam_keys if k in kwargs}

        # Add depth information
        try:
            self.add_depth(**depth_args)
        except Exception as e:
            warnings.warn(f"Failed to add depth due to error: {str(e)}")

        # Add location information
        try:
            self.Sv = add_location(self.Sv, self.echodata, **location_args)
        except Exception as e:
            warnings.warn(f"Failed to add location due to error: {str(e)}")

        # Add split-beam angle information
        try:
            add_splitbeam_angle(self.Sv, self.echodata, **splitbeam_args)
        except Exception as e:
            warnings.warn(f"Failed to add split-beam angle due to error: {str(e)}")

        return self.Sv

    def filter_by_depth(self, min_depth: float, max_depth: float) -> xr.Dataset:
        """
        Filter the Sv dataset by a specified depth range.

        Args:
            min_depth (float): Minimum depth to include in the dataset.
            max_depth (float): Maximum depth to include in the dataset.

        Returns:
            xr.Dataset: The filtered Sv dataset.
        """
        return self.Sv.sel(range_sample=slice(min_depth, max_depth))

    def remove_background_noise(self, noise_threshold: float) -> xr.Dataset:
        """
        Remove background noise from the Sv dataset based on a specified threshold.

        Args:
            noise_threshold (float): Threshold above which data is considered noise and will be removed.

        Returns:
            xr.Dataset: The denoised Sv dataset.
        """
        self.Sv = self.Sv.where(self.Sv > noise_threshold, drop=True)
        return self.Sv

    def apply_mask(self, mask: xr.DataArray) -> xr.Dataset:
        """
        Apply a mask to the Sv dataset to exclude unwanted data.

        Args:
            mask (xr.DataArray): A boolean mask indicating which data points to keep.

        Returns:
            xr.Dataset: The masked Sv dataset.
        """
        self.Sv = self.Sv.where(mask, drop=True)
        return self.Sv

    def detect_targets(self, threshold: float) -> xr.Dataset:
        """
        Detect targets in the Sv dataset based on a specified threshold.

        Args:
            threshold (float): Threshold for target detection.

        Returns:
            xr.Dataset: The dataset with detected targets marked.
        """
        targets = self.Sv > threshold
        self.Sv = self.Sv.assign(targets=targets)
        return self.Sv

    def compute_mean_sv(self) -> xr.Dataset:
        """
        Compute the mean Sv value over the dataset.

        Returns:
            xr.Dataset: The dataset containing mean Sv values.
        """
        mean_sv = self.Sv.mean(dim="ping_time")
        return mean_sv

    def plot_sv(self, **plot_args):
        """
        Plot the Sv dataset.

        Args:
            **plot_args: Additional arguments for plotting.

        This function could use matplotlib or another plotting library to visualize the Sv data.
        """
        # Placeholder for actual plotting code
        import matplotlib.pyplot as plt

        plt.figure(figsize=(10, 6))
        plt.imshow(self.Sv.T, aspect='auto', **plot_args)
        plt.colorbar(label='Sv (dB)')
        plt.xlabel('Range Sample')
        plt.ylabel('Ping Time')
        plt.title('Sv Data')
        plt.show()

    def export_to_csv(self, filename: str):
        """
        Export the Sv dataset to a CSV file using Dask DataFrames to handle large volumes of data.

        Args:
            filename (str): The path to the CSV file where the data will be saved.
        """
        dask_df = self.Sv.to_dataframe().reset_index()
        dask_ddf = dd.from_pandas(dask_df, npartitions=10)
        dask_ddf.to_csv(filename, index=False)

    def apply_scattering_model(self, model: Callable[[xr.DataArray], xr.DataArray]) -> xr.Dataset:
        """
        Apply a specific scattering model to the Sv data.

        Args:
            model (Callable[[xr.DataArray], xr.DataArray]): A function that represents the scattering model.

        Returns:
            xr.Dataset: The Sv dataset with the scattering model applied.
        """
        self.Sv = self.Sv.map(model)
        return self.Sv

    def compute_nasc(self) -> xr.Dataset:
        """
        Compute the Nautical Area Scattering Coefficient (NASC) from the Sv data.

        Returns:
            xr.Dataset: The dataset with computed NASC values.
        """
        # Placeholder for actual NASC computation
        pass

    def segment_and_classify_traces(self, classifier: Callable[[xr.DataArray], xr.DataArray]) -> xr.Dataset:
        """
        Segment the Sv data into distinct echo traces and classify them.

        Args:
            classifier (Callable[[xr.DataArray], xr.DataArray]): A function to classify the echo traces.

        Returns:
            xr.Dataset: The dataset with classified echo traces.
        """
        self.Sv = self.Sv.map(classifier)
        return self.Sv

    def compute_acoustic_biomass(self, conversion_factor: float) -> xr.Dataset:
        """
        Compute the acoustic biomass from the Sv data using a specified conversion factor.

        Args:
            conversion_factor (float): The factor to convert Sv values to biomass.

        Returns:
            xr.Dataset: The dataset with computed acoustic biomass.
        """
        self.Sv = self.Sv * conversion_factor
        return self.Sv

    def temporal_aggregation(self, freq: str) -> xr.Dataset:
        """
        Aggregate the Sv data temporally.

        Args:
            freq (str): The frequency to aggregate the data (e.g., 'H' for hourly, 'D' for daily).

        Returns:
            xr.Dataset: The temporally aggregated dataset.
        """
        self.Sv = self.Sv.resample(time=freq).mean()
        return self.Sv

    def spatial_aggregation(self, lat_bins: int, lon_bins: int) -> xr.Dataset:
        """
        Aggregate the Sv data spatially.

        Args:
            lat_bins (int): Number of latitude bins.
            lon_bins (int): Number of longitude bins.

        Returns:
            xr.Dataset: The spatially aggregated dataset.
        """
        self.Sv = self.Sv.coarsen(lat=lat_bins, lon=lon_bins, boundary='trim').mean()
        return self.Sv

    def compute_volume_backscatter(self) -> xr.Dataset:
        """
        Compute the volume backscattering strength (Sv) over the dataset.

        Returns:
            xr.Dataset: The dataset with computed volume backscattering strength.
        """
        # Implement volume backscattering strength computation here
        pass

    def merge_with_other_dataset(self, other_dataset: xr.Dataset, on: Tuple[str]) -> xr.Dataset:
        """
        Merge the current Sv dataset with another dataset on specified coordinates.

        Args:
            other_dataset (xr.Dataset): The other dataset to merge with.
            on (Tuple[str]): The coordinates on which to merge the datasets.

        Returns:
            xr.Dataset: The merged dataset.
        """
        merged_dataset = xr.merge([self.Sv, other_dataset], join='inner')
        return merged_dataset

    def interpolate_missing_data(self, method: str = 'linear') -> xr.Dataset:
        """
        Interpolate missing data in the Sv dataset using a specified method.

        Args:
            method (str): The interpolation method to use. Default is 'linear'.

        Returns:
            xr.Dataset: The dataset with interpolated data.
        """
        self.Sv = self.Sv.interpolate_na(method=method)
        return self.Sv

    def interpolate_sv(
        self, method: str = "linear", with_edge_fill: bool = False
    ) -> xr.Dataset:
        """
        Apply masks to the Sv DataArray in the dataset and interpolate over the resulting NaN values.

        Parameters:
        - method (str): Interpolation method.
        - with_edge_fill (bool): Flag to allow filling the edges of echograms

        Returns:
        - xr.Dataset: Dataset with the masked and interpolated Sv DataArray.
        """
        # Initialize an empty list to store the processed channels
        processed_channels = []

        # Loop over each channel
        for channel in self.Sv["channel"]:
            channel_data = self.Sv.sel(channel=channel)

            # Convert from dB to linear scale
            channel_data_linear = db_to_linear(channel_data)

            # Perform interpolation to fill NaN values in linear scale using Xarray's interpolate_na
            interpolated_channel_data_linear = channel_data_linear.interpolate_na(
                dim="ping_time", method=method, use_coordinate=True
            )

            if with_edge_fill:
                interpolated_channel_data_linear = interpolated_channel_data_linear.ffill(dim="ping_time")
                interpolated_channel_data_linear = interpolated_channel_data_linear.bfill(dim="ping_time")

            # Convert back to dB scale
            interpolated_channel_data = linear_to_db(interpolated_channel_data_linear)

            # Append the processed channel data to the list
            processed_channels.append(interpolated_channel_data)

        # Combine the processed channels back into a single DataArray
        interpolated_sv = xr.concat(processed_channels, dim="channel")

        # Update the Sv DataArray in the dataset with the interpolated values
        self.Sv["Sv"] = interpolated_sv

        return self.Sv

    def format_data_points(self, current_datetime: datetime, days_back: int = 10) -> Tuple[str, str]:
        """
        Format the start and end dates for fetching data from the Copernicus API.

        Args:
            current_datetime (datetime): The current datetime.
            days_back (int): The number of days to look back from the current datetime.

        Returns:
            Tuple[str, str]: The formatted start and end dates.
        """
        current_date_str = current_datetime.strftime("%Y-%m-%d")
        earlier_datetime = current_datetime - timedelta(days=days_back)
        earlier_date_str = earlier_datetime.strftime("%Y-%m-%d")
        return earlier_date_str, current_date_str

    def copernicus_salinity_temp(self, target_latitude: float, target_longitude: float, region_padding_degrees: float, time_point: datetime, average_location: bool = False, days_back: int = 10) -> xr.Dataset:
        """
        Fetch salinity and temperature data from the Copernicus API.

        Args:
            target_latitude (float): The target latitude.
            target_longitude (float): The target longitude.
            region_padding_degrees (float): The padding in degrees around the target location.
            time_point (datetime): The time point for fetching data.
            average_location (bool): Whether to average the data spatially.
            days_back (int): The number of days to look back from the time point.

        Returns:
            xr.Dataset: The dataset containing salinity and temperature data.
        """
        start_time, end_time = self.format_data_points(time_point, days_back)

        measurement_ds = copernicusmarine.open_dataset(
            dataset_id="cmems_mod_glo_phy-so_anfc_0.083deg_P1D-m",
            minimum_longitude=target_longitude - region_padding_degrees,
            maximum_longitude=target_longitude + region_padding_degrees,
            minimum_latitude=target_latitude - region_padding_degrees,
            maximum_latitude=target_latitude + region_padding_degrees,
            start_datetime=start_time,
            end_datetime=end_time,
            variables=["sea_water_salinity"],
            username='test',  # Replace with actual username
            password='test'   # Replace with actual password
        )

        temp_ds = copernicusmarine.open_dataset(
            dataset_id="cmems_mod_glo_phy-thetao_anfc_0.083deg_P1D-m",
            minimum_longitude=target_longitude - region_padding_degrees,
            maximum_longitude=target_longitude + region_padding_degrees,
            minimum_latitude=target_latitude - region_padding_degrees,
            maximum_latitude=target_latitude + region_padding_degrees,
            start_datetime=start_time,
            end_datetime=end_time,
            variables=["sea_water_potential_temperature"],
            username='test',  # Replace with actual username
            password='test'   # Replace with actual password
        )

        measurement_ds['thetao'] = temp_ds['thetao']

        if average_location:
            measurement_ds = measurement_ds.mean(dim=['time', 'latitude', 'longitude'])
        else:
            measurement_ds = measurement_ds.mean(dim=['time'])

        return measurement_ds

    def compute_sound_speed_gsw(self, measurement_ds: xr.Dataset) -> xr.Dataset:
        """
        Compute the sound speed using the GSW library.

        Args:
            measurement_ds (xr.Dataset): The dataset containing salinity and temperature data.

        Returns:
            xr.Dataset: The dataset with computed sound speed using GSW.
        """
        potential_temps = measurement_ds['thetao']
        latitudes = measurement_ds['latitude']
        longitudes = measurement_ds['longitude']
        depths = measurement_ds['depth']
        salinities = measurement_ds['so']
        pressures = gsw.p_from_z(-depths, latitudes)
        CT_temps = gsw.CT_from_pt(salinities, potential_temps)
        temps = gsw.t_from_CT(salinities, CT_temps, pressures)
        absolute_salinities = gsw.SA_from_SP(salinities, pressures, longitudes, latitudes)
        measurement_ds['temp'] = temps
        measurement_ds['GSW_sound_speed'] = gsw.sound_speed_t_exact(absolute_salinities, temps, pressures)
        return measurement_ds

    def Mackenzie_formula(self, temp: xr.DataArray, so: xr.DataArray, depth: xr.DataArray) -> xr.DataArray:
        """
        Compute sound speed using the Mackenzie formula.

        Args:
            temp (xr.DataArray): Temperature data.
            so (xr.DataArray): Salinity data.
            depth (xr.DataArray): Depth data.

        Returns:
            xr.DataArray: The computed sound speed.
        """
        return 1448.96 + 4.591 * temp - 0.05304 * (temp ** 2) + 2.374e-4 * (temp ** 3) + 1.34 * (so - 35) + 0.0163 * depth

    def compute_sound_speed_Mackenzie(self, measurement_ds: xr.Dataset) -> xr.Dataset:
        """
        Compute the sound speed using the Mackenzie formula.

        Args:
            measurement_ds (xr.Dataset): The dataset containing salinity and temperature data.

        Returns:
            xr.Dataset: The dataset with computed sound speed using the Mackenzie formula.
        """
        potential_temps = measurement_ds['thetao']
        depths = measurement_ds['depth']
        salinities = measurement_ds['so']
        latitudes = measurement_ds['latitude']
        pressures = gsw.p_from_z(-depths, latitudes)
        CT_temps = gsw.CT_from_pt(salinities, potential_temps)
        temps = gsw.t_from_CT(salinities, CT_temps, pressures)
        measurement_ds['temp'] = temps
        measurement_ds['Mackenzie_sound_speed'] = self.Mackenzie_formula(temps, salinities, depths)
        return measurement_ds

    def fetch_and_compute_sound_speed(self, target_latitude: float, target_longitude: float, region_padding_degrees: float, time_point: datetime, method: str = "GSW", average_location: bool = False, days_back: int = 10) -> xr.Dataset:
        """
        Fetch salinity and temperature data from the Copernicus API and compute the sound speed.

        Args:
            target_latitude (float): The target latitude.
            target_longitude (float): The target longitude.
            region_padding_degrees (float): The padding in degrees around the target location.
            time_point (datetime): The time point for fetching data.
            method (str): The method to use for sound speed calculation ("GSW" or "Mackenzie").
            average_location (bool): Whether to average the data spatially.
            days_back (int): The number of days to look back from the time point.

        Returns:
            xr.Dataset: The dataset with computed sound speed.
        """
        # Fetch salinity and temperature data from the Copernicus API
        measurement_ds = self.copernicus_salinity_temp(target_latitude, target_longitude, region_padding_degrees, time_point, average_location, days_back)

        # Compute sound speed using the specified method
        if method == "GSW":
            sound_speed_ds = self.compute_sound_speed_gsw(measurement_ds)
        elif method == "Mackenzie":
            sound_speed_ds = self.compute_sound_speed_Mackenzie(measurement_ds)
        else:
            raise ValueError(f"Unsupported method: {method}")

        return sound_speed_ds

def db_to_linear(data: xr.DataArray) -> xr.DataArray:
    """
    Convert data from dB to linear scale.

    Args:
        data (xr.DataArray): Data in dB scale.

    Returns:
        xr.DataArray: Data in linear scale.
    """
    return 10 ** (data / 10)

def linear_to_db(data: xr.DataArray) -> xr.DataArray:
    """
    Convert data from linear to dB scale.

    Args:
        data (xr.DataArray): Data in linear scale.

    Returns:
        xr.DataArray: Data in dB scale.
    """
    return 10 * np.log10(data)
