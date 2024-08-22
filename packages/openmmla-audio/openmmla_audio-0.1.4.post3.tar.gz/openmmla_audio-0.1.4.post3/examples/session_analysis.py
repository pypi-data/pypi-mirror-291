"""This script demonstrates how to perform session analysis based on audio measurement data."""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))

from openmmla_audio.utils.analyze_utils import session_analysis_audio
from openmmla_audio.utils.influx_client import InfluxDBClientWrapper
from openmmla_audio.utils.input_utils import get_bucket_name

project_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')
config_path = os.path.join(project_dir, 'conf/audio_base.ini')
influx_client = InfluxDBClientWrapper(config_path)
bucket_name = get_bucket_name(influx_client)
session_analysis_audio(project_dir, bucket_name, influx_client)
