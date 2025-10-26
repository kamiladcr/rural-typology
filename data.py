import geopandas as gpd
import json
import os

gdf = gpd.read_parquet("data/typology_kmeans_silhouette_11_5cl.parquet")
gdf = gdf.explode(ignore_index=True)

print(f"Original features: {len(gdf):,}")

print("Simplifying geometries...")
gdf["geometry"] = gdf.geometry.simplify(tolerance=50, preserve_topology=True)

print("Dissolving by urbanization_rank...")
gdf_dissolved = gdf.dissolve(by="urbanization_rank", as_index=False, aggfunc="first")

print(f"After dissolving: {len(gdf_dissolved)} features")

print("Exploding MultiPolygons...")
gdf_exploded = gdf_dissolved.explode(index_parts=False, ignore_index=True)

print(f"After exploding: {len(gdf_exploded):,} separate regions")

print("Reprojecting to WGS84...")
gdf_exploded = gdf_exploded.to_crs("EPSG:4326")

gdf_exploded["geometry"] = gdf_exploded.geometry.simplify(
    tolerance=0.0005, preserve_topology=True
)

output_path = "layers/polygons_dissolved_exploded.geojson"
print(f"Exporting to {output_path}...")
gdf_exploded.to_file(output_path, driver="GeoJSON")

file_size = os.path.getsize(output_path) / 1024 / 1024
print(f"Exported {len(gdf_exploded):,} features")
print(f"File size: {file_size:.2f} MB")
