'''
Neuroscience toolkit
Written for Python 3.12.4
@ Jeremy Schroeter, August 2024
'''

import os
import errno
import json
import importlib
import numpy as np
import matplotlib.pyplot as plt
from subprocess import PIPE, run
from scipy.io import loadmat
from scipy import signal
from scipy.signal import lfilter, butter, filtfilt, dimpulse, find_peaks
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


class LabChartDataset:
    '''
    Dataset wrapper class which organizes and provides a way to interact with
    LabChart data that has been exported as a MATLAB file

    Example usage:
        dataset = LabChartDataset(file_path)
        channel_data = dataset.data['Channel #']
        block_n = dataset.get_block(n)
    '''
    def __init__(self, file_path: str):

        # scipy throw an error w/o this, but this should be less verbose of an
        # error
        if os.path.exists(file_path) is False:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)

        self.matlab_dict = loadmat(file_name=file_path)
        self.n_channels = len(self.matlab_dict['titles'])

        self.data = {f'Channel {ch + 1}': self._split_blocks(ch) for ch in range(self.n_channels)}

    def _split_blocks(self, channel_idx: int) -> list[np.ndarray]:
        '''
        Private method for building the data dictionary
        '''

        raw = self.matlab_dict['data'].reshape(-1)
        channel_starts = self.matlab_dict['datastart'][channel_idx] - 1
        channel_ends = self.matlab_dict['dataend'][channel_idx]

        n_blocks = channel_starts.shape[0]
        channel_blocks = []

        for idx in range(n_blocks):
            start = int(channel_starts[idx])
            end = int(channel_ends[idx])
            channel_blocks.append(raw[start: end])

        return channel_blocks

    def _get_single_block(self, block_index: int) -> np.ndarray:
        '''
        Private method for getting a single block
        '''
        if self.n_channels == 1:
            return self.data['Channel 1'][block_index]

        block = []
        for ch in self.data.keys():
            block.append(self.data[ch][block_index])
        return np.stack(block)

    def _get_multiple_blocks(self, block_indices: list[int]) -> np.ndarray:
        '''
        Private method for getting multiple blocks. Blocks must be the same
        length
        '''
        if self.n_channels == 1:
            return np.stack([self.data['Channel 1'][idx] for idx in block_indices])

        blocks = []
        for channel in self.data.keys():
            for idx in block_indices:
                blocks.append(self.data[channel][idx])
        return np.array(blocks)

    def get_block(self, indices: list[int] | int) -> np.ndarray:
        '''
        Given a block index number, returns a (channel, timepoints) array
        containing the data for that block. If only 1 channel, returns a
        1D array of size (timepoints,)
        '''

        if isinstance(indices, int):
            return self._get_single_block(indices)
        else:
            return self._get_multiple_blocks(indices)

    @property
    def fs(self) -> np.ndarray:
        '''
        Property which returns the sample rate for all channels.
        '''
        return self.matlab_dict['samplerate']

    @property
    def channels(self) -> int:
        '''
        Property which returns the number of channels in the dataset.
        '''
        return self.n_channels


class Filter:
    '''
    Class for implementing low-, high-, and band-pass filters to 1d signals.
    Parameters
    -------------

        fs : int
            Signal sample rate

        filter_type : {'low', 'high', 'band'}
            Which type of filter to apply

        lowcut : float
            Lowcut frequency for a high or band pass filter. Leave as none if
            implementing low pass

        highcut: float
            Highcut frequency for a low or band pass filter. Leave as none if
            implementing high pass.
    '''

    def __init__(
            self,
            fs: int,
            filter_type: str,
            lowcut: float = None,
            highcut: float = None):

        if filter_type == 'band':
            if lowcut is None or highcut is None:
                raise ValueError(
                    "Both lowcut and highcut must be provided for a bandpass filter."
                )
            self.lowcut = lowcut
            self.highcut = highcut
            self.b, self.a = butter(4, [lowcut, highcut], btype=filter_type, fs=fs)
        elif filter_type == 'low':
            if highcut is None:
                raise ValueError("Highcut must be provided for a lowpass filter.")
            self.highcut = highcut
            self.b, self.a = butter(4, highcut, btype=filter_type, fs=fs)
        elif filter_type == 'high':
            if lowcut is None:
                raise ValueError("Lowcut must be provided for a highpass filter.")
            self.lowcut = lowcut
            self.b, self.a = butter(4, lowcut, btype=filter_type, fs=fs)
        else:
            raise ValueError("Invalid filter type. Supported types are 'band', 'low', and 'high'.")

    def apply(self, arr: np.ndarray) -> np.ndarray:
        '''
        Apply filter to 1d signal arr
        Parameters
        -------------
        arr: np.ndarray
            signal to apply filter to
        '''
        return filtfilt(self.b, self.a, arr)

    @property
    def kernel(self) -> np.ndarray:
        '''
        Kernel/IR of the filter.
        '''
        system = (self.b, self.a, 1)
        _, h = dimpulse(system, n=100)
        return h[0].flatten()

    @property
    def high(self) -> float:
        '''
        Filter highcut frequency
        '''
        return self.highcut

    @property
    def low(self) -> float:
        '''
        Filter lowcut frequency
        '''
        return self.lowcut


