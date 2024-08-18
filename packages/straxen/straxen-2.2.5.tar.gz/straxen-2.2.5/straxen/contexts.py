import os
import warnings
from typing import Dict, Any, List, Optional
from immutabledict import immutabledict
import socket

from pandas.util._decorators import deprecate_kwarg
import strax
import straxen

from straxen import HAVE_ADMIX

common_opts: Dict[str, Any] = dict(
    register_all=[],
    # Register all peak/pulse processing by hand as 1T does not need to have
    # the high-energy plugins.
    register=[
        straxen.PulseProcessing,
        straxen.Peaklets,
        straxen.PeakletClassification,
        straxen.MergedS2s,
        straxen.Peaks,
        straxen.PeakBasics,
        straxen.PeakProximity,
        straxen.Events,
        straxen.EventBasics,
        straxen.EventPositions,
        straxen.CorrectedAreas,
        straxen.EnergyEstimates,
        straxen.EventInfoDouble,
        straxen.DistinctChannels,
    ],
    check_available=("peak_basics", "event_basics"),
    store_run_fields=("name", "number", "start", "end", "livetime", "mode", "source"),
)

xnt_common_config = dict(
    n_tpc_pmts=straxen.n_tpc_pmts,
    n_top_pmts=straxen.n_top_pmts,
    gain_model="cmt://to_pe_model?version=ONLINE&run_id=plugin.run_id",
    gain_model_nv="cmt://to_pe_model_nv?version=ONLINE&run_id=plugin.run_id",
    gain_model_mv="cmt://to_pe_model_mv?version=ONLINE&run_id=plugin.run_id",
    channel_map=immutabledict(
        # (Minimum channel, maximum channel)
        # Channels must be listed in a ascending order!
        tpc=(0, 493),
        he=(500, 752),  # high energy
        aqmon=(790, 807),
        aqmon_nv=(808, 815),  # nveto acquisition monitor
        tpc_blank=(999, 999),
        mv=(1000, 1083),
        aux_mv=(1084, 1087),  # Aux mv channel 2 empty  1 pulser and 1 GPS
        mv_blank=(1999, 1999),
        nveto=(2000, 2119),
        nveto_blank=(2999, 2999),
    ),
    # Clustering/classification parameters
    # Event level parameters
    fdc_map=(
        "itp_map://"
        "resource://"
        "cmt://"
        "format://fdc_map_{alg}"
        "?alg=plugin.default_reconstruction_algorithm"
        "&version=ONLINE"
        "&run_id=plugin.run_id"
        "&fmt=binary"
        "&scale_coordinates=plugin.coordinate_scales"
    ),
    z_bias_map=(
        "itp_map://"
        "resource://"
        "XnT_z_bias_map_chargeup_20230329.json.gz?"
        "fmt=json.gz"
        "&method=RegularGridInterpolator"
    ),
)
# these are placeholders to avoid calling cmt with non integer run_ids. Better solution pending.
# s1, s2 and fd corrections are still problematic

# Plugins in these files have nT plugins, E.g. in pulse&peak(let)
# processing there are plugins for High Energy plugins. Therefore, do not
# st.register_all in 1T contexts.
xnt_common_opts = common_opts.copy()
xnt_common_opts.update(
    {
        "register": list(common_opts["register"])
        + [
            straxen.PeakletSOMClass,
            straxen.PeaksSOMClassification,
            straxen.EventSOMClassification,
        ],
        "register_all": list(common_opts["register_all"])
        + [
            straxen.plugins,
        ],
        "use_per_run_defaults": False,
    }
)


##
# XENONnT
##


def xenonnt(cmt_version="global_ONLINE", xedocs_version=None, _from_cutax=False, **kwargs):
    """XENONnT context."""
    if not _from_cutax and cmt_version != "global_ONLINE":
        warnings.warn("Don't load a context directly from straxen, use cutax instead!")
    st = straxen.contexts.xenonnt_online(**kwargs)
    st.apply_cmt_version(cmt_version)

    if xedocs_version is not None:
        st.apply_xedocs_configs(version=xedocs_version, **kwargs)

    return st


def xenonnt_som(cmt_version="global_ONLINE", xedocs_version=None, _from_cutax=False, **kwargs):
    """XENONnT context for the SOM."""

    st = straxen.contexts.xenonnt(
        cmt_version=cmt_version, xedocs_version=xedocs_version, _from_cutax=_from_cutax, **kwargs
    )
    del st._plugin_class_registry["peaklet_classification"]
    st.register(
        (
            straxen.PeakletClassificationSOM,
            straxen.PeaksSOM,
            straxen.PeakBasicsSOM,
            straxen.EventBasicsSOM,
        )
    )

    return st


