import multiprocessing as mp

import tables
import numpy as np
import torch
from torch.utils.data import Dataset, Subset
from gammalearn.constants import SOURCE, TARGET, REAL_DATA_ID
from astropy.table import Table
import astropy.units as u
from ctapipe.instrument import CameraGeometry, SubarrayDescription
from ctapipe.image import tailcuts_clean
from lstchain.io.io import read_simu_info_merged_hdf5
from lstchain.io.io import dl1_images_lstcam_key, dl1_params_lstcam_key, get_dataset_keys
from dl1_data_handler.image_mapper import ImageMapper
import pandas as pd
import random
from torchvision import transforms
import os
from PIL import Image
import logging
import tqdm
from functools import partial
from itertools import islice
from typing import Tuple


class TqdmLoggingHandler(logging.Handler):
    def __init__(self, level=logging.NOTSET):
        super().__init__(level)

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.tqdm.write(msg)
            self.flush()
        except Exception:
            self.handleError(record)


DL1_SUBARRAY_TRIGGER_KEY = 'dl1/event/subarray/trigger'
DL1_SUBARRAY_LAYOUT = 'configuration/instrument/subarray/layout'


def fetch_dataset_geometry(dataset):
    if isinstance(dataset, torch.utils.data.Subset):
        return fetch_dataset_geometry(dataset.dataset)
    elif isinstance(dataset, torch.utils.data.ConcatDataset):
        return fetch_dataset_geometry(dataset.datasets[0])
    else:
        return dataset.camera_geometry


class VisionDomainAdaptationDataset(Dataset):
    def __init__(self, source_dataset, target_dataset):
        super().__init__()
        # assert len(source_dataset) == len(target_dataset)
        self.source_dataset = source_dataset
        self.target_dataset = target_dataset
        self.camera_geometry = None

    def __len__(self):
        # If __len__ returns len(self.source_dataset) + len(self.target_dataset), the idx will range from 0 to
        # len(self.source_dataset) + len(self.target_dataset) - 1, which is not compatible with the currently
        # implemented __getitem__ function
        return max(len(self.source_dataset), len(self.target_dataset))

    def __getitem__(self, idx):
        idx_source = idx % len(self.source_dataset)
        idx_target = idx % len(self.target_dataset)
        sample_source = {k + '_source': v for k, v in self.source_dataset[idx_source].items()}
        sample_target = {k + '_target': v for k, v in self.target_dataset[idx_target].items()}
        sample = {**sample_source, **sample_target}

        return sample


class GlearnDomainAdaptationDataset(VisionDomainAdaptationDataset):
    def __init__(self, source_dataset, target_dataset):
        super(GlearnDomainAdaptationDataset, self).__init__(source_dataset, target_dataset)
        camera_geometry_source = fetch_dataset_geometry(source_dataset)
        camera_geometry_target = fetch_dataset_geometry(target_dataset)
        assert camera_geometry_source == camera_geometry_target, 'Source and target camera geometry must be the same.'
        self.camera_geometry = camera_geometry_source


class WrongGeometryError(Exception):
    pass


class MockLSTDataset(Dataset):

    def __init__(self, hdf5_file_path, camera_type, group_by, targets=None, particle_dict=None, use_time=False, train=True,
                 subarray=None, transform=None, target_transform=None, **kwargs):

        self.images = np.random.rand(50, 1855).astype(np.float32)
        self.times = np.random.rand(50, 1855).astype(np.float32)

        self.particle_dict = {0: 0, 101: 1}

        self.camera_type = 'LST_LSTCam'
        self.group_by = 'image'
        self.original_geometry = CameraGeometry.from_name('LSTCam')
        self.camera_geometry = CameraGeometry.from_name('LSTCam')
        self.simu = True
        self.dl1_params = {
            'event_id': np.arange(50),
            'mc_type': np.random.choice([101, 0], size=50),
            'mc_energy': np.random.rand(50).astype(np.float32),
            'log_mc_energy': np.random.rand(50).astype(np.float32),
            'mc_alt_tel': np.full(50, np.deg2rad(70), dtype=np.float32),
            'mc_az_tel': np.full(50, np.deg2rad(180), dtype=np.float32),
            'mc_alt': np.random.rand(50).astype(np.float32),
            'mc_az': np.random.rand(50).astype(np.float32),
            'mc_core_x': np.random.rand(50).astype(np.float32),
            'mc_core_y': np.random.rand(50).astype(np.float32),
            'tel_id': np.random.rand(50).astype(np.float32),
            'tel_pos_x': np.random.rand(50).astype(np.float32),
            'tel_pos_y': np.random.rand(50).astype(np.float32),
        }

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        data = np.stack([self.images[idx], self.times[idx]])
        dl1_params = {n: p[idx] for n, p in self.dl1_params.items()}
        labels = {'energy': np.array([dl1_params['log_mc_energy']], dtype=np.float32),
                  'impact': np.array([dl1_params['mc_core_x'] - dl1_params['tel_pos_x'],
                                      dl1_params['mc_core_y'] - dl1_params['tel_pos_y']], dtype=np.float32),
                  'direction': np.array([dl1_params['mc_alt'] - dl1_params['mc_alt_tel'],
                                         dl1_params['mc_az'] - dl1_params['mc_az_tel']], dtype=np.float32),
                  'class':  self.particle_dict.get(dl1_params['mc_type'], -1)
                  }
        sample = {'image': data,
                  'dl1_params': dl1_params,
                  'label': labels}

        return sample

    def filter_image(self, filter_dict):
        pass

    def filter_event(self, filter_dict):
        pass


