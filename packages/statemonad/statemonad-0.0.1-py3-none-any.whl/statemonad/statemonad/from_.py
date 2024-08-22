from statemonad.statemonadtree.init import init_from
from statemonad.statemonad.statemonad import StateMonad
from statemonad.statemonad.init import init_state_monad


class from_[State]:
    """
    This function creates a constant state monad. It sets the return value to `value` 
    while leaving the state unchanged.
    """
    
    def __new__[U](_, value: U) -> StateMonad[State, U]:
        return init_state_monad(child=init_from(value=value))


class get[State]:
    def __new__(_) -> StateMonad[State, State]:
        return from_(None).get()
