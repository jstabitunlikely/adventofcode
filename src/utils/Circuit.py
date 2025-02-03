from typing import Any
import networkx as nx


class Circuit:

    def __init__(self) -> None:
        self.graph = nx.DiGraph()
        self.input_signals: dict[str, Any] = {}

    def add_gate(self,
                 gate_type: str,
                 inputs: list[str],
                 output: str) -> None:
        match gate_type:
            case 'AND', 'OR', 'XOR':
                assert len(inputs) == 2
            case 'NOT':
                assert len(inputs) == 1
        self.graph.add_node(output, type=gate_type)
        for i in inputs:
            self.graph.add_edge(i, output)

    def do_topological_ordering(self):
        generations = list(nx.topological_generations(self.graph))
        for layer, nodes in enumerate(generations):
            for node in nodes:
                self.graph.nodes[node]["layer"] = layer

    def set_input_signals(self, signals: dict[str, Any]) -> None:
        for k, v in signals.items():
            signals[k] = int(v)
        self.input_signals = signals

    def set_input_vectors(self, vectors: dict[str, Any]) -> None:
        self.input_signals = {}
        for k, (vector, width) in vectors.items():
            for i in range(width-1, -1, -1):
                if i >= len(vector):
                    bit = '0'
                else:
                    bit = vector[::-1][i]
                self.input_signals[f'{k}{i:02d}'] = int(bit)

    def is_input(self, node):
        return self.graph.in_degree(node) == 0

    def is_xor(self, node):
        return self.graph.nodes[node]['type'] == 'XOR'

    def is_and(self, node):
        return self.graph.nodes[node]['type'] == 'AND'

    def is_or(self, node):
        return self.graph.nodes[node]['type'] == 'OR'

    def _evaluate(self,
                  signal: str,
                  evaluated: dict):
        if signal in evaluated:
            return evaluated[signal]

        if signal in self.input_signals:
            evaluated[signal] = self.input_signals[signal]
            return evaluated[signal]

        if signal not in self.graph:
            raise ValueError(f"Signal not in graph: {signal}")

        inputs = list(self.graph.predecessors(signal))
        input_values = [self._evaluate(i, evaluated) for i in inputs]

        gate_type = self.graph.nodes[signal]['type']
        match gate_type:
            case 'AND':
                evaluated[signal] = all(input_values)
            case 'OR':
                evaluated[signal] = any(input_values)
            case 'NOT':
                evaluated[signal] = not input_values[0]
            case 'XOR':
                evaluated[signal] = input_values[0] ^ input_values[1]
            case _:
                raise ValueError(f"Unknown gate type: {gate_type}")

        return evaluated[signal]

    def evaluate(self, signal: str) -> bool:
        evaluated: dict[str, bool] = {}
        return self._evaluate(signal, evaluated)

    def get_vector_width(self, prefix: str) -> int:
        width = 0
        while f'{prefix}{width:02d}' in self.graph:
            width += 1
        return width-1

    def evaluate_vector(self,
                        prefix: str) -> int:
        vector_width = self.get_vector_width(prefix)
        evaluated_bitvector: str = ''
        for i in range(vector_width):
            signal = f'{prefix}{i:02d}'
            evaluated_signal = self.evaluate(signal)
            assert evaluated_signal is not None
            evaluated_bitvector += str(int(evaluated_signal))
        evaluated_bitvector = evaluated_bitvector[::-1]
        return int(evaluated_bitvector, 2)

    def get_coi(self, signal: str) -> set[str]:
        ancestors = nx.ancestors(self.graph, signal) | {signal}
        return ancestors

    def swap_outputs(self,
                     output1: str,
                     output2: str) -> None:
        # Get the predecessors (inputs) of each output
        preds1 = list(self.graph.predecessors(output1))
        preds2 = list(self.graph.predecessors(output2))

        # Remove existing edges
        for pred in preds1:
            self.graph.remove_edge(pred, output1)
        for pred in preds2:
            self.graph.remove_edge(pred, output2)

        # Add new edges to swap the connections
        for pred in preds1:
            self.graph.add_edge(pred, output2)
        for pred in preds2:
            self.graph.add_edge(pred, output1)

        # Swap the gate types as well
        type1 = self.graph.nodes[output1]['type']
        type2 = self.graph.nodes[output2]['type']
        self.graph.nodes[output1]['type'] = type2
        self.graph.nodes[output2]['type'] = type1
