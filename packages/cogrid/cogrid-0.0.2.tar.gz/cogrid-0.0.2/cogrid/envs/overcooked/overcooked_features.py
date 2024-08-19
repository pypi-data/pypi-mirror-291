import collections

from cogrid.feature_space import feature
from cogrid.feature_space import features
from cogrid.feature_space import feature_space
from cogrid.core import grid_utils
from cogrid import cogrid_env
from cogrid.core import grid_object
from cogrid.envs.overcooked import overcooked_grid_objects
import numpy as np


def euclidian_distance(pos_1: tuple[int, int], pos_2: tuple[int, int]) -> int:
    """Calculate the euclidian distance between two points.

    :param pos_1: The first point on the grid.
    :type pos_1: tuple[int, int]
    :param pos_2: The second point on the grid.
    :type pos_2: tuple[int, int]
    :return: The euclidian distance between the two points.
    :rtype: int
    """
    return np.sqrt((pos_1[0] - pos_2[0]) ** 2 + (pos_1[1] - pos_2[1]) ** 2)


class OvercookedCollectedFeatures(feature.Feature):
    """
    A wrapper class to create all overcooked features as a single array.

    For each agent j, calculate:

        - Agent j Direction
        - Agent j Inventory
        - Agent j Adjacent to Counter
        - Agent j Dist to closest {onion, plate, platestack, onionstack, onionsoup, deliveryzone}
        - Agent j Pot Features
            - pot_j_reachable: {0, 1}
            - pot_j_status: onehot of {empty | full | is_cooking | is_ready}
            - pot_j_contents: integer of the number of onions in the pot
            - pot_j_cooking_timer: integer for the number of ts remaining if cooking, 0 if finished, -1 if not cooking
            - pot_j_distance: (dy, dx) from the player's location
            - pot_j_location: (row, column) of the pot on the grid
        - Agent j Distance to other agents j != i
        - Agent j Position

    The observation is the concatenation of all these features for all players.
    """

    def __init__(self, env: cogrid_env.CoGridEnv, **kwargs):
        # num_pots = np.sum(
        #     [
        #         int(isinstance(grid_obj, overcooked_grid_objects.Pot))
        #         for grid_obj in env.grid.grid
        #     ]
        # )

        num_agents = 2
        max_num_pots = 2

        self.features = [
            features.AgentDir(),
            OvercookedInventory(),
            NextToCounter(),
            ClosestObj(focal_object_type=overcooked_grid_objects.Onion),
            ClosestObj(focal_object_type=overcooked_grid_objects.Plate),
            ClosestObj(focal_object_type=overcooked_grid_objects.PlateStack),
            ClosestObj(focal_object_type=overcooked_grid_objects.OnionStack),
            ClosestObj(focal_object_type=overcooked_grid_objects.OnionSoup),
            ClosestObj(focal_object_type=overcooked_grid_objects.DeliveryZone),
            ClosestObj(focal_object_type=grid_object.Counter),
            OrderedPotFeatures(num_pots=max_num_pots),
            DistToOtherPlayers(num_other_players=num_agents - 1),
            features.AgentPosition(),
            LayoutID(),
        ]

        full_shape = num_agents * np.sum(
            [feature.shape for feature in self.features]
        )

        super().__init__(
            low=-np.inf,
            high=np.inf,
            shape=(full_shape,),
            name="overcooked_features",
            **kwargs,
        )

    def generate(
        self, env: cogrid_env.CoGridEnv, player_id, **kwargs
    ) -> np.ndarray:
        player_encodings = [self.generate_player_encoding(env, player_id)]

        for pid in env.agent_ids:
            if pid == player_id:
                continue
            player_encodings.append(self.generate_player_encoding(env, pid))

        encoding = np.hstack(player_encodings).astype(np.float32)
        assert np.array_equal(self.shape, encoding.shape)

        return encoding

    def generate_player_encoding(
        self, env: cogrid_env.CoGridEnv, player_id: str | int
    ) -> np.ndarray:
        encoded_features = []
        for feature in self.features:
            encoded_features.append(feature.generate(env, player_id))

        return np.hstack(encoded_features)


feature_space.register_feature(
    "overcooked_features", OvercookedCollectedFeatures
)