class BaseLSTDataset(Dataset):
    """camera simulation dataset for lstchain DL1 hdf5 files. Tested with lstchain 0.7"""

    def __init__(self, hdf5_file_path, camera_type, group_by, targets=None, particle_dict=None, use_time=False,
                 train=True, subarray=None, transform=None, target_transform=None, domain_dict=None, domain=None, **kwargs):
        """
        Parameters
        ----------
            hdf5_file_path (str): path to hdf5 file containing the data
            camera_type (str) : name of the camera used (e.g. camera_type='LST_LSTCam)
            group_by (str): the way to group images in the dataset (e.g. 'event_triggered_tels' :
            by event only for telescopes which triggered)
            targets (list, optional): the targets to include in the sample
            particle_dict (dict, optional): Dictionary of particle types
            use_time (bool, optional): whether or not include the time peak in the sample
            train (bool, optional): defines the dataset mode (train or test)
            subarray (Array, optional): array of telescopes ids that defines the subarray used
            transform (callable, optional): Optional transform to be applied on a sample
            target_transform (callable, optional): Optional transform to be applied on a sample
        """
        self.hdf5_file_path = hdf5_file_path
        self.hdf5_file = None
        self.camera_type = camera_type
        if not self.camera_type == 'LST_LSTCam':
            WrongGeometryError("passed camera_type should be LST_LSTCam")

        self.targets = targets if targets is not None else {}
        self.particle_dict = particle_dict
        self.transform = transform
        self.target_transform = target_transform
        self.use_time = use_time
        self.train = train

        self.images = None
        self.pedestals = None
        self.times = None
        self.filtered_indices = None
        self.lstchain_version = None
        self.simu = True
        self.domain = 'source' if domain is None else domain
        self.domain_dict = domain_dict

        self.mc_only_dl1_parameters = ['disp_angle', 'disp_dx', 'disp_dy', 'disp_norm', 'disp_sign', 'log_mc_energy',
                                       'src_x', 'src_y']
        self.lst1_only_dl1_parameters = ('dragon_time', 'tib_time', 'ucts_time', 'ucts_trigger_type')

        group_by_options = ['image', 'event_all_tels', 'event_triggered_tels']

        assert group_by in group_by_options, '{} is not a suitable group option. Must be in {}'.format(group_by,
                                                                                                       group_by_options)

        self.group_by = group_by

        # LSTCam is used as default geometry at the moment.
        # all data (MC and real) are converted to this geom.
        self.camera_geometry = CameraGeometry.from_name('LSTCam')

        geometry_paths = [
            '/configuration/instrument/telescope/camera/geometry_LSTCam',
            '/configuration/instrument/telescope/camera/geometry_0'
        ]
        for geom_path in geometry_paths:
            try:
                geom_table = Table.read(hdf5_file_path, path=geom_path)
                break
            except OSError as e:
                pass
            # if none of the paths worked, raise an error
        else:
            raise OSError(f"The file {hdf5_file_path} does not contain a LSTCam geometry at a known path. Tried {geometry_paths}")

        self.original_geometry = CameraGeometry.from_table(geom_table)

        # Note: when using ctapipe>=0.12, the following code might be used:
        # self.original_geometry = SubarrayDescription.from_hdf(hdf5_file_path).tel[1].camera.geometry

        # Rotate the original geometry as well to align both geometries
        # self.original_geometry.rotate(self.original_geometry.pix_rotation)

        self.inj_table = self.original_geometry.position_to_pix_index(self.camera_geometry.pix_x,
                                                                      self.camera_geometry.pix_y)

        # Load run config
        try:
            self.run_config = {'mcheader': read_simu_info_merged_hdf5(self.hdf5_file_path)}
        except IndexError as e:
            self.simu = False
            self.run_config = {}
        if self.simu:
            assert particle_dict is not None, 'You must define a particle dictionary for MC dataset !'
        self.targets = {} if self.targets is None else self.targets
        self.run_config['metadata'] = {}

        with tables.File(hdf5_file_path, 'r') as hdf5_file:
            for attr in hdf5_file.root._v_attrs._f_list('user'):
                self.run_config['metadata'][attr] = hdf5_file.root._v_attrs[attr]

            self.dl1_params = hdf5_file.root[dl1_params_lstcam_key][:]
            self.dl1_param_names = hdf5_file.root[dl1_params_lstcam_key].colnames

            # Update MC only dl1 parameters with all parameters starting with "mc_"
            self.mc_only_dl1_parameters.extend([col for col in self.dl1_param_names
                                                if 'mc_' in col and col != 'mc_type'])

            # image related infos
            self.filtered_indices = np.arange(len(hdf5_file.root[dl1_images_lstcam_key]), dtype=int)

            # LST subarray
            layout = hdf5_file.root[DL1_SUBARRAY_LAYOUT][:]
            lst_layout_mask = layout['name'] == b'LST'
            self.layout_tel_ids = layout['tel_id'][lst_layout_mask]

            # Keep a copy of triggered energies for gammaboard
            if self.simu:
                dl1_params_df = pd.DataFrame(
                    {
                        'obs_id': self.dl1_params['obs_id'],
                        'event_id': self.dl1_params['event_id']
                    }
                )
                dl1_params_df = dl1_params_df.set_index(['obs_id', 'event_id'])
                unique_event_mask = ~dl1_params_df.index.duplicated(keep='first')
                self.trig_energies = self.dl1_params['mc_energy'][unique_event_mask]
                self.trig_tels = hdf5_file.root[DL1_SUBARRAY_TRIGGER_KEY][:]['tels_with_trigger']
            else:
                self.trig_energies = None
                self.trig_tels = np.full((len(self.dl1_params), 6), False)
                self.trig_tels[:, np.searchsorted(layout['tel_id'], self.dl1_params[
                    'tel_id'])] = True  # TODO fix when real data has several tels
                
                # Get the pedestal id
                params = hdf5_file.root[dl1_params_lstcam_key][:]
                images = hdf5_file.root[dl1_images_lstcam_key][:]
                pedestals_id = params[params["event_type"] == 2]['event_id']
                # Filter the images based on the event id and keep the pedestal images only
                images_id = np.in1d(images['event_id'], pedestals_id)
                self.pedestals = images[images_id]['image']

            # Select sub-subarray
            if subarray is not None:
                assert np.in1d(subarray, self.layout_tel_ids).all(), 'All the telescopes of the subarray must be LSTs'
                self.layout_tel_ids = subarray
            subarray_mask = np.any(self.trig_tels[:, np.searchsorted(layout['tel_id'], self.layout_tel_ids)], axis=1)
            if self.trig_energies is not None:
                self.trig_energies = self.trig_energies[subarray_mask]
            event_mask = np.in1d(self.dl1_params['tel_id'], self.layout_tel_ids)
            self.dl1_params = self.dl1_params[event_mask]
            self.filtered_indices = self.filtered_indices[event_mask]

            # Load event info
            self.unique_event_ids = np.unique(self.dl1_params[:]['event_id'])

            if not self.simu and 'mc_type' not in self.dl1_params.dtype.names:
                self.dl1_params['mc_type'] = np.full(len(self.dl1_params), -9999)

            if self.simu:
                # Turn distances into km
                self.dl1_params['mc_x_max'] /= 1000
                self.dl1_params['mc_core_x'] /= 1000
                self.dl1_params['mc_core_y'] /= 1000
            self.dl1_params['tel_pos_x'] /= 1000
            self.dl1_params['tel_pos_y'] /= 1000
            self.dl1_params['tel_pos_z'] /= 1000

        # setup the ImageMapper transform
        if self.transform is not None:
            if hasattr(self.transform, 'setup_geometry'):
                self.transform.setup_geometry(self.camera_geometry)
            elif hasattr(self.transform, 'transforms'):
                for t in self.transform.transforms:
                    if hasattr(t, 'setup_geometry'):
                        t.setup_geometry(self.camera_geometry)

    def __len__(self):
        if self.group_by == 'image':
            return len(self.filtered_indices)
        else:
            return len(self.unique_event_ids)

    def _get_sample(self, idx):
        if self.group_by == 'image':
            data_t = self._get_image_data(idx)
            data = np.stack(data_t) if self.use_time else data_t[0]
            dl1_params = self.dl1_params[idx]
        else:
            event_id = self.unique_event_ids[idx]
            filtered_images_ids = np.arange(len(self.dl1_params))[self.dl1_params['event_id'] == event_id]
            dl1_params = self.dl1_params[self.dl1_params['event_id'] == event_id]
            tel_ids = dl1_params['tel_id'] - 1  # telescope ids start from 1
            dl1_params = dl1_params[0] if dl1_params.ndim > 1 else dl1_params
            if self.group_by == 'event_all_tels':
                # We want as many images as telescopes
                images_ids = np.full(len(self.layout_tel_ids), -1)
                images_ids[tel_ids] = filtered_images_ids
            elif self.group_by == 'event_triggered_tels':
                images_ids = filtered_images_ids
            else:
                raise ValueError('group_by option has an incorrect value.')
            data_t = self._get_image_data(images_ids)
            if self.use_time:
                assert len(data_t) == 2, 'When using both charge and peakpos you need the same' \
                                         'amount of each'
                event_images = data_t[0]
                event_times = data_t[1]
                event_images = np.nan_to_num(event_images)
                event_times = np.nan_to_num(event_times)

                data = np.empty((event_images.shape[0] * 2, event_images.shape[1]), dtype=np.float32)
                data[0::2, :] = event_images
                data[1::2, :] = event_times
            else:
                data = data_t[0]

        # We reogranize the pixels to match the 'LSTCam' geometry
        sample = {'image': data[..., self.inj_table]}
        transform_params = {}
        if self.transform:
            if isinstance(self.transform, GLearnCompose):
                sample['image'], transform_params = self.transform(sample['image'], **{'simu': self.simu, 'pedestals': self.pedestals})
            else:
                sample['image'] = self.transform(sample['image'])

        labels = {}
        if self.simu:
            dl1_parameters = {n: p for n, p in zip(self.dl1_param_names, dl1_params)
                              if n not in self.mc_only_dl1_parameters}
            for t in self.targets:
                if t == 'energy':
                    labels[t] = np.array([dl1_params['log_mc_energy']], dtype=np.float32)
                elif t == 'impact':
                    if self.group_by == 'image':
                        labels[t] = np.array([dl1_params['mc_core_x'] - dl1_params['tel_pos_x'],
                                              dl1_params['mc_core_y'] - dl1_params['tel_pos_y']], dtype=np.float32)
                    else:
                        labels[t] = np.array([dl1_params['mc_core_x'], dl1_params['mc_core_y']], dtype=np.float32)
                elif t == 'direction':
                    if self.group_by == 'image':
                        labels[t] = np.array([dl1_params['mc_alt'] - dl1_params['mc_alt_tel'],
                                              dl1_params['mc_az'] - dl1_params['mc_az_tel']], dtype=np.float32)
                    else:
                        labels[t] = np.array([dl1_params['mc_alt'], dl1_params['mc_az']], dtype=np.float32)
                elif t == 'xmax':
                    labels[t] = np.array([dl1_params['mc_x_max']])
                elif t == 'class':  # TODO replace by try except
                    labels[t] = self.particle_dict.get(dl1_params['mc_type'], -1)
                    if labels[t] == -1:
                        print(dl1_params['mc_type'])
                        print(self.hdf5_file_path)
                elif t == 'domain_class':
                    labels[t] = self._get_domain_label()
                elif t == 'autoencoder':
                    labels[t] = sample['image']
        else:
            dl1_parameters = {n: p for n, p in zip(self.dl1_param_names, dl1_params)
                              if n not in self.lst1_only_dl1_parameters}
            for t in self.targets:
                if t == 'class':
                    labels[t] = REAL_DATA_ID
                elif t == 'domain_class':
                    labels[t] = self._get_domain_label()
                elif t == 'autoencoder':
                    labels[t] = sample['image']

        if not self.train:
            dl1_parameters = {n: p for n, p in zip(self.dl1_param_names, dl1_params)}
                
        if labels:
            if self.target_transform:
                sample['label'] = {t: self.target_transform(label) for t, label in sample['label'].items()}
            else:
                sample['label'] = labels

        sample['dl1_params'] = dl1_parameters
        sample['transform_params'] = transform_params

        return sample

    def _get_domain_label(self):
        if self.domain == 'source':
            return torch.tensor(self.domain_dict[SOURCE], dtype=torch.int64)
        elif self.domain == 'target':
            return torch.tensor(self.domain_dict[TARGET], dtype=torch.int64)
        else:
            raise ValueError("Invalid domain. Must be 'source' or 'target'.")

    def _get_image_data(self, idx):
        raise NotImplementedError

    def filter_event(self, filter_dict):
        filter_mask = np.full(len(self.dl1_params), True)
        for filter_func, params in filter_dict.items():
            filter_mask = filter_mask & filter_func(self, **params)
        # Apply filtering
        self._update_events(filter_mask)
        # update images
        self.update_images(filter_mask)

    def _update_events(self, filter_mask):
        self.dl1_params = self.dl1_params[filter_mask]
        self.unique_event_ids = np.unique(self.dl1_params[:]['event_id'])

    def _filter_image(self, filter_dict):
        filter_mask = np.full(len(self.images), True)
        for filter_func, params in filter_dict.items():
            filter_mask = filter_mask & filter_func(self, **params)
        # Apply filtering
        self.update_images(filter_mask)
        self._update_events(filter_mask)

    def update_images(self, image_mask):

        raise NotImplementedError

    def filter_image(self, filter_dict):

        raise NotImplementedError


