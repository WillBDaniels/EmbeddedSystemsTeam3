package edu.csci.team3;

import org.junit.Test;


/**
* This class is specifically for parsing up a KML file and outputting the list of lat/longs
*/
public class KMLParserTest{
    @Test
    public void testBasicKMLParse(){
        KMLParser parse = new KMLParser();
        parse.parseKml(getClass().getResourceAsStream("test.kml"));
    }
}