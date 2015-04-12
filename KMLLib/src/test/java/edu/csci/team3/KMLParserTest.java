package edu.csci.team3;

import java.util.List;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;
import org.junit.Test;


/**
* This class is specifically for parsing up a KML file and outputting the list of lat/longs
*/
public class KMLParserTest{
    @Test
    public void testBasicKMLParse(){
        KMLParser parse = new KMLParser();
        List<CoordTriple> coordList = parse.parseKml(getClass().getResourceAsStream("test.kml"));
        assertNotNull(coordList);
        assertTrue(!coordList.isEmpty());
        System.out.println("Contents of the test KML file: " + coordList);
    }
}