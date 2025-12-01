"""Unit tests for AI cost tracking."""

import pytest
from catholic_liturgy_tools.ai.cost_tracker import CostTracker


class TestCostTrackerCalculation:
    """Tests for token cost calculation."""
    
    def test_calculate_cost_claude_3_5_sonnet_pricing(self):
        """Test cost calculation uses correct Claude 3.5 Sonnet pricing."""
        tracker = CostTracker()
        
        # Pricing: $3.00/M input, $15.00/M output
        # 1000 input + 1000 output = (1000 * 3.00 / 1_000_000) + (1000 * 15.00 / 1_000_000)
        expected_cost = (1000 * 3.00 / 1_000_000) + (1000 * 15.00 / 1_000_000)
        actual_cost = tracker.calculate_cost(input_tokens=1000, output_tokens=1000)
        
        assert abs(actual_cost - expected_cost) < 0.0001  # Allow floating point tolerance
        
    def test_calculate_cost_zero_tokens(self):
        """Test that zero tokens results in zero cost."""
        tracker = CostTracker()
        
        cost = tracker.calculate_cost(input_tokens=0, output_tokens=0)
        
        assert cost == 0.0
        
    def test_calculate_cost_input_only(self):
        """Test cost calculation with only input tokens."""
        tracker = CostTracker()
        
        # 10000 input tokens * $3.00 / 1_000_000
        expected_cost = 10000 * 3.00 / 1_000_000
        actual_cost = tracker.calculate_cost(input_tokens=10000, output_tokens=0)
        
        assert abs(actual_cost - expected_cost) < 0.0001
        
    def test_calculate_cost_output_only(self):
        """Test cost calculation with only output tokens."""
        tracker = CostTracker()
        
        # 10000 output tokens * $15.00 / 1_000_000
        expected_cost = 10000 * 15.00 / 1_000_000
        actual_cost = tracker.calculate_cost(input_tokens=0, output_tokens=10000)
        
        assert abs(actual_cost - expected_cost) < 0.0001
        
    def test_calculate_cost_large_token_counts(self):
        """Test cost calculation with realistic token counts."""
        tracker = CostTracker()
        
        # Typical reflection: 2000 input + 600 output
        input_tokens = 2000
        output_tokens = 600
        expected_cost = (input_tokens * 3.00 / 1_000_000) + (output_tokens * 15.00 / 1_000_000)
        actual_cost = tracker.calculate_cost(input_tokens=input_tokens, output_tokens=output_tokens)
        
        assert abs(actual_cost - expected_cost) < 0.0001
        assert actual_cost < 0.04  # Should be well under $0.04 limit


class TestCostTrackerRecording:
    """Tests for recording API calls and tracking cumulative costs."""
    
    def test_record_call_single_operation(self):
        """Test recording a single API call."""
        tracker = CostTracker()
        
        tracker.record_call(operation="synopsis", input_tokens=500, output_tokens=50)
        
        summary = tracker.get_summary()
        assert summary["total_cost"] > 0
        assert len(summary["calls"]) == 1
        assert summary["calls"][0]["operation"] == "synopsis"
        
    def test_record_call_multiple_operations(self):
        """Test recording multiple API calls accumulates costs."""
        tracker = CostTracker()
        
        tracker.record_call(operation="synopsis", input_tokens=500, output_tokens=50)
        tracker.record_call(operation="synopsis", input_tokens=500, output_tokens=50)
        tracker.record_call(operation="reflection", input_tokens=2000, output_tokens=600)
        
        summary = tracker.get_summary()
        assert len(summary["calls"]) == 3
        assert summary["total_cost"] > 0
        
    def test_total_cost_property(self):
        """Test total_cost property returns cumulative cost."""
        tracker = CostTracker()
        
        tracker.record_call(operation="synopsis", input_tokens=500, output_tokens=50)
        cost_after_first = tracker.total_cost
        
        tracker.record_call(operation="reflection", input_tokens=2000, output_tokens=600)
        cost_after_second = tracker.total_cost
        
        assert cost_after_second > cost_after_first
        assert cost_after_second == tracker.get_summary()["total_cost"]
        
    def test_get_summary_structure(self):
        """Test get_summary returns correct structure."""
        tracker = CostTracker()
        tracker.record_call(operation="synopsis", input_tokens=500, output_tokens=50)
        
        summary = tracker.get_summary()
        
        assert "total_cost" in summary
        assert "calls" in summary
        assert isinstance(summary["calls"], list)
        assert len(summary["calls"]) > 0
        assert "operation" in summary["calls"][0]
        assert "input_tokens" in summary["calls"][0]
        assert "output_tokens" in summary["calls"][0]
        assert "cost" in summary["calls"][0]