class MemoryLSTDataset(BaseLSTDataset):

    def __init__(self, hdf5_file_path, camera_type, group_by, targets=None, particle_dict=None, use_time=False,
                 train=True, subarray=None, transform=None, target_transform=None, **kwargs):

        super(MemoryLSTDataset, self).__init__(hdf5_file_path, camera_type, group_by, targets, particle_dict,
                                               use_time, train, subarray, transform, target_transform, **kwargs)

        with tables.File(hdf5_file_path, 'r') as hdf5_file:
            # Load images and peak times
            self.images = hdf5_file.root[dl1_images_lstcam_key].col('image').astype(np.float32)[self.filtered_indices]
            self.images = np.nan_to_num(self.images)
            if self.use_time:
                self.times = hdf5_file.root[dl1_images_lstcam_key].col('peak_time').astype(np.float32)[
                    self.filtered_indices]
                self.times = np.nan_to_num(self.times)

    def __getitem__(self, idx):
        return self._get_sample(idx)

    def _get_image_data(self, idx):
        if isinstance(idx, np.ndarray):
            data = np.zeros((len(idx), self.images.shape[1]))
            time = None
            if self.use_time:
                time = np.zeros((len(idx), self.times.shape[1]))
            for i, ind in enumerate(idx):
                if ind > -1:
                    indice = np.argwhere(self.filtered_indices == ind).item()
                    data[i] = self.images[indice]
                    if self.use_time:
                        time[i] = self.times[indice]
            data = (data,)
            if self.use_time:
                data += (time,)
        else:
            data = (self.images[idx],)
            if self.use_time:
                data += self.times[idx],
        return data

    def filter_image(self, filter_dict):
        self._filter_image(filter_dict)

    def update_images(self, image_mask):
        self.images = self.images[image_mask]
        if self.times is not None:
            self.times = self.times[image_mask]
        self.filtered_indices = np.arange(len(self.images))


