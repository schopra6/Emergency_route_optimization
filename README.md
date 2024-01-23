# Emergency_route_optimization

 This system optimize in real-time situation in emergency multiple ambulance routes. In a dense city with its dense population and intricate transit network, exemplifies an urban landscape where efficient response is vital. The proposed system in this project aims to utilize the city's existing transit infrastructure effectively while introducing flexible measures to ensure rapid and safe evacuation. This is known as generalization of the Traveling Salesman Problem (TSP). In this problem, a demand node may
have capacity requirements that exceed the capacity of a single vehicle. This necessitates formulating a problem that allows for that demand node to be visited by more than one vehicle.

## Constraints

- The objective function is to minimizes the total distance traveled by all vehicles. 
- Ensures that each vehicle leaves a node that it enters and each node is visited only once,
- Ensures that each vehicle leaves the depot at most once
- ensures that the capacity of each ambulance is not exceeded
- Miller-Tucker-Zemlin (MTZ) constraints to eliminate subtours, i.e., cycling routes that do not pass through the depot.
- Impose a distance restriction of Dmax on travel between any two nondepot nodes. This is to ensure that the model does not generate routes that are infeasible in the real world.
