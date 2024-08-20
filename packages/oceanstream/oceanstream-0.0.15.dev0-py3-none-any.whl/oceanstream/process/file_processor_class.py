import logging
import os
import time
import echopype as ep

from pathlib import Path
from rich import print
from rich.traceback import install, Traceback
from rich.progress import Progress, TimeElapsedColumn, BarColumn, TextColumn

from oceanstream.plot import plot_sv_data_with_progress, plot_sv_data
from oceanstream.echodata import get_campaign_metadata, read_file

from .process import compute_sv, process_file_with_progress, read_file_with_progress

install(show_locals=False, width=120)


def get_chunk_sizes(var_dims, chunk_sizes):
    return {dim: chunk_sizes[dim] for dim in var_dims if dim in chunk_sizes}


def apply_chunks(Sv, chunks):
    if chunks:
        for var in Sv.data_vars:
            var_chunk_sizes = get_chunk_sizes(Sv[var].dims, chunks)
            Sv[var] = Sv[var].chunk(var_chunk_sizes)
            if 'chunks' in Sv[var].encoding:
                del Sv[var].encoding['chunks']
    return Sv


def get_chunk_store(storage_config, path):
    if storage_config['storage_type'] == 'azure':
        from adlfs import AzureBlobFileSystem
        azfs = AzureBlobFileSystem(**storage_config['storage_options'])
        return azfs.get_mapper(f"{storage_config['container_name']}/{path}")
    else:
        raise ValueError(f"Unsupported storage type: {storage_config['storage_type']}")