class FileLSTDataset(BaseLSTDataset):

    def __init__(self, hdf5_file_path, camera_type, group_by, targets=None, particle_dict=None, use_time=False,
                 train=True, subarray=None, transform=None, target_transform=None, **kwargs):

        super(FileLSTDataset, self).__init__(hdf5_file_path, camera_type, group_by, targets, particle_dict,
                                             use_time, train, subarray, transform, target_transform, **kwargs)

    def __getitem__(self, idx):
        if self.hdf5_file is None:
            self.hdf5_file = tables.File(self.hdf5_file_path, 'r')
        return self._get_sample(idx)

    def _get_image_data(self, idx):
        image_id = self.filtered_indices[idx]
        if isinstance(image_id, np.ndarray):
            image_size = self.hdf5_file.root[dl1_images_lstcam_key].col('image').shape[1]
            data = np.zeros((len(image_id), image_size))
            time = None
            if self.use_time:
                time = np.zeros((len(image_id), image_size))
            for i, ind in enumerate(image_id):
                if ind > -1:
                    data[i] = np.nan_to_num(
                        self.hdf5_file.root[dl1_images_lstcam_key].col('image')[ind].astype(np.float32))
                    if self.use_time:
                        time[i] = np.nan_to_num(
                            self.hdf5_file.root[dl1_images_lstcam_key].col('peak_time')[ind].astype(np.float32))
            data = (data,)
            if self.use_time:
                data += time
        else:
            data = np.nan_to_num(self.hdf5_file.root[dl1_images_lstcam_key].col('image')[image_id].astype(np.float32)),
            if self.use_time:
                time = np.nan_to_num(
                    self.hdf5_file.root[dl1_images_lstcam_key].col('peak_time')[image_id].astype(np.float32))
                data += time,
        return data

    def filter_image(self, filter_dict):
        self._open_file()
        self._filter_image(filter_dict)
        self._close_file()

    def update_images(self, image_mask):
        self.filtered_indices = self.filtered_indices[image_mask]

    def _open_file(self):
        if self.hdf5_file is None:
            self.hdf5_file = tables.File(self.hdf5_file_path, 'r')
            self.images = np.nan_to_num(self.hdf5_file.root[dl1_images_lstcam_key].col('image')[self.filtered_indices])
            self.times = np.nan_to_num(
                self.hdf5_file.root[dl1_images_lstcam_key].col('peak_time')[self.filtered_indices])

    def _close_file(self):
        if self.hdf5_file is not None:
            self.hdf5_file.close()
            self.hdf5_file = None
            self.images = None
            self.times = None


