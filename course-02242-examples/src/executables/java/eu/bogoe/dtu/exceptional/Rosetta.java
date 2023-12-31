package eu.bogoe.dtu.exceptional;

import java.util.Arrays;

import dtu.compute.exec.Case;

public class Rosetta {

    @Case //https://rosettacode.org/wiki/Array_concatenation#Java
    int[] concat() {
        int[] arrayA = new int[100];
        int[] arrayB = new int[100];
        
        int[] array = new int[arrayA.length + arrayB.length];
        for (int index = 0; index < arrayA.length; index++) {
            assert index < array.length;
            assert index < arrayA.length;
            array[index] = arrayA[index];
        }
        for (int index = 0; index < arrayB.length; index++) {
            assert index < array.length;
            assert index < arrayB.length;
            
            int offsetIndex = index + arrayA.length;
            assert offsetIndex < array.length;    
            
            array[offsetIndex] = arrayB[index];
        }
        return array;
    }


    @Case // https://rosettacode.org/wiki/Deconvolution/1D#Java 
    public static int[] deconv(int[] g, int[] f) {
        int[] h = new int[g.length - f.length + 1];
        for (int n = 0; n < h.length; n++) {
            h[n] = g[n];
            int lower;
            if (n - f.length + 1 >= 0) {
                lower = n - f.length + 1;
            } else {
                lower = 1; 
            }
            //int lower = Math.max(n - f.length + 1, 0);
            for (int i = lower; i < n; i++)
                h[n] -= h[i] * f[n - i];
            h[n] /= f[0];
        }
        return h;
    }


    @Case //https://rosettacode.org/wiki/Dot_product#Java  
    public static double dotProd(double[] a, double[] b){
		if(a.length != b.length){
			throw new IllegalArgumentException("The dimensions have to be equal!");
		}
		double sum = 0;
		for(int i = 0; i < a.length; i++){
			sum += a[i] * b[i];
		}
		return sum;
	}

    // maybe these two if we inline and remove calls to log??
    // https://rosettacode.org/wiki/Fast_Fourier_transform#Java
    public static int bitReverse(int n, int bits) {
        int reversedN = n;
        int count = bits - 1;

        n >>= 1;
        while (n > 0) {
            reversedN = (reversedN << 1) | (n & 1);
            count--;
            n >>= 1;
        }

        return ((reversedN << count) & ((1 << bits) - 1));
    }

    @Case // changed a lot of things so does not compute fft at all but u know
    static void fft(int[] buffer) {

        //int bits = (int) (log(buffer.length) / log(2));
        int bits = buffer.length;
        for (int j = 1; j < buffer.length / 2; j++) {

            int swapPos = bitReverse(j, bits);
            int temp = buffer[j];
            buffer[j] = buffer[swapPos];
            buffer[swapPos] = temp;
        }

        for (int N = 2; N <= buffer.length; N <<= 1) {
            for (int i = 0; i < buffer.length; i += N) {
                for (int k = 0; k < N / 2; k++) {

                    int evenIndex = i + k;
                    int oddIndex = i + k + (N / 2);
                    int even = buffer[evenIndex];
                    int odd = buffer[oddIndex];

                    double term = (-2 * 3.14 * k) / (double) N;
                    //Complex exp = (new Complex(cos(term), sin(term)).mult(odd));
                    int exp = 1;
                    buffer[evenIndex] = even + exp;
                    buffer[oddIndex] = even - exp;
                }
            }
        }
    }

    @Case // https://rosettacode.org/wiki/Binary_search#Java
    public static int binarySearch(int[] nums, int check) {
        int hi = nums.length - 1;
        int lo = 0;
        while (hi >= lo) {
            int guess = (lo + hi) >>> 1;  // from OpenJDK
            if (nums[guess] > check) {
                hi = guess - 1;
            } else if (nums[guess] < check) {
                lo = guess + 1;
            } else {
                return guess;
            }
        }
        return -1;
    }

    //https://rosettacode.org/wiki/100_doors#Java
    @Case // this if change to int
    public static void hundredDoors() {
        int[] doors = new int[101];

        for (int i = 1; i < doors.length; i++) {
            for (int j = i; j < doors.length; j += i) {
                doors[j] = -doors[j];
            }
        }

/*         for (int i = 1; i < doors.length; i++) {
            if (doors[i] >= 0) {
                System.out.println(doors[i]);
            }
        } */
    }

    @Case // https://rosettacode.org/wiki/Knuth_shuffle#Java call to random removed 
    public static void shuffle (int[] array) {
        int n = array.length;
        while (n > 1) {
            n = n - 1;

            int k = n; //decrements after using the value
            int temp = array[n];
            array[n] = array[k];
            array[k] = temp;
        }
    }

    @Case 
    public static void transpose(){
        double[][] m = {{1, 1, 1, 1},
                        {2, 4, 8, 16},
                        {3, 9, 27, 81},
                        {4, 16, 64, 256},
                        {5, 25, 125, 625}};
        double[][] ans = new double[m[0].length][m.length];
        for(int rows = 0; rows < m.length; rows++){
                for(int cols = 0; cols < m[0].length; cols++){
                        ans[cols][rows] = m[rows][cols];
                }
        }
        //for(double[] i:ans){//2D arrays are arrays of arrays
        //        System.out.println(Arrays.toString(i));
        //}
    }
}
