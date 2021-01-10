package ro.ubb.emoca;

import ro.ubb.emoca.service.MeanFilter;
import java.io.IOException;

public class Main {

    public static void main(String[] args) {
        System.out.println("\nStarting algorithm");
        long start = System.currentTimeMillis();
        MeanFilter meanFilter = new MeanFilter("D:\\PDP\\Project\\Threads\\src\\main\\resources\\test.jpg");
        long end = System.currentTimeMillis();
        System.out.println("Finished algorithm in " + (end - start) + " ms.");
        try {
            meanFilter.createOutputImage();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}