"""Track AI API costs to enforce budget limits."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class APICall:
    """Record of a single API call."""

    operation: str  # "synopsis" or "reflection"
    input_tokens: int
    output_tokens: int
    cost_usd: float


@dataclass
class CostTracker:
    """Track API costs per reflection generation session."""

    max_cost_usd: float = 0.04
    calls: List[APICall] = field(default_factory=list)

    # Anthropic Claude 3.5 Sonnet pricing (as of Nov 2025)
    # Input: $3.00 per million tokens
    # Output: $15.00 per million tokens
    INPUT_COST_PER_MILLION = 3.00
    OUTPUT_COST_PER_MILLION = 15.00

    def __post_init__(self):
        """Validate initialization parameters."""
        if self.max_cost_usd <= 0:
            raise ValueError("max_cost must be positive")

    @property
    def max_cost(self) -> float:
        """Get maximum cost limit (for compatibility)."""
        return self.max_cost_usd

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost in USD for given token counts.
        
        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            
        Returns:
            Cost in USD
            
        Raises:
            ValueError: If token counts are negative
        """
        if input_tokens < 0 or output_tokens < 0:
            raise ValueError("Token counts cannot be negative")
        
        input_cost = (input_tokens / 1_000_000) * self.INPUT_COST_PER_MILLION
        output_cost = (output_tokens / 1_000_000) * self.OUTPUT_COST_PER_MILLION
        return input_cost + output_cost

    def record_call(
        self, operation: str, input_tokens: int, output_tokens: int
    ) -> None:
        """Record an API call and check cost limit.
        
        Args:
            operation: Type of operation ("synopsis" or "reflection")
            input_tokens: Number of input tokens used
            output_tokens: Number of output tokens generated
            
        Raises:
            RuntimeError: If recording would exceed max cost
        """
        cost = self.calculate_cost(input_tokens, output_tokens)
        
        # Check if adding this would exceed limit
        total_with_new = self.total_cost + cost
        if total_with_new > self.max_cost_usd:
            raise RuntimeError(
                f"Cost limit exceeded: ${total_with_new:.4f} > ${self.max_cost_usd:.2f} "
                f"(current: ${self.total_cost:.4f}, new call: ${cost:.4f})"
            )
        
        call = APICall(
            operation=operation,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost
        )
        self.calls.append(call)

    @property
    def total_cost(self) -> float:
        """Calculate total cost of all recorded calls."""
        return sum(call.cost_usd for call in self.calls)

    @property
    def total_input_tokens(self) -> int:
        """Calculate total input tokens across all calls."""
        return sum(call.input_tokens for call in self.calls)

    @property
    def total_output_tokens(self) -> int:
        """Calculate total output tokens across all calls."""
        return sum(call.output_tokens for call in self.calls)

    @property
    def remaining_budget(self) -> float:
        """Calculate remaining budget in USD."""
        return self.max_cost_usd - self.total_cost

    def get_summary(self) -> dict:
        """Get summary of costs and token usage.
        
        Returns:
            Dictionary with cost summary including "total_cost" and "calls" keys
        """
        return {
            "total_calls": len(self.calls),
            "total_cost": self.total_cost,  # For compatibility
            "total_cost_usd": self.total_cost,
            "max_cost_usd": self.max_cost_usd,
            "remaining_budget_usd": self.remaining_budget,
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "calls": [
                {
                    "operation": call.operation,
                    "input_tokens": call.input_tokens,
                    "output_tokens": call.output_tokens,
                    "cost": call.cost_usd,  # For compatibility
                    "cost_usd": call.cost_usd,
                }
                for call in self.calls
            ],
        }