class VisionDataset(Dataset):
    """
    The Dataset class corresponding to the following vision datasets :
        - digits : mnist, mnistm, usps
        - visda : synthetic, real

    Parameters
        ----------
        paths: (list) Paths to the datasets.
        dataset_parameters: (dict) The corresponding parameters to the datasets. These parameters will be applied to all
        datasets.
        transform: The transforms applied to the images.
        target_transform: The transforms applied to the targets.
        train: (bool) If train is 'True', returns the train datasets, otherwise returns the test datasets.
        domain: (str) In the domain adaptation context, gives an extra domain label 'source' or 'target'. Otherwise, set
        to 'None' (default).
        max_files: (int) The number of images to load in each dataset. If set to '-1' (default), all images and targets
        will be loaded.
    """

    def __init__(self, paths, dataset_parameters, transform=None, target_transform=None, train=True, domain=None,
                 max_files=-1, num_workers=10):
        self.paths = paths
        self.dataset_parameters = dataset_parameters
        self.camera_geometry = None  # Mandatory
        self.targets = list(dataset_parameters['targets'])
        self.train = train
        self.domain = 'source' if domain is None else domain
        self.console_logger = logging.getLogger(__name__)
        self.console_logger.addHandler(TqdmLoggingHandler())
        self.num_workers = num_workers if num_workers > 0 else 1
        self.max_files = -1 if max_files is None else max_files

        self.dataset = []
        for path in self.paths:  # TODO: Currently working only for paths[0], cf multiprocessing data loading
            self.dataset += self.load_dataset(path)

        self.transform = transform
        self.target_transform = target_transform

    def _get_domain_label(self):
        if self.domain == 'source':
            return torch.tensor(self.dataset_parameters['domain_dict'][SOURCE],dtype=torch.int64)
        elif self.domain == 'target':
            return torch.tensor(self.dataset_parameters['domain_dict'][TARGET], dtype=torch.int64)
        else:
            raise ValueError("Invalid domain. Must be 'source' or 'target'.")

    def load_dataset(self, path):
        split = 'train' if self.train else 'test'
        with open(os.path.join(path, split, "image_list.txt")) as f:
            lines = f.readlines()
            # Truncate the list if 'max_files' is defined
            if self.max_files > 0:
                random.shuffle(lines)
                lines = lines[:self.max_files]

            # Split the main list into 'num_workers' sublists
            a = len(lines) // self.num_workers
            b = len(lines) % self.num_workers
            length_to_split = self.num_workers * [a]
            length_to_split[-1] += b
            lines_iter = iter(lines)
            lines_list = [list(islice(lines_iter, elem)) for elem in length_to_split]

            # Multiprocessing
            ctx = mp.get_context('spawn')
            pool = ctx.Pool(processes=self.num_workers)

            dataset_list = list(pool.imap(self.load_subset, lines_list))
            dataset = sum(dataset_list, [])
            # dataset = self.load_subset(os.path.join(path, split), lines)

        return dataset

    def load_subset(self, lines, path=None):
        subset = []

        # TODO: makes it more generic: include multiple paths (partial func ?)
        split = 'train' if self.train else 'test'
        path = os.path.join(self.paths[0], split)

        for i in tqdm.tqdm(range(len(lines))):
            img_path = lines[i].split(' ')[0]
            label = int(lines[i].split(' ')[1])
            img_pil = Image.open(os.path.join(path, img_path))
            data = (img_pil.copy(), label)
            subset.append(data)
            img_pil.close()

        return subset

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, item):
        data = self.dataset[item]
        image, label_class = data[0], data[1]

        if self.transform:
            if isinstance(self.transform, GLearnCompose):
                image, transform_params = self.transform(image)
            else:
                image = self.transform(image)
                transform_params = {}

        labels = {}
        for t in self.targets:
            if t == 'class':
                labels['class'] = torch.tensor(label_class)
            elif t == 'domain_class':
                labels['domain_class'] = self._get_domain_label()
            elif t == 'autoencoder':
                labels['autoencoder'] = image.clone()

        if self.target_transform: 
            pass  # TODO: TO BE IMPLEMENTED

        return {'image': image, 'label': labels, 'transform_params': transform_params}


