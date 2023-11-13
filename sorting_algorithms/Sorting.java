

// Sorting algorithms taken from: https://stackabuse.com/sorting-algorithms-in-java/

public class Sorting {
    public static void bubbleSort(int[] array) {
        boolean sorted = false;
        int temp;
        while(!sorted) {
            sorted = true;
            for (int i = 0; i < array.length - 1; i++) {
                if (array[i] > array[i+1]) {
                    temp = array[i];
                    array[i] = array[i+1];
                    array[i+1] = temp;
                    sorted = false;
                }
            }
        }
    }

    public static void bubbleSort1(int[] array) { 
        int temp;
        for (int i = 0; i < array.length; i++) { 
            for (int j = i+1; j < array.length; j++) {
                if (array[j] < array[i]) {
                    temp = array[j];
                    array[j] = array[i];
                    array[i] = temp; 
                }
            }
        }
    }

    public static void insertionSort(int[] array) {
        for (int i = 1; i < array.length; i++) {
            int current = array[i];
            int j = i - 1;
            while(j >= 0 && current < array[j]) {
                array[j+1] = array[j];
                j--;
            }
            // at this point we've exited, so j is either -1
            // or it's at the first element where current >= a[j]
            array[j+1] = current;
        }
    }

    public static void insertionSort1(int[] array) {
        for (int i = 1; i < array.length; i++) { 
            int j = i;
            while(j > 0 && array[j-1] > array[j]) {
                int temp = array[j];
                array[j] = array[j-1];
                array[j-1] = temp;
                j--;
            } 
        }
    }

    public static void selectionSort(int[] array) {
        for (int i = 0; i < array.length; i++) {
            int min = array[i];
            int minId = i;
            for (int j = i+1; j < array.length; j++) {
                if (array[j] < min) {
                    min = array[j];
                    minId = j;
                }
            }
            // swapping
            int temp = array[i];
            array[i] = min;
            array[minId] = temp;
        }
    }
    
    // not from that site. return index or -1
    public static int binarySearch(int[] array, int target) {
        int low = 0;
        int high = array.length - 1;

        while(low <= high) {
            int mid = (low + high) / 2;
            if(array[mid] < target) {
                low = mid + 1;
            } else if (array[mid] > target) {
                high = mid - 1;
            } else {
                return mid; // found target
            }
        }

        return -1;
    }

    public static void printArray(int[] array) {
        for(int i = 0; i < array.length; i++) {
            System.out.print(array[i] + " ");
        }
        System.out.println("");
    }

    public static void main(String[] args) {
        int[] myNums1 = {1432, 2023, 3, 40};
        int[] myNums2 = {1432, 2023, 3, 40};
        int[] myNums3 = {1432, 2023, 3, 40};
        bubbleSort1(myNums1);
        insertionSort1(myNums2);
        selectionSort(myNums3);

        printArray(myNums1);
        printArray(myNums2);
        printArray(myNums3);

        System.out.println(binarySearch(myNums3, 1431));
        
        
    }

} 