class FiringRate:
    '''
    Class for converting spike trains to firing rates.

    Parameters
    -------------
    fs : int
        Sample rate of spike train

    filter_type : {'gaussian', 'exponential', 'boxcar'}, default='gaussian'
        Type of kernel to convolve spike train with. All are causal filters

    time_constant : float, default=0.01
        Parameter (units of seconds) determining the size of the kernel
    '''
    def __init__(self, fs: int, filter_type: str = 'gaussian', time_constant: float = 0.01):

        self.filter_type = filter_type
        self.time_constant = time_constant
        self.fs = fs
        self.kernel = self._create_filter_kernel()

    def _create_filter_kernel(self) -> np.ndarray:
        '''
        Private method for building the specified kernel
        '''

        if self.filter_type == 'gaussian':
            n = int(self.time_constant * self.fs * 5)
            t = np.arange(0, n) / self.fs
            kernel = np.exp(-0.5 * (t / self.time_constant) ** 2)
            kernel /= kernel.sum()

        elif self.filter_type == 'exponential':
            n = int(self.time_constant * self.fs * 5)
            t = np.arange(0, n) / self.fs
            kernel = np.exp(-t / self.time_constant)
            kernel /= kernel.sum()

        elif self.filter_type == 'boxcar':
            n = int(self.time_constant * self.fs)
            t = np.arange(0, n) / self.fs
            kernel = np.ones(n) / n

        else:
            raise ValueError('Unsupported filter type. Choose "exponential", "boxcar", or "gaussian"')
        return kernel

    def apply(self, spike_train: np.ndarray) -> np.ndarray:
        '''
        Apply filter to spike train.
        '''
        firing_rate = lfilter(self.kernel, [1], spike_train)
        return firing_rate * self.fs


class SortedSpikes:
    '''
    Object for interacting with the results of running the spike sorter.
    This object should only be returned by SpikeSorter and not created by the user.

    Parameters
    ----
    sort_summary : dict
        output of _organize_clusters private method from SpikeSorter class
    '''
    def __init__(self, sort_summary: dict):
        print(list(sort_summary.keys())[:-5])
        self.sorted_spikes = {cluster: sort_summary[cluster] for cluster in list(sort_summary.keys())[:-5]}
        self.params = sort_summary['parameters']
        self.pca_embeddings = sort_summary['pca_embeddings']
        self.pca_var_explained = sort_summary['pca_var_explained']
        self.clusters = sort_summary['cluster_labels']

    def get_cluster_waveforms(self, cluster: int) -> np.ndarray:
        '''
        Given a cluster number, returns the waveforms associated with that cluster
        '''
        return self.sorted_spikes[f'cluster_{cluster}']['waveforms']

    def get_cluster_spike_times(self, cluster: int) -> np.ndarray:
        '''
        Given a clsuter number, returns the spike times associated with that cluster
        '''
        return self.sorted_spikes[f'cluster_{cluster}']['spike_times']

    def plot_clusters(self) -> None:
        '''
        Plot all the waveforms colored by cluster as well as the mean
        waveform of each cluster.
        '''

        for idx in range(len(self.sorted_spikes)):
            waveforms = self.get_cluster_waveforms(idx + 1)
            avg = waveforms.mean(0)
            for i, wav in enumerate(waveforms):
                if i == 0:
                    plt.plot(wav, alpha=0.3, c=f'C{idx}', label=f'cluster {idx + 1}')
                else:
                    plt.plot(wav, alpha=0.3, c=f'C{idx}')
            plt.plot(avg, c='black', lw=3)

        plt.ylabel('V')
        plt.xlabel('time (samples)')
        plt.legend()
        plt.show()

    def plot_pca(self) -> None:
        '''
        Plot the PCA embeddings of the waveforms colored by their cluster.
        '''
        for cluster_id in np.unique(self.clusters):
            cluster_wfs = self.pca_embeddings[self.clusters == cluster_id]
            plt.scatter(cluster_wfs[:, 0], cluster_wfs[:, 1], label=f'cluster {cluster_id + 1}')
        plt.xlabel('PC1')
        plt.ylabel('PC2')
        plt.legend()
        plt.show()