class NumpyDataset(Dataset):
    def __init__(self, data, labels, transform=None, target_transform=None):
        self.images = data
        self.labels = labels
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, item):
        if self.transform:
            self.images[item] = self.transform(self.images[item])
        if self.target_transform:
            self.labels[item] = self.target_transform(self.labels[item])

        return self.images[item], self.labels[item]


class HDF5Dataset(Dataset):
    """Loads data in a Dataset from a HDF5 file.

    Args:
        path (str): The path to the HDF5 file.
        transform (callable, optional): A callable or a composition of callable to be applied to the data.
        target_transform (callable, optional): A callable or a composition of callable to be applied to the labels.
    """

    def __init__(self, path, camera_type, transform=None, target_transform=None, telescope_transform=None):
        with tables.File(path, 'r') as f:
            self.images = f.root['images'][:][()]
            self.labels = f.root['labels'][:][()]
        self.transform = transform
        self.target_transform = target_transform
        self.camera_type = camera_type

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, item):
        image, label = self.images[item], self.labels[item]
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.transform(label)

        return {'image': image, 'label': label}


# Transforms classes
class GLearnCompose(transforms.Compose):
    """
    Custom transform Compose that can receive/output extra parameters when called.
    """
    def __call__(self, img, **kwargs):
        transform_params = {}
        for t in self.transforms:
            if isinstance(t, AddPoissonNoise):
                img = t(img, kwargs['simu'])
                transform_params['poisson_rate'] = t.rate_sampled
            elif isinstance(t, GetPoissonNoiseFromPedestals):
                img = t(img, kwargs['simu'], kwargs['pedestals'])
                transform_params['poisson_rate'] = t.rate_sampled
            elif isinstance(t, AddGaussianNoise):
                img = t(img)
                transform_params['gaussian_mean'] = t.mu_sampled
                transform_params['gaussian_std'] = t.sigma_sampled
            else:
                img = t(img)
        return img, transform_params


class Patchify:
    """Transform an image into patches."""

    def __init__(self, n_h, n_w, n_c=0):
        self.n_h = n_h
        self.n_w = n_w
        self.n_c = n_c

    def __call__(self, x):
        n = len(x.shape)
        if self.n_c > 0:
            x = x.unfold(n - 3, self.n_c, self.n_c)
        patches = x.unfold(n - 2, self.n_h, self.n_h).unfold(n - 1, self.n_w, self.n_w)

        if self.n_c > 0:
            return patches.reshape(-1, self.n_c, self.n_h, self.n_w)
        else:
            return patches.reshape(-1, self.n_h, self.n_w)


class TransformIACT:

    def setup_geometry(self, camera_geometry):
        raise NotImplementedError


