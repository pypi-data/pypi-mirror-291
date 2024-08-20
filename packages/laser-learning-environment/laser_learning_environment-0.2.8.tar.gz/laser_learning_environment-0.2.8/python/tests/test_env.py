from typing import Any
from lle import LLE, Action, WorldState, ObservationType
from lle.envs.reward_strategy import REWARD_DEATH, REWARD_GEM, REWARD_EXIT, REWARD_DONE, RW_DEATH_IDX, RW_GEM_IDX, RW_EXIT_IDX, RW_DONE_IDX
from copy import deepcopy
import numpy as np


def test_available_actions():
    env = LLE.from_str(
        """
@ @ L0S @  @
@ .  .  .  @
@ X  .  S0 @
@ X  .  S1 @
@ @  @  @  @
"""
    ).build()
    env.reset()
    available_actions = env.available_actions()
    # Agent 0
    assert available_actions[0, Action.NORTH.value]
    assert not available_actions[0, Action.EAST.value]
    assert not available_actions[0, Action.SOUTH.value]
    assert available_actions[0, Action.WEST.value]
    assert available_actions[0, Action.STAY.value]

    # Agent 1
    assert not available_actions[1, Action.NORTH.value]
    assert not available_actions[1, Action.EAST.value]
    assert not available_actions[1, Action.SOUTH.value]
    assert available_actions[1, Action.WEST.value]
    assert available_actions[1, Action.STAY.value]


def test_available_actions2():
    env = LLE.from_str(
        """
@   @ @  @  @ @ @
@   . S0 S1 . . @
@   . .  .  . . @
L0E . .  .  . . @
@   . .  .  . G @
@   . X  X  . . @
@   @ @  @  @ @ @"""
    ).build()
    obs = env.reset()

    def check_available_actions(available: np.ndarray[np.int32, Any], expected_available: list[list[Action]]) -> bool:
        available_actions = np.full((2, Action.N), False, dtype=bool)
        for agent_id, actions in enumerate(expected_available):
            for action in actions:
                available_actions[agent_id, action.value] = True
        return np.array_equal(available, available_actions)

    assert check_available_actions(
        obs.available_actions, [[Action.SOUTH, Action.WEST, Action.STAY], [Action.SOUTH, Action.EAST, Action.STAY]]
    )

    # Move the agent to the end location and check the available actions
    for _ in range(3):
        obs, *_ = env.step([Action.SOUTH.value, Action.SOUTH.value])
        check_available_actions(
            obs.available_actions,
            [[Action.NORTH, Action.SOUTH, Action.WEST, Action.STAY], [Action.NORTH, Action.SOUTH, Action.EAST, Action.STAY]],
        )
    obs, *_ = env.step([Action.SOUTH.value, Action.SOUTH.value])
    check_available_actions(obs.available_actions, [[Action.STAY] * 2])


def test_width_height():
    env = LLE.from_str(
        """S0 X .
.  . .
.  . ."""
    ).build()
    assert env.width == 3
    assert env.height == 3

    env = LLE.from_str(
        """S0 X . .
.  . . .
G  . . ."""
    ).build()
    assert env.width == 4
    assert env.height == 3


def test_state_default():
    env = LLE.from_str(
        """S0 X .
                        .  . .
                        .  . ."""
    ).build()
    assert env.state_shape == (env.n_agents * 2 + env.world.n_gems,)
    env.reset()
    state = env.get_state()
    assert state.shape == env.state_shape


def test_state_flattened():
    env = (
        LLE.from_str(
            """S0 X .
.  . .
.  . .""",
        )
        .state_type(ObservationType.FLATTENED)
        .build()
    )
    assert env.state_shape == (np.prod(env.state_shape),)
    env.reset()
    state = env.get_state()
    assert state.shape == env.state_shape


def test_action_meanings():
    env = LLE.from_str(
        """S0 X .
.  . .
.  . ."""
    ).build()
    assert env.action_space.action_names == [a.name for a in Action.ALL]


