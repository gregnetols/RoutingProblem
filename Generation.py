import random
import numpy as np


class Generation(object):
    def __init__(self, size, routes, origin, network):
        '''
        Initializes a generation of a set size of solutions with a set number routes that all start and end at the origin specified
        Param size: The size of a generation
        Param routes: The total number of routes in a solution
        Param origin: The origin which all routes start and end at
        Param Network: A network object that contains a list of nodes
        '''
        self.size = size
        self.routes = routes
        self.origin = origin
        self.network = network
        self.solution_list = []

        for i in range(0, size):
            random_solution = Solution(self.routes, self.origin, self.network)
            self.solution_list.append(random_solution)


    def generation_average_score(self):
        '''
        Calculates the average score for all the solutions in a generations
        Returns: Average score for the solutions in a generation
        '''
        return np.mean([solution.score for solution in self.solution_list])


    def remove_weakest_half(self):
        '''
        Sorts the solutions in solution_list and then removes the weakest half
        '''
        sorted_solutions = sorted(self.solution_list, key=lambda x: x.score)
        self.solution_list = sorted_solutions[:len(sorted_solutions)//2]


    def generation_step(self, mutation_chance):
        '''
        Mate each solution with a random solution that is not itself
        Mutate the child solutions generated from the mate step
        Param muataion_chance: The probability which each node in the child solution experiences a mutation
        '''
        child_solution_list = []

        for parent_a in self.solution_list:
            parent_a_splices = []
            child_route_list = []

            # Each solution will mate once with a random solution that is not itself
            other_solutions = [other_solution for other_solution in self.solution_list if other_solution != parent_a]
            parent_b = random.choice(other_solutions)

            # Create random splices in parent_a
            for parent_a_route in parent_a.route_list:
                parent_a_splices.append(random_route_splice(parent_a_route))

            # combine all nodes from random splices into a single list
            random_splice_nodes = [node for route in parent_a_splices for node in route]

            # remove nodes from parent b that are in the random splices from parent a.
            # Then cut parent b in half and insert the parent a splice in betweeen the two halves
            for parent_b_route, parent_a_splice in zip(parent_b.route_list, parent_a_splices):
                parent_b_route_extra_nodes =  [ node for node in parent_b_route if node not in random_splice_nodes + [self.origin]]

                cut = random.randint(0, len(parent_b_route_extra_nodes))
                parent_b_left = parent_b_route_extra_nodes[:cut]
                parent_b_right = parent_b_route_extra_nodes[cut:]

                child_route = [self.origin] + parent_b_left + parent_a_splice + parent_b_right + [self.origin]
                child_route_list.append(child_route)

            # Create a child solution with the child route that resulted from mating parent_a with parent_b
            child_solution = Solution(self.routes, self.origin, self.network, child_route_list)

            # Mutate the child solution
            child_solution.mutate(mutation_chance)

            child_solution_list.append(child_solution)

        self.solution_list = self.solution_list + child_solution_list



    def get_best_solution(self):
        '''
        Finds the first solution with the minimum score
        Retruns: A solution object that has the minimum score
        '''
        min_distance = 9999999
        for solution in self.solution_list:
            if solution.score < min_distance:
                min_distance = solution.score

        for solution in self.solution_list:
            if solution.score == min_distance:
                return solution


class Solution(object):
    def __init__(self, routes, origin, network, route_list=None):
        '''
        Initalizes a solution to the routing problem. If no route_list is provided initalize random routes
        Param - routes: The total number of routes that are in a solution
        Param - origin: The index of a node that all routes must begin and end at
        Param - network: A network object that contains a list of all nodes
        Param - route_list: A set of routes that a solution will be initalized with
        '''
        self.routes = routes
        self.origin = origin
        self.distance_matrix = network.distance_matrix

        # Initalize route_list if set values where not passed in
        if route_list == None:
            self.route_list = [ [] for i in range(0,routes) ]

            # From the available nodes construct a list of node indexes that do not contain the origin
            available_nodes = [node.index for node in network.node_list if node.index != origin]
            random.shuffle(available_nodes)

            # Start each route list with the origin
            for route in self.route_list:
                route.append(origin)

            # Pop a node from available_nodes and add it the a random routes
            while(len(available_nodes)) > 0:
                random_route = random.choice(self.route_list)
                random_route.append(available_nodes.pop())

            # End each route with the origin
            for route in self.route_list:
                route.append(origin)
        else:
            self.route_list = route_list

        self.score_solution()

    def score_solution(self):
        '''
        Scores a solution based on the sum of distances traveled between all nodes
        '''
        score = 0

        for route in self.route_list:
            for i in range(0, len(route)-1):
                node_a, node_b =  route[i:i+2]
                score = score + self.distance_matrix[(node_a, node_b)]

        self.score = score

    def mutate(self, mutation_chance):
        '''
        Swaps a node with a random node in a solution from any route with proability mutation mutation_chance
        Param muataion_chance: The probability a mutation occurs for each node
        '''
        for route in self.route_list:
            if len(route[1:-1]) > 0:
                for idx, node_id in enumerate(route[1:-1]):
                    if random.random() < mutation_chance:
                        node_a_idx = idx + 1

                        random_route = random.choice(self.route_list)
                        node_b_idx = random.randint(0, len(random_route[1:-1])-1) + 1

                        route[node_a_idx], random_route[node_b_idx] = random_route[node_b_idx], route[node_a_idx]


    def valid_solution(self):
        '''
        Evaluates if a solution is a valid solution
        Returns: Boolean True - valid solution, False - invalid solution
        '''
        all_nodes = []

        for route in self.route_list:
            # Check route ends and begins at origin
            if route[:1] != [self.origin] or route[-1:] != [self.origin]:
                print("A route exists that does not start or end with the origin: ", route)
                return False

            for node in route:
                if node != self.origin:
                    all_nodes.append(node)

        if len(all_nodes) > len(set(all_nodes)):
            print("There exists a node in the solution that is traveled to more than once")
            return False

        return True


def random_route_splice(list):
    route_no_origin = list[1:-1]

    start_index = random.randint(0, len(route_no_origin)-1)
    end_index = random.randint(start_index + 1, len(route_no_origin))

    return route_no_origin[start_index:end_index]