class ResampleImage(TransformIACT):
    """
    Resample an hexagonal image with DL1 Data Handler Image Mapper
    The class needs to be instantiated first to be passed to a Dataset class but can be setup later when the camera
    information is available to the user
    """

    def __init__(self, mapping, output_size):
        self.camera = None
        self.image_mapper = None
        self.mapping = mapping
        self.output_size = output_size

    def setup_geometry(self, camera_geometry):
        # We need to rotate the camera for ImageMapper
        camera_geometry.rotate(camera_geometry.pix_rotation)
        pix_pos = np.array([camera_geometry.pix_x.to_value(u.m),
                            camera_geometry.pix_y.to_value(u.m),
                            ])
        self.camera = camera_geometry.camera_name
        self._setup_image_mapper(pix_pos)

    def _setup_image_mapper(self, pix_pos):
        self.image_mapper = ImageMapper(pixel_positions={self.camera: pix_pos},
                                        camera_types=[self.camera],
                                        mapping_method={self.camera: self.mapping},
                                        interpolation_image_shape={self.camera: self.output_size}
                                        )

    def __call__(self, data):
        mapped_data = self.image_mapper.map_image(data.T, self.camera)
        return mapped_data.T


class RescaleCharge(object):

    def __init__(self, scale):
        self.scale = scale

    def __call__(self, data):
        if data.ndim == 1:
            data = data * self.scale
        elif data.ndim == 2:
            data[0] = data[0] * self.scale
        return data


class ReducePixelValue(object):
    def __call__(self, data):
        if data.ndim == 1:
            data = data / data.max()
        elif data.ndim == 2:
            data[0] = data[0] / data[0].max()
            data[1] = data[1] / data[1].max()
        return data


class AddPoissonNoise(object):
    """
    Add a noise sampled from a Poisson distribution to the pixel charges. 
    The noise is sampled from a Poisson distribution with a rate defined by the user.
    This transform can also be used in the heterogeneous case that the data contains both real and simulated data. 
    If the __call__() method contains the 'simu' variable set to False, the noise is not added to the data. It is set to
    True by default. If the GLearnCompose is used, it is set to False for real data.

    Parameters
    ----------
    rate (float or list): the rate of the Poisson distribution. If a list, the rate is sampled from a uniform
    distribution between the two values. 
    """
    def __init__(self, rate: list):
        rate = rate if isinstance(rate, list) else [rate]
        assert all(isinstance(r, float) for r in rate), 'The rate list must contain only floats.'
        assert 1 <= len(rate) <= 2, 'The rate list must contain either one (rate) or two (min and max) elements.'
        self.rate = rate

    def sample_rate(self) -> float:
        if len(self.rate) == 2:
            return np.random.uniform(self.rate[0], self.rate[1])
        else:
            return self.rate

    def compute_noise(self, data: np.ndarray) -> np.ndarray:
        self.rate_sampled = torch.tensor([self.sample_rate()], dtype=torch.float32)
        poisson = torch.distributions.poisson.Poisson(self.rate_sampled)
        if data.ndim == 1:
            sample_shape = torch.Size(list(data.shape))
        elif data.ndim == 2:
            sample_shape = torch.Size(list(data[0].shape))
        return poisson.sample(sample_shape=sample_shape).numpy()
    
    def apply_noise(self, data: np.ndarray, noise: np.ndarray) -> np.ndarray:
        if data.ndim == 1:
            data = data + noise
        elif data.ndim == 2:
            data[0] = data[0] + noise.T  # Apply noise to the charge image
        return data

    def __call__(self, data: np.ndarray, simu: bool) -> np.ndarray:
        if simu:
            noise = self.compute_noise(data)
            return self.apply_noise(data, noise)
        else:  # Real data
            noise = self.compute_noise(data)  # Set the rate_sampled attribute, but do not apply the noise
            return data
        

class GetPoissonNoiseFromPedestals(object):
    """
    Get a noise from the pedestals within a subrun. The sampled rate corresponds to the difference between the trained
    Monte Carlo noise rate and the rate computed from the pedestals images
    δλ = λ_pedestals - λ_mc > 0

    Parameters
    ----------
    rate_mc (float or list): the rate of the Poisson distribution. If a list, the rate is sampled from a uniform
    distribution between the two values. 
    """
    def __init__(self, rate_mc: float):
        assert isinstance(rate_mc, float), 'The rate must be a float.'
        self.rate_mc = rate_mc  # λ_mc
        self.rate_sampled = torch.tensor([0], dtype=torch.float32)  # δλ

    def compute_rate_from_pedestals(self, pedestals: np.ndarray) -> None:
        if pedestals is not None:
            rate_real = np.mean(pedestals)
            rate_sampled = rate_real - self.rate_mc 
            self.rate_sampled = torch.tensor([rate_sampled], dtype=torch.float32)

    def __call__(self, data: np.ndarray, simu: bool, pedestals: np.ndarray) -> np.ndarray:
        if not simu:  # Real data
            self.compute_rate_from_pedestals(pedestals)
        return data
        

