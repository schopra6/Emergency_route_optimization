# Emergency Route Optimization

 This system optimize in real-time situation in emergency for multiple ambulance routes. In a dense city with its dense population and intricate transit network, exemplifies an urban landscape where efficient response is vital. The proposed system in this project aims to utilize the city's existing transit infrastructure effectively while introducing flexible measures to ensure rapid and safe evacuation. This is known as generalization of the Traveling Salesman Problem (TSP). In this problem, a demand node may
have capacity requirements that exceed the capacity of a single vehicle. This necessitates formulating a problem that allows for that demand node to be visited by more than one vehicle.

## Constraints

- The objective function is to minimizes the total distance traveled by all vehicles. 
- Ensures that each vehicle leaves a node that it enters and each node is visited only once,
- Ensures that each vehicle leaves the depot at most once
- ensures that the capacity of each ambulance is not exceeded
- Miller-Tucker-Zemlin (MTZ) constraints to eliminate subtours, i.e., cycling routes that do not pass through the depot.
- Impose a distance restriction of Dmax on travel between any two nondepot nodes. This is to ensure that the model does not generate routes that are infeasible in the real world.

### Streamlit Application

1. Run `pip install -r requirements.txt` to install all the necessary packages
2. Run `streamlit run streamlit/app.py` to run the app
3. Add a depot location, wait for the distance matrix to be calculated, and then add a traffic area
4. Choose the parameters and run the model
