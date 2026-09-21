# Memory Evolution Engine Implementation

This plan outlines the design of the `EvolutionEngine`, a new layer dedicated to analyzing memory metadata and determining the appropriate lifecycle action for each memory.

## Architectural Design

The engine will follow the **Strategy Pattern** to ensure high modularity, allowing different evaluation policies to be plugged in or swapped seamlessly.

### 1. New Enum: `EvolutionAction`
We will create an Enum representing the possible recommendations:
- `KEEP`: Do nothing, the memory is healthy.
- `MERGE`: The memory overlaps with others and should be consolidated.
- `PROMOTE`: The memory is frequently accessed and its `importance_score` should be increased.
- `ARCHIVE`: The memory hasn't been accessed recently but shouldn't be deleted.
- `DELETE`: The memory is stale, rarely accessed, or irrelevant.

### 2. New Interface: `EvolutionPolicy`
We will define an abstract base class `EvolutionPolicy` with a single method:
```python
def evaluate(self, memory: MemoryRecord) -> EvolutionAction:
```
This guarantees that any future policy (e.g., `TimeDecayPolicy`, `FrequencyPolicy`, or even an `LLMEvaluationPolicy`) will adhere to a consistent contract.

### 3. The `EvolutionEngine` Component
We will create the main `EvolutionEngine` class. It will:
- Accept a list of `EvolutionPolicy` strategies during initialization.
- Provide an `analyze_memories(memories: List[MemoryRecord])` method.
- Pass each memory through the policies and return a mapping/list of recommendations (e.g., `Dict[str, EvolutionAction]` mapping memory IDs to actions).

## File Structure
All of these components will be cleanly encapsulated within a new file:
- **[NEW]** `app/memory/evolution.py`

## Verification Plan
1. I will write a verification script to instantiate an `EvolutionEngine` with a basic default policy (e.g., a simple time/frequency heuristic).
2. I will pass mock `MemoryRecord` objects with varying metadata through the engine.
3. I will verify that the engine correctly outputs the expected `EvolutionAction` (like `PROMOTE` for high retrieval counts or `ARCHIVE` for old `last_accessed` dates) without mutating the actual data.

## Open Questions
> [!IMPORTANT]  
> Are there any specific mathematical thresholds you want for the initial default policy? For example, should a memory be recommended for `PROMOTE` if `retrieval_count > 10`? Or should I just implement a dummy/basic threshold policy for now to prove the architecture?