class AddGaussianNoise(object):
    """
    Add a noise sampled from a Gaussian distribution to the image. 
    The noise is sampled from a Gaussian distribution with a mean and standard deviation defined by the user.

    Parameters
    ----------
    mu (float or list): the mean of the Gaussian distribution. If a list, the rate is sampled from a uniform
    distribution between the two values. 
    sigma (float or list): the stadard deviation of the Gaussian distribution. If a list, the rate is sampled 
    from a uniform distribution between the two values. 
    """
    def __init__(self, mu: list, sigma: list):
        mu = mu if isinstance(mu, list) else [mu]
        sigma = sigma if isinstance(sigma, list) else [sigma]
        assert all(isinstance(m, float) for m in mu), 'The mu list must contain only floats.'
        assert all(isinstance(s, float) for s in sigma), 'The sigma list must contain only floats.'
        assert 1 <= len(mu) <= 2, 'The mu list must contain either one (mu) or two (min and max) elements.'
        assert 1 <= len(sigma) <= 2, 'The sigma list must contain either one (sigma) or two (min and max) elements.'
        self.mu = mu
        self.sigma = sigma

    def sample(self) -> Tuple[float, float]:
        if len(self.mu) == 2:
            mu = np.random.uniform(self.mu[0], self.mu[1])
        else:
            mu = self.mu

        if len(self.sigma) == 2:
            sigma = np.random.uniform(self.sigma[0], self.sigma[1])
        else:
            sigma = self.sigma

        return torch.tensor(mu, dtype=torch.float32).view(-1, 1), torch.tensor(sigma, dtype=torch.float32).view(-1, 1)

    def compute_noise(self, data: torch.Tensor) -> torch.Tensor:
        self.mu_sampled, self.sigma_sampled = self.sample()
        sample_shape = torch.Size(data.shape)
        if self.mu_sampled == self.sigma_sampled == 0.:
            # This case triggers an error with the Normal class from Pytorch
            return torch.zeros_like(data)
        else:
            gaussian = torch.distributions.normal.Normal(self.mu_sampled, self.sigma_sampled)
            return gaussian.sample(sample_shape=sample_shape).view(sample_shape)
    
    def apply_noise(self, data: torch.Tensor, noise: torch.Tensor) -> torch.Tensor:
        return data + noise

    def __call__(self, data: torch.Tensor, **kwargs) -> torch.Tensor:
        noise = self.compute_noise(data)
        return self.apply_noise(data, noise)


class FlattenNumpy(object):
    def __init__(self, start_dim=0):
        self.start_dim = start_dim

    def __call__(self, data):
        size = np.prod(data.shape[self.start_dim:])
        return data.reshape(data.shape[:self.start_dim] + tuple([size]))


class NumpyToTensor(object):
    """Convert a numpy array to a tensor"""

    def __call__(self, data):
        data = torch.tensor(data)
        return data


class RotateImage(object):
    """Rotate telescope image based on rotated indices"""

    def __init__(self, rotated_indices):
        self.rotated_indices = rotated_indices

    def __call__(self, data):
        assert data.shape[-1] == self.rotated_indices.shape[0], 'The length of rotated indices must match the size ' \
                                                                'of the image to rotate. '
        return data[..., self.rotated_indices]


class NormalizePixel(object):

    def __init__(self, max_pix):
        self.max = max_pix

    def __call__(self, data):
        return data / self.max


class CleanImages(TransformIACT):
    """
    Cleaning transform.
    Parameters
    ----------
    new_channel (Bool): if True, adds the cleaning mask to the data as a new channel.
    If False, apply the cleaning mask to the data.
    """
    def __init__(self, new_channel=False, **opts):
        self.opts = opts
        self.new_channel = new_channel
        self.camera_geometry = None

    def setup_geometry(self, camera_geometry):
        self.camera_geometry = camera_geometry

    def __call__(self, data):
        image = data if data.ndim == 1 else data[0]
        clean_mask = tailcuts_clean(self.camera_geometry, image, **self.opts)
        if self.new_channel:
            return np.concatenate([data, np.expand_dims(clean_mask, axis=0).astype(np.float32)])
        else:
            return data * clean_mask


# Augment data functions

def augment_via_duplication(datasets, scale, num_workers):
    """
    Augment data by duplicating events based on the inverse detected energies distribution
    Parameters
    ----------
    datasets (list): list of Subsets
    scale (float): the scale to constrain the maximum duplication factor
    num_workers (int): number of processes to use

    Returns
    -------

    """

    def get_factor(energy, scale):
        fitlog = 1.19 * (2.59 - energy) * (1 - np.exp(-2.91 - energy))
        p = 1 / (10 ** fitlog) * 1 / (1 / (10 ** fitlog)).min()
        return np.floor(1 + scale * np.log10(p)).astype(np.int)

    def process_subset():
        torch.set_num_threads(1)
        while True:
            if input_queue.empty():
                break
            else:
                sub = input_queue.get()
                factors = get_factor(np.log10(sub.dataset.energies), scale)
                augmented_ids = np.repeat(np.arange(len(sub.dataset)), factors)
                sub.indices = augmented_ids[np.in1d(augmented_ids, sub.indices)]
                new_datasets.append(sub)

    input_queue = mp.Queue()
    for subset in datasets:
        input_queue.put(subset)
    manager = mp.Manager()
    new_datasets = manager.list()
    workers = [mp.Process(target=process_subset) for _ in range(num_workers)]
    for w in workers:
        w.start()
    input_queue.close()
    for w in workers:
        w.join()
    return list(new_datasets)
