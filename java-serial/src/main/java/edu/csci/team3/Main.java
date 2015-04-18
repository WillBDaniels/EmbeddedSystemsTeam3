package edu.csci.team3;

import gnu.io.CommPort;
import gnu.io.CommPortIdentifier;
import gnu.io.SerialPort;

import java.io.FileDescriptor;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;


public class Main{

	public static void main(String[] args){
		System.out.println("hello!");
	}

private void connect ( String portName) throws Exception{
	CommPortIdentifier portIdentifier = CommPortIdentifier.getPortIdentifer(portName);
	if (portIdentifier.isCurrentlyOwned()){

