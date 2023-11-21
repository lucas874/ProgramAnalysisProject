package eu.bogoe.dtu.exceptional;

import dtu.compute.exec.Case;

public class Rosetta {

    @Case //https://rosettacode.org/wiki/Array_concatenation#Java
    int[] concat(int[] arrayA, int[] arrayB) {
        int[] array = new int[arrayA.length + arrayB.length];
        for (int index = 0; index < arrayA.length; index++)
            array[index] = arrayA[index];
        for (int index = 0; index < arrayB.length; index++)
            array[index + arrayA.length] = arrayB[index];
        return array;
    }


    @Case // https://rosettacode.org/wiki/Deconvolution/1D#Java 
    public static int[] deconv(int[] g, int[] f) {
        int[] h = new int[g.length - f.length + 1];
        for (int n = 0; n < h.length; n++) {
            h[n] = g[n];
            int lower = Math.max(n - f.length + 1, 0);
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

    static void fft(Complex[] buffer) {

        int bits = (int) (log(buffer.length) / log(2));
        for (int j = 1; j < buffer.length / 2; j++) {

            int swapPos = bitReverse(j, bits);
            Complex temp = buffer[j];
            buffer[j] = buffer[swapPos];
            buffer[swapPos] = temp;
        }

        for (int N = 2; N <= buffer.length; N <<= 1) {
            for (int i = 0; i < buffer.length; i += N) {
                for (int k = 0; k < N / 2; k++) {

                    int evenIndex = i + k;
                    int oddIndex = i + k + (N / 2);
                    Complex even = buffer[evenIndex];
                    Complex odd = buffer[oddIndex];

                    double term = (-2 * PI * k) / (double) N;
                    Complex exp = (new Complex(cos(term), sin(term)).mult(odd));

                    buffer[evenIndex] = even.add(exp);
                    buffer[oddIndex] = even.sub(exp);
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
        boolean[] doors = new boolean[101];

        for (int i = 1; i < doors.length; i++) {
            for (int j = i; j < doors.length; j += i) {
                doors[j] = !doors[j];
            }
        }

        for (int i = 1; i < doors.length; i++) {
            if (doors[i]) {
                System.out.printf("Door %d is open.%n", i);
            }
        }
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
}
