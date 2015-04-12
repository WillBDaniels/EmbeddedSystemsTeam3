package edu.csci.team3;

/**
 * This class is for holding 'coordinate triples' that will be a lot easier to manage throughout the 
 * program 
 * 
 * @author Wdaniels
 */
public class CoordTriple {
    private double lat, lon, alt;

    public CoordTriple(double lat, double lon, double alt) {
        this.lat = lat;
        this.lon = lon;
        this.alt = alt;
    }

    public double getLat() {
        return lat;
    }

    public void setLat(double lat) {
        this.lat = lat;
    }

    public double getLon() {
        return lon;
    }

    public void setLon(double lon) {
        this.lon = lon;
    }

    public double getAlt() {
        return alt;
    }

    public void setAlt(double alt) {
        this.alt = alt;
    }

    @Override
    public String toString(){
        return "Latitude: " + getLat() + " Longitude: " + getLon() + " Altitude: " + getAlt() + "\n";
    }

    
}
