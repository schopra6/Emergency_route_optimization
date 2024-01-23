import folium
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from folium.plugins import Draw


def add_depot_map(stops_df):
    m = folium.Map()

    for stop in stops_df.itertuples():
        folium.CircleMarker(
            location=[stop.stop_lat, stop.stop_lon],
            radius=3,
            color="darkgreen",
            fill=True,
            fill_opacity=1,
            fill_color="darkgreen",
            tooltip=f"{stop.stop_name} ({stop.stop_id})",
            popup=f"""
            <div>
                <h4>{stop.stop_name} ({stop.stop_id})</h4>
            </div>
            """,
        ).add_to(m)

    # Add drawing tool to the map
    draw = Draw(
        draw_options={
            "polyline": False,
            "rectangle": False,
            "circle": False,
            "marker": True,
            "circlemarker": False,
            "polygon": False,
        }
    )
    draw.add_to(m)

    return m


def add_traffic_area(stops_df):
    m = folium.Map(
        location=[45.5048542, -73.5691235],
        zoom_start=11,
        tiles="cartodbpositron",
        width="100%",
    )

    for stop in stops_df.itertuples():
        folium.CircleMarker(
            location=[stop.stop_lat, stop.stop_lon],
            radius=3,
            color="darkgreen" if stop.stop_id != "0" else "blue",
            fill=True,
            fill_opacity=1,
            fill_color="darkgreen" if stop.stop_id != "0" else "blue",
            tooltip=f"{stop.stop_name} ({stop.stop_id})",
            popup=f"""
            <div>
                <h4>{stop.stop_name} ({stop.stop_id})</h4>
            </div>
            """,
        ).add_to(m)

    # Add drawing tool to the map
    draw = Draw(
        draw_options={
            "polyline": False,
            "rectangle": True,
            "circle": False,
            "marker": True,
            "circlemarker": False,
            "polygon": False,
        }
    )
    draw.add_to(m)

    return m


def show_unsolved_network(
    stops_df, traffic_area, stops_in_traffic_area, distance_matrix
):
    m = folium.Map(
        location=[45.5048542, -73.5691235],
        zoom_start=11,
        tiles="cartodbpositron",
        width="100%",
    )

    # Add disaster area
    folium.GeoJson(
        traffic_area,
        name="Disaster area",
        style_function=lambda x: {
            "color": "#ff0000",
            "fillColor": "#ff0000",
            "weight": 1,
            "fillOpacity": 0.4,
        },
    ).add_to(m)

    for stop in stops_df.itertuples():
        folium.CircleMarker(
            location=[stop.stop_lat, stop.stop_lon],
            radius=3,
            color=(
                "red"
                if stop.stop_id in stops_in_traffic_area.stop_id.values.tolist()
                else "darkgreen"
                if stop.stop_id != "0"
                else "blue"
            ),
            fill=True,
            fill_opacity=1,
            fill_color=(
                "red"
                if stop.stop_id in stops_in_traffic_area.stop_id.values.tolist()
                else "darkgreen"
                if stop.stop_id != "0"
                else "blue"
            ),
            tooltip=f"{stop.stop_name} ({stop.stop_id})",
            popup=f"""
            <div>
                <h4>{stop.stop_name} ({stop.stop_id})</h4>
                <h4>Distance from depot: {distance_matrix.loc["0", stop.stop_id]:.1f} km</h4>
            </div>
            """,  # noqa: E501
        ).add_to(m)

    folium.plugins.Fullscreen(position="topright").add_to(m)
    folium.plugins.MousePosition(position="topright").add_to(m)

    return m


def plot_routes(
    distance_matrix,
    traffic_area,
    stops_in_traffic_area,
    bus_path_df,
    routes_gdf,
    num_buses,
    split_type,
):
    colormap_route = [
        mcolors.rgb2hex(c) for c in list(plt.cm.rainbow(np.linspace(0, 1, num_buses)))
    ]

    route_map = folium.Map(
        location=[45.5048542, -73.5691235],
        zoom_start=11,
        tiles="cartodbpositron",
        width="100%",
    )

    folium.GeoJson(
        traffic_area,
        name="Disaster area",
        style_function=lambda x: {
            "color": "#ff0000",
            "fillColor": "#ff0000",
            "weight": 1,
            "fillOpacity": 0.3,
        },
    ).add_to(route_map)

    mc = folium.plugins.MarkerCluster(name="Individual stops").add_to(route_map)

    for stop in bus_path_df.itertuples():
        c = folium.CircleMarker(
            location=[stop.geometry.coords[0][1], stop.geometry.coords[0][0]],
            radius=5,
            color=(
                colormap_route[stop.bus]
                if not stop.is_split
                else "purple"
                if stop.stop_id != "0"
                else "black"
            ),
            fill=True,
            fill_opacity=1,
            fill_color=(
                colormap_route[stop.bus]
                if not stop.is_split
                else "purple"
                if stop.stop_id != "0"
                else "black"
            ),
            tooltip=f"""
            <b>{stop.stop_name} ({stop.stop_id})</b>
            <br>
            Route: {bus_path_df[bus_path_df["stop_id"] == stop.stop_id]['bus'].values[0]}
            <br>
            Step: {bus_path_df[bus_path_df["stop_id"] == stop.stop_id]['step'].values[0] + 1}
            <br>
            Demand: {bus_path_df[bus_path_df["stop_id"] == stop.stop_id]['demand'].values[0]}
            <br>
            Load: {bus_path_df[bus_path_df["stop_id"] == stop.stop_id]['step_demand'].values[0]}
            <br>
            Has split demand?: {stop.is_split}
            """,
            popup=f"""
            <div>
                <h4>{stop.stop_name} ({stop.stop_id})</h4>
                <h4>Distance from depot: {distance_matrix.loc["0", stop.stop_id]:.1f} km</h4>
            </div>
            """,
        )

        if stop.stop_id == "0" or stop.is_split:
            c.add_to(route_map)
        else:
            c.add_to(mc)

    for stop in stops_in_traffic_area.itertuples():
        folium.CircleMarker(
            location=[stop.geometry.coords[0][1], stop.geometry.coords[0][0]],
            radius=5,
            color="red",
            fill=True,
            fill_opacity=1,
            fill_color="red",
            tooltip=f"""
            <b>{stop.stop_name} ({stop.stop_id})</b>
            """,
            popup=f"""
            <div>
                <h4>{stop.stop_name} ({stop.stop_id})</h4>
                <h4>Distance from depot: {distance_matrix.loc["0", stop.stop_id]:.1f} km</h4>
            </div>
            """,
        ).add_to(route_map)

    for route in routes_gdf.itertuples():
        route_layer = folium.FeatureGroup(f"Route {route.bus}")
        folium.PolyLine(
            locations=[(p[1], p[0]) for p in route.geometry.coords],
            color=colormap_route[route.bus],
            weight=3,
            opacity=0.6,
            tooltip=f"Route {route.bus}",
            popup=f"""
            <div>
                <h5>Route {route.bus}</h5>
                <h5>Total demand: {route.demand}</h5>
            </div>
            """,
        ).add_to(route_layer)

        route_layer.add_to(route_map)

    folium.plugins.Fullscreen(position="topright").add_to(route_map)
    folium.plugins.MousePosition(position="topright").add_to(route_map)
    folium.LayerControl().add_to(route_map)

    route_map.save(f"route_map_split_{split_type}.html")
    return route_map
