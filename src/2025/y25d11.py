from Day import Day
import networkx as nx
import matplotlib.pyplot as plt


class y25d11(Day):

    def __init__(self,
                 auto_fetch: bool = True,
                 auto_parse: bool = True) -> None:
        super().__init__(year='2025', day='11', auto_fetch=auto_fetch, auto_parse=auto_parse)

    def parse_puzzle(self) -> None:
        super().parse_puzzle()
        self.puzzle = []
        for device in self.puzzle_raw.strip().split('\n'):
            device_id, device_connections = device.split(':')
            self.puzzle.append((device_id, device_connections.split()))

    def solve_part_1(self) -> int:
        network = nx.DiGraph()
        for dev_id, dev_conn in self.puzzle:
            for o in dev_conn:
                network.add_edge(dev_id, o)
        nof_paths = len(list(nx.all_simple_paths(network, 'you', 'out')))
        return nof_paths

    def solve_part_2(self) -> int:
        network = nx.DiGraph()
        for dev_id, dev_conn in self.puzzle:
            for o in dev_conn:
                network.add_edge(dev_id, o)

        self.do_topological_ordering(network)
        # self.visualize(network)

        try:
            print("SVR-DAC-FFT-OUT")
            print("\tSVR-DAC")
            nof_paths_svr_dac = len(list(nx.shortest_simple_paths(network, 'svr', 'dac')))
            print("\tDAC-FFT")
            nof_paths_dac_fft = len(list(nx.shortest_simple_paths(network, 'dac', 'fft')))
            print("\tFFT-OUT")
            nof_paths_fft_out = len(list(nx.shortest_simple_paths(network, 'fft', 'out')))
        except nx.NetworkXNoPath:
            nof_paths_svr_dac = 0
            nof_paths_dac_fft = 0
            nof_paths_fft_out = 0

        try:
            print("SVR-FFT-DAC-OUT")
            print("\tSVR-FFT")
            nof_paths_svr_fft = len(list(nx.shortest_simple_paths(network, 'svr', 'fft')))
            print("\tFFT-DAC")
            nof_paths_fft_dac = len(list(nx.shortest_simple_paths(network, 'fft', 'dac')))
            print("\tDAC-OUT")
            nof_paths_dac_out = len(list(nx.shortest_simple_paths(network, 'dac', 'out')))
        except nx.NetworkXNoPath:
            nof_paths_svr_fft = 0
            nof_paths_fft_dac = 0
            nof_paths_dac_out = 0

        nof_paths_svr_dac_fft_out = nof_paths_svr_dac * nof_paths_dac_fft * nof_paths_fft_out
        nof_paths_svr_fft_dac_out = nof_paths_svr_fft * nof_paths_fft_dac * nof_paths_dac_out
        nof_paths_total = nof_paths_svr_dac_fft_out + nof_paths_svr_fft_dac_out
        return nof_paths_total

    def do_topological_ordering(self, dag: nx.DiGraph) -> None:
        generations = list(nx.topological_generations(dag))
        for layer, nodes in enumerate(generations):
            for node in nodes:
                dag.nodes[node]['label'] = node
                dag.nodes[node]['layer'] = layer

    def visualize(self, dag: nx.DiGraph) -> None:
        pos = nx.multipartite_layout(dag, subset_key="layer", align="horizontal")
        fig, ax = plt.subplots()
        fig.set_figheight(6)
        fig.set_figwidth(12)
        nx.draw_networkx_nodes(G=dag, pos=pos, ax=ax, node_shape="s", node_size=400)
        nx.draw_networkx_edges(G=dag, pos=pos, ax=ax, node_shape="s", node_size=400)
        node_labels = dict(dag.nodes(data='label'))  # type:ignore
        nx.draw_networkx_labels(G=dag, pos=pos, ax=ax, font_size=8, labels=node_labels)
        dag.nodes()
        plt.show()


def main() -> dict[str, int]:  # pragma: no cover
    today = y25d11()
    today.solve()
    return today.answer


if __name__ == "__main__":  # pragma: no cover
    answer = main()
    print(f'Part 1: {answer['part_1']}')
    print(f'Part 2: {answer['part_2']}')
