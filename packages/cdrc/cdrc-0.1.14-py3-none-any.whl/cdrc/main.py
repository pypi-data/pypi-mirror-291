import json
import os
import re
from pathlib import Path
from urllib.parse import quote

import geopandas
import httpx

from cdrc.common import get_projection_id, inverse_geojson, return_properties, save_stripped_file
from cdrc.schemas import FeatureSearchByCog, FeatureSearchIntersect
import warnings
warnings.filterwarnings("ignore")


class CDRClient:
    def __init__(self, token, output_dir="."):
        self.cog_url = "https://s3.amazonaws.com/public.cdr.land"
        # self.cog_url = "http://localhost:9000/public.cdr.land"
        self.projection_id = ""
        self.output_dir = output_dir
        self.base_url = "https://api.cdr.land/v1"
        # self.base_url = "http://localhost:8333/v1"
        self.headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
        self.client = httpx.Client(timeout=None)

    def features_search(self, cog_id, feature_types, system_versions, validated):
        payload = {
            "feature_types": feature_types,
            "system_versions": system_versions,
            "search_text": "",
            "validated": validated,
            "legend_ids": [],
            "georeferenced_data": True,
            "page": 0,
            "size": 20,
        }
        validated_payload = FeatureSearchByCog(**payload).model_dump()
        validated_payload["feature_types"] = [ft.value for ft in validated_payload["feature_types"]]
        all_data = []
        while True:
            response = self.client.post(
                f"{self.base_url}/features/{cog_id}", json=validated_payload, headers=self.headers, timeout=None
            )
            if response.status_code != 200:
                print(response.text)
                print("There was an error connecting to the cdr.")
                break
            data = response.json()
            if not data:
                break

            all_data.extend(data)
            validated_payload["page"] = validated_payload["page"] + 1
            print(f"{len(all_data)} legend items downloded...")

        return all_data

    def features_intersect_search(
        self, cog_ids, feature_type, system_versions, validated, search_text, intersect_polygon, search_terms
    ):
        payload = {
            "cog_ids": cog_ids,
            "category": feature_type,
            "system_versions": system_versions,
            "search_text": search_text,
            "search_terms": search_terms,
            "validated": validated,
            "legend_ids": [],
            "intersect_polygon": intersect_polygon,
            "page": 0,
            "size": 100000,
        }
        validated_payload = FeatureSearchIntersect(**payload).model_dump()
        all_data = []
        while True:
            response = self.client.post(
                f"{self.base_url}/features/intersect", json=validated_payload, headers=self.headers, timeout=None
            )
            if response.status_code != 200:
                print(response.text)
                print("There was an error connecting to the cdr.")
                break
            data = response.json()
            if not data:
                break

            all_data.extend(data)
            validated_payload["page"] = validated_payload["page"] + 1
            print(f"{len(all_data)} legend items downloded...")

        return all_data

    def legend_builder(self, legend_features, output_dir):
        if legend_features.get("px_geojson"):
            system = legend_features.get("system")
            system_version = legend_features.get("system_version")
            label = legend_features.get("label")
            abbreviation = legend_features.get("abbreviation")
            category = legend_features.get("category")
            cog_id = legend_features.get("cog_id")
            legend_contour_feature = {
                "type": "Feature",
                "geometry": inverse_geojson(legend_features.get("px_geojson")),
                "properties": {
                    "legend_id": legend_features.get("legend_id", ""),
                    "category": category,
                    "label": label,
                    "abbreviation": abbreviation,
                    "description": legend_features.get("description"),
                    "validated": legend_features.get("validated"),
                    "system": system,
                    "system_version": system_version,
                    "model_id": legend_features.get("model_id"),
                    "confidence": legend_features.get("confidence"),
                    "map_unit_age_text": legend_features.get("map_unit_age_text"),
                    "map_unit_lithology": legend_features.get("map_unit_lithology"),
                    "map_unit_b_age": legend_features.get("map_unit_b_age"),
                    "map_unit_t_age": legend_features.get("map_unit_t_age"),
                },
            }

            obj = {"type": "FeatureCollection", "features": [legend_contour_feature]}
            thing = label[:20] + "__" + abbreviation[:20]
            thing = thing.strip().lower()
            if thing == "__":
                thing = legend_features.get("description", "")[:20]
                thing = re.sub(r"\s+", "", thing).lower()
            thing = thing.replace("\\", "")
            thing = thing.replace("/", "")
            thing = thing.replace(";", "")

            with open(
                os.path.join(
                    output_dir + "/pixel",
                    f"{cog_id}__{system}__{system_version}__{thing}_{category}_legend_contour.geojson",
                ),
                "w",
            ) as out:
                out.write(json.dumps(obj, indent=2))

    def set_latest_projection_id(self, feature):
        cdr_projection_id = get_projection_id(feature)
        if self.projection_id != cdr_projection_id:
            self.projection_id = cdr_projection_id

    def legend_feature_builder(self, legend_features, output_dir):
        """
        For each feature associated with a legend item build the Feature obj to save as geojson or geopackage.
        """
        system = legend_features.get("system")
        system_version = legend_features.get("system_version")
        label = legend_features.get("label", "")
        abbreviation = legend_features.get("abbreviation", "")
        category = legend_features.get("category")
        description = legend_features.get("description", "")
        cog_id = legend_features.get("cog_id")

        pixel_features = []
        geom_features = []

        for result in legend_features.get(f"{category}_extractions", []):
            self.set_latest_projection_id(result)
            feature = {
                "type": "Feature",
                "geometry": inverse_geojson(result["px_geojson"]),
                "properties": return_properties(legend_features, result),
            }
            pixel_features.append(feature)
            if result.get("projected_feature"):
                geom_feature = {
                    "type": "Feature",
                    "geometry": result.get("projected_feature")[0].get("projected_geojson"),
                    "properties": return_properties(legend_features, result),
                }
                geom_features.append(geom_feature)
            else:
                pass

        px_obj = {"type": "FeatureCollection", "features": pixel_features}
        thing = label[:20] + "__" + abbreviation[:20]
        thing = thing.strip().lower()

        if thing == "__":
            thing = description[:20]
            thing = re.sub(r"\s+", "", thing).lower()
        thing = thing.replace("\\", "")
        thing = thing.replace("/", "")
        thing = thing.replace(";", "")

        with open(
            os.path.join(
                output_dir + "/pixel",
                f"{cog_id}__{system}__{system_version}__{thing}_{category}_features.geojson",
            ),
            "w",
        ) as out:
            out.write(json.dumps(px_obj, indent=2))

        if geom_features:
            geom_obj = {"type": "FeatureCollection", "features": geom_features}

            df = geopandas.GeoDataFrame.from_features(geom_obj)
            # always 4326 from cdr
            vector = df.set_crs("EPSG:4326", allow_override=True)
            vector.to_file(
                os.path.join(
                    output_dir + "/projected",
                    f"{cog_id}__{system}__{system_version}__{thing}_{category}_features.gpkg",
                ),
                driver="GPKG",
            )

    def build_cog_geopackages(self, cog_id, feature_types, system_versions, validated, rasters=True):
        print("Querying the CDR...")

        legend_items = self.features_search(cog_id, feature_types, system_versions, validated)
        if not legend_items:
            print(f"Querying the CDR Complete!\n0 legend items and associated features downloaded")
            return
        else:
            print(f"Querying the CDR Complete!\n{len(legend_items)} legend items and associated features downloaded.")

        Path(self.output_dir + "/" + cog_id + "/pixel").mkdir(parents=True, exist_ok=True)
        Path(self.output_dir + "/" + cog_id + "/projected").mkdir(parents=True, exist_ok=True)

        print("Converting JSONs to Geopackages...")
        for legend_item in legend_items:
            self.legend_builder(legend_item, self.output_dir + f"/{legend_item.get('cog_id')}")
            self.legend_feature_builder(legend_item, self.output_dir + f"/{legend_item.get('cog_id')}")

        if rasters:
            print("Downloading pixel space and projected COGs...")
            self.download_projected_and_pixel_cog(cog_id=cog_id)
        print(f"Done!\nCheck this directory for a folder named '{cog_id}'")

    def build_cma_geopackages(
        self,
        cog_ids: list,
        feature_type: str,
        system_versions: list,
        validated,
        search_text,
        intersect_polygon,
        cma_name: str = "",
        search_terms: list = []
    ):
        if cma_name == "":
            print("Please provide a 'cma_name' to be the folder name output for geopackes.")
            return

        if intersect_polygon:
            Path(self.output_dir + "/" + cma_name + "/projected").mkdir(parents=True, exist_ok=True)
            # with open(self.output_dir + "/" + cma_name + "/projected/intersect_polygon.geojson", "w") as f:
            #     json.dump(intersect_polygon, f)

        print("Querying the CDR...")

        feature_items = self.features_intersect_search(
            cog_ids, feature_type, system_versions, validated, search_text, intersect_polygon, search_terms
        )
        print(f"Querying the CDR Complete!\n{len(feature_items)} legend items and associated features downloaded.")

        legend_items = {}
        for feature in feature_items:
            legend_item_ = feature.get("legend_item") or {}
            if legend_item_.get("legend_id", "") not in legend_items.keys():
                legend_items[legend_item_.get("legend_id", "")] = legend_item_
                legend_items[legend_item_.get("legend_id", "")][f"{feature_type}_extractions"] = []

            legend_items[legend_item_.get("legend_id", "")][f"{feature_type}_extractions"].append(feature)

        if not legend_items.values():
            print("CDR didn't return any features for this search returned")
            return

        Path(self.output_dir + "/" + cma_name + "/pixel").mkdir(parents=True, exist_ok=True)
        Path(self.output_dir + "/" + cma_name + "/projected").mkdir(parents=True, exist_ok=True)

        print("Converting JSONs to Geopackages...")
        for legend_item in legend_items.values():
            self.legend_builder(legend_item, self.output_dir + f"/{cma_name}")
            self.legend_feature_builder(legend_item, self.output_dir + f"/{cma_name}")
        print(f"Done!\nCheck this directory for a folder named '{cma_name}'")

    def download_cog(self, cog_id):
        r = httpx.get(f"{self.cog_url}/cogs/{cog_id}.cog.tif", timeout=None)
        Path(self.output_dir + "/" + cog_id + "/pixel").mkdir(parents=True, exist_ok=True)
        # open(f"{self.output_dir}/{cog_id}/pixel/{cog_id}.cog.tif", "wb").write(r.content)
        save_stripped_file(r.content, f"{self.output_dir}/{cog_id}/pixel/{cog_id}.cog.tif")

    def download_projected_and_pixel_cog(self, cog_id):
        self.download_cog(cog_id=cog_id)
        if self.projection_id:
            path = f"/maps/cog/projection/{self.projection_id}"

            encoded_url_path = quote(path)

            resp = self.client.get(self.base_url + encoded_url_path, headers=self.headers, timeout=None)
            if resp.status_code == 403 or resp.status_code == 404:
                print("Unable to find projection.")
                return
            if resp.status_code == 200:
                data = resp.json()
                if data.get("download_url"):
                    url_ = self.cog_url + quote(
                        f"/test/cogs/{cog_id}/{data.get('system')}/{data.get('system_version')}/{self.projection_id}"
                    )
                    r = httpx.get(url_, timeout=None)
                    if r.status_code != 200:
                        print(r.status_code)
                        return
                    open(f"{self.output_dir}/{cog_id}/projected/{cog_id}.projected.cog.tif", "wb").write(r.content)
