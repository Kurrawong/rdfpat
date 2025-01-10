import shapely
from rdflib import Graph, URIRef, BNode, Literal, Namespace, IdentifiedNode, XSD
from rdflib.namespace import GEO, RDF, RDFS, SDO
from shapely import Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, LinearRing, coords
from typing import TypeAlias, Literal as TLiteral

ShapelyGeometry: TypeAlias = Point | MultiPoint | LineString | MultiLineString | Polygon | MultiPolygon | LinearRing

from patterns.rdfpattern import RdfPattern


class Geometry(RdfPattern):
    def __init__(
            self,
            coordinates: ShapelyGeometry,
            csr: str = "http://www.opengis.net/def/crs/OGC/1.3/CRS84",
            name: str = None,
            description: str = None,
            serialization_type: TLiteral["wkt", "geojson"] = "wkt"
    ):
        self.coordinates = coordinates
        self.crs = URIRef(csr)
        self.name = Literal(name) if name is not None else None
        self.description = Literal(description) if description is not None else None
        self.serialization_type = serialization_type

    def to_graph(self) -> Graph:
        g = Graph()
        geom = BNode()
        g.add((geom, RDF.type, GEO.Geometry))
        if self.serialization_type == "geojson":
            g.add((geom, GEO.asWKT, Literal(shapely.to_geojson(self.coordinates), datatype=GEO.geoJSONLiteral)))
        else:
            g.add((geom, GEO.asWKT, Literal(self.coordinates.wkt, datatype=GEO.wktLiteral)))
        if self.name is not None:
            g.add((geom, SDO.name, Literal(self.name)))
        if self.description is not None:
            g.add((geom, SDO.description, Literal(self.description)))

        self.node_id = geom
        return g