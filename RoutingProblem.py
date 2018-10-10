import Network
import Utilities
import Generation



def main():

    # Read yaml configuration file
    routing_config = Utilities.read_yml("routing_config.yml")
    routes = routing_config['routes']
    generations = routing_config['generations']
    generation_size = routing_config['generation_size']
    mutation_chance = routing_config['mutation_chance']
    origin = routing_config['origin']

    # Read in csv to a dictionary
    #nodes_dict = Utilities.read_input_nodes("Kiosk Coords.csv")
    nodes_dict = Utilities.read_json_states("state_capitals.json")

    #  Creates a Network object for the purpose of organizing the Nodes for use in the genetic algorithm
    node_network = Network.Network('StateCapitols', origin, nodes_dict)

    # Create the initial generation of solutions
    solution_generation = Generation.Generation(size=generation_size, routes=routes, origin=origin, network=node_network)

    # Begin iterating through generations
    best_solution = None
    for i in range(1, generations + 1):

        solution_generation.generation_step(mutation_chance)
        solution_generation.remove_weakest_half()

        # Log best solutions
        if best_solution is not None:
            current_best_solution = solution_generation.get_best_solution()
            if (best_solution.score > current_best_solution.score):
                best_solution = current_best_solution
        else:
            best_solution = solution_generation.get_best_solution()

        if i % 100 == 0:
            print("Generation:   ", i)
            print("Average distance: ", solution_generation.generation_average_score())
            print("Min Distance: ", best_solution.score)
            print("")

    #print(best_solution.route_list)
    #print(best_solution.score)

    # If the best solution was found to be valid print output and generate a quick plot for validation
    if best_solution.valid_solution():
        node_network.process_solution(best_solution)
        node_network.display_routes()
        node_network.plot_routes()
    else:
        print("Error: Best solution is invalid")

if __name__ == '__main__':
    main()
