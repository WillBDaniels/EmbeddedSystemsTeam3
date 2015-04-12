package edu.csci.team3;

import de.micromata.opengis.kml.v_2_2_0.Boundary;
import de.micromata.opengis.kml.v_2_2_0.Coordinate;
import de.micromata.opengis.kml.v_2_2_0.Document;
import de.micromata.opengis.kml.v_2_2_0.Feature;
import de.micromata.opengis.kml.v_2_2_0.Geometry;
import de.micromata.opengis.kml.v_2_2_0.Kml;
import de.micromata.opengis.kml.v_2_2_0.LinearRing;
import de.micromata.opengis.kml.v_2_2_0.Placemark;
import de.micromata.opengis.kml.v_2_2_0.Polygon;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.List;


/**
* This class is specifically for parsing up a KML file and outputting the list of lat/longs
*/
public class KMLParser{
    //Java class that supposedly converts kml files into latitude, longitude, and altitude (prints them)
    public List<CoordTriple> parseKml(String inputFileLocation) {
        String src = inputFileLocation;
        InputStream is = getClass().getClassLoader().getResourceAsStream(src);
        Kml kml = Kml.unmarshal(is);
        Feature feature = kml.getFeature();
        return parseFeature(feature);
    }
    
    public List<CoordTriple> parseKml(InputStream resource){
        Kml kml = Kml.unmarshal(resource);
        Feature feature = kml.getFeature();
        return parseFeature(feature);
    }

    private List<CoordTriple> parseFeature(Feature feature) {
        if(feature != null) {
            if(feature instanceof Document) {
                Document document = (Document) feature;
                List<Feature> featureList = document.getFeature();
                for(Feature documentFeature : featureList) {
                    if(documentFeature instanceof Placemark) {
                        Placemark placemark = (Placemark) documentFeature;
                        Geometry geometry = placemark.getGeometry();
                        //obviously this will only get the first oen currently, which needs fixing. 
                        return parseGeometry(geometry);
                    }
                }
            }
        }
        return null;
    }

    private List<CoordTriple> parseGeometry(Geometry geometry) {
        List<CoordTriple> coordList = new ArrayList<>();
        if(geometry != null) {
            if(geometry instanceof Polygon) {
                Polygon polygon = (Polygon) geometry;
                Boundary outerBoundaryIs = polygon.getOuterBoundaryIs();
                if(outerBoundaryIs != null) {
                    LinearRing linearRing = outerBoundaryIs.getLinearRing();
                    if(linearRing != null) {
                        List<Coordinate> coordinates = linearRing.getCoordinates();
                        if(coordinates != null) {
                            for(Coordinate coordinate : coordinates) {
                               coordList.add(new CoordTriple(coordinate.getLatitude(), coordinate.getLongitude(), coordinate.getAltitude()));
                            }
                        }
                    }
                }
            }
        }
        return coordList;
    }

   
}