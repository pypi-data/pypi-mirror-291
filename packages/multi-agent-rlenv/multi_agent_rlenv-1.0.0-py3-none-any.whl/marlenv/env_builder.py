from dataclasses import dataclass
from typing import Literal, Optional, TypeVar, Generic, overload


from .models import RLEnv, ActionSpace, DiscreteActionSpace
from . import wrappers

A = TypeVar("A", bound=ActionSpace, covariant=True)

try:
    from pettingzoo import ParallelEnv

    @overload
    def make(env: ParallelEnv) -> RLEnv[ActionSpace]: ...

    HAS_PETTINGZOO = True
except ImportError:
    HAS_PETTINGZOO = False


try:
    from gymnasium import Env

    @overload
    def make(env: Env) -> RLEnv[ActionSpace]: ...

    HAS_GYM = True
except ImportError:
    HAS_GYM = False

try:
    from smac.env import StarCraft2Env

    @overload
    def make(env: StarCraft2Env) -> RLEnv[DiscreteActionSpace]: ...

    HAS_SMAC = True
except ImportError:
    HAS_SMAC = False


@overload
def make(env: str) -> RLEnv[ActionSpace]:
    """
    Make an RLEnv from a string.

    Formats:
        - "smac:<map_name>" for SMAC environments
        - Any other string is assumed to be a Gymnasium environment (e.g. "CartPole-v1")
    """


@overload
def make(env: RLEnv[A]) -> RLEnv[A]:
    """Why would you do this ?"""


def make(env):
    """Make an RLEnv from str (Gym) or PettingZoo"""
    match env:
        case RLEnv():
            return env
        case str():
            import gymnasium
            from marlenv.adapters import Gym

            return Gym(gymnasium.make(env, render_mode="rgb_array"))

    try:
        from marlenv.adapters import PettingZoo

        if isinstance(env, ParallelEnv):
            return PettingZoo(env)
    except ImportError:
        pass
    try:
        from smac.env import StarCraft2Env
        from marlenv.adapters import SMAC

        if isinstance(env, StarCraft2Env):
            return SMAC(env)
    except ImportError:
        pass

    raise ValueError(f"Unknown environment type: {type(env)}")


@dataclass
class Builder(Generic[A]):
    """Builder for environments"""

    _env: RLEnv[A]

    def __init__(self, env: RLEnv[A]):
        self._env = env

    def time_limit(self, n_steps: int, add_extra: bool = False, truncation_penalty: Optional[float] = None):
        """
        Limits the number of time steps for an episode. When the number of steps is reached, then the episode is truncated.

        - If the `add_extra` flag is set to True, then an extra signal is added to the observation, which is the ratio of the
        current step over the maximum number of steps. In this case, the done flag is also set to True when the maximum
        number of steps is reached.
        - The `truncated` flag is only set to `True` when the maximum number of steps is reached and the episode is not done.
        - The `truncation_penalty` is subtracted from the reward when the episode is truncated. This is only possible when
        the `add_extra` flag is set to True, otherwise the agent is not able to anticipate this penalty.
        """
        self._env = wrappers.TimeLimit(self._env, n_steps, add_extra, truncation_penalty)
        return self

    def pad(self, to_pad: Literal["obs", "extra"], n: int):
        match to_pad:
            case "obs":
                self._env = wrappers.PadObservations(self._env, n)
            case "extra":
                self._env = wrappers.PadExtras(self._env, n)
            case other:
                raise ValueError(f"Unknown padding type: {other}")
        return self

    def agent_id(self):
        """Adds agent ID to the observations"""
        self._env = wrappers.AgentId(self._env)
        return self

    def last_action(self):
        """Adds the last action to the observations"""
        self._env = wrappers.LastAction(self._env)
        return self

    def centralised(self):
        """Centralises the observations and actions"""
        self._env = wrappers.Centralised(self._env)
        return self

    def record(
        self,
        folder: str,
        encoding: Literal["mp4", "avi"] = "mp4",
    ):
        """Add video recording of runs. Onnly records tests by default."""
        self._env = wrappers.VideoRecorder(self._env, folder, video_encoding=encoding)
        return self

    def available_actions(self):
        """Adds the available actions to the observations extras"""
        self._env = wrappers.AvailableActions(self._env)
        return self

    def blind(self, p: float):
        """Blinds the observations with probability p"""
        self._env = wrappers.Blind(self._env, p)
        return self

    def time_penalty(self, penalty: float):
        self._env = wrappers.TimePenalty(self._env, penalty)
        return self

    def build(self) -> RLEnv[A]:
        """Build and return the environment"""
        return self._env