class EchoProcessor:
    def __init__(self, config_data, base_path=None):
        self.config_data = config_data
        self.base_path = base_path

    def compute_paths(self):
        file_path = self.config_data.get('raw_path')
        if file_path:
            file_path = Path(file_path)
            file_base_name = file_path.stem
            if self.base_path:
                relative_path = file_path.relative_to(self.base_path)
                if relative_path.parent != ".":
                    zarr_path = Path(relative_path.parent) / file_base_name
                else:
                    zarr_path = relative_path.stem
            else:
                zarr_path = file_base_name
            output_path = Path(self.config_data["output_folder"]) / zarr_path
            output_path.mkdir(parents=True, exist_ok=True)
            zarr_file_name = f"{file_base_name}_Sv.zarr"
        else:
            zarr_path = self.base_path
            zarr_file_name = f"{zarr_path}_Sv.zarr"
            output_path = zarr_path

        return {"zarr_path": zarr_path, "zarr_file_name": zarr_file_name, "output": output_path}

    def write_dataset(self, Sv, zarr_paths):
        if 'cloud_storage' in self.config_data:
            store = get_chunk_store(self.config_data['cloud_storage'],
                                         Path(zarr_paths['zarr_path']) / zarr_paths['zarr_file_name'])
        else:
            store = os.path.join(zarr_paths['output'], zarr_paths['zarr_file_name'])
        Sv.to_zarr(store, mode='w')

    def plot_data(self, Sv, zarr_paths):
        try:
            plot_sv_data(Sv, file_base_name=zarr_paths['zarr_file_name'], output_path=zarr_paths['output'],
                         echogram_path=zarr_paths['zarr_path'], config_data=self.config_data)
        except Exception as e:
            logging.exception(f"Error plotting echogram for {self.config_data['raw_path']}:")
            raise e

    def compute_Sv_to_zarr(self, echodata, chunks=None, plot_echogram=False, **kwargs):
        waveform_mode = kwargs.get("waveform_mode", "CW")
        encode_mode = "power" if waveform_mode == "CW" else "complex"
        Sv = compute_sv(echodata, encode_mode=encode_mode, **kwargs)
        zarr_paths = self.compute_paths()
        Sv = apply_chunks(Sv, chunks)
        self.write_dataset(Sv, zarr_paths)
        if plot_echogram:
            self.plot_data(Sv, zarr_paths)
        return zarr_paths['output']

    @staticmethod
    def with_progress(task_name, total):
        def decorator(func):
            def wrapper(*args, **kwargs):
                with Progress(
                        TextColumn(f"[progress.description]{task_name}"),
                        BarColumn(),
                        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                        TimeElapsedColumn()
                ) as progress:
                    task = progress.add_task(task_name, total=total)
                    result = func(progress, task, *args, **kwargs)
                    progress.update(task, advance=total - progress.tasks[task].completed)
                    return result

            return wrapper

        return decorator

    @staticmethod
    def attempt(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.error(f"Error in {func.__name__}: {e}")
                print(Traceback())
                return None

        return wrapper

    @attempt
    async def process_raw_file_with_progress(self, plot_echogram, waveform_mode="CW", depth_offset=0):
        with Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn()
        ) as progress:
            print(f"[green] Processing file: {self.config_data['raw_path']}[/green]")
            read_task = progress.add_task("[cyan]Reading raw file data...", total=100)
            campaign_id, date, sonar_model, metadata, _ = get_campaign_metadata(self.config_data['raw_path'])
            if self.config_data['sonar_model'] is None:
                self.config_data['sonar_model'] = sonar_model
            echodata, encode_mode = await read_file_with_progress(self.config_data, progress, read_task)
            echodata.to_zarr(save_path=self.config_data["output_folder"], overwrite=True, parallel=False)
            progress.update(read_task, advance=100 - progress.tasks[read_task].completed)
            if plot_echogram:
                zarr_file_name = self.config_data['raw_path'].stem
                if waveform_mode == "BB":
                    encode_mode = "complex"
                compute_task = progress.add_task(
                    f"[cyan]Computing Sv with waveform_mode={waveform_mode} and encode_mode={encode_mode}...",
                    total=100)
                sv_dataset = await self.compute_sv_with_progress(progress, compute_task, echodata, encode_mode,
                                                                 waveform_mode, depth_offset)
                progress.update(compute_task, advance=100 - progress.tasks[compute_task].completed)
                print(f"[blue]📝 Computed Sv and wrote zarr file to: {self.config_data['output_folder']}[/blue]")
                print(f"[green]✅ Plotting echogram for: {self.config_data['raw_path']}[/green]")
                plot_task = progress.add_task("[cyan]Plotting echogram...", total=100)
                await plot_sv_data_with_progress(sv_dataset, output_path=self.config_data["output_folder"],
                                                 progress=progress,
                                                 file_base_name=zarr_file_name, plot_task=plot_task)
                progress.update(plot_task, advance=100 - progress.tasks[plot_task].completed)
                print(f"[blue]📊 Plotted echogram for the data in: {self.config_data['output_folder']}[/blue]")

    @attempt
    def convert_raw_file(self, file_path, progress_queue=None):
        logging.debug("Starting processing of file: %s", file_path)
        file_path_obj = Path(file_path)
        self.config_data['raw_path'] = file_path_obj
        if self.base_path:
            relative_path = file_path_obj.relative_to(self.base_path).parent
        else:
            relative_path = file_path_obj.name
        echodata, encode_mode = read_file(self.config_data, use_swap=True, skip_integrity_check=True)
        if 'cloud_storage' in self.config_data:
            file_name = file_path_obj.stem + ".zarr"
            store = get_chunk_store(self.config_data['cloud_storage'], Path(relative_path) / file_name)
            echodata.to_zarr(save_path=store, overwrite=True, parallel=False)
        else:
            output_path = Path(self.config_data["output_folder"]) / relative_path
            output_path.mkdir(parents=True, exist_ok=True)
            echodata.to_zarr(save_path=output_path, overwrite=True, parallel=False)
        if progress_queue:
            progress_queue.put(file_path)

    @attempt
    def compute_single_file(self, **kwargs):
        file_path = self.config_data["raw_path"]
        start_time = time.time()
        chunks = kwargs.get("chunks")
        echodata = ep.open_converted(file_path, chunks=chunks)
        try:
            output_path = self.compute_Sv_to_zarr(echodata, chunks=chunks, **kwargs)
            print(f"[blue]✅ Computed Sv and saved to: {output_path}[/blue]")
        except Exception as e:
            logging.error(f"Error computing Sv for {file_path}")
            print(Traceback())
        finally:
            end_time = time.time()
            total_time = end_time - start_time
            print(f"Total time taken: {total_time:.2f} seconds")


# Example usage
config_data = {
    'raw_path': 'path/to/raw/file',
    'output_folder': 'path/to/output/folder',
    'sonar_model': None,
    'cloud_storage': {
        'storage_type': 'azure',
        'storage_options': {
            # Azure storage options
        },
        'container_name': 'mycontainer'
    }
}
base_path = 'path/to/base'
processor = EchoProcessor(config_data, base_path)
processor.compute_single_file(chunks={'time': 100})
