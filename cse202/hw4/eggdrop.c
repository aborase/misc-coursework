#include <stdio.h>
#include <string.h>
#include <time.h>

int main()
{
    //time_t start, end;
    FILE *ifp;
    int floors = 0;
    int eggs = 0;
    int num = 0;

    //start = clock();
    // Read Input
    ifp = fopen("./input.txt", "r");
    if (fscanf(ifp, "%d,%d", &floors, &eggs) > 0)
    {
        //printf("floors=%d, eggs=%d \n", floors, eggs);
    } else {
        //printf("Unable to read Input file, check format. \n");
    }
    fclose(ifp);

    //solution 2D-matrix
    int sol[eggs][floors+1];

    // setup base cases
    int i, j;
    memset(sol, 0, eggs*sizeof sol[0]);

    for(i=1; i<floors+1; i++)
    {
        sol[0][i] = i;
    }

    for(i=1; i<eggs; i++)
    {
        sol[i][1] = 1;
    }

    int e, f, min, temp;
    for(e=1; e<eggs; e++)
    {
        for(f=2; f<floors+1; f++)
        {
            //print("finding for f=%d,e=%d" % (f, e))
            //min1 = sol[e][f-1] + 1
            min = f;
            for(i=1; i<f+1; i++)
            {
                temp = 0;
                //shouldn't this be e==1
                if (sol[e-1][i-1] >= sol[e][f-i]) 
                {
                    temp = 1 + sol[e-1][i-1];
                } else {
                    temp = 1 + sol[e][f-i];
                }
                //printf("E=%d, F=%d, i=%d", e, f, i);
                //printf("temp=%d max1=%d max2=%d min1=%d", temp, sol[e-1][i-1], sol[e][f-i], min);

                if (temp < min)
                {
                    min = temp;
                }
            }
            sol[e][f] = min;
        }
    }
    //end = clock();
    /*
    for(i=0; i<eggs; i++)
    {
        sol[i][1] = 0;
    }

    for(i=1; i<floors+1; i++)
    {
        sol[0][i] = i-1;
    }
    */
    /* 
    for(i=0; i<eggs; i++)
    {
        for(j=0; j<floors+1; j++)
        {
            printf("%3d ", sol[i][j]);
        }
        printf("\n");
    }
    */

    FILE *ofp = fopen("output.txt", "w");
    fprintf(ofp, "%d", sol[eggs-1][floors-1]);
    fclose(ofp);
    //printf("Answer: sol[%d][%d]=%d \n", eggs-1, floors, sol[eggs-1][floors-1]);
    //printf("Time taken: %f \n", difftime(end, start)/1000000);
}