class LayoutID(feature.Feature):
    shape = (5,)

    def __init__(self, **kwargs):
        super().__init__(low=0, high=1, name="layout_id", **kwargs)
        self.overcooked_layouts = [
            "overcooked_cramped_room_v0",
            "overcooked_asymmetric_advantages_v0",
            "overcooked_coordination_ring_v0",
            "overcooked_forced_coordination_v0",
            "overcooked_counter_circuit_v0",
        ]

    def generate(self, env: cogrid_env.CoGridEnv, player_id, **kwargs):
        encoding = np.zeros(self.shape, dtype=np.int32)
        encoding[self.overcooked_layouts.index(env.current_layout_id)] = 1
        assert np.array_equal(self.shape, encoding.shape)
        return encoding


class OvercookedInventory(feature.Feature):
    shape = (3,)

    def __init__(self, **kwargs):
        super().__init__(low=0, high=1, name="overcooked_inventory", **kwargs)

    def generate(self, env: cogrid_env.CoGridEnv, player_id, **kwargs):
        encoding = np.zeros(self.shape, dtype=np.int32)
        agent = env.grid.grid_agents[player_id]

        if not agent.inventory:
            return encoding

        objs = [
            overcooked_grid_objects.Onion,
            overcooked_grid_objects.OnionSoup,
            overcooked_grid_objects.Plate,
        ]
        encoding[objs.index(type(agent.inventory[0]))] = 1
        assert np.array_equal(self.shape, encoding.shape)
        return encoding


class NextToCounter(feature.Feature):
    """A feature that represents a multi-hot encoding of whether or not there is a counter
    immediately in each of the four cardinal directions.

    For example, let '#' be the counter and '@' be the player. The following situation
        ####
        #  #
        # @#
        ####

    would result in the feature [0, 1, 1, 0], corresponding to having a counter
    immediately to the east and south, but not north and west.
    """

    shape = (4,)

    def __init__(self, **kwargs):
        super().__init__(low=0, high=1, name="next_to_counter", **kwargs)

    def generate(self, env: cogrid_env.CoGridEnv, player_id, **kwargs):
        encoding = np.zeros((4,), dtype=np.int32)
        agent = env.grid.grid_agents[player_id]

        for i, (row, col) in enumerate(
            grid_utils.adjacent_positions(*agent.pos)
        ):
            adj_cell = env.grid.get(row, col)
            if isinstance(adj_cell, grid_object.Counter):
                encoding[i] = 1

        assert np.array_equal(self.shape, encoding.shape)
        return encoding


class ClosestObj(feature.Feature):
    """
    This feature calculates (dy, dx) to the closest instance of a specified object.

    # TODO(chase): Use BFS here, right now we're just doing (agent_y - pos_y, agent_x - pos_x)!
    It uses BFS to calculate a path from the player's position to the target, if
    there is no possible path, returns (-1, -1).

    If the object is in the inventory of the player, it returns (0, 0).
    """

    shape = (2,)

    def __init__(self, focal_object_type: grid_object.GridObj, **kwargs):
        super().__init__(
            low=-1,
            high=np.inf,
            name=f"closest_{focal_object_type.object_id}_dist",
            **kwargs,
        )
        self.focal_object_type = focal_object_type

    def generate(self, env: cogrid_env.CoGridEnv, player_id, **kwargs):
        agent = env.grid.grid_agents[player_id]

        # If the agent is holding the specified item, return (0, 0)
        if agent.inventory and any(
            [
                isinstance(held_obj, self.focal_object_type)
                for held_obj in agent.inventory
            ]
        ):
            return np.zeros(self.shape, dtype=np.int32)

        # collect the distances
        distances: list[tuple[int, int]] = []
        euc_distances: list[float] = []
        for grid_obj in env.grid.grid:
            if isinstance(grid_obj, self.focal_object_type):
                distances.append(np.array(agent.pos) - np.array(grid_obj.pos))
                euc_distances.append(
                    euclidian_distance(agent.pos, grid_obj.pos)
                )

        # if there were no instances of that object, return (-1, -1)
        if not distances:
            return np.array([-1, -1], dtype=np.int32)

        # find the closest instance and return that array
        min_dist_idx = np.argmin(euc_distances)
        encoding = np.asarray(distances[min_dist_idx], dtype=np.int32)
        assert np.array_equal(self.shape, encoding.shape)

        return encoding


