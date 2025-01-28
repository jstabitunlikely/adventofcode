import time
import re
from pathlib import Path
import copy
import logging
logger = logging.getLogger(__name__)


# Step 0. Set up some logging
my_name = Path(__file__).stem
logging.basicConfig(filename=f"{my_name}.log",
                    filemode="w",
                    level=logging.WARNING,
                    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
console = logging.StreamHandler()
logger.addHandler(console)
logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)


def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


class map_lib():

    def __init__(self, maps):
        sources = []
        for k, v in maps.items():
            map_name = k.split("-to-")
            assert len(
                map_name) == 2, "map name must be <source>-to-<destination>"
            assert map_name[0] not in sources, "there can be exatctly one map for each source"
            sources.append(map_name[0])
        self.maps = self.normalize(maps)

    def get_next_map(self, src2dst):
        """Return the key of the next map based on the key of the current map"""
        src = src2dst.split("-to-")[-1]
        next_map = [s for s in self.maps.keys() if s.startswith(src)]
        assert (len(next_map) < 2)
        return next_map

    def get_list_of_maps(self, src):
        """Return a list of maps to use, starting from the source"""
        list_of_maps = []
        next_map = self.get_next_map(src)
        while next_map:
            list_of_maps.append(next_map[0])
            next_map = self.get_next_map(next_map[0])
        logger.debug(f"List of maps to use: \n\t{list_of_maps}")
        return list_of_maps

    def get_destination(self, seed, start="seed", end="location"):
        assert "location" == end, "Endpoints other than location are not supported!"
        next_seed = seed
        list_of_maps = self.get_list_of_maps(start)
        assert list_of_maps[-1].split(
            "-to-")[1] == end, "Couldn't get to the final map!"
        for map in list_of_maps:
            logger.debug(f"{map} map:")
            for [offset, s0, s1] in self.maps[map]:
                # +1 to get an inclusive range
                if next_seed in range(s0, s1+1):
                    next_seed += offset
                    logger.debug(
                        f"\tinput: {seed} -> entry: {(offset,s0,s1)} -> output: {next_seed}")
                    break
            # Note: next_seed won"t be changed if there was no range found, as per spec
        logger.debug(f"{start}:{seed} => {end}:{next_seed}")
        return next_seed

    def get_destinations(self, seeds, start="seed", end="location"):
        return [self.get_destination(s, start, end) for s in seeds]

    def get_destination2(self, seed, start="seed", end="location"):
        assert "location" == end, \
            "Endpoints other than location are not supported!"
        # Assemble a chain of maps that takes us from <start> to <end>
        list_of_maps = self.get_list_of_maps(start)
        assert list_of_maps[-1].split("-to-")[1] == end, \
            "Couldn't get to the final map!"
        # We need to get the seeds through all the maps
        chunks_in = seed
        for map in list_of_maps:
            # The map might slice the seeds into smaller chunks for the next map
            chunks_out = []
            for [chi0, chi1] in chunks_in:
                # We have a list of map entries and a chunk that look e.g. like this:
                # map_ext[N]:                      mN.0        mN.1
                # map_ext[1]:             m1.0     m1.1          |
                # map_ext[0]:  m0.0       m0.1       |           |
                # map_ext   :    ||---------|--------|----------||
                # map       :               ||-------|----------||
                # chunk_in  :    |----------------------|
                #               chi0                   chi1
                # chunks_out:    |----------|--------|--|
                # We need an extended map in case the chunk starts/ends below/above of it
                map_ext = copy.deepcopy(self.maps[map])
                map_start = map_ext[0][1]
                map_end = map_ext[-1][2]
                # The chunk starts below the map, insert a dummy entry at the beginning
                if chi0 < map_start:
                    map_ext.insert(0, [0, chi0, map_start-1])
                # The chunk ends above the map, inserts a dummy entry at the end
                elif chi1 > map_end:
                    map_ext.append([0, map_end+1, chi1])
                # Keep all the map entries that overlap with the chunk
                map_ext = [m for m in map_ext if (m[1] <= chi1 and m[2] >= chi0)]
                # Tailor the first/last map entry to the chunk
                map_ext[0][1] = chi0
                map_ext[-1][2] = chi1
                # Finally, do the mapping by adding the offset from the map entry
                chunks_out += [[c0+o, c1+o] for [o, c0, c1] in map_ext]
            # Prepare for the next map
            chunks_in = chunks_out
        # We only need the smallest endpoint
        return min([s0 for [s0, s1] in chunks_in])

    def get_destinations2(self, seeds, start="seed", end="location"):
        return [self.get_destination2([s], "seed", "location") for s in seeds]

    def normalize(self, maps):
        """
        Original representation: [dst, src, range]
        Transform this into: [offset, s0, s1]
        This will make calculations simpler.
        Also, sorting the map based on s0, not important but might help debug.
        Also, fill the gaps so the maps are contigous.
        """
        for key, map in maps.items():
            for i, [dst, src, rng] in enumerate(map):
                map[i] = [dst-src, src, src+rng-1]
            map.sort(key=lambda c: c[1])
            gaps = []
            for i, [o, s0, s1] in enumerate(map[0:-1]):
                next_section_s0 = map[i+1][1]
                if s1 != next_section_s0-1:
                    gaps.append([0, s1+1, next_section_s0-1])
            map += gaps
            map.sort(key=lambda c: c[1])
        return maps


def main():
    ############################################################################
    logger.info("Day 5 - First puzzle")

    # Step 1. Get the puzzle input into an appropriate data structure
    seeds = []
    maps = {}
    with open("day5_input.txt", "r") as f:
        data = f.read()
        # Find the seeds with a regex
        m = re.search(r"seeds: ([0-9 ]+)", data)
        # Get the seeds as a list of integers
        seeds = [int(s) for s in m.group(1).split(" ")]
        logger.debug(f"Seeds: {seeds}")

        # Get all the maps with regex
        map_re = re.compile(r"(\S+) map:\n(((\d+) (\d+) (\d+)\n)+)")
        for name, map in [(m.group(1), m.group(2)) for m in map_re.finditer(data)]:
            # Split into lines
            map = map.split("\n")
            # Split lines into different numbers (plus remove any empty lines)
            map = [line.split(" ") for line in map if line]
            # Convert into integers
            map = [[int(n) for n in line] for line in map]
            maps.update({name: map})

    # Step 2. Solve the puzzle
    my_map_lib = map_lib(maps)
    locations = my_map_lib.get_destinations(seeds, "seed", "location")
    logger.info(f"\tAnswer 1: {min(locations)}")

    ############################################################################
    logger.info("Day 5 - Second puzzle")

    # Split seeds into list of lists: [first_seed, range]
    seeds = list(divide_chunks(seeds, 2))
    # Transform seeds into vectors with first and last coordinates: [first_seed, last_seed]
    for i, [s, rng] in enumerate(seeds):
        seeds[i] = [s, s+rng-1]

    st = time.process_time()
    locations = my_map_lib.get_destinations2(seeds, "seed", "location")
    et = time.process_time()
    logger.info(f"\tAnswer2: {min(locations)}")
    logger.info(f"CPU time: {(et-st)*1000.0}ms")


if __name__ == "__main__":
    main()