def test_deep_copy():
    env = LLE.from_str("S0 X").build()
    copy = deepcopy(env)
    assert env is not copy

    env.reset()
    copy.reset()

    _, _, done, _, _ = env.step([Action.EAST.value])
    assert done
    # If the deepcopy is not correct, the copy should also be done and the game should crash
    # If the deepcopy is properly done, then the copy should not be done
    _, _, done, _, _ = copy.step([Action.STAY.value])
    assert not done


def test_move_end_game():
    env = LLE.from_str(
        """
    S0 X .
    .  . .
    .  . .""",
    ).build()
    env.reset()
    env.step([Action.SOUTH.value])
    assert not env.done
    env.step([Action.SOUTH.value])
    assert not env.done
    env.step([Action.EAST.value])
    assert not env.done
    env.step([Action.NORTH.value])
    assert not env.done
    env.step([Action.NORTH.value])
    assert env.done


def test_time_reward():
    env = LLE.from_str(
        """
    . .  . X
    . S0 . .
    . .  . ."""
    ).build()
    env.reset()
    for action in Action.ALL:
        _obs, reward, *_ = env.step([action.value])
        assert reward.item() == 0


def test_finish_reward():
    env = LLE.from_str(
        """@ @ @  @ @ @
@ . .  . . @
@ . S0 . . @
@ . .  X . @
@ @ @  @ @ @"""
    ).build()
    env.reset()
    env.step([Action.EAST.value])
    reward = env.step([Action.SOUTH.value])[1]
    assert reward.item() == REWARD_DONE + REWARD_EXIT


def test_arrive_reward_only_once():
    """Some kind of adversarial game where only one agent can move at a time."""
    env = LLE.from_str(
        """
    S0 . G
    S1 X X
""",
    ).build()
    action_rewards = [
        ([Action.EAST, Action.STAY], 0),  # Agent 0
        ([Action.STAY, Action.EAST], 1),  # Agent 1 finishes the game
        ([Action.STAY, Action.STAY], 0),  # Agent 0
        ([Action.STAY, Action.STAY], 0),  # Agent 1
        ([Action.EAST, Action.STAY], 1),  # Agent 0 collects the gem
        ([Action.STAY, Action.STAY], 0),  # Agent 1
        ([Action.SOUTH, Action.STAY], 2),  # Agent 0 finishes the game
    ]
    env.reset()
    for action, reward in action_rewards:
        r = env.step([a.value for a in action])[1]
        assert r.item() == reward


def test_void_reward():
    env = LLE.from_str("S0 V X").build()
    env.reset()
    assert env.step([Action.EAST.value])[1].item() == REWARD_DEATH
    assert env.done


def test_collect_reward():
    env = LLE.from_str(
        """S0 X . .
.  . . .
G  . . ."""
    ).build()
    env.reset()
    env.step([Action.SOUTH.value])
    reward = env.step([Action.SOUTH.value])[1]
    assert reward.item() == REWARD_GEM


def test_reward_after_reset():
    env = LLE.from_str(
        """
    S0 X . .
    .  . . .
    G  . . .
    """
    ).build()

    def play():
        """Collect the gem and finish the game. Check that the reward is is correct when collecting it."""
        env.reset()
        env.step([Action.SOUTH.value])
        reward = env.step([Action.SOUTH.value])[1].item()
        assert reward == REWARD_GEM
        assert not env.done
        r = env.step([Action.NORTH.value])[1].item()
        assert r == 0
        r = env.step([Action.NORTH.value])[1].item()
        assert r == 0
        reward = env.step([Action.EAST.value])[1].item()
        assert env.done
        assert reward == REWARD_DONE + REWARD_EXIT

    for _ in range(10):
        play()


def test_reward_after_set_state():
    """After forcing the state of the environment, make sure that
    the reward is correct, and does not include the reward of
    forcing the state."""
    env = LLE.from_str(
        """
    S0 . G
    S1 X X""",
    ).build()
    env.reset()
    state = WorldState([(0, 1), (1, 1)], [False])
    env.set_state(state)
    assert env.step([Action.EAST.value, Action.STAY.value])[1].item() == REWARD_GEM