class SpikeSorter:
    '''
    Class for performing spike sorting on a 1d raw voltage trace.

    Parameters
    ----------------
    fs : int
        Sample rate

    bp_lowcut : float
        Lowcut for the bandpass

    bp_highcut : float
        Highcut for the bandpass

    ma_window_size : float
        Window size for the moving average calculation, units in seconds
    '''
    def __init__(
            self,
            fs: int,
            bp_lowcut: float = 100,
            bp_highcut: float = 9000,
            ma_window_size: float = 0.025,
            wf_ws: int = 30):

        self.fs = fs
        self.bp_lowcut = bp_lowcut
        self.bp_highcut = bp_highcut
        self.ma_window_size = ma_window_size
        self.wf_ws = wf_ws
        self.params = {
            'fs': fs,
            'bp_lowcut': bp_lowcut,
            'bp_highcut': bp_highcut,
            'ma_window_size': ma_window_size,
            'wf_ws': wf_ws
        }

    def _apply_band_pass(self, arr: np.ndarray) -> np.ndarray:
        '''
        Private method for applying bandpass to 1d signal
        '''
        filter = Filter(self.fs, 'band', self.bp_lowcut, self.bp_highcut)
        return filter.apply(arr)

    def _moving_average(self, arr: np.ndarray) -> np.ndarray:
        '''
        Private method for computing a moving average
        '''
        n = int(self.fs * self.ma_window_size)
        window = np.ones(n) / n
        return signal.convolve(arr, window, mode='same')

    def _moving_std(self, arr: np.ndarray) -> np.ndarray:
        '''
        Private method for computing a moving standard deviation
        '''
        avg = self._moving_average(arr)
        avg_sq = self._moving_average(arr ** 2)
        return np.sqrt(avg_sq - avg ** 2)

    def _adaptive_threshold_spike_detection(self, arr: np.ndarray) -> np.ndarray:
        '''
        Private method for doing spike event detection using a moving average technique
        '''
        mov_avg, mov_std = self._moving_average(arr), self._moving_std(arr)
        adaptive_threshold = mov_avg + 4 * mov_std
        peaks, _ = find_peaks(arr, height=adaptive_threshold)
        return peaks

    def _extract_waveforms(self, filtered_arr: np.ndarray, spike_times: np.ndarray) -> np.ndarray:
        '''
        Private method for extracting waveforms givne spike times and recording
        '''
        return np.vstack([filtered_arr[spike - self.wf_ws: spike + self.wf_ws]
                          for spike in spike_times])

    def _apply_pca(self, waveforms: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        '''
        Private method for applying PCA to extracted waveforms.
        '''
        pca = PCA()
        scaler = StandardScaler(with_std=False)
        scaled_waveforms = scaler.fit_transform(waveforms)
        pca_embeddings = pca.fit_transform(scaled_waveforms)
        return pca_embeddings, pca.explained_variance_ratio_

    def _fit_clusters(self, pca_embeddings: np.ndarray) -> np.ndarray:
        '''
        Private method for clustering PCA embeddings. Tries a number of cluster
        numbers and returns the one that maximizes the silhoutte score
        '''
        top_two_embeddings = pca_embeddings[:, :10]

        scores = []
        cluster_range = range(2, 11)
        for n_clusters in cluster_range:
            kmeans = KMeans(n_clusters, n_init='auto').fit(top_two_embeddings)
            labels = kmeans.labels_
            scores.append(silhouette_score(top_two_embeddings, labels))

        best_cluster_number = cluster_range[np.array(scores).argmax()]
        kmeans = KMeans(best_cluster_number, n_init='auto').fit(top_two_embeddings)
        return kmeans.labels_, scores

    def _organize_clusters(
            self,
            spike_times: np.ndarray,
            waveforms: np.ndarray,
            labels: np.ndarray,
            pca_embeddings: np.ndarray,
            clustering_scores: np.ndarray,
            pca_var_explained: np.ndarray) -> dict:
        '''
        Private method for constructing a dictionary containing sorted spikes and metrics
        '''

        sort_summary = {
            f'cluster_{i + 1}': {
                'spike_times': spike_times[np.where(labels == i)],
                'waveforms': waveforms[np.where(labels == i)]
            }
            for i in np.unique(labels)
        }

        sort_summary['parameters'] = self.params
        sort_summary['cluster_labels'] = labels
        sort_summary['clustering_scores'] = clustering_scores
        sort_summary['pca_var_explained'] = pca_var_explained
        sort_summary['pca_embeddings'] = pca_embeddings
        return sort_summary

    def apply(self, recording: np.ndarray) -> SortedSpikes:
        '''
        Spike sort a 1d signal
        '''

        arr_filtered = self._apply_band_pass(recording)
        self.spike_times = self._adaptive_threshold_spike_detection(arr_filtered)
        self.waveforms = self._extract_waveforms(arr_filtered, self.spike_times)
        self.pca_embeddings, self.pca_explained_var = self._apply_pca(self.waveforms)
        cluster_labels, self.cluster_scores = self._fit_clusters(self.pca_embeddings)

        self.sort_summary = self._organize_clusters(
            self.spike_times,
            self.waveforms,
            cluster_labels,
            self.pca_embeddings,
            self.cluster_scores,
            self.pca_explained_var
        )

        print('Spikes sorted')
        print(f'Found {len(self.sort_summary) - 4} neurons in recording')

        return SortedSpikes(self.sort_summary)

    def update_clusters(self, new_cluster_labels: np.ndarray) -> SortedSpikes:
        self.sort_summary = {}
        for i in np.unique(new_cluster_labels):
            self.sort_summary[f'cluster_{i + 1}'] = {
                'spike_times': self.spike_times[np.where(new_cluster_labels == i)],
                'waveforms': self.waveforms[np.where(new_cluster_labels == i)]
            }
        self.sort_summary['parameters'] = self.params
        self.sort_summary['cluster_labels'] = new_cluster_labels
        self.sort_summary['clustering_scores'] = self.cluster_scores
        self.sort_summary['pca_var_explained'] = self.pca_explained_var
        self.sort_summary['pca_embeddings'] = self.pca_embeddings
        self.sort_summary['cluster_labels'] = new_cluster_labels
        return SortedSpikes(self.sort_summary)


def time_above_half_max(arr: np.ndarray, fs: int, above_baseline: bool) -> float:
    '''
    Compute the time above half max

    Parameters
    ------------
    arr : np.ndarray
        Array to compute time above half max for

    fs : int
        Sample rate of arr
    '''
    if above_baseline:
        return np.where(arr > arr.max() / 2)[0].size / fs
    else:
        return np.where(-arr > -arr.max() / 2)[0].size / fs


def area_under_curve(arr: np.ndarray, fs: int, above_baseline: bool) -> float:
    '''
    Compute the area under the curve of a waveform

    Parameters
    ------------
    arr : np.ndarray
        Array to compute area under curve for

    fs : int
        Sample rate of arr
    '''
    if above_baseline:
        return np.trapz(arr, dx=1/fs)
    else:
        return np.trapz(-arr, dx=1/fs)


def peak_to_peak(arr: np.ndarray) -> float:
    '''
    Compute the peak to peak of a waveform

    Parameters
    ------------

    arr : np.ndarray
        Array to compute peak to peak for
    '''
    return arr.max() - arr.min()


def rise_time(arr: np.ndarray, fs: int, threshold: float) -> float:
    '''
    Compute the rise time of a waveform

    Parameters
    ------------

    arr : np.ndarray
        Array to compute rise time for

    fs : int
        Sample rate of arr

    threshold : float
        Threshold amplitude to find start of rise time
    '''
    start_time = np.where(arr > threshold)[0][0]
    return (np.argmax() - start_time) / fs


def hand_pick_clusters(embeddings: np.ndarray) -> np.ndarray:
    '''
    Function for hand picking the clusters with a lasso selector
    if you are unhappy with the fit from KMeans

    Parameters
    ------------
    embeddings : np.ndarray
        PCA embeddings of the waveforms
    '''

    # Create file paths where we will store temporary data
    input_filename = os.path.join(os.getcwd(), 'embeddings.json')
    output_filename = os.path.join(os.getcwd(), 'clusters.json')

    # Create tempfile
    with open(input_filename, 'w') as f:
        json.dump(embeddings.tolist(), f)

    # Get path to lasso script
    with importlib.resources.path('neuscitk', 'lasso_clusters.py') as path:
        path = os.path.join(path)

    # Rum script as a subprocess
    run(['python', path, input_filename, output_filename], stdout=PIPE, stderr=PIPE, text=True, check=True)

    # Load and return newly chos`en clusters
    with open(output_filename, 'r') as f:
        new_clusters = json.load(f)
    new_clusters = np.array(new_clusters)

    # Delete temp files
    os.remove(input_filename)
    os.remove(output_filename)

    return new_clusters
