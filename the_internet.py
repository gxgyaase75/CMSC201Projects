"""
File: the_internet.py
    Author: Gabriel Gyaase
    Date: 11/30/2024
    Section: 10
    E-mail: ggyaase1@umbc.edu
    Description: This file simulates the internet,
                 where the user is able to create servers
                 of different websites, and trace the routes
                 between each server.

    Given Score: 77.5/90
"""
QUIT_STRING = 'quit'
"""
Dictionary Structure:
{server_name: 'server', ip_address: 'XXX.XXX.XXX.XXX',
connections: {connected_server: seconds (connection_time)}}
"""
        

def create_server(server_name, ip_v4_address, server_dict, ip_dict):
    """
    :param server_name: the name of the server to be added.
    :param ip_v4_address: the unique IP address of the requested server.
    :param server_dict: A dictionary that holds all of the servers in the 
                        internet.
    :param ip_dict: A dictionary that holds all of the IP addresses, which
                    corresponds each of the server names.
    :return: Add a new server to the dictionary, unless the IP address is
             already in use, in which it doesn't, or the name is already in
             use, in which it chanes the IP address.
    """
    if ip_v4_address in ip_dict: # Checks if IP is already being used.
        print("Error: That IP address is already in use. Please try again.")
    elif server_name in servers: # Checks if server is already being used
        remove_ip = ''
        connections = server_dict[server_name]["connections"]
        server_dict[server_name] = {'ip_address': ip_v4_address, \
            'connections': connections}
        for x in ip_dict:
            if ip_dict[x] == server_name:
                remove_ip = x
        ip_dict[ip_v4_address] = server_name
        del ip_dict[remove_ip] # Removes old IP from ip_dict
        print(\
            "Success: IP Address has been changed. Servers have been updated.")
    else:
        server_dict[server_name] = \
        {'ip_address': ip_v4_address, 'connections': {}}
        ip_dict[ip_v4_address] = server_name
        print(\
           f"Success: Server {server_name} was created at IP {ip_v4_address}.")

def create_connection(server_1, server_2, connect_time, server_list):
    """
    :param server_1: The first inputted server to be connected
    :param server_2: The second inputted server to be connected
    :param connect_time: The ping (in milliseconds) it takes to go from
                         server_1 to server_2.
    :param server_list: The list of all servers on the internet.
    :return: The two servers are now connected, and added to their connections
             dictionary.
    """
    if server_1 in server_list and server_2 in server_list:
        if server_1 == server_2: # Checks if the servers are the same
            print(f"Error: Server {server_1} cannot be connected with itself.")
        elif server_1 in server_list[server_2]['connections'] or \
        server_2 in server_list[server_1]['connections']:
            # Checks for any pre-existing connections
            print(\
            "Error: There is already a connection between these two servers.")
        else:
            # Creates each connection in each dictionary
            server_list[server_1]['connections'][server_2] = connect_time
            server_list[server_2]['connections'][server_1] = connect_time
            print(f"Success: Servers", server_1, "and", server_2, 
                  "have been connected.")
    else:
        print("Error: Invalid servers inputted. Please try again.")

def set_server(server_or_address, server_dict, ip_dict, home_address):
    """
    :param server_or_address: The server or ip address of a chosen site
    :param server_dict: Dictionary holding all of the dictionaries
    :param ip_dict: Dictionary holding all of the IP addresses
    :param home_address: The currently set server, '' if not set yet
    """
    the_server = ''
    if server_or_address in ip_dict:
        the_server = ip_dict[server_or_address]
    elif server_or_address in server_dict:
        the_server = server_or_address
    home_address = the_server # Changes old set server to new set server.
    print(f"Success: Server {home_address} has been selected.")
    return home_address

def stream_visit(server_or_address, home_server, server_dict, ip_dict, \
                 search_type):
    """
    :param server_or_address: the server
    :param home_server: the currently set server
    :param server_dict: Dictionary of all servers on the internet
    :param ip_dict: Dictionary of all IP addresses of each server
    :param search_type: the recursive function that the user requested
    :return: the return for the ping or trace_route of the home server
    """
    target_server = ''
    if len(server_or_address.split()) > 1:
        server_or_address = server_or_address.split()[1]
    if server_or_address in ip_dict:
        target_server = ip_dict[server_or_address]
    elif server_or_address in server_dict:
        target_server = server_or_address
    visited = {} # Visited dictionary checks off which servers have been seen
    for site in server_dict:
        visited[site] = False
    if search_type == 'ping':
        the_ping = ping(home_server, target_server, server_dict, visited)
        if the_ping != 0:
            return the_ping
        else:
            return -1 # Returns negative number so error is shown
    elif search_type == 'traceroute':
        the_route = \
            trace_route(home_server, target_server, server_dict, visited)
        return the_route # Route won't have target_server if there's no way
            
