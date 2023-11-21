package eu.bogoe.dtu.exceptional;

import dtu.compute.exec.Case;


// Sorting algorithms taken from: https://stackabuse.com/sorting-algorithms-in-java/

public class Sorting {
    
    @Case
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

    // Not from that site. But lends itself more to our analysis. + does not use booleans
    @Case
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
    
    @Case
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

    // version better for our analysis
    @Case
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

    @Case
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
    @Case
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

    @Case // https://rosettacode.org/wiki/Sorting_algorithms/Gnome_sort#Java
    public static void gnomeSort(int[] a) {
        int i=1;
        int j=2;
    
        while(i < a.length) {
            if ( a[i-1] <= a[i] ) {
            i = j; j++;
            } else {
            int tmp = a[i-1];
            a[i-1] = a[i];
            a[i--] = tmp;
            i = (i==0) ? j++ : i;
            }
        }
    }
    @Case // https://rosettacode.org/wiki/Sorting_algorithms/Cycle_sort#Java
    static int cycleSort(int[] a) {
        int writes = 0;

        for (int cycleStart = 0; cycleStart < a.length - 1; cycleStart++) {
            int val = a[cycleStart];

            // count the number of values that are smaller than val
            // since cycleStart
            int pos = cycleStart;
            for (int i = cycleStart + 1; i < a.length; i++)
                if (a[i] < val)
                    pos++;

            // there aren't any
            if (pos == cycleStart)
                continue;

            // skip duplicates
            while (val == a[pos])
                pos++;

            // put val into final position
            int tmp = a[pos];
            a[pos] = val;
            val = tmp;
            writes++;

            // repeat as long as we can find values to swap
            // otherwise start new cycle
            while (pos != cycleStart) {
                pos = cycleStart;
                for (int i = cycleStart + 1; i < a.length; i++)
                    if (a[i] < val)
                        pos++;

                while (val == a[pos])
                    pos++;

                tmp = a[pos];
                a[pos] = val;
                val = tmp;
                writes++;
            }
        }
        return writes;
    }

/*     @Case // https://rosettacode.org/wiki/Sorting_algorithms/Heapsort#Java
    public static void heapSort(int[] a){
        int count = a.length;
    
        //first place a in max-heap order
        heapify(a, count);
    
        int end = count - 1;
        while(end > 0){
            //swap the root(maximum value) of the heap with the
            //last element of the heap
            int tmp = a[end];
            a[end] = a[0];
            a[0] = tmp;
            //put the heap back in max-heap order
            siftDown(a, 0, end - 1);
            //decrement the size of the heap so that the previous
            //max value will stay in its proper place
            end--;
        }
    }
    
    public static void heapify(int[] a, int count){
        //start is assigned the index in a of the last parent node
        int start = (count - 2) / 2; //binary heap
    
        while(start >= 0){
            //sift down the node at index start to the proper place
            //such that all nodes below the start index are in heap
            //order
            siftDown(a, start, count - 1);
            start--;
        }
        //after sifting down the root all nodes/elements are in heap order
    }
    
    public static void siftDown(int[] a, int start, int end){
        //end represents the limit of how far down the heap to sift
        int root = start;
    
        while((root * 2 + 1) <= end){      //While the root has at least one child
            int child = root * 2 + 1;           //root*2+1 points to the left child
            //if the child has a sibling and the child's value is less than its sibling's...
            if(child + 1 <= end && a[child] < a[child + 1])
                child = child + 1;           //... then point to the right child instead
            if(a[root] < a[child]){     //out of max-heap order
                int tmp = a[root];
                a[root] = a[child];
                a[child] = tmp;
                root = child;                //repeat to continue sifting down the child now
            }else
                return;
        }
    } */

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