from math import sin, cos, sqrt, atan2, radians
import matplotlib.pyplot as plt



class Node(object):
    def __init__(self, index, name, address, latitude, longitude):
        '''
        Initializes a node in the networkself.
        Param index: Integer value to identify a node
        Param name: Name of the node
        Param address: Address of the node
        Param latitude: Latitude of the nodes location
        Param longitude: Longitude of the nodes location
        '''
        self.index = index
        self.name = name
        self.address = address
        self.latitude = float(latitude)
        self.longitude = float(longitude)

    def __eq__(self, other):
        '''
        Returns a boolean for if the two nodes share the same index
        Param - other: A second node to use in the comparison
        Returns: Boolean for if the two nodes are equal
        '''
        return self.index == other.index

    def __str__(self):
        '''
        Printable representation for a node
        '''
        return str(self.index) + ' -- ' + self.name + ' -- latitude: ' + str(self.latitude) + ' -- longitude: ' + str(self.longitude)

    def calculate_node_distance(self, other_node):
        '''
        Caluclates the distance between two node_list
        Param - self: The first node object
        Param - other_node: The second node object
        Returns: The distance between the two nodes in kilometers
        '''
        r = 6373.0

        lat1 = radians(self.latitude)
        lon1 = radians(self.longitude)
        lat2 = radians(other_node.latitude)
        lon2 = radians(other_node.longitude)

        dlon = lon2 - lon1
        dlat = lat2 -lat1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))

        return r * c


class Network(object):
    def __init__(self, name, origin, node_dict):
        '''
        Initializes a  network of nodes
        Param - name: The name of the network
        Param - node_dict: A dictionary of nodes to add to the network
        '''
        self.name = name
        self.origin = origin
        self.node_list = []
        for idx, node in enumerate(node_dict):
            new_node = Node(idx, node['name'],node['address'],node['latitude'],node['longitude'])
            self.node_list.append(new_node)
        self.build_distance_matrix()
        self.route_list = []

    def __str__(self):
        '''
        Printable representation for a network
        '''
        string = self.name + '\n'
        string = string + '---------- \n'
        for node in self.node_list:
            string = string + str(node) + '\n'
        return string

    def get_node(self, idx):
        '''
        Gets a node with the specific index
        Param - idx: Index for a nodes
        Returns: A Node object with the matching index
        '''
        for node in self.node_list:
            if node.index == idx:
                return node

    def build_distance_matrix(self):
        '''
        Initializes distance_matrix and populates it with the distances between all combinations of node_list
        '''
        self.distance_matrix = {}

        for node_a in self.node_list:
            for node_b in self.node_list:
                if node_a != node_b:
                    self.distance_matrix[(node_a.index, node_b.index)] = node_a.calculate_node_distance(node_b)
                else:
                    self.distance_matrix[(node_a.index, node_b.index)] = 0.0

    def process_solution(self, solution):
        '''
        Builds a RouteDetails object for each route in a solution
        Param solution: Solution to build RouteDetails objects from
        '''
        self.score = solution.score
        # remove all previously added routes before adding the new best solution
        self.route_list = []
        for idx_route, route in enumerate(solution.route_list):
            current_route = RouteDetails(idx_route+1, self.origin)

            for node in route:
                current_route.add_node(self.get_node(node))

            self.route_list.append(current_route)

    def display_routes(self):
        '''
        Prints all routes in a route details object
        '''
        print("Total Distance Traveled: ", self.score)
        for route in self.route_list:
            print(route)

    def plot_routes(self):
        '''
        Creates a plot where each route is a different colorself. Can handle up to 5 routes.
        '''
        color = ['green', 'red','blue', 'yellow', 'orange']
        for idx, route in enumerate(self.route_list):
            route_number = route.route_number
            lon_list = []
            lat_list = []
            for node in route.route_order_node_list:
                lon_list.append(node.longitude)
                lat_list.append(node.latitude)

            plt.plot(lon_list, lat_list, color=color[idx])

        plt.show()


class RouteDetails(object):
    def __init__(self, route_number, route_origin):
        '''
        Creates a route details object that is used to describe a route for display and plotting
        Param route_number: The route number out of the total number of routes
        Param route_origin: The location which the route begins and ends
        '''
        self.route_number = route_number
        self.route_origin = route_origin
        self.route_order_node_list = []

    def add_node(self, node):
        '''
        Adds a node to a ordered list of nodes
        Param node: node to add to the ordered list of nodes
        '''
        self.route_order_node_list.append(node)

    def __str__(self):
        '''
        String representation of a RouteDetails object
        '''
        string = 'Route Number: ' + str(self.route_number) + '\n'

        for idx, node in enumerate(self.route_order_node_list):
            string = string + 'Stop:  ' + str(idx + 1) + '\t' + 'Location: ' + node.name + '\n'

        string = string + '\n'

        return string
