from tqdm import tqdm

from ._experiment_session import ExperimentSession
from ._path import PureSequencePath
from ._return_or_raise import unwrap
from ._state import State


def copy_sequence(
    source_session: ExperimentSession,
    target_session: ExperimentSession,
    sequence_path: PureSequencePath,
) -> None:
    """Copy a sequence from one session to another.

    The two sessions must be activated and must be different.
    """

    created_paths = unwrap(target_session.paths.create_path(sequence_path))
    for path in created_paths:
        target_session.paths.update_creation_date(
            path, unwrap(source_session.paths.get_path_creation_date(sequence_path))
        )
    target_session.sequences.create(
        sequence_path,
        source_session.sequences.get_parameters(sequence_path),
        source_session.sequences.get_iteration_configuration(sequence_path),
        source_session.sequences.get_time_lanes(sequence_path),
    )
    state = unwrap(source_session.sequences.get_state(sequence_path))
    if not state.is_editable():
        target_session.sequences.set_state(sequence_path, State.PREPARING)
        device_configs = source_session.sequences.get_device_configurations(
            sequence_path
        )
        target_session.sequences.set_device_configurations(
            sequence_path, device_configs
        )
        target_session.sequences.set_state(sequence_path, State.RUNNING)
        shots = unwrap(source_session.sequences.get_shots(sequence_path))
        for shot in tqdm(shots, desc=f"Copying {sequence_path}"):
            target_session.sequences.create_shot(
                sequence_path,
                shot_index=shot.index,
                shot_parameters=shot.get_parameters(source_session),
                shot_data=shot.get_data(source_session),
                shot_start_time=shot.get_start_time(source_session),
                shot_end_time=shot.get_end_time(source_session),
            )
        target_session.sequences.set_state(sequence_path, state)
    stats = unwrap(source_session.sequences.get_stats(sequence_path))
    target_session.sequences.update_start_and_end_time(
        sequence_path, stats.start_time, stats.stop_time
    )