def find_rucio_local_path(include_rucio_local, _rucio_local_path):
    """Check the hostname to determine which rucio local path to use. Note that access to
    /dali/lgrandi/rucio/ is possible only if you are on dali compute node or login node.

    :param include_rucio_local: add the rucio local storage frontend. This is only needed if one
        wants to do a fuzzy search in the data the runs database is out of sync with rucio
    :param _rucio_local_path: str, path of local RSE of rucio. Only use for testing!

    """
    hostname = socket.gethostname()
    # if you are on dali compute node, do nothing
    if ("dali" in hostname) and ("login" not in hostname):
        _include_rucio_local = include_rucio_local
        __rucio_local_path = _rucio_local_path
    # Assumed the only other option is 'midway' or login nodes,
    # where we have full access to dali and project space.
    # This doesn't make sense outside XENON but we don't care.
    else:
        _include_rucio_local = True
        __rucio_local_path = "/project/lgrandi/rucio/"
        print(
            "You specified _auto_append_rucio_local=True and you are not on dali compute nodes, "
            f"so we will add the following rucio local path: {__rucio_local_path}"
        )

    return _include_rucio_local, __rucio_local_path


@deprecate_kwarg("_minimum_run_number", "minimum_run_number")
@deprecate_kwarg("_maximum_run_number", "maximum_run_number")
@deprecate_kwarg("_include_rucio_remote", "include_rucio_remote")
@deprecate_kwarg("_add_online_monitor_frontend", "include_online_monitor")
def xenonnt_online(
    output_folder: str = "./strax_data",
    we_are_the_daq: bool = False,
    minimum_run_number: int = 7157,
    maximum_run_number: Optional[int] = None,
    # Frontends
    include_rucio_remote: bool = False,
    include_online_monitor: bool = False,
    include_rucio_local: bool = False,
    # Frontend options
    download_heavy: bool = False,
    _auto_append_rucio_local: bool = True,
    _rucio_path: str = "/dali/lgrandi/rucio/",
    _rucio_local_path: Optional[str] = None,
    _raw_paths: List[str] = ["/dali/lgrandi/xenonnt/raw"],
    _processed_paths: List[str] = [
        "/dali/lgrandi/xenonnt/processed",
        "/project2/lgrandi/xenonnt/processed",
        "/project/lgrandi/xenonnt/processed",
    ],
    # Testing options
    _context_config_overwrite: Optional[dict] = None,
    _database_init: bool = True,
    _forbid_creation_of: Optional[dict] = None,
    **kwargs,
):
    """XENONnT online processing and analysis.

    :param output_folder: str, Path of the strax.DataDirectory where new data can be stored
    :param we_are_the_daq: bool, if we have admin access to upload data
    :param minimum_run_number: int, lowest number to consider
    :param maximum_run_number: Highest number to consider. When None (the default) consider all runs
        that are higher than the minimum_run_number.
    :param include_rucio_remote: add the rucio remote frontend to the context
    :param include_online_monitor: add the online monitor storage frontend
    :param include_rucio_local: add the rucio local storage frontend. This is only needed if one
        wants to do a fuzzy search in the data the runs database is out of sync with rucio
    :param download_heavy: bool, whether or not to allow downloads of heavy data (raw_records*, less
        the aqmon)
    :param _auto_append_rucio_local: bool, whether or not to automatically append the rucio local
        path
    :param _rucio_path: str, path of rucio
    :param _rucio_local_path: str, path of local RSE of rucio. Only use for testing!
    :param _raw_paths: list[str], common path of the raw-data
    :param _processed_paths: list[str]. common paths of output data
    :param _context_config_overwrite: dict, overwrite config
    :param _database_init: bool, start the database (for testing)
    :param _forbid_creation_of: str/tuple, of datatypes to prevent form being written (raw_records*
        is always forbidden).
    :param kwargs: dict, context options
    :return: strax.Context

    """
    context_options = {**straxen.contexts.xnt_common_opts, **kwargs}

    st = strax.Context(config=straxen.contexts.xnt_common_config, **context_options)
    st.register(
        [
            straxen.DAQReader,
            straxen.LEDCalibration,
            straxen.LEDAfterpulseProcessing,
            straxen.nVeto_reflectivity,
        ]
    )

    if _auto_append_rucio_local:
        include_rucio_local, _rucio_local_path = find_rucio_local_path(
            include_rucio_local, _rucio_local_path
        )

    st.storage = (
        [
            straxen.RunDB(
                readonly=not we_are_the_daq,
                minimum_run_number=minimum_run_number,
                maximum_run_number=maximum_run_number,
                runid_field="number",
                new_data_path=output_folder,
                rucio_path=_rucio_path,
            )
        ]
        if _database_init
        else []
    )
    if not we_are_the_daq:
        for _raw_path in _raw_paths:
            st.storage += [
                strax.DataDirectory(_raw_path, readonly=True, take_only=straxen.DAQReader.provides)
            ]
        for _processed_path in _processed_paths:
            st.storage += [strax.DataDirectory(_processed_path, readonly=True)]

        if output_folder:
            st.storage += [
                strax.DataDirectory(
                    output_folder,
                    provide_run_metadata=True,
                )
            ]
        st.context_config["forbid_creation_of"] = straxen.daqreader.DAQReader.provides
        if _forbid_creation_of is not None:
            st.context_config["forbid_creation_of"] += strax.to_str_tuple(_forbid_creation_of)

    # Add the rucio frontend if we are able to
    if include_rucio_remote and HAVE_ADMIX:
        rucio_frontend = straxen.RucioRemoteFrontend(
            staging_dir=os.path.join(output_folder, "rucio"),
            download_heavy=download_heavy,
        )
        st.storage += [rucio_frontend]

    if include_rucio_local:
        rucio_local_frontend = straxen.RucioLocalFrontend(path=_rucio_local_path)
        st.storage += [rucio_local_frontend]

    # Only the online monitor backend for the DAQ
    if _database_init and (include_online_monitor or we_are_the_daq):
        st.storage += [
            straxen.OnlineMonitor(
                readonly=not we_are_the_daq,
                take_only=(
                    "veto_intervals",
                    "online_peak_monitor",
                    "event_basics",
                    "online_monitor_nv",
                    "online_monitor_mv",
                    "individual_peak_monitor",
                ),
            )
        ]

    # Remap the data if it is before channel swap (because of wrongly cabled
    # signal cable connectors) These are runs older than run 8797. Runs
    # newer than 8796 are not affected. See:
    # https://github.com/XENONnT/straxen/pull/166 and
    # https://xe1t-wiki.lngs.infn.it/doku.php?id=xenon:xenonnt:dsg:daq:sector_swap
    st.set_context_config(
        {
            "apply_data_function": (
                straxen.remap_old,
                straxen.check_loading_allowed,
            )
        }
    )
    if _context_config_overwrite is not None:
        warnings.warn(
            f"_context_config_overwrite is deprecated, please pass to context as kwargs",
            DeprecationWarning,
        )
        st.set_context_config(_context_config_overwrite)

    return st


