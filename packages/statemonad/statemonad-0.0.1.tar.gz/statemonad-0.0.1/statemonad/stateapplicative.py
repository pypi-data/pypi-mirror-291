from abc import abstractmethod, ABC


class StateApplicative[State, U](ABC):
    """
    This mixin class provides an `apply` method for stateful computations. The `apply` method takes an initial state as input
    and returns a tuple containing an updated state and a result.
    """

    @abstractmethod
    def apply(self, state: State) -> tuple[State, U]:
        """
        Apply the stateful computation.

        Parameters:
            state: The initial state before the computation.

        Returns:
            A tuple (new_state, result):
                new_state: The state after the computation.
                result: The result of the computation.
        """