def ping(start_server, end_server, server_dict, visited, total_ping=0):
    """
    :param start_server: The currently set_server on the internet
    :param end_server: The server they want to gather the ping from
    :param server_dict: Dictionary of all servers on the internet
    :param visited: Dictionary of sites that the recursion has/hasn't been
                    through
    :param total_ping: The ping counted across all of the servers on the way
                       to the end_server
    :return: total_ping, as an integer
    """

    # Must use recursion
    if total_ping == 0: # Checks if there is a possible route to the end_server
        visited_copy = {} # Makes a copy of visited so it doesn't interfere
        for key, value in visited.items(): # Returns 0 if there's no path
            visited_copy[key] = value
        if end_server not in trace_route(start_server, end_server, server_dict,
                                          visited_copy):
            return 0
    if start_server == end_server:
        return 0 # returns 0 because the servers are the same
    if end_server in server_dict[start_server]['connections']:
        # Goes to the connection is directly under the server
        return server_dict[start_server]['connections'][end_server]
    # setting the visited to true so we don't loop back.
    visited[start_server] = True
    for connected_server in server_dict[start_server]['connections']:
        if not visited[connected_server]: # Loops through all connections
            total_ping = \
                server_dict[start_server]['connections'][connected_server]
            if total_ping:
                total_ping = total_ping + ping(connected_server, end_server, \
                                               server_dict, visited, 
                                               total_ping) 
                # Only adds if on correct path
    visited[start_server] = False
    return total_ping
    
def trace_route(start_server, end_server, server_dict, visited):
    """
    :param start_server: The currently set_server on the internet
    :param end_server: The server they want to gather the ping from
    :param server_dict: Dictionary of all servers on the internet
    :param visited: Dictionary of sites that the recursion has/hasn't been
                    through
    :return: The route the program has taken to reach the end_server from the 
             start_server
    """
    planned_route = []
    # setting the visited to true so we don't loop back.
    visited[start_server] = True
    if start_server == end_server:
        return [end_server]
    if end_server in server_dict[start_server]['connections']:
        return [start_server] + trace_route(end_server, end_server, 
                                            server_dict, visited)
    # Base Case: If the end_server is a connection or is the connected server
    for connected_server in server_dict[start_server]['connections']:
        if not visited[connected_server]:
            planned_route = [start_server]
            if planned_route:
                planned_route = planned_route + trace_route(connected_server, \
                                                end_server, server_dict, \
                                                visited)
    visited[start_server] = False
    return planned_route # Returns current route in case of dead end

def ip_config(home_server, server_dict):
    """
    :param home_server: the currently set server
    :param server_dict: dictionary of all of the servers
    :return: Prints a string that reports what the set server is and its IP
             address
    """
    if home_server == '':
        print("Error: There is no set server.")
    else: # Uses f-string to show set server and IP address.
        print(f"{home_server}\t{server_dict[home_server]['ip_address']}")

def display_servers(server_list):
    """
    :param server_list: The server list of all the servers on the internet
    :return: Displays all of the servers, IP addresses and connections
    """ # Uses nested for loop to display servers and indents for related info
    for x in server_list: 
        print("\t", x, "\t", server_list[x]['ip_address'])
        for y in server_list[x]['connections']:
            print("\t\t", y, "\t", server_list[y]['ip_address'], '\t', 
                  server_list[x]['connections'][y])