class TestCostTrackerLimitEnforcement:
    """Tests for $0.04 cost limit enforcement."""
    
    def test_default_max_cost_is_0_04(self):
        """Test that default maximum cost is $0.04."""
        tracker = CostTracker()
        
        assert tracker.max_cost == 0.04
        
    def test_custom_max_cost(self):
        """Test that custom maximum cost can be set."""
        tracker = CostTracker(max_cost_usd=0.10)
        
        assert tracker.max_cost == 0.10
        
    def test_record_call_under_limit_succeeds(self):
        """Test that calls under cost limit succeed."""
        tracker = CostTracker(max_cost_usd=0.04)
        
        # Small synopsis: ~$0.002
        tracker.record_call(operation="synopsis", input_tokens=500, output_tokens=50)
        
        # Should not raise exception
        assert tracker.total_cost < 0.04
        
    def test_record_call_at_limit_succeeds(self):
        """Test that calls at or just under limit succeed."""
        tracker = CostTracker(max_cost_usd=0.04)
        
        # Calculate tokens to reach just under $0.04
        # Cost = (input * 3 + output * 15) / 1_000_000
        # Using 1000 input, 2500 output: (1000*3 + 2500*15)/1_000_000 = 0.0405
        # Using 1000 input, 2400 output: (1000*3 + 2400*15)/1_000_000 = 0.039
        tracker.record_call(operation="test", input_tokens=1000, output_tokens=2400)
        
        # Should succeed since under limit
        assert tracker.total_cost < 0.04
        
    def test_record_call_exceeding_limit_raises_error(self):
        """Test that calls exceeding cost limit raise RuntimeError."""
        tracker = CostTracker(max_cost_usd=0.01)  # Very low limit
        
        with pytest.raises(RuntimeError, match="Cost limit exceeded"):
            # Large reflection: ~$0.015
            tracker.record_call(operation="reflection", input_tokens=2000, output_tokens=600)
            
    def test_cumulative_cost_exceeding_limit_raises_error(self):
        """Test that cumulative costs exceeding limit raise RuntimeError."""
        tracker = CostTracker(max_cost_usd=0.04)
        
        # First call: OK
        tracker.record_call(operation="synopsis", input_tokens=1000, output_tokens=100)
        
        # Second call: OK
        tracker.record_call(operation="synopsis", input_tokens=1000, output_tokens=100)
        
        # Third call: Should push over $0.04 limit
        with pytest.raises(RuntimeError, match="Cost limit exceeded"):
            tracker.record_call(operation="reflection", input_tokens=5000, output_tokens=3000)
            
    def test_error_message_includes_cost_details(self):
        """Test that cost limit error includes helpful details."""
        tracker = CostTracker(max_cost_usd=0.01)
        
        try:
            tracker.record_call(operation="reflection", input_tokens=2000, output_tokens=600)
            pytest.fail("Expected RuntimeError to be raised")
        except RuntimeError as e:
            error_message = str(e)
            assert "0.01" in error_message  # Max cost
            assert "$" in error_message  # Currency symbol


class TestCostTrackerEdgeCases:
    """Tests for edge cases and error handling."""
    
    def test_negative_tokens_raises_error(self):
        """Test that negative token counts raise ValueError."""
        tracker = CostTracker()
        
        with pytest.raises(ValueError):
            tracker.calculate_cost(input_tokens=-100, output_tokens=100)
            
    def test_negative_max_cost_raises_error(self):
        """Test that negative max cost raises ValueError."""
        with pytest.raises(ValueError):
            CostTracker(max_cost_usd=-0.01)
            
    def test_zero_max_cost_raises_error(self):
        """Test that zero max cost raises ValueError."""
        with pytest.raises(ValueError):
            CostTracker(max_cost_usd=0.0)
            
    def test_empty_tracker_has_zero_cost(self):
        """Test that new tracker has zero total cost."""
        tracker = CostTracker()
        
        assert tracker.total_cost == 0.0
        
    def test_empty_tracker_has_empty_calls_list(self):
        """Test that new tracker has empty calls list."""
        tracker = CostTracker()
        
        summary = tracker.get_summary()
        assert summary["calls"] == []
        assert summary["total_cost"] == 0.0
