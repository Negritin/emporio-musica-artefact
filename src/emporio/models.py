"""Contratos pequenos entre classificação, ferramentas e interface."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Plan(BaseModel):
    model_config = ConfigDict(extra="forbid")
    route: Literal["catalog", "policies", "hybrid", "private", "outside", "clarify"]
    query: str = Field(default="", max_length=100)
    category: str = Field(default="", max_length=60)
    max_price: float | None = Field(default=None, ge=0, le=1000000)
    min_price: float | None = Field(default=None, ge=0, le=1000000)
    available_only: bool = True
    policy_query: str = Field(default="", max_length=500)
    clarification: str = Field(default="", max_length=300)


class Event(BaseModel):
    name: str
    status: Literal["ok", "erro", "bloqueado"] = "ok"
    duration_ms: float
    model: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    cost_usd: float | None = None
    error: str | None = None


class Turn(BaseModel):
    question: str
    answer: str
    events: list[Event] = Field(default_factory=list)
    sources: list[dict] = Field(default_factory=list)
    products: list[dict] = Field(default_factory=list)
    route: str = ""
    success: bool = True

    @property
    def known_cost_usd(self) -> float | None:
        costs = [e.cost_usd for e in self.events if e.cost_usd is not None]
        return sum(costs) if costs else None