if __name__ == '__main__':
    current_server = ''
    servers = {}
    ip_v4_addresses = {}
    # While loop simulates the constant inputs
    server_input = input(">>> ").strip().lower()
    while server_input != QUIT_STRING: # Only stops for 'quit'
        if 'create-server' in server_input:
            creation_prompt = server_input.split()
            if len(creation_prompt) == 3:
                # Prevents extra or missing words in the input
                creation_prompt = creation_prompt[1:]
                creation_prompt = server_input.split()[1:]
                server_name = creation_prompt[0]
                server_ip_address = creation_prompt[1]
                create_server(server_name, server_ip_address, \
                servers, ip_v4_addresses)
            else:
                print(\
                    "Error: Please enter the server name and IP address.")
        elif 'create-connection' in server_input: # create_connection
            connection_prompt = server_input.split()
            if len(connection_prompt) == 4:
                connection_prompt = server_input.split()[1:]
                server_one = connection_prompt[0].strip()
                server_two = connection_prompt[1].strip()
                connection_time = int(connection_prompt[2].strip())
                create_connection(server_one, server_two, \
                                  connection_time, servers)
            else:
                print(\
                "Error: Please enter the server names and connection time.")
        elif 'set-server' in server_input: # set_server
            if len(server_input.split()) == 2:
                set_server_prompt = server_input.split()[1]
                if set_server_prompt in servers or \
                    set_server_prompt in ip_v4_addresses:
                    current_server = \
                        set_server(set_server_prompt, servers, \
                                   ip_v4_addresses, current_server)
                else:
                    print("Error: Invalid entry. Please try again.")
            else:
                print(\
                "Error: Please enter the server name or the IP address.")
        elif 'ping' in server_input: # ping (relies on stream_visit)
            if current_server == '': # Checks for prompt errors
                print("Error: There is no set server.")
            elif len(server_input.split()) == 2:
                ping_prompt = server_input.split()[1]
                ping_ip = ''
                if ping_prompt not in ip_v4_addresses and \
                    ping_prompt not in servers:
                    print("Error: Invalid server or IP address.")
                else:
                    if ping_prompt in ip_v4_addresses:
                        ping_ip = ping_prompt   
                    elif ping_prompt in servers:
                        ping_ip = servers[ping_prompt]['ip_address']
                    if current_server == ping_prompt:
                        print("Set Server", ping_prompt, 
                              "is target Server", ping_prompt,
                                ". \nReply from ", ping_ip, "time = 0 ms")
                    elif ping_ip != '':
                        ping_signal = stream_visit(server_input, \
                                        current_server, servers, \
                                        ip_v4_addresses, 'ping')
                        if ping_signal < 0:
                            print("Error: No Connection from Server",
                                  current_server, "to Server",
                                  f"{ip_v4_addresses[ping_ip]}.")
                        else:
                            print(\
                            f"Reply from {ping_ip} time = {ping_signal} ms")
            else:
                print("Error: Please enter the server name or IP address.")
        elif 'traceroute' in server_input or 'tracert' in server_input:
            if current_server == '': # traceroute (relies on stream_visit)
                print("Error: There is no set server.")
            elif len(server_input.split()) == 2:
                route_prompt = server_input.split()[1]
                route_ip = ''
                if route_prompt in ip_v4_addresses: # Turns prompt into IP
                    route_ip = route_prompt
                elif route_prompt in servers:
                    route_ip = servers[route_prompt]['ip_address']
                else: # Checks for prompt errors
                    print("Error: Invalid server or IP address.")
                if current_server == route_prompt:
                    print("Error: Set server", route_prompt, 
                          f"is Target Server {route_prompt}.")
                elif route_ip != '':
                    route_signal = stream_visit(server_input, current_server, \
                    servers, ip_v4_addresses, 'traceroute')
                    if route_ip not in route_signal and \
                        ip_v4_addresses[route_ip] not in route_signal:
                        print("Error: Unable to route target system", 
                              ip_v4_addresses[route_ip])
                    else:
                        print("Tracing route to server", 
                              ip_v4_addresses[route_ip], f"[{route_prompt}]")
                        for i in range(len(route_signal)):
                            if i == 0:
                                ping_num = 0
                            else:
                                ping_num = \
                                    servers[route_signal[i]]['connections']\
                                        [route_signal[i-1]]
                            print('\t', i, '\t', ping_num, '\t', 
                                f"[{servers[route_signal[i]]['ip_address']}]", 
                                  '\t', route_signal[i])
                        print("Trace complete.")
            else:
                print("Error: Please enter the server name or IP address.")
        elif 'ip-config' in server_input:
            ip_config(current_server, servers)
        elif 'display-servers' in server_input:
            display_servers(servers)
        server_input = input(">>> ").strip().lower()
        # Continues the while loop.
