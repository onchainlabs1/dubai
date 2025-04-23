"""Lightweight online regressor for occupancy prediction (numeric-only)."""

from typing import Dict
from river import linear_model, preprocessing


class OnlineOccupancyRegressor:
    """Regressor que aprende on-line ocupação entre 0 e 1.

    - Filtra features não numéricas (ex.: strings).
    - Usa StandardScaler + regressão linear do River.
    """

    def __init__(self):
        self.model = preprocessing.StandardScaler() | linear_model.LinearRegression()

    # --------------------------------------------------------------------- #
    # helpers
    # --------------------------------------------------------------------- #
    @staticmethod
    def _numeric_only(features: Dict) -> Dict[str, float]:
        """Remove chaves cujo valor não seja int ou float."""
        return {k: v for k, v in features.items() if isinstance(v, (int, float))}

    # --------------------------------------------------------------------- #
    # API pública
    # --------------------------------------------------------------------- #
    def predict(self, features: Dict) -> float:
        x = self._numeric_only(features)
        y_pred = self.model.predict_one(x) or 0.8          # fallback 80 % ocupação
        return max(0.0, min(1.0, y_pred))                  # clamp 0-1

    def learn(self, features: Dict, target: float) -> None:
        x = self._numeric_only(features)
        self.model.learn_one(x, target)