def xenonnt_led(**kwargs):
    st = xenonnt_online(**kwargs)
    st.set_context_config(
        {
            "check_available": ("raw_records", "led_calibration"),
            "free_options": list(xnt_common_config.keys()),
        }
    )
    # Return a new context with only raw_records and led_calibration registered
    st = st.new_context(replace=True, config=st.config, storage=st.storage, **st.context_config)
    st.register(
        [
            straxen.DAQReader,
            straxen.LEDCalibration,
            straxen.nVETORecorder,
            straxen.nVETOPulseProcessing,
            straxen.nVETOHitlets,
            straxen.nVetoExtTimings,
        ]
    )
    st.set_config({"coincidence_level_recorder_nv": 1})
    return st


##
# XENON1T, see straxen/legacy
##


def demo():
    """Return strax context used in the straxen demo notebook."""
    return straxen.legacy.contexts_1t.demo()


def fake_daq():
    """Context for processing fake DAQ data in the current directory."""
    return straxen.legacy.contexts_1t.fake_daq()


def xenon1t_dali(output_folder="./strax_data", build_lowlevel=False, **kwargs):
    return straxen.legacy.contexts_1t.xenon1t_dali(
        output_folder=output_folder, build_lowlevel=build_lowlevel, **kwargs
    )


def xenon1t_led(**kwargs):
    return straxen.legacy.contexts_1t.xenon1t_led(**kwargs)
