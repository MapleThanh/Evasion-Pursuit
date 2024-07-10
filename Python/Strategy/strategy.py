class EvasionStrategy:
    @staticmethod
    def calculate_move(evader, pursuers, boundaries):
        raise NotImplementedError("Subclasses must implement calculate_move method")

class PursuitStrategy:
    @staticmethod
    def calculate_move(pursuer, evader, boundaries):
        raise NotImplementedError("Subclasses must implement calculate_move method")