def test_reward_set_state_all_arrived():
    env = LLE.from_str(
        """
    S0 . G
    S1 X X""",
    ).build()
    env.reset()
    state = WorldState([(0, 2), (1, 1)], [True])
    env.set_state(state)
    r = env.step([Action.SOUTH.value, Action.STAY.value])[1]
    assert r.item() == REWARD_DONE + REWARD_EXIT


def test_set_state():
    env = LLE.from_str("S0 G X").build()
    env.reset()
    env.step([Action.EAST.value])
    env.set_state(WorldState([(0, 0)], [False]))
    assert env.world.agents_positions == [(0, 0)]
    assert env.world.gems_collected == 0
    assert not env.done

    env.set_state(WorldState([(0, 2)], [True]))
    assert env.world.agents_positions == [(0, 2)]
    assert env.world.gems_collected == 1
    assert env.done


# Test cases
def test_reward():
    env = LLE.from_str(
        """
    S0 G .
    .  . X
    """
    ).build()
    env.reset()
    assert env.step([Action.EAST.value])[1].item() == REWARD_GEM
    assert env.step([Action.EAST.value])[1].item() == 0.0
    assert env.step([Action.SOUTH.value])[1].item() == REWARD_EXIT + REWARD_DONE


def test_reward_death():
    env = LLE.from_str(
        """
    S0 L0S X
    S1  .  X
    """
    ).build()
    env.reset()
    assert env.step([Action.STAY.value, Action.EAST.value])[1].item() == REWARD_DEATH
    assert env.done


def test_reward_collect_and_death():
    env = LLE.from_str(
        """
    S0 L0S X
    S1  G  X
    """
    ).build()
    env.reset()
    assert env.step([Action.STAY.value, Action.EAST.value])[1].item() == REWARD_DEATH
    assert env.done


def test_force_end_state():
    env = LLE.from_str(
        """
        S0 . G
        X  . .
    """,
    ).build()
    env.reset()
    s = WorldState([(1, 0)], [True])
    env.set_state(s)
    assert env.done


def test_force_state_agent_dies():
    env = LLE.from_str(
        """
        S0 S1 G
        X  X L0W
    """,
    ).build()
    env.reset()

    s = WorldState([(1, 0), (1, 1)], [False])
    env.set_state(s)
    assert env.done


def test_agent_state_size():
    env = LLE.level(1).build()
    assert env.agent_state_size == 2

    env = LLE.level(1).state_type(ObservationType.FLATTENED).build()
    try:
        env.agent_state_size
        assert False, "So far, only state generators of type `StateGenerator` have a `agent_state_size`."
    except (ValueError, NotImplementedError):
        pass


def test_multi_objective_rewards():
    env = (
        LLE.from_str(
            """
    S0 G .
    .  . X
    """,
        )
        .multi_objective()
        .build()
    )
    indices = [RW_GEM_IDX, RW_EXIT_IDX, RW_DONE_IDX, RW_DEATH_IDX]
    env.reset()
    # Collect the gem
    reward = env.step([Action.EAST.value])[1]
    assert reward[RW_GEM_IDX] == REWARD_GEM
    for idx in indices:
        if idx != RW_GEM_IDX:
            assert reward[idx] == 0

    # Step east
    assert np.all(env.step([Action.EAST.value])[1] == 0.0)
    # Finish the level
    _, reward, done, *_ = env.step([Action.SOUTH.value])
    assert done
    assert reward[RW_EXIT_IDX] == REWARD_EXIT
    assert reward[RW_DONE_IDX] == REWARD_DONE
    for idx in indices:
        if idx not in [RW_EXIT_IDX, RW_DONE_IDX]:
            assert reward[idx] == 0


def test_multi_objective_death():
    env = (
        LLE.from_str(
            """
    S0 L0S X
    S1  G  X
    """,
        )
        .multi_objective()
        .build()
    )
    env.reset()
    reward = env.step([Action.STAY.value, Action.EAST.value])[1]
    assert reward[RW_DEATH_IDX] == REWARD_DEATH
    for idx in [RW_GEM_IDX, RW_EXIT_IDX, RW_DONE_IDX]:
        assert reward[idx] == 0