class OrderedPotFeatures(feature.Feature):
    """Encode features related to the pot. Note that this assumes the number of pots is fixed,
    otherwise the feature size will vary and will cause errors. For each pot, calculate:
        - pot_j_reachable: {0, 1}  # TODO(chase): use BFS to calculate this, currently fixed at 1.
        - pot_j_status: onehot of {empty | full | is_cooking | is_ready}
        - pot_j_contents: integer of the number of onions in the pot
        - pot_j_cooking_timer: integer for the number of ts remaining if cooking, 0 if finished, -1 if not cooking
        - pot_j_distance: (dy, dx) from the player's location
        - pot_j_location: (row, column) of the pot on the grid

    We will sort based on the euclidian distance to the player's location and then concatenate all pot features.
    """

    def __init__(self, num_pots=1, **kwargs):
        super().__init__(
            low=-np.inf,
            high=np.inf,
            shape=(num_pots * 11,),
            name="pot_features",
            **kwargs,
        )

    def generate(self, env: cogrid_env.CoGridEnv, player_id, **kwargs):
        pot_feature_dict = {}
        agent = env.grid.grid_agents[player_id]
        count = 0
        pot_features = np.zeros(self.shape, dtype=np.float32)
        for grid_obj in env.grid.grid:
            if not isinstance(grid_obj, overcooked_grid_objects.Pot):
                continue
            count += 1

            # Encode if the pot is reachable (size 1)
            pot_reachable = [1]  # TODO(chase): use search to determine

            # Encode if the pot is empty, cooking, or ready (size 4)
            pot_status = np.zeros(
                (4,), dtype=np.int32
            )  # empty, cooking, ready, ptr
            if grid_obj.dish_ready:
                pot_status[0] = 1
            elif len(grid_obj.objects_in_pot) == 0:
                pot_status[1] = 1
            elif len(grid_obj.objects_in_pot) == grid_obj.capacity:
                pot_status[2] = 1
            else:
                pot_status[3] = 1

            # Encode the number of each legal content in the pot (size legal_contents)
            pot_contents = np.zeros((len(grid_obj.legal_contents),))
            item_types_in_pot = [
                grid_obj.legal_contents.index(type(pot_content_obj))
                for pot_content_obj in grid_obj.objects_in_pot
            ]
            for obj_index, obj_count in collections.Counter(
                item_types_in_pot
            ).items():
                pot_contents[obj_index] = obj_count

            # Encode cooking time (size 1)
            pot_cooking_time = np.array(
                (grid_obj.cooking_timer if grid_obj.is_cooking else -1,),
                dtype=np.int32,
            )

            # encode the distance from agent to pot (size 2)
            pot_distance = np.asarray(agent.pos) - np.asarray(grid_obj.pos)

            # encode the pot location (size 2)
            pot_location = np.asarray(grid_obj.pos)

            # concatenate all features and store distance
            euc_dist = euclidian_distance(agent.pos, grid_obj.pos)

            pot_features = np.hstack(
                [
                    pot_reachable,
                    pot_status,
                    pot_contents,
                    pot_cooking_time,
                    pot_distance,
                    pot_location,
                ]
            )
            pot_feature_dict[grid_obj.uuid] = (euc_dist, pot_features)

        # sort based on euclidian distance
        # 1 indexes the value, 0 the euc_distance from above
        pot_feature_dict = dict(
            sorted(pot_feature_dict.items(), key=lambda item: item[1][0])
        )

        pot_feature_values = [v[1] for v in pot_feature_dict.values()]
        encoding = np.hstack(pot_feature_values)

        padded_encoding = np.zeros(self.shape, dtype=np.float32)
        padded_encoding[: len(encoding)] = encoding

        return padded_encoding


class DistToOtherPlayers(feature.Feature):
    """Return an encoding of the distance to all other players, unsorted."""

    def __init__(self, num_other_agents=1, **kwargs):
        super().__init__(
            low=1,
            high=np.inf,
            shape=(num_other_agents * 2,),
            name="dist_to_other_players",
            **kwargs,
        )
        self.num_other_agents = num_other_agents

    def generate(self, env: cogrid_env.CoGridEnv, player_id, **kwargs):
        encoding = np.zeros((2 * (self.num_other_agents),), dtype=np.int32)
        agent = env.grid.grid_agents[player_id]

        other_agent_nums = 0
        for pid, other_agent in env.grid.grid_agents.items():
            if pid == player_id:
                continue

            encoding[other_agent_nums * 2 : other_agent_nums * 2 + 2] = (
                np.asarray(agent.pos) - np.asarray(other_agent.pos)
            )
        other_agent_nums += 1

        assert np.array_equal(self.shape, encoding.shape), (
            "DistToOtherPlayers shape is off. You likely are using an environment with > 2 "
            "agents, in which case you should change the feature encoding."
        )
        return encoding
