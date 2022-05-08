import java.io.*;

class Main {
    public static void main(String[] args) {
        // Program that prints "Hello world" to the console
        System.out.println("Hello world");

        // Sample code for reading from the stdin
        int a, b;
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        try {
            a = Integer.parseInt(br.readLine());
            b = Integer.parseInt(br.readLine());
         System.out.println(a + " + " + b + " = " + (a+b));
        } catch (IOException ioe) {
            System.out.println(ioe);
        }
    }
} 
